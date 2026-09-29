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

<span style="color:#1f6feb"><em>**编写建议**：本模板是系统层测试报告，由测试计划（tests.system-test-plan）的执行流程（§4/§7）产出：汇总一次计划执行的逐 Case 结果、覆盖复算与 Gate 建议。报告是 Verdict 的唯一权威；没有有效 Run 不得写 PASS。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本报告绑定软件系统：父设计经 `--parent-document-id` 写入 metadata。

### 模板定位：报告、方案、Case 设计、计划与 Run 证据的边界

<span style="color:#1f6feb"><em>**编写建议**：系统层报告：汇总一次系统计划执行；分母对照系统方案（tests.system-test-scheme）；验收结论另循验收活动，本报告不代替。</em></span>

- **Verdict 唯一持有**：执行状态（NOT_RUN/BLOCKED/INVALID）与实际判定（PASS/FAIL）只在测试报告与 Run 证据中产生；方案与 Case 文档不预填任何结果。
- **引用不复制**：逐 Case 结果引用 Run ID 与证据路径，不把 stdout 全文搬进报告。
- **保留失败**：失败、阻塞、无效与未运行如实保留；重跑生成新报告不覆盖旧失败。
- **不越权**：Gate 建议不是批准；验收与发布授权另循其轨。

### 状态语义：执行状态与 Verdict

<span style="color:#1f6feb"><em>**编写建议**：Verdict 只能来自有效 Run 的断言结果；环境缺失记 BLOCKED、执行未命中设计记 INVALID、未运行记 NOT_RUN——三者都不是 FAIL 也不是 PASS。判定不改预期迁就实现。</em></span>

| 状态 | 取值 | 含义 | 判定事实 |
|---|---|---|---|
| 执行状态 | `NOT_RUN` / `BLOCKED` / `INVALID` | 未运行 / 环境阻断 / 执行未命中设计 | 运行记录与环境事实 |
| 实际判定 Verdict | `PASS` / `FAIL` | 断言与独立 Oracle 一致 / 不一致 | 有效 Run 的断言结果 |

<span style="color:#1f6feb"><em>**完成条件**：同一事实只能得到可解释的判定；从任一 Verdict 能追到唯一 Run 与原始证据。</em></span>

## 1. 执行摘要与结论

<span style="color:#1f6feb"><em>**本节目的**：给出一眼可判的总结论。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：本报告覆盖的计划与方案版本、执行范围、结果分布（PASS/FAIL/BLOCKED/INVALID/NOT_RUN 计数）、Gate 达成情况；结论与 §3–§5 明细一致。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 SYS-APP：4 PASS、1 BLOCKED（环境）。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者不读明细也知道本轮结论与边界。</em></span>

- 报告范围（计划/方案版本）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">系统计划 TSP-APP v1.0 / 方案 TSS-APP v1.0</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 结果分布与总结论：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">4 PASS、0 FAIL、1 BLOCKED、0 INVALID、0 NOT_RUN</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- Gate 达成情况：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">条件接受：G-EX-3 环境排期后补真实环境 Case</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 2. 被测基线与实际环境

<span style="color:#1f6feb"><em>**本节目的**：固定实际被测基线与环境，单列偏差。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：实际代码/构建/环境版本与计划基线对照；差异逐条列出；不同基线的结果不合并统计。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 SYS-APP：预生产环境版本差异。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：基线可核验；偏差不隐藏。</em></span>

- 实际基线（与计划对照）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-APP/v1；预生产镜像 2026.09（计划为 2026.08）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 环境偏差及影响：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">镜像差异已记录；存储测试实例版本一致</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 逐 Case 执行记录

<span style="color:#1f6feb"><em>**本节目的**：逐 Case 汇总执行结果。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：引用方案清单的每个 Case：执行状态、Verdict、Run ID 与证据路径、关联缺陷；NOT_RUN/BLOCKED/INVALID 如实保留；不复制原始输出。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下表灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：方案清单每个 Case 有一行；任一行可定位 Run。</em></span>

