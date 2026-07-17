"""Phase 3: secondary-profile adapter registry + same-token conflict detection."""
import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from gateway.config import GatewayConfig, Platform, PlatformConfig
from gateway.run import GatewayRunner


class _FakeAdapter:
    def __init__(self, token=None, config=None):
        self.token = token
        self.config = config


class _FatalProfileAdapter:
    platform = Platform.TELEGRAM
    fatal_error_code = "telegram_network_error"
    fatal_error_message = "network unavailable"
    fatal_error_retryable = True

    def __init__(self):
        self.disconnect_calls = 0

    async def disconnect(self):
        self.disconnect_calls += 1


class _DisconnectFailureProfileAdapter(_FatalProfileAdapter):
    async def disconnect(self):
        self.disconnect_calls += 1
        raise RuntimeError("disconnect failed")


class TestCredentialFingerprint:
    def test_none_without_token(self):
        assert GatewayRunner._adapter_credential_fingerprint(_FakeAdapter()) is None

    def test_stable_and_log_safe(self):
        a = _FakeAdapter(token="secret-bot-token")
        fp1 = GatewayRunner._adapter_credential_fingerprint(a)
        fp2 = GatewayRunner._adapter_credential_fingerprint(_FakeAdapter(token="secret-bot-token"))
        assert fp1 == fp2  # stable
        assert "secret-bot-token" not in (fp1 or "")  # never the raw token
        assert len(fp1) == 16

    def test_distinct_tokens_distinct_fp(self):
        a = GatewayRunner._adapter_credential_fingerprint(_FakeAdapter(token="tok-A"))
        b = GatewayRunner._adapter_credential_fingerprint(_FakeAdapter(token="tok-B"))
        assert a != b

    def test_reads_alt_attrs(self):
        class _AltAdapter:
            def __init__(self):
                self.bot_token = "alt-token"
        assert GatewayRunner._adapter_credential_fingerprint(_AltAdapter()) is not None

    def test_reads_platform_config_token(self):
        class _Config:
            token = "config-token"

        fp = GatewayRunner._adapter_credential_fingerprint(
            _FakeAdapter(token=None, config=_Config())
        )

        assert fp is not None
        assert "config-token" not in fp


    def test_reads_config_token(self):
        """Adapters like Discord store token on `config`, not on self.

        Without the config-token fallback, every Discord adapter in a
        multiplexed gateway returns None here and the same-token conflict
        check is silently skipped — N adapters start polling the same bot
        token and race on every inbound message.
        """
        class _Config:
            token = "discord-bot-token"
        class _ConfigBackedAdapter:
            config = _Config()
        fp = GatewayRunner._adapter_credential_fingerprint(_ConfigBackedAdapter())
        assert fp is not None
        assert "discord-bot-token" not in fp
        assert len(fp) == 16

    def test_distinct_config_tokens_distinct_fp(self):
        class _CfgA:
            token = "tok-A"
        class _CfgB:
            token = "tok-B"
        class _A:
            config = _CfgA()
        class _B:
            config = _CfgB()
        a = GatewayRunner._adapter_credential_fingerprint(_A())
        b = GatewayRunner._adapter_credential_fingerprint(_B())
        assert a is not None and b is not None
        assert a != b

    def test_direct_token_takes_precedence_over_config(self):
        """If both `adapter.token` and `adapter.config.token` exist, direct wins."""
        class _Cfg:
            token = "from-config"
        class _Both:
            token = "from-direct"
            config = _Cfg()
        fp = GatewayRunner._adapter_credential_fingerprint(_Both())
        import hashlib
        expected = hashlib.sha256(b"hermes-mux:from-direct").hexdigest()[:16]
        assert fp == expected

    def test_config_without_token_returns_none(self):
        """config present but no token attribute → None (no false positive)."""
        class _Cfg:
            pass
        class _Adapter:
            config = _Cfg()
        assert GatewayRunner._adapter_credential_fingerprint(_Adapter()) is None


