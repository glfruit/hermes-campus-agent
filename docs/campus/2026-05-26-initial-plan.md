# Hermes Campus Agent 初步规划

日期：2026-05-26

## 项目定位

Hermes Campus Agent 是基于 Hermes Agent 的轻量、可扩展 AI 智慧校园平台。第一期不追求覆盖全校所有人群，而是聚焦两个真实角色：

- 教学部门负责教学管理工作的副职：处理教学运行、质量监控、材料汇总、会议与通知、数据解释、制度问答。
- 一线教师：处理备课、课程资料、教学材料、学生沟通、成绩与课堂反馈分析、日常事务查询。

第一期目标不是“全能校园大脑”，而是一个能在现有信息化环境旁边落地的 AI 工作台：先辅助检索、分析、起草、提醒和材料组织；对强规则办事流程只做引导、预审和草稿，不直接越权提交或决策。

## 核心原则

1. Hermes 作为 Agent 编排层，不作为业务规则唯一决策者。
2. 校园知识库独立建设，通过 MCP 或插件接入 Hermes。
3. 强规则流程使用代码、状态机、权限和审计保证，不靠 Prompt 保证。
4. 第一阶段所有业务系统写操作默认关闭，必要时采用人工确认。
5. 优先适配现有环境：Web + 企业微信入口，内部系统通过 adapter/MCP 逐步接入。
6. 一个人开发时保持架构瘦身：少语言、少服务、少抽象，先形成可验证闭环。

## 一期用户场景

### 教学管理副职

高频工作：

- 查询教学制度、校历、教学运行安排。
- 汇总课程、教师、班级、考试、补考、调课等信息。
- 起草通知、会议纪要、教学检查方案、工作总结。
- 追踪重点任务：听课、督导、材料提交、考试安排、教学事故处理。
- 分析教学数据：课程开设、成绩分布、挂科率、补考率、教师工作量、课堂反馈。
- 向上级汇报时生成结构化材料和风险提示。

一期能力：

- 教学制度问答，回答必须带来源。
- 教学运行日程助手，支持周计划、提醒、待办。
- 通知与会议材料生成。
- 简单表格/数据上传后的摘要分析。
- 任务台账：人工录入或导入任务，AI 帮助生成进展摘要。

不做或只做辅助：

- 自动审批调课、缓考、成绩变更。
- 自动发布正式通知。
- 自动认定教学事故。
- 自动向学生或教师发送敏感结论。

### 教师

高频工作：

- 备课、教案、PPT 提纲、课堂活动设计。
- 根据课程大纲和教学日历安排周教学内容。
- 生成作业、测验、评分量规。
- 分析学生作业/考试表现，形成反馈草稿。
- 查询教学制度、课程资源、办事流程。
- 起草给学生、教研室、教学办的沟通内容。

一期能力：

- 教学设计助手：基于课程目标、课时、学生基础生成教案框架。
- 作业与评分量规助手。
- 教学材料整理：把文档、表格、会议要求整理成待办和草稿。
- 学生反馈草稿：只生成建议，不自动给出最终评价。
- 制度与流程问答。

不做或只做辅助：

- 自动给学生最终成绩。
- 自动判断学生处分、心理风险或奖助资格。
- 自动代表教师提交正式审批。

## 产品入口

### Web

Web 是主工作台，承载复杂交互：

- 对话区：与教师助手、教学管理助手交互。
- 知识库引用区：展示来源、版本、发布日期、适用范围。
- 任务区：待办、提醒、会议材料、教学运行事项。
- 文档区：上传、解析、摘要、生成草稿。
- 数据分析区：上传表格后生成统计、异常点、图表说明。
- 管理区：知识库、权限、审计、用户反馈。

第一期 Web 不做营销式首页，直接进入工作台。

### 企业微信

企业微信是轻量入口，适合移动端和提醒：

- 今日待办、周计划、任务提醒。
- 简短制度问答。
- 通知草稿预览。
- 会议纪要或材料生成结果提醒。
- 通过链接跳转 Web 完成复杂操作。

企业微信端不承载复杂流程配置、长文档编辑和高风险审批。

## 总体架构

```text
Web 工作台 / 企业微信
        ↓
校园应用后端
认证、会话、权限、任务、审计、企业微信回调、BFF API
        ↓
校园对话与流程层
意图路由、信息项状态、规则校验、人工确认、流程审计
        ↓
Hermes Agent
Profiles、Skills、MCP、工具调用、模型路由、Cron/Kanban
        ↓
校园知识与系统连接层
RAG 知识库、文档解析、教务/OA/学工/课表/文件系统 Adapter
        ↓
数据层
Postgres/pgvector、对象存储、审计日志、任务状态、权限索引
```

## Hermes 的使用边界

适合交给 Hermes：

- 多步骤分析、材料生成、复杂问答。
- 调用工具读取知识库、读取文档、生成摘要。
- 通过 Skills 固化教学材料写作、制度问答、公文草稿、数据分析流程。
- 用 Cron 做定时简报、周报和提醒。
- 用 Kanban 或任务队列管理较长周期的材料准备。

不直接交给 Hermes：

