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

> 本设计绑定单一软件模块：模块对象 ID 经 `--design-object-id` 写入 metadata；模块设计 ID/版本、源码修订与 Test Owner 在 §1 与 §7 固定，测试代码与 Run 报告路径按 §3、§6、§7 登记。

### 模板定位：与 `assurance.test-specification` 的关系

<!-- 编写建议（定位结论，比较依据见下）：本模板定位为独立模板，不是通用测试规格的 unit profile。理由：(1) 通用规格的 Case Matrix 是单张索引表，本模板要求逐 Case 成节并给完整函数声明、逐参数输入与独立 Oracle，深度以指导写测试代码为准，通用规格装不下；(2) 本模板的覆盖分母绑定模块设计（design.definition §14）的 Function/Constraint/Rule/Interface/Transition/Invariant 与关键错误出口 ID，并继承其正向覆盖"一个来源 ID 一条记录"的规则，这是模块设计侧特有的承接语义；(3) §3 的替身证明边界（mock 不得证明事务/原子性）、§5 的条件适用裁决是单元隔离层特有的判据。共同字段（范围、环境、判定、证据）按 STD 惯例各自维护编写建议，但权威分工如下，不形成两份同权威测试规格： -->

- **权威分工**：对单个软件模块的单元隔离测试设计，本文件是输入构造、独立 Oracle 与 Case 结构的唯一权威；整模块组装后的对外接口与内部流程 Case 权威在 `tests.module-test-design`，两者 Case 互不重复写入；`assurance.test-specification` 继续负责 contract、integration、system 等层级及跨层级 Case Matrix 汇总，其内容不因本模板而修改。
- **与模块设计的关系**：覆盖分母消费 `design.definition` §14.1/§14.2 的来源 ID 与 VRC；规则、约束、接口语义仍以模块设计为唯一权威，本设计只固定其单元层验证实例，不复制规则定义。两者 Expected 不一致时回溯模块设计修订，不在测试侧私改。模块设计 §14.2 的 VRC 已足够且不写测试代码时，可不使用本模板。
- **不得双写**：项目若已为本模块另立单元层 test-specification，其用例矩阵职能由本设计取代，只在原规格中以引用登记；不得在两处逐格维护同一批 Case 与 Expected。
- **不强制空壳**：模块的单元用例不需要此深度时（如薄适配层），直接用通用 `assurance.test-specification` 并注明理由；不为本模板保留只有标题的空文档。
- **本模板不含**：性能/容量/时序章（跟随通用规格 §6 按事实裁剪）、多模块用例矩阵、执行步骤规程与运行报告；各自引用相邻模板，不在本文件复制。

### 状态语义：四种状态分开

<!-- 编写建议：§2 的覆盖记录、§4 的 Case、§6 的判定和 §7 的证据必须能区分下列四种状态；混用任何两种都视为模板违例。 -->

| 状态种类 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| Case 设计状态 | `Designed` / `Gap`（具名缺口）/ `Tailored-N/A` | §2 覆盖记录、§4.N | 未设计写成已设计；N/A 无设计事实依据 |
| 测试代码实现状态 | `Planned` / `Implemented` | §4.N 实现位置 | 计划中的测试函数冒充可执行入口 |
| 执行状态 | `NOT_RUN` / `BLOCKED` / `INVALID` | §6、§7 引用的 Run 报告 | 未运行、被阻断或无效的执行计为通过 |
| 实际判定 Verdict | `PASS` / `FAIL` | 仅 Run 报告 | 本设计文档预填 Actual 或 Verdict |

<!-- 完成条件：任一 Case 能同时报出四种状态且互不矛盾，如 Designed + Implemented + NOT_RUN（无 Verdict）。 -->

<!-- 编写建议：本模板只设计一个软件模块的隔离测试。测试代码默认位于 tests/unit/<module>/ 或项目已登记的共置路径；<module> 是稳定代码目录名，不是 Module ID。Run 报告保存在该类测试自己的 reports/<run-id>/。不要把实际运行结果、批准或系统验收结论填进本设计。 -->