class TestProfileMessageHandler:
    @pytest.mark.asyncio
    async def test_stamps_profile_on_unstamped_source(self):
        runner = GatewayRunner.__new__(GatewayRunner)
        seen = {}

        async def _fake_handle(event):
            seen["profile"] = event.source.profile
            return "ok"

        runner._handle_message = _fake_handle
        handler = runner._make_profile_message_handler("coder")

        class _Src:
            profile = None

        class _Evt:
            source = _Src()

        result = await handler(_Evt())
        assert result == "ok"
        assert seen["profile"] == "coder"

    @pytest.mark.asyncio
    async def test_does_not_override_existing_profile(self):
        runner = GatewayRunner.__new__(GatewayRunner)
        seen = {}

        async def _fake_handle(event):
            seen["profile"] = event.source.profile
            return "ok"

        runner._handle_message = _fake_handle
        handler = runner._make_profile_message_handler("coder")

        class _Src:
            profile = "writer"  # already stamped (e.g. by URL prefix)

        class _Evt:
            source = _Src()

        await handler(_Evt())
        assert seen["profile"] == "writer"


class TestProfileReconnectOwnership:
    @pytest.mark.asyncio
    async def test_secondary_fatal_retries_its_profile_not_root(self, tmp_path):
        """A secondary fatal must retain its profile config ownership."""
        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(
            platforms={
                Platform.TELEGRAM: PlatformConfig(enabled=True, token=None),
            },
            multiplex_profiles=True,
        )
        adapter = _FatalProfileAdapter()
        # A primary profile may own the same platform with another credential;
        # that must not make this secondary failure look stale.
        runner.adapters = {
            Platform.API_SERVER: object(),
            Platform.TELEGRAM: object(),
        }
        runner._profile_adapters = {
            "edu-tl": {Platform.TELEGRAM: adapter},
        }
        runner._profile_homes = {"edu-tl": tmp_path}
        runner._failed_platforms = {}
        runner.delivery_router = MagicMock()
        runner._update_platform_runtime_status = MagicMock()
        runner._schedule_profile_reconnect = MagicMock()
        runner.stop = AsyncMock()

        await runner._handle_adapter_fatal_error(adapter)

        assert Platform.TELEGRAM not in runner._profile_adapters["edu-tl"]
        assert adapter.disconnect_calls == 1
        assert runner._failed_platforms == {}
        runner._schedule_profile_reconnect.assert_called_once_with(
            "edu-tl", tmp_path, Platform.TELEGRAM
        )

    @pytest.mark.asyncio
    async def test_secondary_fatal_writes_only_its_profile_status(
        self, tmp_path, monkeypatch
    ):
        root_home = tmp_path / "root"
        profile_home = tmp_path / "profiles" / "edu-tl"
        root_home.mkdir()
        profile_home.mkdir(parents=True)
        monkeypatch.setenv("HERMES_HOME", str(root_home))

        runner = GatewayRunner.__new__(GatewayRunner)
        adapter = _FatalProfileAdapter()
        runner.adapters = {}
        runner._profile_adapters = {"edu-tl": {Platform.TELEGRAM: adapter}}
        runner._profile_homes = {"edu-tl": profile_home}
        runner._failed_platforms = {}
        runner.delivery_router = MagicMock()
        runner._schedule_profile_reconnect = MagicMock()

        await runner._handle_adapter_fatal_error(adapter)

        from gateway.status import read_runtime_status

        assert not (root_home / "gateway_state.json").exists()
        record = read_runtime_status(profile_home / "gateway_state.json")
        assert record["platforms"]["telegram"]["state"] == "retrying"

    @pytest.mark.asyncio
    async def test_disconnect_failure_does_not_prevent_profile_reconnect(self, tmp_path):
        runner = GatewayRunner.__new__(GatewayRunner)
        adapter = _DisconnectFailureProfileAdapter()
        runner.adapters = {}
        runner._profile_adapters = {"edu-tl": {Platform.TELEGRAM: adapter}}
        runner._profile_homes = {"edu-tl": tmp_path}
        runner._failed_platforms = {}
        runner.delivery_router = MagicMock()
        runner._update_platform_runtime_status = MagicMock()
        runner._schedule_profile_reconnect = MagicMock()

        await runner._handle_adapter_fatal_error(adapter)

        assert adapter.disconnect_calls == 1
        runner._schedule_profile_reconnect.assert_called_once_with(
            "edu-tl", tmp_path, Platform.TELEGRAM
        )

    @pytest.mark.asyncio
    async def test_reconnect_loop_rebuilds_only_failed_profile(self, tmp_path):
        runner = GatewayRunner.__new__(GatewayRunner)
        runner._running = True
        runner.adapters = {}
        runner._profile_adapters = {"edu-tl": {}}
        runner._profile_reconnect_tasks = {}
        runner._background_tasks = set()

        async def reconnect(profile_name, profile_home, _claimed, **kwargs):
            assert profile_name == "edu-tl"
            assert profile_home == tmp_path
            assert kwargs == {
                "only_platform": Platform.TELEGRAM,
                "is_reconnect": True,
            }
            runner._profile_adapters[profile_name][Platform.TELEGRAM] = object()
            return 1

        runner._start_one_profile_adapters = AsyncMock(side_effect=reconnect)
        runner._profile_reconnect_claims = MagicMock(return_value={})

        await runner._profile_reconnect_loop(
            "edu-tl", tmp_path, Platform.TELEGRAM
        )

        runner._start_one_profile_adapters.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_reconnect_loop_stops_after_non_retryable_failure(self, tmp_path):
        runner = GatewayRunner.__new__(GatewayRunner)
        runner._running = True
        runner.adapters = {}
        runner._profile_adapters = {"edu-tl": {}}
        runner._profile_terminal_reconnects = set()

        async def reconnect(profile_name, _profile_home, _claimed, **_kwargs):
            runner._profile_terminal_reconnects.add(
                (profile_name, Platform.TELEGRAM)
            )
            return 0

        runner._start_one_profile_adapters = AsyncMock(side_effect=reconnect)
        runner._profile_reconnect_claims = MagicMock(return_value={})

        await runner._profile_reconnect_loop(
            "edu-tl", tmp_path, Platform.TELEGRAM
        )

        runner._start_one_profile_adapters.assert_awaited_once()


