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

<span style="color:#1f6feb"><em>**编写建议**：本模板是系统测试方案，与 design.software-system（系统设计阶段）一一对应。方案只登记测试分类与 Case 清单（每 Case 一行责任摘要），不写 Case 细节；逐 Case 展开一 Case 一文档（tests.system-case）。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本方案绑定软件系统：父设计 Document ID 经 `--parent-document-id` 写入 metadata；系统设计 ID/版本在 §1 固定。

### 模板定位：方案、用例与计划的边界

<span style="color:#1f6feb"><em>**编写建议**：本方案对应系统设计阶段（design.software-system；总体设计的软件分支同用本模板）。分母来源是系统设计的端到端流程（§7）、对外接口（§8）、系统约束与预算，以及机制的端到端保证（design.system-mechanism §15 承接进入本分母——机制不单独立测试文档）。子系统层归 tests.subsystem-test-scheme；验收活动不在本家族，按项目 tailoring 承接。</em></span>

- **权威分工**：系统层测试的 Case 清单（ID、分类、优先级、责任摘要、设计状态）以本方案为唯一登记处；单 Case 展开归 `tests.system-case`（一 Case 一文档）；活动组织归 `tests.system-test-plan`。
- **只有摘要**：本方案每条 Case 只写责任摘要（要测什么），不写输入构造、Oracle 或步骤。
- **下层 PASS 不关闭本层**；本层 PASS 不关闭上层组合目标。

### 状态语义：用例状态

<span style="color:#1f6feb"><em>**编写建议**：本方案只持有 用例状态（Designed / Gap / Tailored-N/A）；实现状态（Planned/Implemented）在对应 case-design 文档，执行状态与 Verdict 只在 Run 报告。混层即违例。</em></span>

| 状态 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| 用例状态 | `Designed` / `Gap`（具名缺口）/ `Tailored-N/A` | 本方案 §3 清单 | 未设计写成已设计；N/A 无设计事实依据 |

<span style="color:#1f6feb"><em>**完成条件**：任一 Case 在本方案中只报设计状态；实现与执行状态可沿 Case ID 追到 case-design 文档与 Run 报告。</em></span>

## 1. 目标、范围与被测对象

<span style="color:#1f6feb"><em>**本节目的**：固定整软件系统组装层的对象与边界。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：被测系统与设计基线；真实子系统；外部依赖真实或边界替身及证明边界；不证明的真实环境与验收目标。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 EX-APP 方案覆盖启动/配置/停止流程与机制端到端。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者能说清系统层测什么、验收承接什么。</em></span>

- 被测对象、设计基线与父对象：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-APP/v1 软件系统（含 DIR 等），设计基线 EX-APP/v1</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 本阶段测试边界（真实组成 / 边界替身）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">子系统全部真实；对外存储用独立测试实例（真实协议）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 不证明的组合保证及承接入口：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">真实生产环境、客户验收；承接＝验收活动（tailoring 承接）</span><!-- STD_TEMPLATE_EXAMPLE_END -->


## 1.5 测试方法与测试设计技术

<span style="color:#1f6feb"><em>**本节目相**：固定系统层"怎么测"的方法论——单元层测试设计技术比较单一（mock 为主），上游测试常**多方法共存**，需逐一描述与边界。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：测试设计技术（按 Case 家族用哪些——等价类划分/边界值/状态转换/决策表/错误猜测/属性测试/变异测试等，写明对哪些 family 用哪种及不用哪种）；入场标准（设计文档到位、方案清单冻结、Case 实现就绪、替身 Verified、环境齐）；离场标准（分母每条来源有 Case 或缺口、Verdict 齐全、缺口有主、设计变更触发重跑）；自动化策略（哪些进 CI、单 Case 选择入口、断点/重跑规则、flaky 不掩盖根因）。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——系统层方法（含注入/边界/调用序等具体细节）。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3 Case 行能指出所用方法与环境类型；入场/离场可判定；环境类型与 asset-design 契约对应；无未声明的环境依赖。</em></span>

| Case 家族 | 测试设计技术 | 环境类型引用 | 自动化与判定规则 |
|---|---|---|---|
| <!-- TODO：如 normal/boundary/negative/concurrency/recovery --> | <!-- TODO --> | <!-- 类型名（详见 §1.7） --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；系统层测试方法——含注入/边界/调用序等具体细节）**：</span>

