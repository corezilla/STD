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

<span style="color:#1f6feb"><em>**编写建议**：本模板组织单元层的测试活动，与 design.implementation（单元设计阶段）一一对应。计划只做索引与状态：引用方案（tests.unit-test-scheme）与 Case 文档（tests.unit-test-design，一 Case 一文档），不复制 Case、不预填执行结果。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本计划绑定单一软件模块：模块对象 ID 经 `--design-object-id` 写入 metadata；ISD 基线在 §2 固定。

### 模板定位：方案、Case 设计与计划的边界

<span style="color:#1f6feb"><em>**编写建议**：本计划对应实现阶段。构成＝单元方案×1（tests.unit-test-scheme）＋Case 文档×N（tests.unit-test-design，一 Case 一文档）＋模块层交接；模块组装层组织归 tests.module-test-plan。</em></span>

- **权威分工**：单元层测试活动组织以本计划为唯一权威；Case 清单归 `tests.unit-test-scheme`；单 Case 展开归 `tests.unit-test-design`（一 Case 一文档）；实际结果权威在 Run 报告。
- **只索引**：构成表引用方案版本与 Case ID 范围，不复制清单或 Case 细节。
- **不预填结果**：任何条目不得出现 PASS 或执行结论；计划不是授权书。

### 计划条目状态语义

<span style="color:#1f6feb"><em>**编写建议**：计划条目只有下列三种状态；执行状态与 Verdict 只存在于 Run 报告，混入计划即违例。</em></span>

| 条目状态 | 含义 | 禁止 |
|---|---|---|
| `Planned` | 已排入计划，方案与责任已定位 | 用 Planned 冒充已执行或已通过 |
| `Deferred` | 经批准裁剪或延后，有 tailoring 依据与恢复条件 | 无依据的“暂不做” |
| `Blocked` | 依赖缺失（设计缺口、环境、上游合同） | 不登记缺口就长期挂起 |

<span style="color:#1f6feb"><em>**完成条件**：任一条目能报出状态、依据与下一步；计划里没有任何执行结论。</em></span>

## 1. 目标、范围与测试构成

<span style="color:#1f6feb"><em>**本节目的**：固定单元层测试活动的范围与构成清单。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：验证对象与不证明什么；构成＝方案×1＋Case 文档×N＋模块/契约交接出口；排除项及 tailoring 依据。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 FrameDecoder：方案 UTS-FD v1.2 ＋ Case 文档 UT-FD-001…005。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者能说清验证对象、构成清单和排除项；每个构成项指向方案、Case 文档或具名缺口。</em></span>

| 构成层 | 文档 / 入口（Document ID 或缺口） | 覆盖责任摘要 | 条目状态 |
|---|---|---|---|
| <!-- 单元方案 ×1 --> | | | |
| <!-- Case 文档 ×N（按方案清单） --> | | | |
| <!-- 相邻层交接出口 --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 构成层 | 文档 / 入口 | 覆盖责任摘要 | 条目状态 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 单元方案 ×1 | UTS-FD v1.2 | 清单与设计状态唯一登记 | Planned |</span>
<span style="color:#6e7681">| Case 文档 ×5 | UT-FD-001…005 | 互斥分支、借用寿命、并发只读 | Planned |</span>
<span style="color:#6e7681">| 模块层交接 | 模块测试计划 | 组装后流程保证 | Planned |</span>
<span style="color:#6e7681">| 契约层交接 | 入口未定义 | wire 互操作 | Blocked（G-EX-1） |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 2. 被测基线与变更重跑范围

<span style="color:#1f6feb"><em>**本节目的**：固定单元层基线与变更→重跑映射。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：设计文档与源码、依赖、构建环境版本；哪些变化触发哪些 Case 重跑；计划只固定基线与规则。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：EX-ISD/v1 修订 2；教学 C++ 目标；无外部依赖</em></span>
<span style="color:#1f6feb"><em>**完成条件**：基线可核验；任一类变更能映射到明确重跑范围。</em></span>

- 设计 / 源码 / 依赖基线：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-ISD/v1 修订 2；教学 C++ 目标；无外部依赖</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 变更 → 重跑范围规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">decode_one 签名变化→方案重裁＋全部 Case 重跑；私有 helper 重构→受影响 Case 复跑</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 策略与覆盖模型

<span style="color:#1f6feb"><em>**本节目的**：说明单元层覆盖如何从方案分母论证，并与相邻层分工。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：按方案 §3 分母归类：函数行为、错误分支、并发/借用、数据规则各自在哪组 Case 关闭；保留 NOT_RUN 分母。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：错误优先级在 UT-FD-003 关闭；wire 互操作留给契约层。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每类保证能定位关闭层与承接文档；不以覆盖率百分比代替论证。</em></span>