class TestSecondaryProfileConfigHandling:
    """Secondary config errors degrade only when the profile is safe to skip."""

    @pytest.mark.asyncio
    async def test_secondary_webhook_uses_degradable_error(self, monkeypatch):
        from gateway.run import SecondaryPortBindingConfigError
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        # reviewer profile config enables webhook (a port-binding platform)
        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            Platform.WEBHOOK: PlatformConfig(enabled=True, extra={"port": 8644}),
        }
        monkeypatch.setattr(
            "gateway.config.load_gateway_config", lambda: reviewer_cfg
        )

        with pytest.raises(SecondaryPortBindingConfigError) as ei:
            await runner._start_one_profile_adapters("reviewer", "/tmp/x", {})
        assert "webhook" in str(ei.value)
        assert "reviewer" in str(ei.value)
        assert "reviewer" not in runner._profile_adapters

    @pytest.mark.asyncio
    async def test_secondary_reports_all_port_binding_platforms(self, monkeypatch):
        from gateway.run import SecondaryPortBindingConfigError
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            # connection_mode=webhook: with #52563's conditional check merged,
            # default (websocket) Feishu no longer binds a port — only webhook
            # mode should be reported here.
            Platform.FEISHU: PlatformConfig(
                enabled=True, extra={"connection_mode": "webhook"}
            ),
            Platform.WEBHOOK: PlatformConfig(enabled=True, extra={"port": 8644}),
            Platform.TELEGRAM: PlatformConfig(enabled=True, token="t"),
        }
        monkeypatch.setattr(
            "gateway.config.load_gateway_config", lambda: reviewer_cfg
        )

        with pytest.raises(SecondaryPortBindingConfigError) as ei:
            await runner._start_one_profile_adapters("reviewer", "/tmp/x", {})
        message = str(ei.value)
        assert "feishu" in message
        assert "webhook" in message
        assert "telegram" not in message
        assert "reviewer" not in runner._profile_adapters

    @pytest.mark.asyncio
    async def test_multiplexer_skips_bad_profile_and_continues(self, monkeypatch, caplog):
        from pathlib import Path
        from gateway.config import GatewayConfig

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner.adapters = {}
        runner._profile_adapters = {}

        async def fake_start_one(profile_name, profile_home, claimed):
            if profile_name == "bad":
                from gateway.run import SecondaryPortBindingConfigError
                raise SecondaryPortBindingConfigError("bad enables webhook")
            runner._profile_adapters[profile_name] = {}
            return 2

        monkeypatch.setattr(
            "hermes_cli.profiles.profiles_to_serve",
            lambda multiplex: [
                ("default", Path("/tmp/default")),
                ("bad", Path("/tmp/bad")),
                ("good", Path("/tmp/good")),
            ],
        )
        monkeypatch.setattr(
            "hermes_cli.profiles.get_active_profile_name",
            lambda: "default",
        )
        monkeypatch.setattr(runner, "_start_one_profile_adapters", fake_start_one)
        monkeypatch.setattr(
            "gateway.status.write_runtime_status",
            lambda **kwargs: None,
        )

        caplog.set_level(logging.WARNING, logger="gateway.run")
        connected = await runner._start_secondary_profile_adapters()

        assert connected == 2
        assert "good" in runner._profile_adapters
        assert "bad" not in runner._profile_adapters
        assert "Skipping secondary profile 'bad'" in caplog.text

    @pytest.mark.asyncio
    async def test_multiplexer_propagates_security_config_error(self, monkeypatch):
        from pathlib import Path
        from gateway.config import GatewayConfig
        from gateway.run import MultiplexConfigError

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner.adapters = {}
        runner._profile_adapters = {}

        async def fake_start_one(profile_name, profile_home, claimed):
            raise MultiplexConfigError(
                f"Profile '{profile_name}' enables open policy without allow-all opt-in"
            )

        monkeypatch.setattr(
            "hermes_cli.profiles.profiles_to_serve",
            lambda multiplex: [
                ("default", Path("/tmp/default")),
                ("unsafe", Path("/tmp/unsafe")),
            ],
        )
        monkeypatch.setattr(
            "hermes_cli.profiles.get_active_profile_name",
            lambda: "default",
        )
        monkeypatch.setattr(runner, "_start_one_profile_adapters", fake_start_one)

        with pytest.raises(MultiplexConfigError, match="open policy"):
            await runner._start_secondary_profile_adapters()

    @pytest.mark.asyncio
    async def test_open_policy_uses_fatal_config_error(self, monkeypatch):
        from gateway.config import GatewayConfig, Platform, PlatformConfig
        from gateway.run import (
            MultiplexConfigError,
            SecondaryPortBindingConfigError,
        )

        monkeypatch.delenv("GATEWAY_ALLOW_ALL_USERS", raising=False)
        monkeypatch.delenv("WECOM_ALLOW_ALL_USERS", raising=False)

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        unsafe_cfg = GatewayConfig(multiplex_profiles=True)
        unsafe_cfg.platforms = {
            Platform.WECOM: PlatformConfig(
                enabled=True,
                extra={"dm_policy": "open"},
            ),
        }
        monkeypatch.setattr("gateway.config.load_gateway_config", lambda: unsafe_cfg)

        with pytest.raises(MultiplexConfigError, match="open policy") as exc_info:
            await runner._start_one_profile_adapters("unsafe", "/tmp/unsafe", {})

        assert not isinstance(exc_info.value, SecondaryPortBindingConfigError)
        assert "unsafe" not in runner._profile_adapters

    @pytest.mark.asyncio
    async def test_secondary_non_binding_platform_ok(self, monkeypatch):
        """A non-port-binding platform (e.g. telegram) is NOT rejected."""
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            Platform.TELEGRAM: PlatformConfig(enabled=True, token="t"),
        }
        monkeypatch.setattr(
            "gateway.config.load_gateway_config", lambda: reviewer_cfg
        )
        # _create_adapter returns None here (no real telegram token wiring), so
        # the loop simply connects nothing — the key assertion is NO raise.
        seen_tokens = []

        def create_adapter(_platform, config):
            seen_tokens.append(config.token)
            return None

        monkeypatch.setattr(runner, "_create_adapter", create_adapter)

        connected = await runner._start_one_profile_adapters("reviewer", "/tmp/x", {})
        assert connected == 0  # nothing connected, but no MultiplexConfigError
        assert seen_tokens == ["t"]

    @pytest.mark.asyncio
    async def test_multiplex_secondary_skips_relay_but_starts_direct_adapter(
        self, monkeypatch
    ):
        """Relay is process-shared; direct adapters remain per-profile."""
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        class _DirectAdapter:
            platform = Platform.TELEGRAM

            def set_message_handler(self, handler):
                self.message_handler = handler

            def set_fatal_error_handler(self, handler):
                self.fatal_error_handler = handler

            def set_session_store(self, store):
                self.session_store = store

            def set_busy_session_handler(self, handler):
                self.busy_session_handler = handler

            def set_topic_recovery_fn(self, handler):
                self.topic_recovery_fn = handler

            def set_authorization_check(self, handler):
                self.authorization_check = handler

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}
        runner.session_store = object()
        runner._handle_adapter_fatal_error = object()
        runner._handle_active_session_busy_message = object()
        runner._recover_telegram_topic_thread_id = object()
        runner._busy_text_mode = "queue"
        runner._make_adapter_auth_check = lambda platform, profile_name=None: object()

        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            Platform.RELAY: PlatformConfig(enabled=True),
            Platform.TELEGRAM: PlatformConfig(enabled=True, token="reviewer-token"),
        }
        monkeypatch.setattr(
            "gateway.config.load_gateway_config", lambda: reviewer_cfg
        )

        direct = _DirectAdapter()
        factory_calls = []

        def _create_adapter(platform, config):
            factory_calls.append(platform)
            if platform is Platform.RELAY:
                raise AssertionError("secondary Relay factory must not be invoked")
            return direct

        connect_calls = []

        async def _connect(adapter, platform):
            connect_calls.append((adapter, platform))
            return True

        monkeypatch.setattr(runner, "_create_adapter", _create_adapter)
        monkeypatch.setattr(runner, "_connect_adapter_with_timeout", _connect)

        connected = await runner._start_one_profile_adapters(
            "reviewer", "/tmp/x", {}
        )

        assert connected == 1
        assert factory_calls == [Platform.TELEGRAM]
        assert connect_calls == [(direct, Platform.TELEGRAM)]
        assert runner._profile_adapters["reviewer"] == {
            Platform.TELEGRAM: direct,
        }

    @pytest.mark.asyncio
    async def test_non_multiplex_profile_adapter_start_keeps_relay(self, monkeypatch):
        """The Relay skip is gated to multiplex mode."""
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        class _RelayAdapter:
            platform = Platform.RELAY

            def set_message_handler(self, handler):
                pass

            def set_fatal_error_handler(self, handler):
                pass

            def set_session_store(self, store):
                pass

            def set_busy_session_handler(self, handler):
                pass

            def set_topic_recovery_fn(self, handler):
                pass

            def set_authorization_check(self, handler):
                pass

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=False)
        runner._profile_adapters = {}
        runner.session_store = object()
        runner._handle_adapter_fatal_error = object()
        runner._handle_active_session_busy_message = object()
        runner._recover_telegram_topic_thread_id = object()
        runner._busy_text_mode = "queue"
        runner._make_adapter_auth_check = lambda platform, profile_name=None: object()

        profile_cfg = GatewayConfig(multiplex_profiles=False)
        profile_cfg.platforms = {
            Platform.RELAY: PlatformConfig(enabled=True),
        }
        monkeypatch.setattr("gateway.config.load_gateway_config", lambda: profile_cfg)

        relay = _RelayAdapter()
        factory_calls = []
        connect_calls = []

        def _create_adapter(platform, config):
            factory_calls.append(platform)
            return relay

        async def _connect(adapter, platform):
            connect_calls.append((adapter, platform))
            return True

        monkeypatch.setattr(runner, "_create_adapter", _create_adapter)
        monkeypatch.setattr(runner, "_connect_adapter_with_timeout", _connect)

        connected = await runner._start_one_profile_adapters(
            "reviewer", "/tmp/x", {}
        )

        assert connected == 1
        assert factory_calls == [Platform.RELAY]
        assert connect_calls == [(relay, Platform.RELAY)]

    @pytest.mark.asyncio
    async def test_secondary_same_config_token_is_refused(
        self, monkeypatch, tmp_path
    ):
        """Adapters that keep their token on config still trip the mux guard."""
        from gateway.config import GatewayConfig, Platform, PlatformConfig
        from gateway.platforms.base import BasePlatformAdapter, SendResult

        class _ConfigTokenAdapter(BasePlatformAdapter):
            def __init__(self, token):
                super().__init__(
                    PlatformConfig(enabled=True, token=token), Platform.TELEGRAM
                )
                self.disconnected = False

            async def connect(self):
                raise AssertionError("duplicate adapter must not connect")

            async def disconnect(self):
                self.disconnected = True
                self._mark_disconnected()

            async def send(self, chat_id, content, reply_to=None, metadata=None):
                return SendResult(success=True)

            async def get_chat_info(self, chat_id):
                return {"id": chat_id}

        root_home = tmp_path / "root"
        profile_home = tmp_path / "profiles" / "reviewer"
        root_home.mkdir()
        profile_home.mkdir(parents=True)
        monkeypatch.setenv("HERMES_HOME", str(root_home))

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            Platform.TELEGRAM: PlatformConfig(enabled=True, token="same-token"),
        }
        duplicate = _ConfigTokenAdapter("same-token")
        claimed = {
            (
                Platform.TELEGRAM,
                GatewayRunner._adapter_credential_fingerprint(
                    _ConfigTokenAdapter("same-token")
                ),
            ): "default"
        }

        monkeypatch.setattr(
            "gateway.config.load_gateway_config", lambda: reviewer_cfg
        )
        monkeypatch.setattr(runner, "_create_adapter", lambda p, c: duplicate)
        monkeypatch.setattr(runner, "_adapter_disconnect_timeout_secs", lambda: 0)

        connected = await runner._start_one_profile_adapters(
            "reviewer", profile_home, claimed
        )

        assert connected == 0
        assert duplicate.disconnected is True
        assert runner._profile_adapters["reviewer"] == {}
        assert not (root_home / "gateway_state.json").exists()
        from gateway.status import read_runtime_status

        record = read_runtime_status(profile_home / "gateway_state.json")
        assert record["platforms"]["telegram"]["state"] == "disconnected"

    def test_port_binding_set_covers_known_listeners(self):
        from gateway.run import _PORT_BINDING_PLATFORM_VALUES
        # Every adapter that binds a TCP port must be in the guard set.
        for p in (
            "webhook",
            "api_server",
            "msgraph_webhook",
            "feishu",
            "wecom_callback",
            "bluebubbles",
            "sms",
            "whatsapp_cloud",
            "line",
        ):
            assert p in _PORT_BINDING_PLATFORM_VALUES
