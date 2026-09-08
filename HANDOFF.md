# STD 项目交接说明

> **范围更正与状态提示（2026-09-07）**：STD 面向今后所有软件、硬件、固件、FPGA
> 及软硬件协同项目，不仅面向 Slinky、Piko、LLMTier。本文是项目启动时的历史规划稿，
> 其中以 arc42 系统设计为中心的目录和交付物已经被首版多模板方案取代。当前实施状态、
> 项目采用方法和迁移指令以 [`MIGRATION_HANDOFF.md`](MIGRATION_HANDOFF.md) 为准。

更新时间：2026-09-07  
项目目录：`/Users/ben/work/STD`  
规范仓库：`corezilla/STD`
状态：项目启动草案，等待在独立 Codex 项目中评审和实施

## 1. 项目目标

STD 用于建立一套供所有现有和后续软硬件项目共同使用的工程文档标准与模板库。
Slinky、Piko、LLMTier 和 HIFM 是首批验证项目，不构成 STD 的适用范围边界。

首版组合使用多套业界体系。arc42 v9.0 仅作为系统/软件架构模板的参考之一；STD 还需要
覆盖项目管理、需求、系统、子系统、模块、实现单元、硬件、固件、FPGA、接口、验证、
评审、发布和运维，并形成可执行、可验证的 docs-as-code 标准。

- API、JSON Schema、事件和错误契约；
- 数据模型、状态机和一致性约束；
- 幂等、事务、持久化与故障恢复；
- Secret、身份、权限和跨项目数据隔离；
- Unit、Contract、Recovery、Security、E2E traceability；
- ADR、Review、版本冻结、发布门禁和证据分级；
- Codex Skill 与 CI 校验；
- 文档门户和 RAG 的派生索引规范。

目标不是把三个项目的设计合并到一个文档中，而是统一结构、质量要求、工具和评审方法，
同时保持每个项目的责任边界与设计 authority。

## 2. 已确定的核心原则

### 2.1 Source of Truth

1. STD Git 仓库是模板、规范、Schema、生成器和校验器的唯一权威来源。
2. 每个项目的实际系统设计仍保存在自己的 Git 仓库中，与代码、Schema、测试和 commit
   一起评审。
3. 项目实例必须固定 `template_version`，不得通过软链接、远程 include 或共享可变文件
   使已评审文档被模板更新静默改变。
4. 模板升级由项目显式执行，并产生可审阅 diff。

### 2.2 RAG 的定位

1. RAG 是检索和发现层，不是模板分发机制，也不是事实权威。
2. 模板应用必须由确定性的生成器、Codex Skill 和 CI validator 完成。
3. RAG 只索引已提交的文档、ADR、契约、QA 和验证证据，并保留来源 commit。
4. 检索必须先应用 project、authority、status、visibility 等 metadata/ACL，再进行语义或
   hybrid retrieval。
5. RAG 回答必须携带来源项目、文件、版本和 commit；不得把 draft、superseded 或其他
   Project authority 的材料冒充当前决定。

### 2.3 文档和协作语言

- STD 的模板、说明、示例和主要设计文档使用中文。
- 必须保留 API field、协议名、状态名和标准术语的精确英文标识符。
- 跨 Slinky、Piko、LLMTier 的正式需求和评审继续通过用户指定的 Matrix/Element
  机制完成；STD 不创建新的跨项目通信路径。

## 3. 推荐目录结构

```text
/Users/ben/work/STD/
├── HANDOFF.md
├── README.md
├── VERSION
├── templates/
│   └── arc42-zh/
│       ├── system-design.md
│       ├── system-design-help.md
│       ├── adr.md
│       ├── review-packet.md
│       ├── review-checklist.md
│       ├── traceability.md
│       └── diagrams/
│           ├── context.mmd
│           ├── container.mmd
│           ├── runtime-sequence.mmd
│           └── deployment.mmd
├── schemas/
│   ├── architecture-document.schema.json
│   ├── template-metadata.schema.json
│   ├── adr-metadata.schema.json
│   └── rag-document-metadata.schema.json
├── scripts/
│   ├── new-design
│   ├── upgrade-template
│   ├── validate-design
│   └── build-rag-manifest
├── skills/
│   └── system-design-doc/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── examples/
│   ├── minimal-service/
│   └── distributed-agent-system/
├── docs/
│   ├── governance.md
│   ├── versioning.md
│   ├── adoption.md
│   ├── rag-ingestion-contract.md
│   └── decisions/
└── tests/
```

