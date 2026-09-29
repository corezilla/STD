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


## 1.5 测试方法与测试设计技术

<span style="color:#1f6feb"><em>**本节目相**：固定单元层"怎么测"的方法论——单元层测试设计技术比较单一（mock 为主），上游测试常**多方法共存**，需逐一描述与边界。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：测试设计技术（按 Case 家族用哪些——等价类划分/边界值/状态转换/决策表/错误猜测/属性测试/变异测试等，写明对哪些 family 用哪种及不用哪种）；入场标准（设计文档到位、方案清单冻结、Case 实现就绪、替身 Verified、环境齐）；离场标准（分母每条来源有 Case 或缺口、Verdict 齐全、缺口有主、设计变更触发重跑）；自动化策略（哪些进 CI、单 Case 选择入口、断点/重跑规则、flaky 不掩盖根因）。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——单元层方法（含注入/边界/调用序等具体细节）。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3 Case 行能指出所用方法与环境类型；入场/离场可判定；环境类型与 asset-design 契约对应；无未声明的环境依赖。</em></span>

| Case 家族 | 测试设计技术 | 环境类型引用 | 自动化与判定规则 |
|---|---|---|---|
| <!-- TODO：如 normal/boundary/negative/concurrency/recovery --> | <!-- TODO --> | <!-- 类型名（详见 §1.7） --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；单元层测试方法——含注入/边界/调用序等具体细节）**：</span>

| Case 家族 | 测试设计技术 | 环境类型引用 | 自动化与判定 |
|---|---|---|---|
| normal | 等价类划分（合法帧/合法用例集） | 独立子程序编译产物 + 冻结向量集 | CI 跑全集；1 次执行即判 |
| | · 注入：完整头 + payload；空白、payload 仅单字节、UTF 边界 | | · 用固定 seed 避免伪随机；断言 exit-code 与 OK bytes 严格相等 |
| boundary | 边界值（长度上限、payload 大小） | 冻结向量集 + 受控时钟 fake | 单 Case --filter；超界→reject |
| | · 注入：合法头 + payload∈{4096 字节；4097 字节}；零字节 payload | | · 边界断言须在「接受」与「超限 reject」之间二选一，无第三态 |
| negative | 错误猜测（注入非法 header/字段组合） | 受控时钟 fake + 边界 fake | 一次性判 PASS/FAIL；不掩盖 FAIL |
| | · 注入：version=2、kind=2、length=0xffffffff、超大 length；多项非法同时出现验证优先级 | | · 优先级 version→kind→length 必须可独立复现 |
| concurrency | 线程对偶 + 受控时钟 fake | 受控时钟 fake | 多次采样统计；一次失败标 INVALID 复现 |
| | · 注入：两个并发线程各读一次冻结向量集；主线程 join 后再销毁输入 | | · 失败须记录样本与线程交错状态以复现；不允许靠「重跑通过」掩盖 |
| recovery | 资源归还（占槽后的释放） | 受控时钟 fake | 异常路径后必须有显式释放动作 |
| | · 注入：占槽后异常提前返回 | | · 验证槽位归还、可重入、并发安全 |
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 1.6 替身使用策略与边界

<span style="color:#1f6feb"><em>**本节目相**：固定单元层替身的使用，让 §3 清单的替身选择可解释可复核。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：替身决策准则（按所有权/可控性/真实性分类——内部真实/边界 fake/真协议测试实例/容器等）；替身形态（mock/fake/stub/spy 的取舍与代价）；替身保真度——契约与自检归 `tests.asset-design`（一资产一文档），方案与 Case 只引用其 ID 不复制行为；交互断言 vs 返回值断言（优先返回值，必要时断言关键调用序，但不耦合内部实现）；反模式（不 mock 你不拥有的接口、不 mock 值对象/纯数据、不为凑覆盖率而 mock、不过度断言内部细节）；与 §1 边界、§3 Case 清单、`tests.unit-case` §2 替身选择一致。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——单元层替身矩阵。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3 Case 行能指出替身类型与契约文档 ID；替身矩阵与 asset-design 一一对应；反模式逐项被排除并有理由。</em></span>

| 协作者类型 | 替身形态 | 替身契约文档（tests.asset-design） | 决策理由 |
|---|---|---|---|
| <!-- TODO --> | <!-- mock/fake/stub/spy --> | <!-- TODO：asset 文档 ID --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；单元层替身矩阵）**：</span>

| 协作者 | 形态 | 替身契约 | 理由 |
|---|---|---|---|
| 独立子程序编译产物（真实） | 受控时钟 fake | 边界 fake（注册/日志） |
| · 契约与自检归 tests.asset-design | | · 不 mock 你不拥有的对象 |
<!-- STD_TEMPLATE_EXAMPLE_END -->