class TestFeishuPortBindingConditional:
    """Feishu websocket mode does NOT bind a port; only webhook mode does (#52563)."""

    @pytest.mark.asyncio
    async def test_feishu_websocket_mode_not_rejected(self, monkeypatch):
        """Feishu in websocket mode (the default) should NOT raise MultiplexConfigError."""
        from gateway.run import MultiplexConfigError
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            Platform.FEISHU: PlatformConfig(
                enabled=True,
                extra={"app_id": "cli_xxx", "app_secret": "sec", "connection_mode": "websocket"},
            ),
        }
        monkeypatch.setattr("gateway.config.load_gateway_config", lambda: reviewer_cfg)
        monkeypatch.setattr(runner, "_create_adapter", lambda p, c: None)

        connected = await runner._start_one_profile_adapters("reviewer", "/tmp/x", {})
        assert connected == 0  # no error, just nothing connected

    @pytest.mark.asyncio
    async def test_feishu_webhook_mode_raises(self, monkeypatch):
        """Feishu in webhook mode binds a port and should raise MultiplexConfigError."""
        from gateway.run import MultiplexConfigError
        from gateway.config import GatewayConfig, Platform, PlatformConfig

        runner = GatewayRunner.__new__(GatewayRunner)
        runner.config = GatewayConfig(multiplex_profiles=True)
        runner._profile_adapters = {}

        reviewer_cfg = GatewayConfig(multiplex_profiles=True)
        reviewer_cfg.platforms = {
            Platform.FEISHU: PlatformConfig(
                enabled=True,
                extra={"app_id": "cli_xxx", "app_secret": "sec", "connection_mode": "webhook"},
            ),
        }
        monkeypatch.setattr("gateway.config.load_gateway_config", lambda: reviewer_cfg)

        with pytest.raises(MultiplexConfigError) as ei:
            await runner._start_one_profile_adapters("reviewer", "/tmp/x", {})
        assert "feishu" in str(ei.value)

    def test_platform_binds_port_helper(self):
        """Unit test for _platform_binds_port helper."""
        from gateway.run import _platform_binds_port

        # Non-port-binding platform
        assert _platform_binds_port("telegram", {}) is False

        # Unconditional port-binding platform
        assert _platform_binds_port("webhook", {}) is True
        assert _platform_binds_port("api_server", {}) is True

        # Feishu: websocket = no port binding
        assert _platform_binds_port("feishu", {"connection_mode": "websocket"}) is False
        assert _platform_binds_port("feishu", {}) is False  # default is websocket

        # Feishu: webhook = port binding
        assert _platform_binds_port("feishu", {"connection_mode": "webhook"}) is True
