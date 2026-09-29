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

<span style="color:#1f6feb"><em>**编写建议**：本模板是单元层测试的**可执行作业指令**，与 design.implementation（单元设计阶段）一一对应：执行者（含 Agent）按本计划从执行前检（§3）经逐 Case 作业（§4）到报告产出（§7）从头做到尾。计划只做索引与流程，不复制 Case、不预填执行结果。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本计划绑定单一软件模块：模块对象 ID 经 `--design-object-id` 写入 metadata；ISD 基线在 §2 固定。

### 模板定位：方案、用例、计划与报告的边界

<span style="color:#1f6feb"><em>**编写建议**：本计划对应实现阶段。构成＝单元方案×1（tests.unit-test-scheme）＋Case 文档×N（tests.unit-case，一 Case 一文档）＋模块层交接；执行产出为 tests.unit-test-report；模块组装层组织归 tests.module-test-plan。</em></span>

- **权威分工**：Case 清单归 `tests.unit-test-scheme`；单 Case 展开归 `tests.unit-case`（一 Case 一文档）；本计划是**可执行作业指令**——执行者（含 Agent）按它从执行前检做到报告产出；执行结果与 Verdict 权威在 `tests.unit-test-report` 与 Run 证据。
- **只索引**：构成表引用方案版本与 Case ID 范围，不复制清单或 Case 细节。
- **测试资产**：工具/夹具/替身/受控时钟的契约与自检在 `tests.asset-design`（一资产一文档，阶段共享）；本计划 §4 Step 0 使其就位。
- **不是授权书**：按用户当前授权交付；计划到期不改判任何事实状态。

### 计划条目状态语义

<span style="color:#1f6feb"><em>**编写建议**：计划条目只有下列三种状态；执行状态（NOT_RUN/BLOCKED/INVALID）与 Verdict（PASS/FAIL）只存在于测试报告与 Run 证据，混入计划即违例。</em></span>

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
<span style="color:#1f6feb"><em>**完成条件**：读者（含 Agent）能说清验证对象、构成清单和排除项；每个构成项指向方案、Case 文档或具名缺口。</em></span>

| 构成层 | 文档 / 入口（Document ID 或缺口） | 覆盖责任摘要 | 条目状态 |
|---|---|---|---|
| <!-- 单元方案 ×1 --> | | | |
| <!-- Case 文档 ×N（按方案清单） --> | | | |
| <!-- 测试资产 ×N（tests.asset-design，需开发时为工作项） --> | | | |
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
<span style="color:#1f6feb"><em>**必须写清楚**：设计文档与源码、依赖、构建环境版本；哪些变化触发哪些 Case 重跑；重跑生成新 Run 与新报告，不覆盖旧失败。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 FrameDecoder：基线 EX-ISD/v1 修订 2；decode_one 签名变化→方案重裁＋全部 Case 重跑。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：基线可核验；任一类变更能映射到明确重跑范围。</em></span>

- 设计 / 源码 / 依赖基线：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-ISD/v1 修订 2；教学 C++ 目标；无外部依赖</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 变更 → 重跑范围规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">decode_one 签名变化→方案重裁＋全部 Case 重跑；私有 helper 重构→受影响 Case 复跑</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 执行前检（Go / No-Go）

<span style="color:#1f6feb"><em>**本节目的**：开始执行前逐项 Go/No-Go，全部通过才进入 §4。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：方案就绪度（清单无未登记缺口且版本固定）；Case 实现状态盘点（未 Implemented 的 Case 明确处理）；环境与工具（构建可用、依赖齐、权限具备）；构建接线（干净全量交付构建通过、消费者链接实际交付库、导出/注册项同步）。任一不满足记 Blocked 并登记缺口，不静默降级执行。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD：编译器可用、5 个 Case 全 Implemented 才 Go。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每一前检项有可判定事实；No-Go 有出口（Blocked＋缺口）。</em></span>

| 前检项 | 判定事实 | 通过条件 | 不满足时 |
|---|---|---|---|
| <!-- 方案就绪度 --> | | | |
| <!-- Case 实现状态盘点 --> | | | |
| <!-- 环境与工具（引用 tests.asset-design 的 Verified 状态） --> | | | |
| <!-- 构建接线（全量交付构建 / 消费者链接实际库） --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| 前检项 | 判定事实 | 通过条件 | 不满足时 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 方案就绪度 | UTS-FD v1.2 清单无未登记缺口 | 分母闭合且版本固定 | Blocked＋缺口 |</span>
<span style="color:#6e7681">| Case 实现状态 | UT-FD-001…005 均 Implemented | 全部 Implemented 或明确跳过登记 | 未实现项标 NOT_RUN 并登记 |</span>
<span style="color:#6e7681">| 环境与工具 | c++ --version 正常、向量集在位 | 构建与运行可用 | 环境性 Blocked，不静默换工具链 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.5 环境实例分配（plan 编排）