## 1. 被测模块与测试边界

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：先用一段话说明模块对外可观察的行为、主要输入输出、真实代码边界和本测试不证明的保证。固定模块设计、接口/数据机器来源、实现提交或 Planned 状态。逐项说明哪些实际代码、依赖和存储参与测试，哪些由替身代替；不能把 mock 返回值当作真实依赖行为已验证。说明本测试和契约、集成、系统测试各自承担什么。 -->

**完成条件**：读者能指出实际被测代码、替代边界、模块设计基线，以及本单元测试不能证明的组合保证。

</details>

- 被测 Module ID、正式名称、父对象与设计基线：<!-- TODO -->
- 被测 API / 行为与源码、构建目标：<!-- TODO -->
- 单元边界、真实依赖与替代依赖：<!-- TODO -->
- 不证明的组合保证及承接测试入口：<!-- TODO -->

<!-- 虚构示例：FrameDecoder 单元测试直接调用真实 decode_one(std::span<const std::uint8_t>) noexcept，使用冻结 hex 向量 fixture，不启动网络服务；它能证明头校验顺序、错误优先级与借用视图，不能证明生产接收链路的丢包处理。后者交给集成测试。完整试填样稿见 STD 仓库模板的附录 A.1。 -->

## 2. 测试依据与正向覆盖

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：从已采用模块设计出发，以适用的 Function、Constraint、Rule、Interface、状态转换、不变量及关键错误分支为分母，逐 ID 给出 Case 或具名缺口。一个来源 ID 保留一条覆盖记录；多个来源可以复用同一 Case，但要分别写清各自的独立判据。不要从已经写好的测试函数反推分母。每条记录的 Case 设计状态（Designed / Gap / Tailored-N/A）按封面后的状态语义填写；未实现与 NOT_RUN 不从覆盖分母删除；不适用须给 tailoring 决定及理由。 -->

**完成条件**：每个适用来源 ID 都有 Case 或具名缺口；组合测试责任没有被单元结果代替。

</details>

| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

<!-- 虚构示例：R-DEC-LEN → 输入声明长度大于实际字节数时返回 TRUNCATED 且不产生 Frame → UT-DEC-003；生产网络分段重组不是本 Case 的结论。 -->

## 3. 环境、夹具、隔离与复位

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：说明测试语言/runner及版本、构建目标、运行位置、数据和随机种子、受控时钟或调度器、真实与替代依赖的装配方式。fixture 优先引用项目 `interfaces/vectors/` 的冻结契约向量与 `tests/fixtures/` 的可提交输入，并固定其版本，不在本设计复制一份向量字节。每个替身要有它代替的边界、允许模拟的行为和未被它证明的性质；对事务、文件格式或并发原子性等保证，不能只用一个会直接返回期望值的 fake 证明。给出 setup、前次残留检查、每 Case 复位、并行隔离键和 teardown；环境无法建立时标 BLOCKED，不静默换环境。 -->

**完成条件**：另一位执行者能独立建立、复位和隔离环境，并知道每个替身未覆盖的真实行为。

</details>

- Runner、版本、构建与运行命令：<!-- TODO -->
- Fixture / seed / golden 数据来源及版本：<!-- TODO -->
- 真实依赖、替身、受控时钟/调度与未覆盖行为：<!-- TODO -->
- Setup、复位确认、并行隔离和 Cleanup：<!-- TODO -->

<!-- 虚构示例：每个 FrameDecoder Case 新建 decoder 实例并从冻结 hex bytes 构造输入；Case 并行运行时不共享可变 fixture。若模块实际依赖 SQLite 的原子事务，单元测试可用独立临时 SQLite，而不是仅用数组 fake 宣称事务已证明。 -->

## 4. 用例设计

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：按实际函数或模块行为建立 4.N Case，不按“正常/异常”堆两份泛泛列表。每例先展示被测函数的完整代码式声明；逐输入写构造方法、字段/范围、初态和触发动作，逐输出或错误写互斥条件、副作用与终态。Expected 在执行前固定，由独立来源或可手算规则推导，不能再调用被测算法计算期望。为每例写清可执行测试函数/文件、状态和所需上级组合用例。至少选择能区分正确实现与常见错误实现的边界和反例。 -->