| Case ID | 执行状态 | Verdict | Run ID / 证据 | 缺陷 / 备注 |
|---|---|---|---|---|
| <!-- 引用方案清单 --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| Case ID | 执行状态 | Verdict | Run ID / 证据 | 缺陷 / 备注 |</span>
<span style="color:#6e7681">|---|---|---|---|---|</span>
<span style="color:#6e7681">| SYS-APP-002 | 有效 Run | PASS | run-20260929-02 | 停止清空无残留 |</span>
<span style="color:#6e7681">| SYS-APP-005 | BLOCKED | — | — | 需真实生产环境（G-EX-3） |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 偏差、无效执行与重跑

<span style="color:#1f6feb"><em>**本节目的**：如实记录偏差与无效执行。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：偏离 Case 文档的原因与批准；无效执行（未命中、环境错配）与重跑的新 Run；旧失败保留。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 SYS-APP：无无效执行。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：偏差可追溯；重跑不覆盖历史。</em></span>

| 偏差 / 无效项 | 原因 | 影响 Case | 处置与重跑 Run |
|---|---|---|---|
| <!-- TODO --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 偏差 / 无效项 | 原因 | 影响 Case | 处置与重跑 Run |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| （无） | — | — | — |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 覆盖复算（对照方案分母）

<span style="color:#1f6feb"><em>**本节目的**：对照方案分母复算覆盖。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：方案 §3 每个来源 ID 逐条对照：Case 状态如何变化、Gap 是否关闭、NOT_RUN 保留在哪；覆盖复算以本报告事实为准，不以计划口径代替。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 SYS-APP：流程与机制关闭、真实环境保留。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：分母每条有着落；未关闭项显式保留。</em></span>

| 方案来源 ID | Case ID | 报告状态 | 剩余缺口 |
|---|---|---|---|
| <!-- 对照方案 §3 清单逐条复算 --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 方案来源 ID | Case ID | 报告状态 | 剩余缺口 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 启动/停止流程 | SYS-APP-001/002 | PASS | — |</span>
<span style="color:#6e7681">| 机制端到端 EX-OBS | SYS-APP-003 | PASS | — |</span>
<span style="color:#6e7681">| 真实生产环境 | SYS-APP-005 | BLOCKED | G-EX-3 保留 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 6. 缺陷与残余风险

<span style="color:#1f6feb"><em>**本节目的**：失败追到缺陷，残余风险显式。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：每个 FAIL 关联缺陷 ID、严重度、状态与回归 Case；残余风险写触发条件与影响，不写“重试即可”。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 SYS-APP：无产品缺陷。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：失败有主；风险可判定。</em></span>

- 缺陷清单（关联 Case 与 Run）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">（无）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 残余风险：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">真实生产环境未验证前，上线决定不得引用 SYS-APP-005</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 7. Gate 结论与建议

<span style="color:#1f6feb"><em>**本节目的**：按计划的 Gate 规则给结论与建议。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：接受/条件接受/拒绝及依据；开放问题与责任方；报告不代替批准决定。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 SYS-APP：条件接受。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：建议可复算（能追到明细与缺口）；不越权。</em></span>

- Gate 结论（接受/条件接受/拒绝）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">条件接受：G-EX-3 排期后补环境验证</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 开放问题与责任方：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">G-EX-3 / 运维 / 预生产排期</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 8. 未决项

<span style="color:#1f6feb"><em>**本节目的**：未决项有主、有期限。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：逐条登记；无未决项时写经核对的“无”。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：G-EX-3 真实生产环境。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：未决项全部有主有期限。</em></span>

| 未决项 / 关联 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|
| <!-- TODO；无未决项时写经核对的“无” --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">G-EX-3 / 真实生产环境 | 运维 / 预生产环境排期 | 排期后补验证。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：任一 Verdict 能否定位唯一 Run 与原始证据；失败与 NOT_RUN 是否如实保留；报告是否越权写成批准。 -->
