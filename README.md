# STD：统一工程文档标准与模板库

STD 面向软件、硬件、固件、FPGA 和软硬件协同项目，提供项目管理、需求、总体系统设计、总体系统机制设计、
子系统设计、模块设计、接口契约、验证测试、评审、发布和运维所需的版本化模板。

当前 `0.1.0-draft.39` 优先覆盖：

- Slinky，以及与其协作的 Piko、LLMTier；
- HIFM，包括软件、DPU-SIM、FPGA/RTL、板卡和系统验证。

本版按[设计数据结构、接口与系统公共错误码描述规范](docs/design-data-interface-format.md)统一六类软件设计模板：数据按性质分类并以真实结构名定义，接口按形态分类并以真实调用形式完整描述；系统公共错误码逐码定义，下级按同一 ID 承接。可按需运行 `python3 scripts/validate-public-error-catalog <系统设计.md>` 检查目录结构和索引；旧项目不会被默认要求升级。其余被修改的模板补充逐节可折叠编写建议；各模板版本独立递增，未改模板保持原版本。

<a id="std-entry"></a>

## Agent 从任意模板进入 STD

STD 是工程文档的标准、模板、编写指南和校验工具库，不是产品设计本身，也不是运行或发布授权。
本 README 是统一执行入口：不依赖 Codex、OpenCode、`AGENTS.md` 或既有会话记忆。
任何 Agent 只要读到一个模板，都应先沿模板开头的链接到这里，再按以下顺序工作。

1. **确认采用来源与任务边界。** 先读目标项目 README、`docs/std.lock.json` 和已有文档 metadata，
   并从项目README靠前入口读取项目规范总索引，再读本任务适用的生效规范；目录、反向链接和强制检查
   见[项目规范索引规则](docs/project-standards.md)。不得漏读项目规则或未经批准覆盖STD。
   使用项目已采用的 STD revision、模板版本及来源清单。普通编写或修改不检查最新版，
   不自动升级。首次接入按[接入规则](docs/adoption.md)明确采用来源；资料缺失或相互冲突时报告缺口，
   不声称已符合标准，也不自行扩大修改范围。
2. **选择正确的文档。** 按[模板选择规则](docs/template-selection.md)确定对象层级和交付责任，
   从[模板目录](templates/catalog.json)确认 Template ID，不因先看到某个模板就强行套用。
3. **读取编写方法。** 读[通用 AI 编写指南](docs/ai-authoring-guide.md)，再按其中映射读取本类型
   的专项指南和模板全部编写建议。设计文档同时遵循[设计编写规范](docs/design-writing-guide.md)；
   接口与数据按[映射规范](docs/interface-data-mapping-standard.md)保持唯一机器来源。
4. **基于项目事实成文。** 新文档按下文生成命令创建 Markdown 与 metadata；修改现有文档则保留
   已有内容和采用版本。先解决方案、约束、流程与失败出口，再用正文、图和表交付结论。
   示例只是教学，不能当作已实现或实测事实；关键设计未决要有责任方及关闭条件。
5. **检查实际交付。** 依据模板完成条件和专项指南检查内容、图文一致性、上下游及接口映射，
   再运行下文结构校验及适用的专项检查。局部修改检查受影响部分及直接依赖。
   结构通过不代表设计完成，设计完成不代表代码实现或运行验证。
6. **按授权交付。** 报告改动、检查结果、未决项及未运行项；提交、push、发布、部署均遵循用户
   当前授权。模板导航、编辑指令和生成过程不进入正式产品正文。