**完成条件**：每个 Case 可按输入、调用、独立 Expected 和失败出口实施，不需要编码者猜测测试意图。

</details>

### 4.N `UT-<MODULE>-<NNN>` · <可观察行为与输入条件>

- **来源 ID / 被测行为 / 适用基线**

  <!-- TODO：写来源版本、函数或规则，不复制第二份权威定义。 -->

- **被测接口声明与输入构造**

  ```text
  <真实函数或方法签名>
  ```

  <!-- TODO：每个输入参数单独描述类型、取值、fixture、初态；若是状态型操作，说明通过什么公开入口形成初态。 -->

- **执行、观察点与独立 Oracle**

  <!-- TODO：写实际调用或事件、观测对象、Expected 的独立推导、允许误差或精确比较方法。 -->

- **成功、错误、副作用与清理判据**

  <!-- TODO：写互斥返回/异常、错误字段、调用后有效状态；失败时确认没有半成品或错误释放。 -->

- **实现位置、自动化入口与状态**

  <!-- TODO：tests/unit/<module>/ 下的测试文件与测试名。按封面后的状态语义分列：实现状态 Planned/Implemented；执行状态 NOT_RUN/BLOCKED/INVALID；PASS/FAIL 只出现在 Run 报告。Actual 与证据归 Run 报告。 -->

<!-- 虚构 Case：UT-DEC-003，decode_one(std::span<const std::uint8_t> input) noexcept -> DecodeResult（variant<Ok,NeedMore,Invalid>）。输入 hex `02 02 ff ff ff ff`：version 与 kind 均非法、声明 length=0xffffffff。Expected=Invalid(Version)、consumed=0、无视图、输入不变；校验顺序 version→kind→length 来自 FD-R1，期望由规则与人手计数推导，不调用 decode_one 再算一遍。将输入改成合法头可作正常对照 Case。完整试填样稿见 STD 仓库模板的附录 A.1。 -->

## 5. 状态、并发与故障测试（条件适用）

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：先按下表用模块设计中的事实逐行裁决适用性，再沿 Transition/Invariant ID 选择代表交错：初态如何从公开入口产生，哪个可控调度点或依赖边界触发故障，注入是否命中，迟到事件如何处理，最终状态和资源如何独立观察。允许受控时钟、依赖替身和故障点；禁止直接改业务终态伪造流程通过。"不适用"必须引用模块设计章节中的事实（如生命周期章的"仅栈变量、无队列/I/O"），并区分"不适用"与"尚未设计"（后者是 Gap，须登记到 §7）；同步只读模块不虚构队列或恢复协议，但并发只读交错仍按 §4 覆盖。 -->

**完成条件**：适用的状态与故障路径有可命中的注入点、独立终态判据和安全退出；不适用有事实依据。

</details>

| 模块事实（引用设计章节） | 第 5 章最低要求 |
|---|---|
| <!-- 同步只读/纯函数，无跨调用状态 --> | <!-- 写事实依据与 tailoring；不设计恢复协议；并发只读交错按 §4 覆盖 --> |
| <!-- 跨调用状态或会话 --> | <!-- 沿 Transition/Invariant 设计初态构造、交错与复位 --> |
| <!-- 异步、定时或取消 --> | <!-- 受控时钟/调度、迟到事件、注入命中证明 --> |
| <!-- 持久化或事务 --> | <!-- 提交点、失败/崩溃出口、UNKNOWN 收敛；替身不得宣称原子性已证明 --> |
| <!-- 共享资源或句柄 --> | <!-- 隔离键、独占、清理可观察 --> |

| Transition / Invariant ID | 前置事实及可控交错或注入 | Case ID | 独立观测与退出条件 |
|---|---|---|---|
| <!-- TODO；不适用则写事实与 tailoring 依据 --> | | | |

<!-- 虚构示例：无状态 FrameDecoder 的本章只留两行事实——仅栈变量、无 I/O/取消 → Tailored-N/A；并发只读 → §4 的 UT-DEC-005 已覆盖。有状态模块按 Transition/Invariant 逐行设计注入，样例见 STD 仓库模板的附录 A.2。 -->