<span style="color:#1f6feb"><em>**本节目相**：把方案 §1.6 的环境类型落实为具体的**实例编号**，并分配给具体 Case——同一类型可多套（如多 docker 用于并行），编号与分配是 plan 的责任，Case 只引用编号。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：列出本计划分配的全部 ENV 实例（编号 + 类型 + 具体配置/位置 + Owner + 分配给哪些 Case + 准备时限 + 状态）；ENV 实例类型与方案 §1.6 类型一致；准备失败标 Blocked 并登记缺口，不静默换其他实例。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——为同一 Case 分配多个 ENV 实例以并行/隔离，或多 Case 复用同一 ENV 实例。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3.1 的 Case 在本表有 ENV 实例；类型一致；准备未完成标 Blocked 并登记缺口，不静默换实例。</em></span>

| ENV 实例编号 | 环境类型 | 具体配置/位置 | Owner | 分配给哪些 Case | 准备时限 | 状态 |
|---|---|---|---|---|---|---|
| <!-- TODO：如 ENV-1、ENV-2 --> | <!-- 类型（引用方案 §1.6） --> | <!-- TODO --> | <!-- TODO --> | <!-- Case ID 范围 --> | <!-- TODO --> | <!-- Blocked/Ready --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；单元层 ENV 实例）**：</span>

<span style="color:#6e7681">| ENV 实例编号 | 环境类型 | 具体配置/位置 | Owner | 分配给哪些 Case | 准备时限 | 状态 |</span>
<span style="color:#6e7681">|---|---|---|---|---|---|---|</span>
<span style="color:#6e7681">| ENV-1 | 独立子程序编译产物 | clang17 编译产物 | 模块 Owner | UT-FD-001/003/005 | 每次发布前 | Ready |
| ENV-2 | 受控时钟 fake | HARNESS-FD-CLOCK v1 | 模块 Owner | UT-FD-005 | 每次发布前 | Ready |
| ENV-3 | 冻结向量集 | `docs/examples/isd-frame-decoder/` v1.2 | 模块 Owner | UT-FD-001/003/005 | 每次发布前 | Ready |
</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 执行流程（逐 Case 作业序列）

<span style="color:#1f6feb"><em>**本节目的**：给执行者（含 Agent）一条从头到尾的作业序列。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：按方案清单优先级逐 Case：定位 Case 文档→按其 §2–§7 前检与运行→判定分路（PASS/FAIL/BLOCKED/INVALID 各有明确出口与下一步）→记录 Run→继续；失败不阻断后续 Case，除非环境性阻塞；全部完成后按 §7 生成报告；阶段门——最小真实链→规模控制面→完整业务→恢复/全量回归，不等所有模块写完才集成；Step 0 资产就位——按消费索引构建全部依赖测试资产（tests.asset-design）并运行其自检，自检不过即环境性 Blocked，不进入 Case 执行。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD：按 P0→P1 逐个执行，UT-FD-003 失败不阻断 UT-FD-004/005。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：执行者不需要临场发明流程；每个分路有确定下一步。</em></span>

| Step | 动作 | 输入 / 依据 | 产出 |
|---|---|---|---|
| <!-- 0 --> | 资产就位：按消费索引构建全部依赖测试资产并跑自检 | tests.asset-design 文档 | 就绪清单（Verified） |
| <!-- 1 --> | 读取方案清单并按优先级排序 | 方案 v__ | 执行队列 |
| <!-- 2 --> | 逐 Case：定位 Case 文档 | Case ID | 实施依据 |
| <!-- 3 --> | 按 Case 文档执行前检与运行 | Case 文档 §2–§7 | Run 记录 |
| <!-- 4 --> | 判定并分路（PASS/FAIL/BLOCKED/INVALID） | 断言与环境事实 | Verdict 归报告 |
| <!-- 5 --> | 全部完成后生成测试报告 | 本计划 §7 | tests.unit-test-report |

| 阶段门 | 目的 | 进入条件 |
|---|---|---|
| <!-- 1 最小真实链 --> | | |
| <!-- 2 规模控制面 --> | | |
| <!-- 3 完整业务 --> | | |
| <!-- 4 恢复 / 全量回归 --> | | |


