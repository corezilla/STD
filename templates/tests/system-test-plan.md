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

<span style="color:#1f6feb"><em>**编写建议**：本模板组织系统层的测试活动，与 design.software-system（系统设计阶段）一一对应。计划只做索引与状态：引用方案（tests.system-test-scheme）与 Case 文档（tests.system-test-design，一 Case 一文档），不复制 Case、不预填执行结果。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本计划绑定软件系统：父设计 Document ID 经 `--parent-document-id` 写入 metadata；系统设计基线在 §2 固定。

### 模板定位：方案、Case 设计与计划的边界

<span style="color:#1f6feb"><em>**编写建议**：本计划对应系统设计阶段。构成＝系统方案×1（tests.system-test-scheme）＋Case 文档×N＋子系统计划×N 引用＋验收交接（tailoring 承接）；子系统层组织归 tests.subsystem-test-plan。</em></span>

- **权威分工**：系统层测试活动组织以本计划为唯一权威；Case 清单归 `tests.system-test-scheme`；单 Case 展开归 `tests.system-test-design`（一 Case 一文档）；实际结果权威在 Run 报告。
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

<span style="color:#1f6feb"><em>**本节目的**：固定系统层测试活动的范围与构成清单。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：验证对象与不证明什么；构成＝系统方案×1＋Case 文档×N＋子系统计划引用＋验收交接。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 EX-APP：方案 TSS-APP v1.0 ＋ Case 文档 SYS-APP-001…005 ＋ 子系统计划 STP-S01。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者能说清验证对象、构成清单和排除项；每个构成项指向方案、Case 文档或具名缺口。</em></span>

| 构成层 | 文档 / 入口（Document ID 或缺口） | 覆盖责任摘要 | 条目状态 |
|---|---|---|---|
| <!-- 系统方案 ×1 --> | | | |
| <!-- Case 文档 ×N（按方案清单） --> | | | |
| <!-- 相邻层交接出口 --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 构成层 | 文档 / 入口 | 覆盖责任摘要 | 条目状态 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 系统方案 ×1 | TSS-APP v1.0 | 清单与设计状态唯一登记 | Planned |</span>
<span style="color:#6e7681">| Case 文档 ×5 | SYS-APP-001…005 | 启动/停止/配置流程、机制端到端 | Planned |</span>
<span style="color:#6e7681">| 子系统计划引用 | STP-S01 | 子系统层组织 | Planned |</span>
<span style="color:#6e7681">| 验收交接 | 验收活动（tailoring） | 客户验收场景 | Deferred（有依据） |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 2. 被测基线与变更重跑范围

<span style="color:#1f6feb"><em>**本节目的**：固定系统层基线与变更→重跑映射。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：设计文档与源码、依赖、构建环境版本；哪些变化触发哪些 Case 重跑；计划只固定基线与规则。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：EX-APP/v1；系统 harness 与外部存储测试实例</em></span>
<span style="color:#1f6feb"><em>**完成条件**：基线可核验；任一类变更能映射到明确重跑范围。</em></span>

- 设计 / 源码 / 依赖基线：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-APP/v1；系统 harness 与外部存储测试实例</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 变更 → 重跑范围规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">流程语义变化→方案重裁＋全部 Case 重跑；子系统内部变化→子系统层重跑后本层回归</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 策略与覆盖模型

<span style="color:#1f6feb"><em>**本节目的**：说明系统层覆盖如何从方案分母论证，并与相邻层分工。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：按方案 §3 分母归类：端到端流程、系统约束与预算、机制端到端保证各在哪组 Case 关闭；验收不替代。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：停止清空在 SYS-APP-002 关闭；验收场景由验收活动承接。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每类保证能定位关闭层与承接文档；不以覆盖率百分比代替论证。</em></span>

| 保证类别（来源 ID 族） | 关闭层 | 承接文档/入口 | 分母缺口 |
|---|---|---|---|
| <!-- 按方案 §3 分母归类 --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 保证类别 | 关闭层 | 承接文档/入口 | 分母缺口 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 启动/停止流程（§7.3/§7.6） | 本层 | SYS-APP-001/002 | — |</span>
<span style="color:#6e7681">| 机制端到端：EX-OBS §15 | 本层 | SYS-APP-003 | — |</span>
<span style="color:#6e7681">| 真实生产环境 | 非本框架 | 验收/运维 | G-EX-3，Blocked |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 环境、资源与隔离