## 6. 自动化执行与判定

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：提供从全新工作区可复现的构建和测试入口、选择模块或单 Case 的命令、环境前检、超时、退出码、失败现场与清理顺序。明确 PASS、FAIL、BLOCKED、INVALID 和 NOT_RUN：断言与设计不符是 FAIL；依赖环境缺失是 BLOCKED；故障注入未命中是 INVALID；尚未运行是 NOT_RUN。flaky 不通过重跑覆盖原失败，应保存每次 Run，记录随机种子和调度。覆盖率可辅助发现漏测，但百分比不替代 §2 的设计保证覆盖。单元层微基准（如堆分配、复杂度断言）按 `assurance.test-specification` §6 的条件裁剪执行，不在本设计另立性能章。 -->

**完成条件**：自动化入口能复现每个 Case，并按事实区分失败、阻塞、无效与未运行。

</details>

- 完整执行命令、单 Case 命令与运行位置：<!-- TODO -->
- 期限、退出码、重跑规则与判定：<!-- TODO -->
- 覆盖率/变异或反例检查（适用时）：<!-- TODO -->

<!-- 虚构示例：教学宿主命令 `c++ -std=c++20 … && ./frame_decoder_test`，退出码 0 且向量输出 PASS 才算成功；并发 Case 若串行执行从未交错记 INVALID 而非 PASS；重跑生成新 run-id 不覆盖原失败。 -->

## 7. 证据、报告与未决项

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：设计只定义证据合同，不预填 Actual 或 PASS。规定 Run ID、命令和版本、fixture/seed、stdout/stderr、断言失败、原始数据及脱敏/保留方式；正式结果在 tests/unit/<module>/reports/<run-id>/ 或共置等价目录。逐项登记无法构造的输入、没有独立 Oracle、缺少注入点或上级合同未定等设计缺口，给 Owner、最晚关闭 Gate 和下一步行动。只有实际 Run 报告才能声明执行结果；单元 PASS 不能关闭契约、集成或系统目标。 -->

**完成条件**：Case 能定位 Run 报告与原始证据；未决设计和未执行测试都不被写成 PASS。

</details>

| 缺口 ID / 关联来源 | 阻断的 Case 或保证 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|---|
| <!-- TODO；无缺口时写经核对的“无” --> | | | |

<!-- 虚构示例：G-EX-1“上级协议组合测试入口未定义”，阻断 UT-DEC-001–003 的组合责任，Owner=教学样例评审，最晚 Gate=下次样例修订，关闭条件=指定组合测试文档或批准裁剪；关闭前 NOT_RUN 保留。 -->

<!-- 交付自查：另一位作者能否从某个来源 ID 找到可执行 Case；从 Case 找到输入、独立 Expected、测试函数及报告路径；从一个失败找到未覆盖范围，而不把单元测试结果提升为系统验证？ -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
## 附录 A. 全链试填样稿（教学数据，仅验证模板槽位）

<details>
<summary>编写建议、示例与完成条件</summary>

<!-- 编写建议：本附录用仓库自有虚构教学样例试填第 1-7 章槽位，验证"来源 ID → Case → fixture → 独立 Oracle → 测试函数 → Run 报告路径"能否闭合。A.1 是同步无状态模块（docs/examples/isd-frame-decoder/ 的教学 FrameDecoder，基线 EX-FRAME-MODULE 1.0.0 / EX-ISD v1 修订 2，规则 FD-R1–FD-R4）；A.2 只示范有状态模块如何填第 5 章（templates/design/implementation-design.md §7 的虚构 CMD-001 图例，无代码实现）。样稿各章只给代表性内容验证槽位，不构成完整实例；正式项目须以自己的模块设计来源 ID 重新推导，不复制教学结论。 -->

**完成条件**：读者能用 A.1 逐章对照检查自己的单元测试设计是否闭合全链，能用 A.2 检查有状态模块第 5 章的注入点、命中证明与替身边界是否可检查；教学标识没有被当作任何项目的接口 authority 或运行证据。