<span style="color:#6e7681">| Case 家族 | 测试设计技术 | 环境类型引用 | 自动化与判定 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| normal（E2E 关键路径） | 端到端跑通启动/业务/配置/停止 | 真实子系统 + 预生产镜像 | CI 跑全集；失败不阻断后续但需复现 |
| | · 注入：标准启动→业务调用→配置变更→正常停止 | | · 验证每阶段事件顺序与状态切换 |
| boundary（全链路集成） | 子系统/机制端到端（含 EX-OBS PARTIAL） | 真实子系统 + 独立存储 + 受控时钟 | 单 Case --filter；机制端到端独立记录 |
| | · 注入：跨子系统全链路正常路径 + 机制端到端 PARTIAL 场景 | | · 验证子系统集成语义、机制在系统级端到端表现 |
| negative（故障注入） | kill/注入失败/迟到完成/跨子系统交接 | 注入 fake | 计数=0 标 INVALID；不掩盖 |
| | · 注入：kill 子系统进程/网络注入/迟到事件/子系统交接失败 | | · 验证恢复后能继续安全接受请求；旧请求不复活 |
| performance（性能/容量） | 启动时长/并发/吞吐/内存峰值 vs 预算 | 真实子系统 + 监控接入 | 一次基线采样；后续回归比对 |
| | · 注入：基线负载 + 峰值负载（启动时长 5s、并发 100、内存 4Gi 等预算口径） | | · 与设计预算对照，越界标 Blocked |
| recovery（灾备） | kill/注入失败/资源回收 | 真实子系统 + 监控日志 | 复现状态与修复分开记录；无因果标未复现 |
| | · 注入：kill 进程/注入失败/磁盘满/资源回收失败 | | · 验证复现状态 vs 修复状态分开记录；无因果证据标未复现 |
| security（安全冒烟） | 鉴权/注入/脱敏（prompt 注入 + 敏感数据） | 真实子系统 | 缺关键 fake 时降级为 Blocked |
| | · 注入：prompt 注入样本 + 敏感数据样本 | | · 必须拒绝/脱敏，不允许泄露系统提示 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 1.6 替身使用策略与边界

<span style="color:#1f6feb"><em>**本节目相**：固定系统层替身的使用，让 §3 清单的替身选择可解释可复核。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：替身决策准则（按所有权/可控性/真实性分类——内部真实/边界 fake/真协议测试实例/容器等）；替身形态（mock/fake/stub/spy 的取舍与代价）；替身保真度——契约与自检归 `tests.asset-design`（一资产一文档），方案与 Case 只引用其 ID 不复制行为；交互断言 vs 返回值断言（优先返回值，必要时断言关键调用序，但不耦合内部实现）；反模式（不 mock 你不拥有的接口、不 mock 值对象/纯数据、不为凑覆盖率而 mock、不过度断言内部细节）；与 §1 边界、§3 Case 清单、`tests.system-case` §2 替身选择一致。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——系统层替身矩阵。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3 Case 行能指出替身类型与契约文档 ID；替身矩阵与 asset-design 一一对应；反模式逐项被排除并有理由。</em></span>

| 协作者类型 | 替身形态 | 替身契约文档（tests.asset-design） | 决策理由 |
|---|---|---|---|
| <!-- TODO --> | <!-- mock/fake/stub/spy --> | <!-- TODO：asset 文档 ID --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；系统层替身矩阵）**：</span>

<span style="color:#6e7681">| 协作者 | 形态 | 替身契约 | 理由 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 真实子系统（全部） | 独立存储测试实例（真协议） | 跨系统接口 fake | 受控时钟 fake |
| · 契约与自检归 tests.asset-design | | · 不 mock 你不拥有的对象 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 1.7 测试环境类型（方案定义）

<span style="color:#1f6feb"><em>**本节目相**：固定本层"在哪类环境上跑"——列出环境**类型**（抽象类别）及其行为/真伪与契约文档（tests.asset-design 或产品规范）；同一类型可多套实例（多 docker 用于并行），具体**实例编号与分配**由 `tests.system-test-plan` §4 编排，Case 在 §2 通过「环境类型 + ENV 实例编号」引用，不在本文档重复描述环境本身。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下方灰字——系统层测试环境类型（含契约与用法具体细节）+ 拓扑。

**拓扑**：系统层测试环境拓扑（ENV 类型 → ENV 实例 → 被测对象）：

```mermaid
flowchart LR
  Sub["真实子系统（全部）<br/>(ENV-1)"] --> SysH["系统 harness<br/>(ENV-1 链接)"]
  Store["独立存储测试实例<br/>STORE-TEST（真协议）<br/>(ENV-2)"] --> SysH
  Fake["跨系统接口 fake<br/>FAKE-REG<br/>(ENV-3)"] --> SysH
  CLK["受控时钟 fake<br/>CLK-APP<br/>(ENV-4)"] --> SysH
  Prod["预生产镜像<br/>G-EX-3 排期中<br/>(ENV-5)"] --> SysH
  SysH --> Case["被测系统（EX-APP）"]
```</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个 §3 Case 行能指出所用环境类型；类型与 asset-design 契约对应；无未声明的环境依赖。</em></span>

| 环境类型 | 行为/真伪 | 契约文档 | 在本层用例中的角色 |
|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；系统层测试环境类型——含契约与用法具体细节）**：</span>