目录是建议结构，不是已经冻结的实现。独立项目应先评审，再一次性建立骨架，避免产生
多套互相竞争的模板或脚本。

## 4. 系统设计模板结构

基础采用 arc42 的十二章：

1. 引言与目标；
2. 架构约束；
3. 系统范围与上下文；
4. 解决方案策略；
5. 构建块视图；
6. 运行时视图；
7. 部署视图；
8. 横切概念；
9. 架构决策；
10. 质量要求；
11. 风险与技术债；
12. 术语表。

STD 增加以下规范化附录：

- A. 数据模型与状态机；
- B. API、Schema、Event 与错误契约；
- C. 数据持久化、一致性、幂等与恢复；
- D. 安全、隐私、Secret 与审计；
- E. 可观测性、容量、性能和 SLO；
- F. 测试设计与需求 traceability；
- G. 部署、迁移、回滚和发布门禁；
- H. 未决问题、外部依赖和后续版本。

模板不得只提供标题。每个重要章节必须包含：写作目的、必填内容、可选内容、禁止事项、
最小示例、Review checklist 和 machine-checkable metadata。

## 5. 项目实例规范

建议各项目使用：

```text
<project>/docs/architecture/
├── system-design-vX.Y.md
├── metadata.json
├── decisions/
├── diagrams/
├── review/
└── evidence/
```

`metadata.json` 至少包含：

```json
{
  "project": "piko",
  "document_type": "system-design",
  "template": "arc42-zh",
  "template_version": "1.0.0",
  "document_version": "0.3",
  "status": "draft",
  "authority": "piko",
  "source_commit": null,
  "supersedes": null
}
```

字段和枚举需要由 JSON Schema 冻结；此处仅为起始建议。

## 6. Codex Skill 目标

创建一个可安装的 `system-design-doc` Skill。它应在用户要求编写、扩写、评审或迁移系统
设计时生效，并强制执行：

1. 读取项目 instructions、现有设计、契约、Schema、QA 和 ADR；
2. 读取并固定 STD template version；
3. 使用 arc42 中文模板，不得随意省略构建块、运行时、部署、持久化、恢复和安全；
4. 根据项目规模选择必要深度，但所有删减必须在 tailoring manifest 中说明；
5. 生成或更新 context、building-block、runtime sequence 和 deployment 图；
6. 将重要决定写为 ADR，并关联需求、Schema、测试和未决问题；
7. 运行 STD validator；
8. 输出 changed files、commit/diff、traceability、验证结果和 blockers；
9. 不替代项目自身的审批和跨项目 Review 流程。

Skill 应引用 STD 版本化资源；不要把完整模板复制进 Skill 后形成另一份权威来源。

## 7. RAG 索引契约

首版先设计 contract 和 manifest generator，不急于选择 vector database 或 embedding
provider。`rag-document-metadata` 至少包含：

```json
{
  "project": "piko",
  "authority": "piko",
  "document_type": "system-design",
  "document_version": "0.3",
  "template_version": "1.0.0",
  "status": "accepted",
  "visibility": "project",
  "source_repository": "corezilla/piko",
  "source_path": "docs/architecture/system-design-v0.3.md",
  "source_commit": "<immutable commit>",
  "section_id": "runtime-view.matrix-ingress",
  "effective_at": "<timestamp>",
  "supersedes": null
}
```

需要冻结的行为：

- 只从 Git commit/tag 构建索引，不直接索引未保存的编辑器内容；
- chunk 边界优先按标题、ADR 和 Schema object，不使用任意定长切割作为唯一策略；
- 保留 section hierarchy、source path、commit 和 authority；
- draft/review/accepted/superseded 必须可过滤；
- 删除或 supersede 时必须可撤销旧索引；
- retrieval 返回引用，调用方能够打开原始文件和 commit；
- ACL 在 retrieval 前执行，不能只依赖生成阶段提示词；
- 对文档中的 prompt injection 和不可信内容建立 ingestion/retrieval guardrail。

## 8. 首轮交付物

第一阶段必须交付：

1. STD repository skeleton；
2. arc42 v9.0 中文版来源、许可证与定制差异说明；
3. `arc42-zh/system-design.md` 完整模板；
4. ADR、Review Packet、Review Checklist、Traceability 模板；
5. template/document/ADR metadata JSON Schema；
6. `new-design` 和 `validate-design` 最小可运行工具；
7. `system-design-doc` Codex Skill；
8. 一个小型服务示例和一个多项目 Agent 系统示例；
9. adoption/versioning/governance 文档；
10. RAG ingestion contract 和 manifest generator，但不要求首轮部署生产 RAG。