<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：</span>
<span style="color:#6e7681">| Step | 动作 | 依据 | 产出 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 0 | 构建教学宿主与冻结向量集并自检 | asset-design：HARNESS-FD/VEC-FD | 资产就绪（Verified） |</span>
<span style="color:#6e7681">| 1 | 读 UTS-FD v1.2 清单并按优先级排序 | 方案 §3 | 执行队列：003→001→004→005 |</span>
<span style="color:#6e7681">| 2 | 逐 Case 定位 Case 文档并前检 | Case 文档 §2–§3 | 各 Case 实施依据 |</span>
<span style="color:#6e7681">| 3 | 运行并记录 Run | Case 文档 §4–§6 | run-20260929-* 证据 |</span>
<span style="color:#6e7681">| 4 | 判定分路：UT-FD-003 FAIL→登记缺陷继续 | 断言与环境事实 | Verdict 汇入报告 |</span>
<span style="color:#6e7681">| 5 | 生成单元测试报告 | 本计划 §7 | tests.unit-test-report 实例 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

- 失败（FAIL）处理路径：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">保留现场与 Run 证据→登记缺陷并关联 Case ID→继续后续 Case；不重跑覆盖原失败</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 阻塞/无效（BLOCKED/INVALID）处理路径：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">BLOCKED（编译器缺失）→环境性阻塞整批停并登记；INVALID（注入未命中/并发未交错）→修 Case 或标无效，不记 PASS</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 环境操作（搭建 / 复位 / 隔离 / 清理）

<span style="color:#1f6feb"><em>**本节目的**：环境操作可复现。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：搭建、每 Case 复位、并行隔离键、清理的具体命令或入口；环境不可重建即 Blocked；单环境串行时写清 case 前检查、软复位/重启/驱动恢复阶梯与时限，失败后确认回到基线，不能只 kill 后继续。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD：教学宿主每 Case 天然复位。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：另一位执行者能独立搭建、复位与清理。</em></span>

- 环境搭建与复位操作：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">教学 C++ 目标构建一次，全量执行后清理临时目录</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 隔离键与清理：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">无共享资源；并发 Case join 后才销毁输入</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 复位阶梯与时限（软复位→重启→驱动恢复）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">无外部资源；每 Case 重建输入即复位（无阶梯，教学例）</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 6. 证据与 Run 记录规则

<span style="color:#1f6feb"><em>**本节目的**：Run 证据规则固定。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：Run ID 命名（对象-时间或序号）、每次 Run 保存的命令/版本/stdout/退出码/种子、保存位置与保留期、脱敏要求；重跑生成新 Run 不覆盖。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD：run-<日期>-<序号>。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：从报告任一 Verdict 能定位唯一 Run 与原始证据。</em></span>

- Run ID 规则与证据位置：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">run-YYYYMMDD-NN；tests/unit/frame_decoder/reports/<run-id>/</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 保存内容与脱敏要求：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">命令、编译器版本、源 hash、stdout、退出码；无敏感数据</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 7. 报告产出与 Gate 规则

<span style="color:#1f6feb"><em>**本节目的**：定义报告产出与 Gate 规则。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：全部 Case 走完后（或按出口准则提前结束）生成 `tests.unit-test-report` 实例；Gate 建议规则（覆盖闭合或缺口有主、失败分级）在此固定，报告只按规则给建议不越权批准。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD：全部 Case 走完后生成报告；Gate＝分母闭合且 G-EX-1 有主。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：报告的生成时机、模板与 Gate 规则确定。</em></span>

- 报告生成时机与模板：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">全部 Case 走完或出口准则触发时生成 tests.unit-test-report</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- Gate 建议规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">覆盖闭合或缺口有 Owner/Gate；G-EX-1 关闭前契约场景保留 NOT_RUN</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 8. 责任、排期与风险

<span style="color:#1f6feb"><em>**本节目的**：责任到人、风险有触发与缓解出口。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：方案维护、Case 编写、执行、评审的责任人与时间窗；风险写触发条件、影响与缓解，不写“重试即可”。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：设计＝模块 Owner、执行＝QA 或 Agent、评审＝模块设计评审。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个构成项有责任人与时间窗；关键风险有可判定触发。</em></span>

| 构成项 / 风险 | Owner | 时间窗 / 最晚 Gate | 冲突或缓解出口 |
|---|---|---|---|
| <!-- TODO --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">方案维护＝模块 Owner / 本迭代；执行＝Agent 按 §4 序列；风险“契约入口未定”缓解＝单元结论先行。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 9. 未决项

<span style="color:#1f6feb"><em>**本节目的**：未决项有主、有期限、有关闭条件。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：逐条登记；无未决项时写经核对的“无”。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：G-EX-1 契约入口未定义。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：未决项全部有主有期限。</em></span>

| 未决项 / 关联 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|
| <!-- TODO；无未决项时写经核对的“无” --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">G-EX-1 / 契约组合入口 | 系统架构组 / 下次契约评审 | 指定契约测试文档；关闭前保留 NOT_RUN。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：执行者能否只凭本计划从 Go/No-Go 走到报告产出；计划里是否出现任何执行结论或 Verdict；到期条目是否被偷偷改判？ -->