| 保证类别（来源 ID 族） | 关闭层 | 承接文档/入口 | 分母缺口 |
|---|---|---|---|
| <!-- 按方案 §3 分母归类 --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 保证类别 | 关闭层 | 承接文档/入口 | 分母缺口 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 头校验顺序与错误优先级（FD-R1） | 本层 | UT-FD-001/003 | — |</span>
<span style="color:#6e7681">| 借用寿命与并发只读（FD-R2/R3） | 本层 | UT-FD-004/005 | — |</span>
<span style="color:#6e7681">| wire 互操作 | 契约层 | 入口未定义 | G-EX-1，Blocked |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 环境、资源与隔离

<span style="color:#1f6feb"><em>**本节目的**：环境资源清单可核验、有 Owner。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：runner、构建目标、向量/夹具资产、所有权；并行隔离单位；缺失登记 Blocked。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：C++20 教学宿主＋冻结 hex 向量；缺编译器整体 Blocked。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：清单可核验；共享与隔离明确；缺失项 Blocked。</em></span>

- 环境与资产清单及 Owner：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">C++20 教学宿主＋冻结 hex 向量集，Owner＝模块 Owner</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 共享资源、隔离与调度：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">无共享设备；缺编译器时相关条目整体 Blocked</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 方案与 Case 家族映射

<span style="color:#1f6feb"><em>**本节目的**：Case 家族只映射到方案清单段落，不复制。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：家族→方案清单段落与 Case ID 范围；方案未覆盖家族以缺口登记。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：negative→UT-FD-003；recovery→方案 §4 N/A（无状态事实）。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个家族能追到方案清单段落或缺口；没有第二份 Case 清单。</em></span>

| Case 家族 | 方案清单段落 / Case ID 范围 | 条目状态 |
|---|---|---|
| <!-- normal / boundary / negative / concurrency / recovery / … --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">negative→方案清单 UT-FD-003；concurrency→UT-FD-005；recovery→方案 §4 裁决 N/A（无状态事实）。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 6. 入口、出口与判定准则

<span style="color:#1f6feb"><em>**本节目的**：开始/结束门槛可判定，判定语义与 Case 文档一致。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：入口（方案就绪、环境、基线）；出口（覆盖闭合或缺口有 Owner/Gate）；执行状态语义引用 Run 报告；到期不改判。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：入口＝方案清单无未登记缺口且构建可用。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：门槛可判定；到期不改变事实状态。</em></span>

- 入口准则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">方案清单无未登记缺口且构建可用</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 出口准则与 Gate 建议：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">覆盖闭合或缺口均有 Owner/Gate；契约场景到期仍 NOT_RUN</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 缺陷登记、偏差与重跑规则（重跑不覆盖失败证据）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">缺陷登记到缺陷库并关联 Case ID；重跑生成新 Run，不覆盖失败证据</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 7. 责任、排期与风险

<span style="color:#1f6feb"><em>**本节目的**：责任到人、风险有触发与缓解出口。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：方案维护、Case 编写、执行、评审的责任人与时间窗；风险写触发条件、影响与缓解，不写“重试即可”。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：设计＝模块 Owner、执行＝QA、评审＝模块设计评审。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个构成项有责任人与时间窗；关键风险有可判定触发。</em></span>

| 构成项 / 风险 | Owner | 时间窗 / 最晚 Gate | 冲突或缓解出口 |
|---|---|---|---|
| <!-- TODO --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">方案维护＝模块 Owner / 本迭代；风险“契约入口未定”触发＝G-EX-1 超 Gate，缓解＝单元结论先行。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 8. 证据汇总、Gate 建议与未决项

<span style="color:#1f6feb"><em>**本节目的**：证据可从各 Run 报告复算，Gate 建议不越权。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：证据从 Run 报告引用汇总；Gate 建议给接受/条件接受/拒绝及依据；未决项有 Owner/Gate/关闭条件；任何条目不写成 PASS。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：证据＝各 Case 文档 Run 引用。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：Gate 建议可复算；未决项有主有期限；无执行结论。</em></span>

- 证据汇总方式与位置：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">引用各 Case 的 reports/<run-id>/ Run 记录</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 单元层 Gate 建议（接受/条件接受/拒绝）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">条件接受（G-EX-1 关闭前契约场景保留 NOT_RUN）</span><!-- STD_TEMPLATE_EXAMPLE_END -->

| 未决项 / 关联 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|
| <!-- TODO；无未决项时写经核对的“无” --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">G-EX-1 / 契约组合入口 | 系统架构组 / 下次契约评审 | 指定契约测试文档；关闭前保留 NOT_RUN。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：能否从任一保证类别追到方案清单、Case 文档与 Run 路径；计划里是否出现任何执行结论；到期条目是否被偷偷改判？ -->
