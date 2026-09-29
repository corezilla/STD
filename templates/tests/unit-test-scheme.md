<!-- STD_DOCUMENT_COVER_BEGIN -->
# {{document_title}}

> STD 使用入口：[STD 主说明与执行流程](../../README.md)。这是工程文档标准模板；作者先读入口，再按项目已采用版本读取适用规范和专项指南。

| 文档字段 | 值 |
|---|---|
| Document ID | `{{document_id}}` |
| Document Version | `{{document_version}}` |
| Status | `{{document_status}}` |
| Project | `{{project}}` |
| Authority | `{{authority}}` |
| Document Owner | {{document_owner}} |
| Authors | {{authors}} |
| Created Date | `{{created_at}}` |
| Last Modified Date | `{{last_modified_at}}` |
| Template ID | `{{template_id}}` |
| Template Version | `{{template_version}}` |
| Template Conformance | `{{template_conformance}}` |
| Tailoring Reference | {{tailoring_ref}} |
| Migration Map Reference | {{migration_map_ref}} |
| Repository | `{{source_repository}}` |
| Canonical Path | `{{source_path}}` |
| Supersedes | {{supersedes}} |

> Reviewer、Approver、Approval Date 和 Release Tag 在进入相应状态时填写。Git commit/tag 是
> 外部不可变证据；不要在文档内容中伪造包含自身的 commit hash。
<!-- STD_DOCUMENT_COVER_END -->

<span style="color:#1f6feb"><em>**编写建议**：本模板是单元测试方案，与 design.implementation（单元设计阶段）一一对应。方案只登记测试分类与 Case 清单（每 Case 一行责任摘要），不写 Case 细节；逐 Case 展开一 Case 一文档（tests.unit-case）。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本方案绑定单一软件模块：模块对象 ID 经 `--design-object-id` 写入 metadata；ISD 设计 ID/版本在 §1 固定；实现状态与执行结果不进本方案。

### 模板定位：方案、用例与计划的边界

<span style="color:#1f6feb"><em>**编写建议**：本方案对应实现阶段。分母来源是 ISD 的函数行为、错误分支、并发/借用与数据规则；模块组装层归 tests.module-test-scheme；已用通用规格承载单元 Case 的项目由本方案取代该职能，不得双写。</em></span>

- **权威分工**：单元层测试的 Case 清单（ID、分类、优先级、责任摘要、设计状态）以本方案为唯一登记处；单 Case 展开归 `tests.unit-case`（一 Case 一文档）；活动组织归 `tests.unit-test-plan`。
- **只有摘要**：本方案每条 Case 只写责任摘要（要测什么），不写输入构造、Oracle 或步骤。
- **下层 PASS 不关闭本层**；本层 PASS 不关闭上层组合目标。

### 状态语义：用例状态

<span style="color:#1f6feb"><em>**编写建议**：本方案只持有 用例状态（Designed / Gap / Tailored-N/A）；实现状态（Planned/Implemented）在对应 case-design 文档，执行状态与 Verdict 只在 Run 报告。混层即违例。</em></span>

| 状态 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| 用例状态 | `Designed` / `Gap`（具名缺口）/ `Tailored-N/A` | 本方案 §3 清单 | 未设计写成已设计；N/A 无设计事实依据 |

<span style="color:#1f6feb"><em>**完成条件**：任一 Case 在本方案中只报设计状态；实现与执行状态可沿 Case ID 追到 case-design 文档与 Run 报告。</em></span>

## 1. 目标、范围与被测对象

<span style="color:#1f6feb"><em>**本节目的**：固定单元层测试的对象与边界。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：被测模块、ISD 基线、被测函数集合；真实代码与替身边界；不证明的组装保证及承接入口。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 FrameDecoder 单元方案覆盖 decode_one 的互斥分支、借用寿命与并发只读。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者能说清单元层测什么、不测什么。</em></span>

- 被测对象、设计基线与父对象：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-FRAME-MODULE 的 M201 FrameDecoder，基线 EX-ISD/v1 修订 2</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 本阶段测试边界（真实组成 / 边界替身）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">全部真实代码；无替身（无外部依赖）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 不证明的组合保证及承接入口：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">组装后流程、wire 互操作、宿主权限；承接＝模块方案与契约层</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 2. 测试分类体系

<span style="color:#1f6feb"><em>**本节目的**：固定本阶段的测试分类体系与适用裁剪。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：采用 STD 统一家族词表（normal/boundary/negative/concurrency/recovery/security/performance/endurance），逐类声明本阶段适用性与裁剪依据；不适用不等于没写 Case，须在 §4 给事实。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字分类示例。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：分类体系可裁剪可追溯，每个适用分类在 §3 清单中至少有 Case 或缺口。</em></span>

| 分类（STD 家族词表） | 本阶段适用性 | 裁剪依据 |
|---|---|---|
| <!-- normal / boundary / negative / concurrency / recovery / security / performance / endurance --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；分类适用性）**：</span>
<span style="color:#6e7681">| normal / boundary / negative / concurrency | 适用 | — |
| recovery | Tailored-N/A | 模块无跨调用状态（ISD §7 事实） |
| security / performance / endurance | 不在本层 | 归模块/系统层与通用规格 §6 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 覆盖分母与 Case 清单