</details>

<!-- 本附录全部为教学数据：教学标识不是任何项目的接口 authority；正式项目不得复制本附录结论作为自己的设计或运行证据。 -->

### A.1 无状态同步模块：教学 FrameDecoder

**第 1 章试填**：被测对象是 EX-FRAME-MODULE 的 M201 FrameDecoder，设计基线 EX-ISD/v1（教学修订 2，与 `docs/examples/isd-frame-decoder/` 三文件同步）。被测 API 为 `DecodeResult decode_one(std::span<const std::uint8_t> input) noexcept`，实现在 `frame_decoder.cc`，构建目标为教学单二进制测试宿主。参与测试的全部是真实代码；模块无网络、持久化、时钟或线程依赖，因此**不引入任何替身**。不证明：宿主访问控制、日志与脱敏（FD-R4 归宿主）、产品协议兼容、调用方长寿命输入与真实峰值负载；承接入口为宿主组合验证（当前 NOT_RUN，见 G-EX-2）。

**第 2 章试填**（一个来源 ID 一条记录；多个 Case 复用时各自判据不同）：

| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|
| FD-R1 / EX-FRAME-MODULE 1.0.0 | 头校验顺序 version→kind→length；载荷不齐 NEED_MORE 且不消费；成功只消费首帧 | UT-DEC-001 / 002 / 003 | Designed | 上级协议组合测试（入口未定义 → G-EX-1） |
| FD-R2 / 同基线 + frame_decoder.h | Ok 只携带借用视图；NeedMore/Invalid 的 consumed=0 且无视图；输入不被修改；并发只读不共享可变状态 | UT-DEC-001 / 004 / 005 | Designed | 宿主长寿命组合（NOT_RUN → G-EX-2） |
| FD-R3 / 同基线 | 不越界读取；先减 6 再比长度防溢出；无堆分配 | UT-DEC-001–004 + 实现核对（各 ID 独立判据） | Designed | — |
| FD-R4 / 同基线 | 错误仅结构化 InvalidReason，库内无日志调用 | UT-DEC-003 + 人工核对 | Designed | 宿主接收链（NOT_RUN → G-EX-2） |

**第 3 章试填**：Runner 为 C++20 教学测试宿主（README 构建命令，无测试框架）；fixture 是冻结 hex 向量，无随机 seed、无 golden 文件、无受控时钟。因无状态，每个向量独立 span、天然复位；并发 Case 由主线程 join 两个线程后才销毁输入。无编译器时记 BLOCKED/skip 并保留记录，不冒充 PASS。

**第 4 章试填**（仅 3 个代表 Case 验证槽位；完整分母以 FD-V1–FD-V3 为准）：

- **UT-DEC-001 · 正常帧与尾随字节**：输入 `01 01 00 00 00 02 41 42 FF`（头 6B：version=1、kind=1、length=2；payload `41 42`；尾随 `FF`）。动作：单次调用。独立 Oracle：人工按 FD-R1 计数 length=2 → consumed=8；`view.data == input+6`、size=2、字节为 `41 42`；尾随 `FF` 不消费——期望由规则与人手计数推导，不调用 decode_one 复算。互斥输出：仅 Ok 分支；输入逐字节不变。副作用与清理：无堆分配、无 I/O。位置：`frame_decoder_test.cc` main 正向量；Implemented / NOT_RUN。
- **UT-DEC-003 · 非法头优先级**：输入 `02 02 ff ff ff ff`（version 与 kind 均非法，length=0xffffffff）。独立 Oracle：version 最先 → `Invalid(Version)`、consumed=0、无视图；不等待"巨大载荷"（长度限界先于载荷判断）。位置：`invalid` helper；Implemented / NOT_RUN。
- **UT-DEC-005 · 并发只读与输入不变**：前置：两个线程以同一冻结 span 并发调用；主线程 join 后才销毁输入。独立 Oracle：两线程结果一致且等于 UT-DEC-001 的人工期望；调用前后输入逐字节不变。命中说明：并发由线程+join 构造（正式 runner 须可复现交错）。位置：main 并发段；Implemented / NOT_RUN。