- 权限判断的最终决策。
- 业务流程状态的唯一来源。
- 教务/OA/财务/人事等系统写操作。
- 高风险学生事务、人事考核、财务付款、处分认定。

对强规则流程，采用“模型理解语言 + 代码执行规则”的模式：

```text
用户自然语言
        ↓
意图识别 / 信息抽取
        ↓
结构化信息项状态
        ↓
代码规则校验 / 权限检查 / 缺失信息判断
        ↓
Hermes 生成解释和下一步提示
```

## 技术栈判断

### Go

优点：

- 单二进制部署，稳定、性能好、并发模型清晰。
- 适合企业微信回调、网关、审计、任务调度等服务。
- 后端工程质量容易做得稳。

不足：

- AI/RAG/文档解析生态不如 Python。
- Web 全栈开发效率不如 TypeScript。
- 一个人开发时，Go + 前端 + Python/Hermes 容易变成多语言负担。

结论：Go 适合后期沉淀网关、任务执行器或高稳定服务；第一期不建议作为主后端。

### Python

优点：

- Hermes 本身是 Python，AI/RAG/文档解析生态强。
- FastAPI + Pydantic 原型速度快。
- 与模型、向量库、文档处理工具集成顺手。

不足：

- Web/BFF 与前端类型共享较弱。
- 长期维护需要更严格的工程纪律。
- 依赖和运行环境比 Go/TypeScript 更容易膨胀。

结论：Python 适合做文档解析、RAG ingestion、AI worker；不建议把第一期 Web 主应用全部压在 Python 上。

### TypeScript

优点：

- Web + 后端 + 企业微信 BFF 可以共用类型和工具链。
- 适合一个人快速做产品闭环。
- 与 Hermes API Server、OpenAI-compatible API、MCP 服务对接方便。
- Next.js/NestJS/Hono/Drizzle/Prisma 等生态成熟。

不足：

- 高并发后台任务和系统级工具不如 Go 干净。
- AI 文档处理生态不如 Python，复杂 OCR/解析可能仍需 Python worker。

结论：第一期主后端建议选 TypeScript。采用 TypeScript 做 Web/BFF/权限/任务/企业微信/流程状态，保留 Python 作为文档解析和 RAG worker，Hermes 继续作为独立 Agent runtime。

推荐组合：

```text
Frontend: React / Next.js
App Backend: TypeScript, preferably Hono or NestJS
DB: Postgres + pgvector
Queue: pg-boss / BullMQ / Temporal later if needed
AI Runtime: Hermes Agent API Server
RAG/Parsing Worker: Python, introduced only when TypeScript is not enough
Deployment: Docker Compose first, later split services
```

如果第一期追求极简，可以先用 SQLite + 本地文件存储；但只要要做真实权限、审计、向量检索和多人使用，建议直接上 Postgres。

## 项目管理方案

### Get Shit Done

适合：

- 快速把想法转成计划、任务切片和执行。
- 单人 AI 辅助开发，需要减少仪式感。
- 原型阶段快速推进。

风险：

- 本机当前未安装 GSD 命令或技能。
- 对长期规范、需求变更、架构约束的沉淀弱于 OpenSpec。
- 社区生态近期有多个来源和分叉，采用前需要固定可信来源和版本。

### OpenSpec + Superpowers

适合：

- 长期维护一个会持续演进的平台。
- 需要把需求、设计、变更、任务、验收标准放进仓库。
- 适合 AI 协作，能减少“边写边漂移”。
- 本机已安装 `openspec`，Claude/Superpowers 插件也已在本地缓存中。

风险：

- 比 GSD 更有仪式感，初期容易写文档多于写代码。
- 如果每个小改动都走完整 spec，会拖慢一个人的节奏。

建议：

- 第一阶段选 OpenSpec + Superpowers 作为主流程。
- 对大功能使用 OpenSpec：认证、企业微信、知识库、Hermes 集成、流程状态、审计。
- 对小任务使用轻量 issue/checklist，不强制完整 spec。
- 暂不引入 GSD；等核心骨架跑通后，再评估是否用 GSD 做短周期执行加速。

## 技能与设计资产

已确认本机相关资源：

- everything-claude-code：已作为 Claude 插件 `ecc` 安装/缓存，来源为 `affaan-m/everything-claude-code`。
- Superpowers：已安装/缓存；可用于 brainstorming、writing-plans、executing-plans、TDD、review 等流程。
- OpenSpec：`/opt/homebrew/bin/openspec` 已存在。
- frontend-design / frontend-patterns：已在共享技能中可用，适合 Web 工作台设计。
- design-md：`.dotfiles` 里已有 Apple、Vercel、Cursor、Claude、Raycast、Stripe 设计参考。

未确认或未发现：

- `google design.md`：未在 `.dotfiles/claude/design-md` 下发现 Google 设计参考。
- `impeccable design`：未在本机技能或插件缓存中发现同名资源。
- `get-shit-done`：未发现本地命令或已安装技能。

建议第一期设计参考：

- 工作台风格优先参考 Cursor/Raycast/Vercel：克制、密集、可扫描。
- 不采用重营销首页，不做大面积装饰。
- 教学管理端强调任务、风险、来源、待办。
- 教师端强调材料生成、课程上下文、学生反馈草稿。