## 1.7 测试环境类型（方案定义）

<span style="color:#1f6feb"><em>**本节目相**：固定本层"在哪类环境上跑"——列出环境**类型**（抽象类别）及其行为/真伪与契约文档（tests.asset-design 或产品规范）；同一类型可多套实例（多 docker 用于并行），具体**实例编号与分配**由 `tests.unit-test-plan` §4 编排，Case 在 §2 通过「环境类型 + ENV 实例编号」引用，不在本文档重复描述环境本身。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——单元层测试环境类型（含契约与用法具体细节）+ 环境拓扑（ENV 类型 → ENV 实例 → 被测对象）。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3 Case 行能指出所用环境类型；类型与 asset-design 契约对应；无未声明的环境依赖。</em></span>

| 环境类型 | 行为/真伪 | 契约文档 | 在本层用例中的角色 |
|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；单元层测试环境类型——含契约与用法具体细节）**：</span>


<span style="color:#6e7681">**拓扑**（ENV 类型 → ENV 实例 → 被测对象）：</span>
| 环境类型 | 行为/真伪 | 契约文档 | 在本层用例中的角色 |
|---|---|---|---|
| 独立子程序编译产物 | 真实 C++20 编译 | — | 单元验证对象自身 |
| · 契约：源码即真实编译产物，不替代、不 mock | | · 用法：每个 Case 直接调用入口函数，无中间件 || 冻结向量集与种子 | 真实但固定 | docs/examples/isd-frame-decoder/ | 正常/边界用例输入 |
| · 契约：固定种子→固定 hex bytes；版本随代码升级 | | · 用法：禁止随机生成，必须从固定集读取 || 受控时钟 fake | 单调推进、advance(ms) | HARNESS-FD-CLOCK | 时间/并发用例 |
| · 契约：advance(ms) 单调、不模拟硬件漂移 | | · 用法：测试前 set_time，测试后 reset || 边界 fake（注册/日志） | 只代返回值与调用参数 | FAKE-REG / HARNESS-FD-LOG | 边界交互用例 |
| · 契约：FAKE-REG 返回配置值/超时；HARNESS-FD-LOG 记录不修改 | | · 用法：测试前重置计数，测试后验证断言调用 |

<span style="color:#6e7681">**总体说明**：C++20 编译器（clang 17），构建目标为教学单二进制；fixture 来源为 docs/examples/isd-frame-decoder/ 冻结 hex 向量集与固定种子；替身资产归 tests.asset-design（HARNESS-FD-CLOCK / -REG / -LOG）；CI 入口为 runner --filter 选单 Case 或全集；并行隔离按模块实例+端口+临时目录；缺编译器记 Blocked/skip，不静默换工具链。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->
![unit层测试环境拓扑](../diagrams/tests/unit-env-topology.svg)

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
| normal / boundary / negative / concurrency | 适用 | — |
| recovery | Tailored-N/A | 模块无跨调用状态（ISD §7 事实） |
| security / performance / endurance | 不在本层 | 归模块/系统层与通用规格 §6 |
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
| 来源 ID / 固定版本 | 设计验证项 ID | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|---|---|
| FD-R1 / EX-FRAME-MODULE 1.0.0 | VRC-EX-ISD-DECODE-01 | UT-FD-001 | normal | P1 | 合法帧解析出借用视图与 consumed，只消费首帧 | Designed | — |
| FD-R1 | VRC-EX-ISD-DECODE-01 | UT-FD-003 | negative | P0 | 头非法时按 version→kind→length 优先级拒绝，不等待载荷 | Designed | — |
| FD-R2 / 同基线 | VRC-EX-ISD-LIFE-01 | UT-FD-005 | concurrency | P1 | 并发只读结果一致且输入不变 | Designed | 宿主长寿命组合（NOT_RUN） |
| 上级 wire 契约 | — | （Gap） | contract | — | wire 互操作非本层责任 | Gap（G-EX-1） | 契约层入口未定义 |
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
<span style="color:#6e7681">**示例（虚构；不适用与缺口裁决）**：</span>

| 上级 wire 契约 / 契约层入口未定义 | Gap（G-EX-1） | 系统架构组 / 指定契约测试文档 |
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

| 设计验证项 ID | 要验证什么 | 设计来源 | §3 Case 覆盖 |
|---|---|---|---|
| VRC-EX-ISD-DECODE-01 | 头校验顺序与错误优先级 | ISD §验证 | UT-FD-001/003 |
| VRC-EX-ISD-LIFE-01 | 借用寿命与并发只读 | ISD §验证 | UT-FD-005 |
| （Gap）上级 wire 契约 | wire 互操作 | 契约层入口未定义 | 缺口 G-EX-1 |
<!-- STD_TEMPLATE_EXAMPLE_END -->