<span style="color:#1f6feb"><em>**本节目的**：环境资源清单可核验、有 Owner。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：runner、构建目标、向量/夹具资产、所有权；并行隔离单位；缺失登记 Blocked。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：系统 harness＋独立存储测试实例＋受控时钟。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：清单可核验；共享与隔离明确；缺失项 Blocked。</em></span>

- 环境与资产清单及 Owner：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">系统 harness＋独立存储测试实例，Owner＝系统 Owner</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 共享资源、隔离与调度：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">子系统实例/端口/数据命名空间按隔离键分开</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 方案与 Case 家族映射

<span style="color:#1f6feb"><em>**本节目的**：Case 家族只映射到方案清单段落，不复制。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：家族→方案清单段落与 Case ID 范围。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：recovery→SYS-APP-002；performance→SYS-APP-004。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个家族能追到方案清单段落或缺口；没有第二份 Case 清单。</em></span>

| Case 家族 | 方案清单段落 / Case ID 范围 | 条目状态 |
|---|---|---|
| <!-- normal / boundary / negative / concurrency / recovery / … --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">normal→SYS-APP-001；recovery→SYS-APP-002；performance→SYS-APP-004（启动时长断言）。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 6. 入口、出口与判定准则

<span style="color:#1f6feb"><em>**本节目的**：开始/结束门槛可判定，判定语义与 Case 文档一致。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：入口（方案就绪、环境、基线）；出口（覆盖闭合或缺口有 Owner/Gate）；执行状态语义引用 Run 报告；到期不改判。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：入口＝方案清单无未登记缺口且环境可用。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：门槛可判定；到期不改变事实状态。</em></span>

- 入口准则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">方案清单无未登记缺口且环境可用</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 出口准则与 Gate 建议：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">覆盖闭合或缺口均有 Owner/Gate；验收场景到期仍归验收活动</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 缺陷登记、偏差与重跑规则（重跑不覆盖失败证据）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">缺陷登记到缺陷库并关联 Case ID；重跑生成新 Run，不覆盖失败证据</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 7. 责任、排期与风险

<span style="color:#1f6feb"><em>**本节目的**：责任到人、风险有触发与缓解出口。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：方案维护、Case 编写、执行、评审的责任人与时间窗；风险写触发条件、影响与缓解，不写“重试即可”。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：设计＝系统 Owner、执行＝QA、评审＝系统设计评审。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个构成项有责任人与时间窗；关键风险有可判定触发。</em></span>

| 构成项 / 风险 | Owner | 时间窗 / 最晚 Gate | 冲突或缓解出口 |
|---|---|---|---|
| <!-- TODO --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">方案维护＝系统 Owner / 本迭代；风险“预生产环境排期”缓解＝机制端到端先行。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 8. 证据汇总、Gate 建议与未决项

<span style="color:#1f6feb"><em>**本节目的**：证据可从各 Run 报告复算，Gate 建议不越权。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：证据从 Run 报告引用汇总；Gate 建议给接受/条件接受/拒绝及依据；未决项有 Owner/Gate/关闭条件；任何条目不写成 PASS。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：证据＝各 Case Run 引用。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：Gate 建议可复算；未决项有主有期限；无执行结论。</em></span>

- 证据汇总方式与位置：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">引用各 Case 的 reports/<run-id>/ Run 记录</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 系统层 Gate 建议（接受/条件接受/拒绝）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">条件接受（G-EX-3 关闭前真实环境保留 NOT_RUN）</span><!-- STD_TEMPLATE_EXAMPLE_END -->

| 未决项 / 关联 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|
| <!-- TODO；无未决项时写经核对的“无” --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">G-EX-3 / 真实生产环境 | 运维 / 预生产环境排期 | 排期后补环境验证；关闭前保留 NOT_RUN。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：能否从任一保证类别追到方案清单、Case 文档与 Run 路径；计划里是否出现任何执行结论；到期条目是否被偷偷改判？ -->
