# Hermes 上游更新维护

生产环境只跟踪 `glfruit/hermes-campus-agent` 的 `main`。该分支由三部分组成：

1. `NousResearch/hermes-agent` 的官方 `main`；
2. campus 项目文件；
3. 尚未进入官方版本的生产修复。

不要在生产机上直接把 `origin` 指向官方仓库。`hermes update` 会强制切换到
`main` 并拉取 `origin/main`，因此生产机的 `origin` 必须始终指向 campus fork。

## 获取官方更新

在 GitHub Actions 中手动运行 **Sync official upstream**，或等待每周任务。工作流会：

1. 获取官方 `main`；
2. 在临时 `automation/upstream-sync-*` 分支执行普通 merge；
3. 如果有冲突则停止，不修改 fork 的 `main`；
4. 创建面向 fork `main` 的 PR；
5. 从受信任的 fork `main` 调度无 Secrets、只读权限的验证 workflow，并把提案 commit SHA 作为 checkout 数据传入。

仓库的 Actions workflow 权限必须保持默认只读，同时启用
**Allow GitHub Actions to create and approve pull requests**。同步 workflow 仅为自身显式申请
`contents: write`、`pull-requests: write` 和 `actions: write`，其他 workflow 不会继承写权限。

同步提案分支不会运行带写权限的主 CI，也不能提供 runner、environment 或 workflow 定义；验证定义固定取自受信任的 fork `main`。只有在只读验证通过并完成代码审查后才合并 PR。合并后，生产机可以运行：

普通 PR 的 `pull_request_target` 只读取元数据并调度隔离的 `workflow_dispatch`，绝不 checkout 或执行 head；原 `ci.yml` 只在已合并的 `main` push 上运行。隔离 validator 无 Secrets、禁用凭据持久化和 Actions cache。受信 finalizer 为每个当前 head 写入 `trusted-pr-validation` commit status；CI-sensitive 文件还必须有 `ci-reviewed` 标签。自动同步器使用同样的唯一 correlation、head SHA 复核和 commit status。结论不会被后续 push 继承。

每次 PR head 更新都会先撤销 `ci-reviewed`、`supply-chain-reviewed`、`mcp-catalog-reviewed` 和 `upstream-validated`，避免新提交继承旧 SHA 的人工授权。

如果同步修改了 `setup.py` 等安装钩子，供应链扫描会保持失败，直到维护者逐行审查后为 PR 添加 `supply-chain-reviewed` 标签；该标签是显式安全确认，不是自动绕过。

```bash
hermes update
```

## 核验生产更新源

```bash
cd ~/.hermes/hermes-agent
git branch --show-current
git remote get-url origin
git rev-parse HEAD
git rev-parse origin/main
```

预期当前分支为 `main`，`origin` 为
`https://github.com/glfruit/hermes-campus-agent.git`。生产修复必须是 `main` 的已提交历史，
不能只存在于工作区、stash 或临时分支。