## `.dotfiles` 初始化入口

当前 `.dotfiles` 的入口是：

```bash
~/.dotfiles/install.sh
```

常用模块：

```bash
~/.dotfiles/install.sh claude
~/.dotfiles/install.sh codex
~/.dotfiles/install.sh skills
```

脚本末尾提示的插件安装命令包括：

```text
/plugin marketplace add https://github.com/affaan-m/everything-claude-code
/plugin marketplace add obra/superpowers-marketplace
/plugin marketplace add openai/codex-plugin-cc
/plugin marketplace add forrestchang/andrej-karpathy-skills

/plugin install codex@openai-codex
/plugin install ecc@ecc
/plugin install superpowers@superpowers-marketplace
/plugin install andrej-karpathy-skills@karpathy-skills
/reload-plugins
```

目前没有发现专门的“新项目初始化脚本”。如果需要，可以后续在 `.dotfiles` 或本项目中补一个 `init-campus-project` 脚本，自动完成 OpenSpec 初始化、目录骨架、pre-commit、env 模板和 Docker Compose。

## 第一阶段功能切片

### Slice 0：项目骨架

- Fork 仓库并建立项目文档。
- 初始化 OpenSpec。
- 确定主后端框架、数据库、包管理器和运行方式。
- 建立 `apps/web`、`apps/api`、`packages/shared` 或等价结构。
- 接入基础 CI：lint、typecheck、test。

### Slice 1：身份与角色

- 本地账号或模拟 SSO。
- 角色：教学管理者、教师、系统管理员。
- 权限上下文注入会话。
- 审计日志基础表。

### Slice 2：Hermes 接入

- 启动 Hermes API Server。
- 应用后端调用 Hermes。
- 建立两个 Profile：teaching-admin-agent、teacher-agent。
- 建立基础 Skills：教学制度问答、教学材料生成、会议纪要。

### Slice 3：知识库 MVP

- 上传文档。
- 文档解析。
- Chunk 与元数据。
- 向量检索。
- 回答时展示引用。
- 权限过滤先按角色和文档域实现。

### Slice 4：Web 工作台

- 教学管理者首页：待办、近期教学事项、制度问答、材料生成。
- 教师首页：课程上下文、备课助手、作业/量规生成、制度问答。
- 对话和来源并排展示。
- 文件上传和结果保存。

### Slice 5：企业微信入口

- 企业微信应用配置。
- 回调验签。
- 文本消息问答。
- 待办/提醒推送。
- 复杂结果链接回 Web。

### Slice 6：教学流程状态 MVP

- 选一个流程做状态驱动样板：调课咨询或缓考/补考咨询。
- 定义信息项、缺失信息、规则校验、人工确认。
- 只做预审和材料生成，不直接提交正式系统。

## 数据模型初稿

核心表：

- users
- roles
- user_roles
- departments
- documents
- document_chunks
- document_permissions
- conversations
- messages
- tool_calls
- tasks
- reminders
- audit_logs
- flow_instances
- flow_items
- approvals

关键设计：

- 所有知识回答记录引用文档。
- 所有工具调用记录输入摘要、输出摘要、操作者、时间、会话。
- 所有流程状态变更采用 append-only audit log。
- 敏感信息字段单独标记，默认不进入大模型上下文。

## 风险与红线

高风险：

- 权限越权检索学生或教师数据。
- 知识库过期导致错误制度回答。
- AI 生成正式通知后未经人工审核直接发布。
- 用户把 AI 草稿当作正式评价或处分依据。
- 企业微信移动端泄露敏感结果。
- 过早接入太多业务系统导致维护失控。

红线：

- 不自动修改成绩。
- 不自动做处分、奖助、心理、财务、人事最终判断。
- 不默认读取全校个人数据。
- 不把业务系统 token 暴露给 Hermes prompt。
- 不允许模型自行决定调用高风险写接口。

## 近期决策

已决：

- Fork 名称：`hermes-campus-agent`。
- 入口：Web + 企业微信。
- 第一阶段角色：教学管理副职 + 教师。
- 主后端建议：TypeScript。
- Hermes 定位：Agent runtime 与工具编排，不直接承担强规则业务决策。
- 项目管理建议：OpenSpec + Superpowers 为主，GSD 暂缓。

待决：

- Web 框架：Next.js 全栈，还是 Vite + Hono/Nest 分离。
- 数据库：第一天就 Postgres，还是 SQLite 原型后迁移。
- RAG 方案：Postgres/pgvector，还是独立向量库。
- Hermes 是作为子进程、Docker 服务，还是外部部署。
- 企业微信是否第一期就对接真实组织，还是先用测试企业。

## 下一步

1. 初始化 OpenSpec。
2. 写第一批 specs：身份权限、知识库 MVP、Hermes 接入、企业微信入口、教学管理工作台。
3. 搭建最小 TypeScript monorepo。
4. 接通 Hermes API Server 的最小问答。
5. 做一个制度文档上传、检索、引用回答闭环。
6. 再接企业微信文本消息入口。