<span style="color:#1f6feb"><em>**本节目的**：把 design.implementation 的适用来源 ID 转成 Case 清单——测试分母的唯一登记。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：一个来源 ID 至少一条记录（可多 Case 分担，分别写责任摘要）；以设计文档（design §12/§14）的验证项 VRC 清单为分母逐项对账：每个 VRC 至少一个 Case——验证项是设计声明的必测点，本清单只引用其 ID 不复制定义、不做附录；Case ID 稳定且唯一（UT-<对象>-<NNN>）；责任摘要只写“要测什么、边界在哪”，不写输入与 Oracle；设计状态按状态语义；未实现与 NOT_RUN 不删；不适用转 §4。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下表灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个适用来源 ID 有 Case 或缺口；每个 Case ID 可追到（或计划有）case-design 文档。</em></span>

| 来源 ID / 固定版本 | 设计验证项 ID | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | | | <!-- TODO --> | <!-- TODO --> | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；一来源至少一条）**：</span>
<span style="color:#6e7681">| 来源 ID / 固定版本 | 设计验证项 ID | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |</span>
<span style="color:#6e7681">|---|---|---|---|---|---|---|</span>
<span style="color:#6e7681">| FD-R1 / EX-FRAME-MODULE 1.0.0 | VRC-EX-ISD-DECODE-01 | UT-FD-001 | normal | P1 | 合法帧解析出借用视图与 consumed，只消费首帧 | Designed | — |</span>
<span style="color:#6e7681">| FD-R1 | VRC-EX-ISD-DECODE-01 | UT-FD-003 | negative | P0 | 头非法时按 version→kind→length 优先级拒绝，不等待载荷 | Designed | — |</span>
<span style="color:#6e7681">| FD-R2 / 同基线 | VRC-EX-ISD-LIFE-01 | UT-FD-005 | concurrency | P1 | 并发只读结果一致且输入不变 | Designed | 宿主长寿命组合（NOT_RUN） |</span>
<span style="color:#6e7681">| 上级 wire 契约 | — | （Gap） | contract | — | wire 互操作非本层责任 | Gap（G-EX-1） | 契约层入口未定义 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 不适用与缺口裁决

<span style="color:#1f6feb"><em>**本节目的**：区分“不适用”与“尚未设计”。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：Tailored-N/A 必须引用设计章节事实；Gap 须有 Owner 与恢复条件；两者都不从分母静默消失。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每条裁决有事实或 Owner；无“顺手 N/A”。</em></span>

| 来源 ID / 事实依据 | 裁决（Tailored-N/A 或 Gap） | Owner / 恢复条件 |
|---|---|---|
| <!-- TODO --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">| 上级 wire 契约 / 契约层入口未定义 | Gap（G-EX-1） | 系统架构组 / 指定契约测试文档 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 文档联动与清单变更规则

<span style="color:#1f6feb"><em>**本节目的**：固定方案—用例—计划的联动规则，防三处漂移。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：新 Case 先入本清单再建 case-design 文档（文档 ID＝Case ID）；清单变更须同步计划构成表；写明方案冻结/版本规则。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：清单与 case-design 文档一一对应；计划只引用不复制。</em></span>

- 方案冻结与变更规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">清单随 ISD 基线冻结；新增 Case 先登记再建文档</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 与 case-design / 计划的同步规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">Case 文档 ID＝Case ID；计划构成表引用本方案版本</span><!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">新增 UT-FD-006（尾随字节）先入清单再建 tests.unit-case 文档；单元计划引用本方案 v1.2。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：每个适用来源 ID 是否都有 Case 或具名缺口；清单里的每个 Case ID 是否都有（或计划有）对应 case-design 文档；方案里是否混入了输入构造或 Oracle 细节？ -->

## 附录 A. 本层设计验证项 VRC 汇集（对照用）

<span style="color:#1f6feb"><em>**本节目的**：把设计文档声明的本层验证项 VRC 汇集于此，供逐项对照 §3 清单的覆盖。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：VRC 清单以设计文档（design §12/§14）为唯一权威，本附录只登记 ID 与要验证什么，不复制判据/Oracle 定义；设计变更时本附录同步；每个 VRC 必须在 §3 清单有至少一个 Case，否则登记缺口。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：本附录 VRC 集合与设计文档一致；每个 VRC 在 §3 清单有 Case 或缺口。</em></span>

| 设计验证项 ID | 要验证什么（名称/责任） | 设计来源 | §3 Case 覆盖 |
|---|---|---|---|
| <!-- TODO --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>

<span style="color:#6e7681">| 设计验证项 ID | 要验证什么 | 设计来源 | §3 Case 覆盖 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| VRC-EX-ISD-DECODE-01 | 头校验顺序与错误优先级 | ISD §验证 | UT-FD-001/003 |</span>
<span style="color:#6e7681">| VRC-EX-ISD-LIFE-01 | 借用寿命与并发只读 | ISD §验证 | UT-FD-005 |</span>
<span style="color:#6e7681">| （Gap）上级 wire 契约 | wire 互操作 | 契约层入口未定义 | 缺口 G-EX-1 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->
