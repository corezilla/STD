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

<span style="color:#1f6feb"><em>**编写建议**：本模板是子系统测试方案，与 design.subsystem（子系统设计阶段）一一对应。方案只登记测试分类与 Case 清单（每 Case 一行责任摘要），不写 Case 细节；逐 Case 展开一 Case 一文档（tests.subsystem-test-design）。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本方案绑定单一子系统：父设计 Document ID 经 `--parent-document-id` 写入 metadata；子系统设计 ID/版本在 §1 固定。

### 模板定位：方案、Case 设计与计划的边界

<span style="color:#1f6feb"><em>**编写建议**：本方案对应子系统设计阶段。分母来源是子系统设计的对外接口（§6）、跨模块流程、承接的系统约束与机制要求（执行位置在本子系统的部分）；模块层归 tests.module-test-scheme，系统层归 tests.system-test-scheme。</em></span>

- **权威分工**：子系统层测试的 Case 清单（ID、分类、优先级、责任摘要、设计状态）以本方案为唯一登记处；单 Case 展开归 `tests.subsystem-test-design`（一 Case 一文档）；活动组织归 `tests.subsystem-test-plan`。
- **只有摘要**：本方案每条 Case 只写责任摘要（要测什么），不写输入构造、Oracle 或步骤。
- **下层 PASS 不关闭本层**；本层 PASS 不关闭上层组合目标。

### 状态语义：Case 设计状态

<span style="color:#1f6feb"><em>**编写建议**：本方案只持有 Case 设计状态（Designed / Gap / Tailored-N/A）；实现状态（Planned/Implemented）在对应 case-design 文档，执行状态与 Verdict 只在 Run 报告。混层即违例。</em></span>

| 状态 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| Case 设计状态 | `Designed` / `Gap`（具名缺口）/ `Tailored-N/A` | 本方案 §3 清单 | 未设计写成已设计；N/A 无设计事实依据 |

<span style="color:#1f6feb"><em>**完成条件**：任一 Case 在本方案中只报设计状态；实现与执行状态可沿 Case ID 追到 case-design 文档与 Run 报告。</em></span>

## 1. 目标、范围与被测对象

<span style="color:#1f6feb"><em>**本节目的**：固定整子系统组装层的对象与边界。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：被测子系统与设计基线；真实内部模块；对其他子系统/外部服务的边界替身；不证明的系统组合保证。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 S01 方案覆盖并发准入与跨模块流程。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者能说清子系统层测什么。</em></span>

- 被测对象、设计基线与父对象：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-S01/v1 目录应用子系统（含 M101），父对象 EX-APP</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 本阶段测试边界（真实组成 / 边界替身）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">准入/M101/聚合全部真实；对 EX-APP 注册接口用 fake</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 不证明的组合保证及承接入口：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">跨子系统业务流与系统预算；承接＝系统方案</span><!-- STD_TEMPLATE_EXAMPLE_END -->

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
<span style="color:#6e7681">| normal / boundary / negative / concurrency / recovery | 适用 | — |
| performance | 裁剪 | 排队上限断言归本层，端到端预算归系统层 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 覆盖分母与 Case 清单

<span style="color:#1f6feb"><em>**本节目的**：把 design.subsystem 的适用来源 ID 转成 Case 清单——测试分母的唯一登记。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：一个来源 ID 至少一条记录（可多 Case 分担，分别写责任摘要）；Case ID 稳定且唯一（ST-<对象>-<NNN>）；责任摘要只写“要测什么、边界在哪”，不写输入与 Oracle；设计状态按状态语义；未实现与 NOT_RUN 不删；不适用转 §4。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下表灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个适用来源 ID 有 Case 或缺口；每个 Case ID 可追到（或计划有）case-design 文档。</em></span>

| 来源 ID / 固定版本 | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | | | <!-- TODO --> | <!-- TODO --> | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；一来源至少一条）**：</span>
<span style="color:#6e7681">| 来源 ID / 固定版本 | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |</span>
<span style="color:#6e7681">|---|---|---|---|---|---|---|</span>
<span style="color:#6e7681">| EX-CON-1 / EX-S01 v1 | ST-S01-001 | concurrency | P0 | 并发准入下输入不可变、整批返回 | Designed | 系统并发预算（系统层，NOT_RUN） |</span>
<span style="color:#6e7681">| 跨模块流程：准入→M101→聚合 | ST-S01-002 | normal | P1 | 排队请求不丢、结果不串 | Designed | — |</span>
<span style="color:#6e7681">| 机制承接：EX-OBS 快照采样 | ST-S01-003 | recovery | P2 | 采样不阻塞业务请求 | Designed | 机制端到端归系统层 |</span>
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
<span style="color:#6e7681">| 系统并发预算 / 预算口径在系统设计 | Gap（G-EX-2） | 系统架构组 / 系统方案定义 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 文档联动与清单变更规则

<span style="color:#1f6feb"><em>**本节目的**：固定方案—Case 设计—计划的联动规则，防三处漂移。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：新 Case 先入本清单再建 case-design 文档（文档 ID＝Case ID）；清单变更须同步计划构成表；写明方案冻结/版本规则。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：清单与 case-design 文档一一对应；计划只引用不复制。</em></span>

- 方案冻结与变更规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">清单随子系统设计基线冻结；变更同步子系统计划</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 与 case-design / 计划的同步规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">Case 文档 ID＝Case ID；tests.subsystem-test-plan 引用本方案版本</span><!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">新增 ST-S01-005 先入清单再建 Case 文档；子系统计划引用本方案 v1.0。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：每个适用来源 ID 是否都有 Case 或具名缺口；清单里的每个 Case ID 是否都有（或计划有）对应 case-design 文档；方案里是否混入了输入构造或 Oracle 细节？ -->