<span style="color:#6e7681">| 环境类型 | 行为/真伪 | 契约文档 | 在本层用例中的角色 |</span>
<span style="color:#6e7681">|---|---|---|---|</span>
<span style="color:#6e7681">| 真实子系统（全部） | 真实 | — | E2E 关键路径/全链路集成用例 |
| · 契约：源码即真实子系统 | | · 用法：系统 harness 链接全部真实 || 独立存储测试实例 | 真协议（独立于生产存储） | STORE-TEST | 数据库/存储相关用例 |
| · 契约：真协议，独立于生产存储 | | · 用法：升级场景测试；不 mock 协议 || 外部接口 fake（注册/接入） | 只代返回值/超时 | FAKE-REG | 跨系统边界用例 |
| · 契约：替代跨系统接口 | | · 用法：测试前配置拒绝/超时 || 受控时钟 fake | 系统级时间推进 | CLK-APP | 时间/调度用例 |
| · 契约：系统级时间单调推进 | | || 预生产镜像 | 真实但受控 | 镜像快照版本 | E2E 与全链路集成 |
| · 契约：受控的预生产环境，记录快照版本 | | · 用法：E2E 端到端在此镜像运行 |</span>

<span style="color:#6e7681">**总体说明**：C++20 系统 harness 链接所有子系统为真实调用；独立存储测试实例（真协议）连接预生产镜像版本；受控时钟 fake（系统级时间推进）；并行隔离按子系统实例+端口+数据命名空间；监控与日志接入；G-EX-3 真实环境（如预生产）有 Owner 与排期；缺关键环境时整批降级为 Blocked 并登记缺口，不静默换工具链。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

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
| performance | 适用 | 启动时长与停止清空期限断言 |
| endurance | 裁剪 | 容量与长稳另立专项（tailoring） |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 覆盖分母与 Case 清单

<span style="color:#1f6feb"><em>**本节目的**：把 design.software-system 的适用来源 ID 转成 Case 清单——测试分母的唯一登记。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：一个来源 ID 至少一条记录（可多 Case 分担，分别写责任摘要）；以设计文档（design §12/§14）的验证项 VRC 清单为分母逐项对账：每个 VRC 至少一个 Case——验证项是设计声明的必测点，本清单只引用其 ID 不复制定义、不做附录；Case ID 稳定且唯一（SYS-<对象>-<NNN>）；责任摘要只写“要测什么、边界在哪”，不写输入与 Oracle；设计状态按状态语义；未实现与 NOT_RUN 不删；不适用转 §4。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下表灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：每个适用来源 ID 有 Case 或缺口；每个 Case ID 可追到（或计划有）case-design 文档。</em></span>

| 来源 ID / 固定版本 | 设计验证项 ID | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | | | <!-- TODO --> | <!-- TODO --> | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；一来源至少一条）**：</span>
<span style="color:#6e7681">| 来源 ID / 固定版本 | 设计验证项 ID | Case ID | 分类 | 优先级 | 责任摘要（要测什么） | 设计状态 | 上级组合验证入口 |</span>
<span style="color:#6e7681">|---|---|---|---|---|---|---|</span>
<span style="color:#6e7681">| 启动流程（系统设计 §7.3） | VRC-APP-001 | SYS-APP-001 | normal | P0 | 全组件按序就绪，失败组件不阻塞重启 | Designed | — |</span>
<span style="color:#6e7681">| 停止清空（§7.6） | VRC-APP-002 | SYS-APP-002 | recovery | P0 | 在途请求退出且无残留，重启前确认 | Designed | — |</span>
<span style="color:#6e7681">| 机制端到端：EX-OBS §15 | VRC-APP-003 | SYS-APP-003 | normal | P1 | 版本核对机制端到端 PARTIAL 语义成立 | Designed | 验收场景预演（不替代验收） |</span>
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
<span style="color:#6e7681">| 真实生产环境验证 / 环境不可得 | Gap（G-EX-3） | 运维 / 预生产环境排期 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 文档联动与清单变更规则

<span style="color:#1f6feb"><em>**本节目的**：固定方案—用例—计划的联动规则，防三处漂移。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：新 Case 先入本清单再建 case-design 文档（文档 ID＝Case ID）；清单变更须同步计划构成表；写明方案冻结/版本规则。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：清单与 case-design 文档一一对应；计划只引用不复制。</em></span>

- 方案冻结与变更规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">清单随系统设计基线冻结；变更同步系统计划</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 与 case-design / 计划的同步规则：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">Case 文档 ID＝Case ID；tests.system-test-plan 引用本方案版本</span><!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">新增 SYS-APP-004 先入清单再建 Case 文档；系统计划引用本方案 v1.0。</span>
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
<span style="color:#6e7681">| VRC-APP-001 | 启动流程按序就绪 | 系统设计 §12 | SYS-APP-001 |</span>
<span style="color:#6e7681">| VRC-APP-002 | 停止清空无残留 | 同 §12 | SYS-APP-002 |</span>
<span style="color:#6e7681">| VRC-APP-003 | 机制端到端 PARTIAL 语义 | 同 §12 | SYS-APP-003 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->
