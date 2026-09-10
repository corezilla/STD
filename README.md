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
AI Agent 的任务计划、输入核查、章节预设计、分步成文、绘图验收和长任务续写方法见
[`docs/ai-system-design-authoring-guide.md`](docs/ai-system-design-authoring-guide.md)。
这是从 HIFM v0.3 迁入的通用执行指南（`0.3.1-draft.11`，待完整写作任务验证），不是新模板，
不改变项目已采用的 STD/模板版本，也不自动授权提交、发布或运行。
指南 §7.9 说明 Agent 如何选择场景/系统/软件/FPGA/板卡图样式，复用 SVG、替换项目内容、
调整排版和连接、落入正文并检查实际渲染；样式复用不等于采用示例设计。
局部修订只检查受影响内容和直接依赖，不重跑完整写作流程；原生图源与生成式插画分别维护，
架构视图、实现状态和验证结果分别记录。

当前工作区的 `design.system` 为待发布的 `6.4.0`：沿用 `6.0.0` 的 Markdown 短封面，正文前仅保留八项
必要控制字段；其余控制信息、修订和长目录在附录 A。§1 只保留 1.1 目的与读者、1.2 范围；
原 §1.3–1.6 移至 §B.1–B.4，统一编写与交付检查移至附录 C。
§2 为产品应用与设计目标，§3 为系统概览，第 4–18 章编号不变。这是显示结构与章节引用的
不兼容调整，因此独立提升系统模板主版本；不会自动迁移已采用旧模板的项目。
`6.3.0` 在 §2.3 展示自动流水线、工业相机及桌前操作人员的逻辑应用场景，不表示实际部署或布线；§5.1 保留已确认的
轻量架构图，§5.2 逐一说明六个组件的职责，不展开子系统内部。旧安装图保留 SVG；新场景及架构插图
保留原始 PNG 与生成提示词，另附简洁 SVG 框图。`6.4.0` 在 §8.1 增加同一案例的软件架构图及
模块职责：无图标、无连接线，左侧标层次名称，重点表达组成与包含关系；调用和数据流另图
表达，并区分逻辑模块、进程/线程和部署边界。该图提供[可复用 SVG 及编辑说明](templates/diagrams/README.md)，
统一层背景、模块配色、字体和间距，不需要额外生成器。§7.1 增加自研板卡顶层布局，§9.1 增加
自研 FPGA 程序架构，两张图保留已确认的 SVG 与 PNG；图后逐组件说明职责与边界。
板卡布局不是实际 PCB 布线，FPGA 程序图不是芯片内部资源架构；三类图不能互相替代。
图件均为原创虚构教学素材，不宣称整套示例已经补齐。明确标记的教学段落在 `new-design`
生成项目空稿时移除，保留章节和填写指导；正式项目图文由作者按项目事实替换。
保留 18 个主章、必需系统概览与
信息安全架构，补充逐功能、逐模式、逐模块的原理写法和数据变换示意，以及完全虚构的贯穿示例。
可测试性覆盖方法/判定、受控故障、部署复位、并发隔离、自动化与验收；观测/自检归于可维护性，
替代依赖与环回归于调试接口，避免重复定义。
进一步展开性能预算、故障隔离/恢复、配置控制、启动/跨域/功热、升级回退和主要页面交互的
设计推导与代表流程；每节要求留下可复核的设计结果，不能只填术语或原则。
第 6 章扩充为“重要过程”，集中描述系统启动、配置加载与生效、数据平面处理、停止/重启、
异常恢复及模式切换；原正常数据流、异常恢复、模式切换分别移至 §6.4、§6.6、§6.7，后续主章
编号不变。相关机制留在专业章节，通过过程 ID 和引用衔接，不重复维护完整流程。
相对已发布的 `4.0.0`，第 6、11.4、12、14 节结构与信息归属有所调整，不是可直接替换的
兼容增补，因此已提升主版本。此前在 `5.0.0` 上补充客户业务场景、章节预设计、系统约束分配、
制造测试预留及统一收口检查，保留现有章节编号，按兼容补充提升至 `5.1.0`。
`5.1.1` 澄清实现计划的先后依赖：接口语义、错误行为和测试向量先评审，两端再并行实现，
分别通过契约测试后集成，端到端验证通过后才关闭相应系统目标。
`design.definition` 保持待发布 `1.1.0`；`design.hardware` 与 `design.fpga` 增加上级约束承接、
本地落实和系统组合验收，独立升为待发布 `1.1.0`，不要求另建通用单元文档。
`design.system-mechanism` 从 `1.1.0` 兼容增补安全恢复指导至待发布 `1.2.0`：失联先核对权威
结果，确认旧执行者停止或隔离并满足幂等/去重条件后才可重试，否则阻塞或转人工。
系统保留端到端原理与关键阶段，机制文档唯一维护详细状态转换及参与方协议。
其他模板版本不变，不新增模板种类或审批流程。
模板保留每节可折叠的段落式指导与完成条件；生成器默认将系统文档层级设为 `system`。
本次尚未发布新的 STD 版本或更新已发布来源/RAG 清单；现有 `draft.26` 的不可变来源保持原样。
已采用旧版的项目继续使用原版本，只有用户要求升级时才评估章节映射与内容差异。

## 上游参考

STD 的覆盖模型参考 ISO/IEC/IEEE 15288、15289 和 42010；系统设计主模板采用面向实现的
设备/软硬件一体设计结构。
项目/系统/软件工程内容参考 NASA Systems Engineering Handbook 与 NASA Software
Engineering Handbook；硬件、接口和验证文档目录参考 ECSS DRD。

STD 不复制受限标准正文。第三方来源和许可证边界见
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。