## 9. 验收标准

首版完成需要满足：

- 所有模板和说明使用中文；
- arc42 十二章与 STD 八个附录均有明确适用规则；
- 模板能够生成单文件或多文件项目实例；
- 所有实例记录 template version；
- validator 能识别缺失必填章节、非法 metadata、未解析占位符和失效本地链接；
- upgrade 产生可审阅 diff，不覆盖项目自定义内容；
- Skill 能在隔离示例项目中生成完整设计并运行 validator；
- RAG manifest 能从项目设计生成带 project/authority/status/commit 的记录；
- 不存在软链接、远程可变 include、RAG-only source of truth 或第二套隐藏模板；
- README 给出新项目采用、已有项目迁移和模板升级的完整命令。

## 10. 非目标

首版不负责：

- 建立完整企业文档门户；
- 选定或部署生产 vector database；
- 自动批准架构设计；
- 自动把 Matrix transcript 当作架构决定；
- 把 Slinky、Piko、LLMTier 的业务 authority 合并到 STD；
- 为不同项目创建互相兼容但内容不同的隐式模板分支。

## 11. 风险与注意事项

- arc42 中文版是上游模板；STD 必须记录上游版本和许可证，不得丢失归属信息。
- 模板过重会导致机械填充；需要 tailoring manifest，但裁剪规则必须显式且可校验。
- RAG 容易把历史草案和当前冻结决定混合；status、effective time、supersedes 和 commit
  metadata 是强制要求。
- Skill、模板和 validator 可能漂移；三者必须共享一个 STD version，并有一致性测试。
- 跨项目设计只能读取用户明确授权的材料；RAG 不扩大原有访问权限。

## 12. 与现有项目的接入顺序

建议顺序：

1. 在 STD 中完成模板、validator 和 Skill 的最小闭环；
2. 以 Piko v0.3 作为第一个真实迁移项目；
3. 由 Piko/Slinky/LLMTier 分别 Review 模板是否覆盖各自边界；
4. 修订 STD，而不是在各项目中复制出不同模板；
5. 再迁移 Slinky 与 LLMTier；
6. 三个项目稳定后生成统一 RAG manifest 并评估检索方案。

Piko 当前可作为输入的材料：

- `/Users/ben/work/piko/docs/design/agent-runtime-service-design-v0.2.md`
- `/Users/ben/work/piko/docs/design/agent-runtime-matrix-collaboration-design-v0.3.md`
- `/Users/ben/work/piko/docs/contracts/agent-runtime-matrix-openapi-v0.3.yaml`
- `/Users/ben/work/piko/docs/contracts/schemas/agent-runtime-matrix-v0.3.schema.json`
- `/Users/ben/work/piko/docs/qa/agent-runtime-contract-qa-v0.3.md`
- `/Users/ben/work/piko/docs/review/matrix-element-v0.3-review-packet.md`

这些文件是迁移输入，不是 STD 模板本身。

## 13. 启动新 Codex 项目的建议首条指令

可在 `/Users/ben/work/STD` 项目中发送：

> 阅读 `HANDOFF.md`，以 arc42 v9.0 中文版为上游基础建立 STD。先检查目录和 Git 状态，
> 然后调研上游许可证与中文模板结构，提出首版目录、版本策略和实施计划。不要直接把
> Piko/Slinky/LLMTier 的项目设计复制为公共模板，不要先部署 RAG。第一阶段完成模板、
> Schema、validator、Codex Skill 和示例的最小闭环；所有文档使用中文，并保留上游归属、
> immutable source version、项目 authority 和可审阅 diff。

## 14. 尚待新项目决定

以下问题在 STD 项目内评审后冻结：

1. STD 的正式全称和 GitHub repository 名称；
2. arc42 中文上游的确切 commit/tag；
3. 首版使用单文件 Markdown、多文件 Markdown，还是两者都生成；
4. Mermaid、PlantUML、Structurizr/C4 或 draw.io 的图形标准；
5. tailoring manifest 的字段和允许裁剪规则；
6. Skill 的安装、更新和版本 pin 方式；
7. CI 支持的运行环境；
8. RAG 首个 consumer、ACL source 和索引更新触发方式。

在这些问题冻结前，可以推进模板调研、仓库骨架、Schema 草案和示例设计，不需要阻塞。
