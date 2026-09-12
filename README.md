# STD：统一工程文档标准与模板库

STD 面向软件、硬件、固件、FPGA 和软硬件协同项目，提供项目管理、需求、系统设计、
子系统设计、模块设计、接口契约、验证测试、评审、发布和运维所需的版本化模板。

当前 `0.1.0-draft.26` 优先覆盖：

- Slinky，以及与其协作的 Piko、LLMTier；
- HIFM，包括软件、DPU-SIM、FPGA/RTL、板卡和系统验证。

## 核心规则

1. STD 仓库是模板、Schema 和校验工具的权威来源。
2. 项目通过确定性工具生成文档实例，并把实例提交到自己的仓库。
3. 每个项目采用记录固定 STD 来源版本；每个文档实例固定模板 ID、模板版本和来源哈希。
4. 项目升级模板必须显式执行并评审 diff，禁止静默跟随 STD 更新。
5. RAG 只负责检索，不负责模板分发、版本选择或事实裁决。
6. 系统、子系统、模块和组件使用一致的分层标识，但可选择不同领域 profile。
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
项目可通过 `--output` 沿用既有结构，并在 tailoring 中记录。封面、版本状态和 GitHub Review 规则分别见
[`docs/document-control.md`](docs/document-control.md) 与
[`docs/github-workflow.md`](docs/github-workflow.md)。
版本域、项目采用和模板独立版本见 [`docs/versioning.md`](docs/versioning.md)；
跨语言最低编码要求见 [`docs/coding-standard.md`](docs/coding-standard.md)；
面向实现的设计文档写法和质量检查见 [`docs/design-writing-guide.md`](docs/design-writing-guide.md)。
系统设计的概览、适用性、状态/证据、图和信息安全写法及正反例见
[`docs/architecture-design-authoring-guide.md`](docs/architecture-design-authoring-guide.md)。
AI 编写入口采用“通用方法 + 模板类型专项”：先读
[`docs/ai-authoring-guide.md`](docs/ai-authoring-guide.md)（`0.2.0-draft.1`），
再按其中的映射选择主专项和项目已采用模板，不需要通读全部指南。
13 类专项覆盖当前 45 个模板，同类模板共享方法，计划、报告和决定仍保留不同完成边界；
精确导航见 [`docs/ai-authoring-guides.json`](docs/ai-authoring-guides.json)。
从 HIFM v0.3 迁入的系统方法保留为
[`docs/ai-system-design-authoring-guide.md`](docs/ai-system-design-authoring-guide.md)（`0.6.0-draft.1`）；
机制方法已独立到 [`docs/ai-guides/system-mechanism.md`](docs/ai-guides/system-mechanism.md)。
这些是方法草案，待实际任务验证，不是新模板，不改变项目已采用的 STD/模板版本，
也不自动授权提交、发布或运行。公共规则只在通用指南维护，专项解释本类型的实际设计/取证方法。
系统专项 §7.9 说明 Agent 如何选择场景/系统/软件/FPGA/板卡图样式，复用 SVG、替换项目内容、
调整排版和连接、落入正文并检查实际渲染；样式复用不等于采用示例设计。
局部修订只检查受影响内容和直接依赖，不重跑完整写作流程；原生图源与生成式插画分别维护，
架构视图、实现状态和验证结果分别记录。

当前工作区的 `design.system` 为待发布的 `8.1.0`，保留 `7.0.0` 的 17 个通用主章。
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
诊断在 §11，替代依赖与环回在 §10.4。系统约束由 §3.2 分配、§13.6 验证、§17.2 承接为
下级设计与验收任务。机制未定时先预设计，不能只登记待定或以局部测试关闭系统目标。

`design.definition` 为待发布 `1.2.0`；`design.hardware` 与 `design.fpga` 增加上级约束承接、
本地落实和系统组合验收，当前为待发布 `1.2.0`，不要求另建通用单元文档。
`design.system-mechanism` 为待发布 `2.0.0`，数据与接口分章，16 个主章保留既有约束和段落式指导，
补齐拓扑/身份、资源寿命、维护命令、测试控制/隔离与能力级双方承接；采用短封面和文末控制记录。
九幅[可复用机制图文样板](templates/diagrams/mechanism/README.md)在模板中直接展示：
保留只读六幅关系图，另加开篇用途图和两幅有副作用过程/依赖图。
[暂存导出完整案例](docs/examples/mechanism-side-effect-example.md)给出完整调用和安全停止后未知结果的收口路径；
[机制 AI 专项指南](docs/ai-guides/system-mechanism.md)补充双方调用演练、异常五轴、条件依赖、验证承接和全篇一致性检查。
本轮补实取证来源封口、缺失/无效/不可读的判定，以及仅通过调用入口完成的执行中取消测试；
副作用收口演练按适用条件执行，只读机制检查中断、迟到与临时资源清理，不照搬取证状态。
示例及内存模型不新增项目协议、运行实现或审批要求；逻辑回归不替代真实 IPC/隔离验证。
有副作用的任务失联先核对权威结果，确认旧执行者
停止或隔离并满足幂等/去重条件后才可重新执行，否则阻塞或转人工；只读重新采样不代表原操作恢复。
系统保留端到端原理与关键阶段，机制文档唯一维护详细状态转换及参与方协议。
本轮受影响模板及各自版本见下方复审记录，未列入的模板版本不变；不新增模板种类或审批流程。
模板保留每节可折叠的段落式指导与完成条件；生成器默认将系统文档层级设为 `system`。
本次尚未发布新的 STD 版本或更新已发布来源/RAG 清单；现有 `draft.26` 的不可变来源保持原样。
已采用旧版的项目继续使用原版本，只有用户要求升级时才评估章节映射与内容差异。

## 接口映射与机制预先规划

[统一映射规范](docs/interface-data-mapping-standard.md)连接可读正文、稳定成员 ID、实际机器契约和下游实现/验证。
系统 §3.4 可先登记机制 Document ID、预定文件名及依赖，再逐份成文；计划路径不冒充已完成设计。
[目录 Schema](schemas/interface-catalog.schema.json)、[只读检查器](scripts/validate-interface-catalog)与
[完整虚构案例](docs/examples/interfaces/README.md)给出字段/签名/错误、双向定位和正反例。
本轮版本、15→16 章迁移与实际检查范围见[复审记录](docs/interface-data-mapping-review.md)；
STD `draft.26` 发布版及既有项目 lock 不变，不自动升级项目或复制私密产品协议。

## 上游参考

STD 的覆盖模型参考 ISO/IEC/IEEE 15288、15289 和 42010；系统设计主模板采用面向实现的
设备/软硬件一体设计结构。
项目/系统/软件工程内容参考 NASA Systems Engineering Handbook 与 NASA Software
Engineering Handbook；硬件、接口和验证文档目录参考 ECSS DRD。

STD 不复制受限标准正文。第三方来源和许可证边界见
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。