**第 5 章试填**：

| 模块事实（引用设计章节） | 第 5 章最低要求 |
|---|---|
| EX-ISD §7 生命周期：仅栈变量、无队列/线程池/I/O/取消接口 | Tailored-N/A，事实依据如左；无恢复协议可设计，不虚构 |
| FD-R2：并发调用不共享可变状态 | 并发只读交错已由 §4 的 UT-DEC-005 覆盖，不构成恢复协议要求 |

**第 6 章试填**：完整命令即 README 构建块（`c++ -std=c++20 … frame_decoder_test` 并执行）；教学宿主无单 Case 过滤开关，只能全量运行——正式 runner 必须提供单 Case 选择命令（正文 §6 已要求，试填确认必要）。前检记录编译器 `--version`；退出码 0 且全部固定向量输出为 PASS 才算本 Run 成功。判定示例：并发 Case 若实现为串行 join、从未真正并发，记 INVALID 而非 PASS。重跑生成新 run-id，不覆盖原失败。

**第 7 章试填**：正式项目 Run 报告位于 `tests/unit/frame_decoder/reports/<run-id>/`（教学例共置于 `docs/examples/isd-frame-decoder/`）；每次 Run 保存完整命令、编译器版本、源文件 hash、stdout 与退出码。

| 缺口 ID / 关联来源 | 阻断的 Case 或保证 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|---|
| G-EX-1 / FD-R1 | 上级协议组合测试入口未定义，UT-DEC-001–003 的组合责任悬空 | 教学样例评审 / 下次样例修订 | 指定组合测试文档，或明示教学范围外并批准裁剪 |
| G-EX-2 / FD-R2、FD-R4 | 宿主长寿命、权限、脱敏接收链未实现 | 宿主设计 / 后续教学样例 | 宿主入口实现后补组合验证；当前保留 NOT_RUN |

<!-- 试填结论：全链可在现有槽位闭合；两处确认——(1) §6 要求单 Case 命令是必要的（教学宿主缺失该能力即被暴露）；(2) BLOCKED（无编译器）与 NOT_RUN（未运行）在状态语义表中可区分表达。 -->

### A.2 有状态模块第 5 章试填（虚构 CMD-001，无实现）

<!-- CMD-001 submit 来自 templates/design/implementation-design.md §7 的有状态提交图例，没有代码实现；本节只示范第 5 章"Transition/Invariant 行"的填法与替身证明边界的写法。 -->

| Transition / Invariant ID | 前置事实及可控交错或注入 | Case ID | 独立观测与退出条件 |
|---|---|---|---|
| INV-CMD-1 幂等重放：request_id 已存在不新增执行 | 初态经公开 submit 真实提交一次形成；在结果记录写入前的依赖边界注入一次失败（记录层替身返回错误一次，替身注入计数=1 即命中证明）；迟到响应用受控时钟触发 | UT-CMD-101 | 第二次 submit 返回原 ResultRecord 或 ACCEPTED+status_ref；query(request_id) 读权威记录确认执行数=1；UNKNOWN 状态下禁止新业务重试 |
| INV-CMD-2 事务原子性：CommandRecord 与 ResultRecord 同事务 | 证明边界声明：数组 fake 直接返回 SUCCEEDED 不证明原子性；单元层用独立临时 SQLite（真实事务）实现本 Case，无法建立时记 Gap 并转 BLOCKED | UT-CMD-102 | 注入后经公开 query 检查：或两记录都在、或都不在；不存在孤立 PENDING |
| 出口：响应丢失 | submit 成功后丢弃响应，经 query(request_id) 收敛 | UT-CMD-103 | query 返回 SUCCEEDED + result；不产生第二次执行 |

<!-- 试填要点：替身若按 §3 禁令所述"直接返回期望值"，INV-CMD-1/2 的证明即降级为 INVALID；A.2 示范把证明边界写成可检查的声明（命中计数、权威记录来源、证明边界的替代手段），这是有状态模块不能跳过第 5 章的原因。 -->

<!-- STD_TEMPLATE_EXAMPLE_END -->