所有文档模板封面标题后均保留同一反向入口；项目 README 必须在标题及简短项目介绍之后、安装和
使用章节之前提供 STD 采用说明，标准片段见[接入规则](docs/adoption.md#readme-entry)。
`scripts/new-design` 将封面入口转换为项目 README 的 `std-entry` 链接，仅保留导航，不把作者指令
复制为产品正文；不传项目根目录时链接当前 STD 来源 README。工具不覆盖项目 README，接入时须补齐
该入口。手工实例化也应维护这条链接。若模板被单独复制导致相对链接失效，应从项目
采用记录定位同一 revision 的 STD README 和指南；找不到时请求提供该来源，不能改读远端最新版本
并宣称仍遵循原锁定版本。导航不替代项目事实或授权，也不要求新建额外 Agent 配置文件。

## 核心规则

**GitNexus 检索入口：** 已接入GitNexus MCP的Agent先用 `list_repos` 找到 `STD`，读取
`gitnexus://repo/STD/context`，再显式指定 `repo: "STD"` 按文件路径读取本README及适用规范。
调用示例、客户端连接和版本核对见[GitNexus快速导航](docs/gitnexus-navigation.md)。
代码搜索无结果不代表规范不存在；检索到的当前版本不得自动替代项目锁定版本。

1. STD 仓库是模板、Schema 和校验工具的权威来源。
2. 项目通过确定性工具生成文档实例，并把实例提交到自己的仓库。
3. 每个项目采用记录固定 STD 来源版本；每个文档实例固定模板 ID、模板版本和来源哈希。
4. 项目升级模板必须显式执行并评审 diff，禁止静默跟随 STD 更新。
5. RAG 只负责检索，不负责模板分发、版本选择或事实裁决。
6. 总体系统下分软件系统、固件系统和硬件系统；软件子系统只用于软件分支，当前不递归，详见[分层设计](docs/template-selection.md#2-分层设计)。
7. 项目 README 和 `docs/std.lock.json` 记录项目采用的 STD 版本；STD 更新不自动推动项目升级。
8. 每个模板独立维护 Template Version；单份文档只追踪自己采用的模板版本和哈希。

## 首版模板

模板清单见 [`templates/catalog.json`](templates/catalog.json)，选择方法见
[`docs/template-selection.md`](docs/template-selection.md)。

```text
templates/
├── management/       项目、开发、SEMP、配置、风险、质量、安全计划
├── requirements/     用户需求、ConOps、需求规格与追踪
├── evaluation/       技术分析、备选比较与证据结论
├── design/           系统、跨子系统机制、分层设计、硬件与 FPGA
├── diagrams/         可直接编辑复用的 SVG 图形样式（不注册为文档类型）
├── product/          解决方案、SKU 规格与产品路线图
├── interfaces/       接口控制
├── contracts/        API、Schema、事件与错误契约
├── assurance/        V&V、测试计划/步骤/报告、验收和 FPGA 实现报告
├── review/           评审包
├── decisions/        ADR
└── operations/       用户、安装、运维、维护、Bring-up、发布与退役
```

## 在项目中使用

新项目先采用[项目 README 模板](templates/_shared/project-readme.md)，将 STD 说明放在首页靠前位置。
已有 README 只合并该入口，不覆盖项目原有内容。它是仓库入口脚手架，不是设计文档实例。

创建文档实例：

```bash
./scripts/new-design \
  --project slinky \
  --template design.system \
  --name system-design \
  --project-root /path/to/project \
  --repository corezilla/slinky \
  --owner system-architecture-team \
  --author "Author Name"
```

校验一个项目的 STD 文档：

```bash
./scripts/validate-design \
  --project-root /path/to/project \
  --require-immutable-std \
  --json /path/to/project/artifacts/std-validation.json
```

生成器会同时创建 Markdown 文档和 `<name>.metadata.json`。项目应提交两者，并保存
`docs/std.lock.json` 与独立的 `docs/std-source-manifest.json`。来源清单用
`scripts/build-source-manifest` 生成、`scripts/verify-source-manifest` 校验；它不是 RAG ingestion
manifest。完整接入规则见 [`docs/adoption.md`](docs/adoption.md)。
该检查覆盖 STD 文档结构，不替代项目契约/Schema 验证或 runtime 与外部依赖证据。

[`docs/repository-layout.md`](docs/repository-layout.md) 给出了完整项目仓库的推荐目录和文档默认落位，
纯软件项目见 [`docs/software-project-layout.md`](docs/software-project-layout.md)；
项目可通过 `--output` 沿用既有结构，并在 tailoring 中记录。
软件源码默认按 `src/<subsystem>/<module>/` 或 `src/<module>/` 组织，模块单元测试按
`tests/unit/<module>/` 组织；目录名须与稳定 Module ID 建立映射。
封面、版本状态和 GitHub Review 规则分别见
[`docs/document-control.md`](docs/document-control.md) 与
[`docs/github-workflow.md`](docs/github-workflow.md)。
版本域、项目采用和模板独立版本见 [`docs/versioning.md`](docs/versioning.md)；
跨语言最低编码要求见 [`docs/coding-standard.md`](docs/coding-standard.md)；
面向实现的设计文档写法和质量检查见 [`docs/design-writing-guide.md`](docs/design-writing-guide.md)。
总体系统设计的概览、适用性、状态/证据、图和信息安全写法及正反例见
[`docs/architecture-design-authoring-guide.md`](docs/architecture-design-authoring-guide.md)。
AI 编写入口采用“通用方法 + 模板类型专项”：先读
[`docs/ai-authoring-guide.md`](docs/ai-authoring-guide.md)（`0.2.0-draft.9`），
再按其中的映射选择主专项和项目已采用模板，不需要通读全部指南。
15 类专项覆盖当前 48 个模板，同类模板共享方法，计划、报告和决定仍保留不同完成边界；
精确导航见 [`docs/ai-authoring-guides.json`](docs/ai-authoring-guides.json)。
软件模块需要独立实现规格时使用可选的 [`ISD模板`](templates/design/implementation-design.md)，
配套 [`ISD规范`](docs/isd-standard.md) 和 [`AI编写指南`](docs/ai-guides/implementation-design.md)。
默认一模块一份，覆盖多个文件；模块设计已足够详细时兼作，不重复增加设计层级。
`design.implementation` 当前为 `1.2.0`：greenfield 不虚构 Current，函数输入/输出/错误、重要流程图、配置落点及状态型/持久化实现必须展开
函数并发契约、错误传播、schema 演进拒绝语义、库状态分支和本地持久化安全；记录型内容采用
固定字段段落，状态矩阵才使用表格；交付检查强制关键函数并发契约、错误传播、schema 策略和六类库状态。
ISD 规范为 `0.5.0-draft.1`，专项指南为 `0.5.0-draft.5`。
从 HIFM v0.3 迁入的系统方法保留为
[`docs/ai-system-design-authoring-guide.md`](docs/ai-system-design-authoring-guide.md)（`0.7.0-draft.8`）；
机制方法已独立到 [`docs/ai-guides/system-mechanism.md`](docs/ai-guides/system-mechanism.md)。
这些是方法草案，待实际任务验证，不是新模板，不改变项目已采用的 STD/模板版本，
也不自动授权提交、发布或运行。公共规则只在通用指南维护，专项解释本类型的实际设计/取证方法。
系统专项 §7.9 说明 Agent 如何选择场景/系统/软件/FPGA/板卡图样式，复用 SVG、替换项目内容、
调整排版和连接、落入正文并检查实际渲染；样式复用不等于采用示例设计。
局部修订只检查受影响内容和直接依赖，不重跑完整写作流程；原生图源与生成式插画分别维护，
架构视图、实现状态和验证结果分别记录。

当前 `design.system`（总体系统设计）为 `10.1.0`，保留 `7.0.0` 的 17 个通用主章。
正文仍采用八项必要字段的短封面，附录 A 保存控制信息与导航，附录 B 保存输入/适用性，
附录 C 保存编写与交付检查。保留各节的段落式编写建议、完成条件及已确认的原创教学图。

`7.0.0` 已完成、`8.0.0` 继续沿用的章节映射（相对 `6.4.0`）：

| 原位置 | `7.0.0` 位置与责任 |
|---|---|
| §3 概览 + §5 总体结构 | §3 系统概览：§3.1 系统架构、§3.2 组成与职责、§3.3 物理与逻辑对应关系 |
| §4.2 功能详细说明 | §4.2 关键功能原理与边界，保留逐功能展开单元 |
| §6.1 / §6.4 / §6.2 / §6.3 | §5.1 总览、§5.2 一次业务处理怎样完成、§5.3 启动、§5.4 配置加载与生效 |
| §6.5–6.7 | §5.5–5.7 停止/重启、异常恢复与模式切换 |
| §7–17 | §6–16，原专业章节顺序及设计义务保留 |
| §18 | §17 决策、风险与未决项；§17.2 下级详细设计与验收任务，保留关联风险和预设计 |

第 3 章不再重复一份总体结构；第 5 章先让读者理解完整业务，再说明生命周期，阅读顺序不
改变启动和配置前提。HIFM 的推理请求标题泛化为业务处理标题，不搬运其项目内容和设计参数。
上述 `7.0.0` 目录调整为 17 个主章，属于不兼容结构调整；其他模板不连带升级。

`8.0.0` 进一步收紧系统/下级责任边界：跨组件共同方案及完整公共契约不得再推迟为下级细化，
因此按版本规范提升 MAJOR。通用子节补充对象/访问拓扑、运行时统筹及确认、公共操作与字段、
命令、硬件连接、配置与兼容核对、自检编排、统计关联及测试控制。每个新增节都有段落式建议、
适用条件、虚构示例、完成条件和正文填写位置；不强制产品新增这些能力。
AI 指南按能力贯通章节、先复用并核对现有契约，再交接双方任务，并提供只读版本核对的完整
小案例；未决设计与待实现/实测分开，不因模板扩展要求旧项目重新迁移。

图形样板的当前落点为：§2.3 逻辑应用场景、§3.1 轻量系统架构、§3.2 逐组件职责、§6.1
自研板卡顶层布局、§7.1 软件分层、§8.1 自研 FPGA 程序架构。原有图件 bytes 不变，
[SVG 样式及编辑说明](templates/diagrams/README.md)可直接复用；位图原件及获准生成记录分别保留。
软件图用左侧层名和无图标、无连接线的模块分组；板卡图不是实际 PCB 布线，FPGA 图不是芯片
内部资源架构。样板均为原创虚构教学素材，不宣称整套示例已经补齐。`new-design` 仍移除明确
标记的教学段落，保留章节与填写指导，由项目作者写入真实设计。

可测试性在 §13 展开方法/判定、受控故障、部署复位、并发隔离、自动化与验收；统计、自检和
诊断在 §11，替代依赖与环回的入口在 §10.4。系统约束由 §3.2 分配、§13.6 验证、§17.2 承接为
下级设计与验收任务。机制未定时先预设计，不能只登记待定或以局部测试关闭系统目标。

新增[软件系统设计说明书模板](templates/design/software-system-design.md) `design.software-system`，当前独立版本 `2.1.0`：§3.6 描述功能与用户任务，§8.4 集中定义 CLI、WebUI 和维护接口，并内嵌命令及页面图例。第 4 章并入 §3 后其余章号前移，属于不兼容结构调整；项目不会自动升级。
软件 AI 指南补充架构分层、正式英文组件命名、图后说明与反例检查，并提供 UI/业务/驱动/按需系统层 SVG 图例；不按对象类型或历史属性分层。
现有主章内新增应用环境、启动、业务、配置、停止和数据流六张 SVG/PNG 图例；功能已合并进 §3.6，当前为 16 个主章，数据小节按统一结构调整。
每个重要流程必须有图、正文和异常分支；先用一节真实方案检验写作质量，再扩展全篇。
方法及完整虚构样稿见[软件 AI 指南](docs/ai-guides/software-system.md)和[启动与恢复示例](docs/examples/software-startup-design-example.md)。
从总体模板派生为 16 个软件主章及文末附录，各节保留段落式编写建议、示例和完成条件。
§3.1 前置软件系统架构图，§3.2 紧接各组件职责，§3.6 展开功能；§4 展开子系统及直属模块概要，不重复全系统总图。
软件组成、运行部署、配置与构建成为主体，保留产品、重要过程、数据/接口、维护、安全、预算与可测试性。
纯软件项目可直接作顶层；领域模式通过父文档承接总体系统的软件职责。
默认生成到 `docs/20_system_design`，配套[软件系统 AI 指南](docs/ai-guides/software-system.md)与两幅可编辑 SVG。
初版仍需真实项目试写，不因结构检查通过声称设计质量或运行验证通过。

新增 [软件子系统设计模板](templates/design/subsystem-design.md) `design.subsystem`，当前独立版本 `1.2.0`，
14 个主章以概要设计为中心：第1章集中输入、第2章第0层整体架构、第3章第1层分层与模块设计、运行设计、数据/接口/配置、
调试维护、部署测试和性能；保留系统约束及下游承接，含同一虚构软件的上下文/整体架构/分层模块三图与逐节指导，不替代模块详细设计。
0.5.0 到 0.6.0 的旧新章节映射见模板附录 A，已有项目不自动迁移。
系统对齐复审补齐身份/模式/过程映射、数据组织与阶段变换、安全执行点、维护测试子节及扩展兼容边界。
软件子系统通过 `parent_document_id` 承接软件系统设计，下接软件模块，不采用递归子系统；组成、接口权威和验证均按对象区分。
生成器支持 `--parent-document-id`，`validate-design --check-design-hierarchy` 可对完整输入显式检查父链并返回父文档关联，不计算子系统深度。
默认生成到 `docs/30_subsystem_design`，共用[软件子系统与模块 AI 指南](docs/ai-guides/unit-design.md)。
旧子系统文档不自动迁移，板卡/FPGA 对象直接采用专项模板。软件系统设计使用独立模板，不用软件子系统模板代替。

`design.definition` 为 `3.2.0`《软件模块设计说明书》，保留 15 个主章；服务型模块可把 HTTP/RPC 端点集登记为操作面，§5–7 显式展开内部组成、文件调用、文件间接口与字段级数据结构，§13 固定文件分解和实现步骤。功能及附录 A 机制承接采用可读的固定字段段落，并登记 ISD 采用模式；附录 A 用 Mechanism Document ID + Requirement ID 精确承接机制 §14.4，落实到正文、接口、文件/symbol 和验证。
配套子系统与模块 AI 指南为 `0.13.0-draft.5`，增加模块试写流程、历史问题复发检查、[异步模块连续案例](docs/examples/module-async-export-example.md)以及经授权的 [LLMTier M001/M002 实证样板](demo/llmtier-module-design/README.md)。新版模块生成限制软件模块层级，并保留内容寻址的教学参考；构建装配、生命周期预算及四类恢复动作分别核对。旧采用实例不自动升级。
`design.hardware` 与 `design.fpga` 增加上级约束承接、
本地落实和系统组合验收，当前均为 `1.4.0`，不要求另建通用单元文档。
`design.system-mechanism`（总体/纯软件系统机制设计）为 `3.2.0`，数据与接口分章，16 个主章保留既有约束和段落式指导，编写指令与教学内容隔离于项目正文；§5 对每个重要接口强制用代表输入完成调用演练，§14 固定为参与方映射、步骤责任、跨单元接口和下级设计输入四段式要求侧，纯软件 API 裁剪示例放附录 A；下级要求、风险和约束使用不同 ID 命名空间。

上述六类软件设计文档的数据主章统一名为“数据结构设计”，按公共基础类型、业务数据、配置规则、通信报文、设备/FPGA 表项、运行状态、数据库表和错误码八类提供可裁剪入口；每个真实结构在所属类别下一处写完定义、字段、约束、寿命、实例与验证，不另建重复清单。总体、系统、机制、子系统、模块和 ISD 仅补本层必要的跨结构分析。[数据字典模板](templates/design/data-dictionary.md)当前为 `2.1.0`，同样按八类逐结构完整呈现字段阅读视图，但不拥有操作接口。公共字段与系统错误码仅由唯一来源定义，下级用相同 ID 承接；详见[设计数据结构、接口与系统错误码描述规范](docs/design-data-interface-format.md)。
上述六类文档的接口主章也统一名为“接口设计”，按软件、消息与数据流、硬件与固件、人机与维护四类适用接口组织；每个真实接口以名称或调用形式为主标题，在一处写完输入、输出、错误、交互、实例和验证。不另建重复的接口清单，也不维护全部调用函数的反向索引；公共签名、字段和错误保持唯一权威。
模板同时补齐机器源/Proposed 两种数据定义分支、拓扑/身份、资源寿命、维护 API/命令、测试控制/隔离与双向承接；采用短封面和文末控制记录。
九幅[可复用机制图形](templates/diagrams/mechanism/README.md)由外部教学案例完整展示：
[只读观测案例](docs/examples/mechanism-readonly-observation-example.md)使用开篇用途图和六幅关系图，
有副作用案例使用过程/依赖图；模板只保留稳定导航，避免把大段教学正文复制进项目文档。
[暂存导出完整案例](docs/examples/mechanism-side-effect-example.md)给出完整调用和安全停止后未知结果的收口路径；
[机制 AI 专项指南](docs/ai-guides/system-mechanism.md)补充双方调用演练、异常五轴、条件依赖、验证承接和全篇一致性检查。
本轮补实取证来源封口、缺失/无效/不可读的判定，以及仅通过调用入口完成的执行中取消测试；
副作用收口演练按适用条件执行，只读机制检查中断、迟到与临时资源清理，不照搬取证状态。
示例及内存模型不新增项目协议、运行实现或审批要求；逻辑回归不替代真实 IPC/隔离验证。
有副作用的任务失联先核对权威结果，确认旧执行者
停止或隔离并满足幂等/去重条件后才可重新执行，否则阻塞或转人工；只读重新采样不代表原操作恢复。
系统保留端到端原理与关键阶段，机制文档唯一维护详细状态转换及参与方协议。
本轮受影响模板及各自版本见下方复审记录，未列入的模板版本不变；上述机制复审不新增模板种类或审批流程；新增子系统模板见上文。
模板保留每节可折叠的段落式指导与完成条件；生成器默认将系统文档层级设为 `system`。
上述改进原随 STD `0.1.0-draft.30` 发布；既有 `draft.26` 来源/RAG 清单作为历史不可变证据保留，
不回写为新版本。已采用旧版的项目继续使用原版本，只有用户要求升级时才评估章节映射与内容差异。

## 接口映射与机制预先规划

[统一映射规范](docs/interface-data-mapping-standard.md)连接可读正文、稳定成员 ID、实际机器契约和下游实现/验证。
系统 §3.4 可先登记机制 ID、上级 Mechanism ID、Document ID、预定文件名及前置依赖，再逐份成文；归属与依赖分开，计划路径不冒充已完成设计。
[目录 Schema](schemas/interface-catalog.schema.json)、[只读检查器](scripts/validate-interface-catalog)与
[完整虚构案例](docs/examples/interfaces/README.md)给出字段/签名/错误、双向定位和正反例。
检查器从源签名推导角色与完整性，并复用原封面/metadata 身份；注释不再拥有独立文档版本。
本轮版本、15→16 章迁移与实际检查范围见[复审记录](docs/interface-data-mapping-review.md)；
既有项目 lock 不自动升级，也不复制私密产品协议；项目只有在用户明确要求后才采用 `draft.32`。

## 批量机制写作准备

接口控制与契约规格模板各为 `0.4.0`，测试规格为 `0.2.1`；三者逐章提供段落式建议、
完成条件及贯穿示例，不仅保留空标题。[机制 AI 指南 §10](docs/ai-guides/system-mechanism.md#10-批量编写与跨文档复审)
说明固定一批输入、共享契约唯一修改、父子承接和受影响文档的组合复查，不引入新的写作平台。
[Host—驱动—FPGA 教学案例](docs/examples/host-fpga-transfer-example.md)给出完整逻辑调用、原生布局、
停止/排空和 V→Case/环境的路径；未实现具体 OS/总线绑定，不宣称真实硬件验证。

接口目录工作模型为 `2.0.0`：新增必填 downstream_inventory，绑定独立承接范围并检测漏消费者、
漏 backend、错模块及无理由的裁剪。它与原 `1.0.0` 不兼容，旧项目仅在明确采用本修订时迁移；
scope 真实性与批准仍需内容复审。当前变更及验证边界见[复审记录 §6](docs/interface-data-mapping-review.md#6-批量写作准备修订)。

## 上游参考

STD 的覆盖模型参考 ISO/IEC/IEEE 15288、15289 和 42010；系统设计主模板采用面向实现的
设备/软硬件一体设计结构。
项目/系统/软件工程内容参考 NASA Systems Engineering Handbook 与 NASA Software
Engineering Handbook；硬件、接口和验证文档目录参考 ECSS DRD。

STD 不复制受限标准正文。第三方来源和许可证边界见
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。
