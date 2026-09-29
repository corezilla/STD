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

<span style="color:#1f6feb"><em>**编写建议**：本模板只设计一个软件模块的隔离单元测试。测试代码默认位于 tests/unit/<module>/ 或项目已登记的共置路径；`<module>` 是稳定代码目录名，不是 Module ID。Run 报告保存在该类测试自己的 reports/<run-id>/。不要把实际运行结果、批准或系统验收结论填进本设计。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本设计绑定单一软件模块：模块对象 ID 经 `--design-object-id` 写入 metadata；模块设计 ID/版本、源码修订与 Test Owner 在 §1 与 §7 固定，测试代码与 Run 报告路径按 §3、§6、§7 登记。

### 模板定位：与 `assurance.test-specification` 的关系

<span style="color:#1f6feb"><em>**编写建议**：本模板定位为独立模板，不是通用测试规格的 unit profile。理由：(1) 通用规格的 Case Matrix 是单张索引表，本模板要求逐 Case 成节并给完整函数声明、逐参数输入与独立 Oracle，深度以指导写测试代码为准，通用规格装不下；(2) 覆盖分母绑定模块设计（design.definition §14）的来源 ID，继承"一个来源 ID 一条记录"规则；(3) §3 替身证明边界、§5 条件适用裁决是单元隔离层特有判据。权威分工如下，不形成两份同权威测试规格：</em></span>

- **权威分工**：对单个软件模块的单元隔离测试设计，本文件是输入构造、独立 Oracle 与 Case 结构的唯一权威；整模块组装后的对外接口与内部流程 Case 权威在 `tests.module-test-design`，两者 Case 互不重复写入；`assurance.test-specification` 继续负责 contract、integration、system 等层级及跨层级 Case Matrix 汇总，其内容不因本模板而修改。
- **与模块设计的关系**：覆盖分母消费 `design.definition` §14.1/§14.2 的来源 ID 与 VRC；规则、约束、接口语义仍以模块设计为唯一权威，本设计只固定其单元层验证实例，不复制规则定义。两者 Expected 不一致时回溯模块设计修订，不在测试侧私改。模块设计 §14.2 的 VRC 已足够且不写测试代码时，可不使用本模板。
- **不得双写**：项目若已为本模块另立单元层 test-specification，其用例矩阵职能由本设计取代，只在原规格中以引用登记；不得在两处逐格维护同一批 Case 与 Expected。
- **不强制空壳**：模块的单元用例不需要此深度时（如薄适配层），直接用通用 `assurance.test-specification` 并注明理由；不为本模板保留只有标题的空文档。
- **本模板不含**：性能/容量/时序章（跟随通用规格 §6 按事实裁剪）、多模块用例矩阵、执行步骤规程与运行报告；各自引用相邻模板，不在本文件复制。

### 状态语义：四种状态分开

<span style="color:#1f6feb"><em>**编写建议**：§2 的覆盖记录、§4 的 Case、§6 的判定和 §7 的证据必须能区分下列四种状态；混用任何两种都视为模板违例。</em></span>

| 状态种类 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| Case 设计状态 | `Designed` / `Gap`（具名缺口）/ `Tailored-N/A` | §2 覆盖记录、§4.N | 未设计写成已设计；N/A 无设计事实依据 |
| 测试代码实现状态 | `Planned` / `Implemented` | §4.N 实现位置 | 计划中的测试函数冒充可执行入口 |
| 执行状态 | `NOT_RUN` / `BLOCKED` / `INVALID` | §6、§7 引用的 Run 报告 | 未运行、被阻断或无效的执行计为通过 |
| 实际判定 Verdict | `PASS` / `FAIL` | 仅 Run 报告 | 本设计文档预填 Actual 或 Verdict |

<span style="color:#1f6feb"><em>**完成条件**：任一 Case 能同时报出四种状态且互不矛盾，如 Designed + Implemented + NOT_RUN（无 Verdict）。</em></span>

## 1. 被测模块与测试边界

<span style="color:#1f6feb"><em>**本节目的**：固定被测单元的身份、设计基线与隔离边界——哪些代码真实参与、哪些依赖被替代、本单元测试不证明什么。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：被测 Module ID、正式名称、父对象与设计基线版本；被测 API/行为与源码、构建目标；逐项列出真实依赖与替身，不能把 mock 返回值当作真实依赖行为已验证；本测试与契约、集成、系统测试各自承担什么，不证明的组合保证写明承接入口。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 FrameDecoder 单元测试直接调用真实 decode_one(std::span<const std::uint8_t>) noexcept，使用冻结 hex 向量 fixture，不启动网络服务；它能证明头校验顺序、错误优先级与借用视图，不能证明生产接收链路的丢包处理——后者交给集成测试。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：读者能指出实际被测代码、替代边界、模块设计基线，以及本单元测试不能证明的组合保证。</em></span>

- 被测 Module ID、正式名称、父对象与设计基线：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-FRAME-MODULE 的 M201 FrameDecoder，父对象 S01，设计基线 EX-ISD/v1 修订 2</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 被测 API / 行为与源码、构建目标：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">decode_one(std::span&lt;const std::uint8_t&gt;) noexcept，实现在 frame_decoder.cc，教学单二进制目标</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 单元边界、真实依赖与替代依赖：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">全部真实代码；无网络/持久化/时钟/线程依赖，不引入替身</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 不证明的组合保证及承接测试入口：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">宿主权限与脱敏（FD-R4）、产品协议兼容、长寿命输入；承接＝宿主组合验证（NOT_RUN → G-EX-2）</span><!-- STD_TEMPLATE_EXAMPLE_END -->




## 2. 测试依据与正向覆盖

<span style="color:#1f6feb"><em>**本节目的**：把模块设计的适用来源 ID 转成单元层覆盖分母，逐 ID 给 Case 或具名缺口，不从已写好的测试函数反推分母。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：以适用的 Function、Constraint、Rule、Interface、状态转换、不变量及关键错误分支为分母；一个来源 ID 保留一条覆盖记录，多个来源可复用同一 Case 但分别写独立判据；每条记录的 Case 设计状态（Designed / Gap / Tailored-N/A）按封面后的状态语义填写；未实现与 NOT_RUN 不从覆盖分母删除；不适用须给 tailoring 决定及理由。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构规则 FD-R1 →“头校验顺序 version→kind→length；载荷不齐 NEED_MORE 且不消费”→ UT-DEC-001/002/003；上级协议组合测试入口未定义登记为缺口 G-EX-1，不用单元结果代替。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：每个适用来源 ID 都有 Case 或具名缺口；组合测试责任没有被单元结果代替。</em></span>

| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；一来源一条记录）**：</span>

| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|
| FD-R1 / EX-FRAME-MODULE 1.0.0 | 头校验顺序 version→kind→length；载荷不齐 NEED_MORE 且不消费；成功只消费首帧 | UT-DEC-001 / 002 / 003 | Designed | 上级协议组合测试（入口未定义 → G-EX-1） |
| FD-R2 / 同基线 + frame_decoder.h | Ok 只携带借用视图；NeedMore/Invalid 的 consumed=0 且无视图；输入不被修改；并发只读不共享可变状态 | UT-DEC-001 / 004 / 005 | Designed | 宿主长寿命组合（NOT_RUN → G-EX-2） |
| FD-R3 / 同基线 | 不越界读取；先减 6 再比长度防溢出；无堆分配 | UT-DEC-001–004 + 实现核对（各 ID 独立判据） | Designed | — |
| FD-R4 / 同基线 | 错误仅结构化 InvalidReason，库内无日志调用 | UT-DEC-003 + 人工核对 | Designed | 宿主接收链（NOT_RUN → G-EX-2） |
<!-- STD_TEMPLATE_EXAMPLE_END -->



## 3. 环境、夹具、隔离与复位

<span style="color:#1f6feb"><em>**本节目的**：让另一位执行者能独立建立、复位和隔离单元测试环境，并知道每个替身未覆盖的真实行为。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：测试语言/runner 及版本、构建目标、运行位置、数据和随机种子、受控时钟或调度器、真实与替代依赖的装配方式；fixture 优先引用项目 interfaces/vectors/ 的冻结契约向量与 tests/fixtures/ 的可提交输入并固定版本，不在本设计复制向量字节；每个替身写清代替的边界、允许模拟的行为和未证明的性质——事务、文件格式或并发原子性不能只用直接返回期望值的 fake 证明；给出 setup、前次残留检查、每 Case 复位、并行隔离键和 teardown；环境无法建立时标 BLOCKED，不静默换环境。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 FrameDecoder 每 Case 新建实例并从冻结 hex 向量构造输入，并行 Case 不共享可变 fixture；若模块实际依赖 SQLite 原子事务，单元测试用独立临时 SQLite，而不是仅用数组 fake 宣称事务已证明。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：另一位执行者能独立建立、复位和隔离环境，并知道每个替身未覆盖的真实行为。</em></span>

- Runner、版本、构建与运行命令：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">C++20 教学测试宿主（无框架）；无 seed、无受控时钟</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- Fixture / seed / golden 数据来源及版本：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">冻结 hex 向量（如 01 01 00 00 00 02 41 42）；无 golden 文件</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 真实依赖、替身、受控时钟/调度与未覆盖行为：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">无替身；若依赖 SQLite 原子事务，用独立临时 SQLite 而非数组 fake</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- Setup、复位确认、并行隔离和 Cleanup：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">每向量独立 span、天然复位；并发 Case join 后才销毁输入；无编译器记 BLOCKED</span><!-- STD_TEMPLATE_EXAMPLE_END -->




## 4. 用例设计

<span style="color:#1f6feb"><em>**本节目的**：把覆盖记录落成可直接实施的逐 Case 设计，编码者不需要猜测测试意图。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：按实际函数或模块行为建立 4.N Case，不按“正常/异常”堆两份泛泛列表；每例先给被测函数完整代码式声明，逐输入写构造方法、字段/范围、初态和触发动作，逐输出或错误写互斥条件、副作用与终态；Expected 在执行前固定，由独立来源或可手算规则推导，不能再调用被测算法计算期望；为每例写清可执行测试函数/文件、状态和所需上级组合用例；至少选择能区分正确实现与常见错误实现的边界和反例。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 Case UT-DEC-003：decode_one 输入 hex `02 02 ff ff ff ff`（version 与 kind 均非法、声明 length=0xffffffff），Expected=Invalid(Version)、consumed=0、无视图、输入不变——校验顺序来自 FD-R1，期望由规则与人手计数推导，不调用 decode_one 再算一遍；把输入改成合法头即正常对照 Case。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：每个 Case 可按输入、调用、独立 Expected 和失败出口实施，不需要编码者猜测测试意图。</em></span>

### 4.N `UT-<MODULE>-<NNN>` · <可观察行为与输入条件>

<span style="color:#1f6feb"><em>**编写建议**：一个 Case 一个小节，标题为 `UT-<MODULE>-<NNN>` 加可观察行为与条件；按下列槽位逐项填写，状态按封面后的状态语义分列，不复制第二份权威定义。</em></span>

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

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
### 4.1 `UT-DEC-003` · 非法头优先级（虚构示例）

<span style="color:#6e7681">- **来源 ID / 被测行为 / 适用基线**</span>

<span style="color:#6e7681">  FD-R1 / EX-FRAME-MODULE 1.0.0：头校验顺序 version→kind→length，非法即拒、不等待载荷。</span>

<span style="color:#6e7681">- **被测接口声明与输入构造**</span>

  ```text
<span style="color:#6e7681">  DecodeResult decode_one(std::span<const std::uint8_t> input) noexcept</span>
  ```

<span style="color:#6e7681">  `input`：hex `02 02 ff ff ff ff`（version 与 kind 均非法，声明 length=0xffffffff），冻结向量。</span>

<span style="color:#6e7681">- **执行、观察点与独立 Oracle**</span>

<span style="color:#6e7681">  单次调用；观察返回变体、consumed 与输入字节。Expected=Invalid(Version)、consumed=0、无视图——由规则与人手计数推导，不调用 decode_one 复算。</span>

<span style="color:#6e7681">- **成功、错误、副作用与清理判据**</span>

<span style="color:#6e7681">  仅 Invalid 分支；输入逐字节不变；无堆分配、无 I/O；无需清理。把输入改成合法头即正常对照 Case UT-DEC-001。</span>

<span style="color:#6e7681">- **实现位置、自动化入口与状态**</span>

<span style="color:#6e7681">  `frame_decoder_test.cc` 的 `invalid` helper；Implemented / NOT_RUN（Actual 归 Run 报告）。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->



## 5. 状态、并发与故障测试（条件适用）

<span style="color:#1f6feb"><em>**本节目的**：按模块事实裁决状态、并发与故障测试的适用性；适用路径有可命中的注入点、独立终态判据和安全退出。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：先用模块事实表逐行裁决，不适用必须引用模块设计章节中的事实并给 tailoring 依据，并区分“不适用”与“尚未设计”（后者是 Gap，登记到 §7）；适用时沿 Transition/Invariant ID 选择代表交错：初态如何从公开入口产生、哪个可控调度点或依赖边界触发故障、注入是否命中、迟到事件如何处理、最终状态和资源如何独立观察；允许受控时钟、依赖替身和故障点，禁止直接改业务终态伪造流程通过。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构无状态 FrameDecoder 本章只留两行事实——仅栈变量、无 I/O/取消 → Tailored-N/A；并发只读 → §4 的 UT-DEC-005 已覆盖。虚构有状态提交模块则按 INV 逐行设计注入，样例见本章正文示例。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：适用的状态与故障路径有可命中的注入点、独立终态判据和安全退出；不适用有事实依据。</em></span>

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

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；无状态模块的事实表与不适用写法）**：</span>

| 模块事实（引用设计章节） | 第 5 章最低要求 |
|---|---|
| EX-ISD §7 生命周期：仅栈变量、无队列/线程池/I/O/取消接口 | Tailored-N/A，事实依据如左；无恢复协议可设计，不虚构 |
| FD-R2：并发调用不共享可变状态 | 并发只读交错已由 §4 的 UT-DEC-005 覆盖，不构成恢复协议要求 |

<span style="color:#6e7681">**示例（虚构；有状态提交模块的 Transition 行）**：</span>

| Transition / Invariant ID | 前置事实及可控交错或注入 | Case ID | 独立观测与退出条件 |
|---|---|---|---|
| INV-CMD-1 幂等重放：request_id 已存在不新增执行 | 初态经公开 submit 真实提交一次；结果记录写入前的依赖边界注入一次失败（替身注入计数=1 即命中证明） | UT-CMD-101 | 第二次 submit 返回原 ResultRecord；query(request_id) 读权威记录确认执行数=1；UNKNOWN 禁止新业务重试 |
| INV-CMD-2 事务原子性：两记录同事务 | 证明边界声明：数组 fake 直接返回 SUCCEEDED 不证明原子性；用独立临时 SQLite，无法建立记 Gap 转 BLOCKED | UT-CMD-102 | 注入后经公开 query 检查：或两记录都在、或都不在；无孤立 PENDING |
<!-- STD_TEMPLATE_EXAMPLE_END -->



## 6. 自动化执行与判定

<span style="color:#1f6feb"><em>**本节目的**：提供可复现的自动化入口，并按事实区分失败、阻塞、无效与未运行。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：从全新工作区可复现的构建和测试入口、选择模块或单 Case 的命令、环境前检、超时、退出码、失败现场与清理顺序；PASS/FAIL/BLOCKED/INVALID/NOT_RUN 的判定条件——断言与设计不符是 FAIL，依赖环境缺失是 BLOCKED，故障注入未命中是 INVALID，尚未运行是 NOT_RUN；flaky 不通过重跑覆盖原失败，保存每次 Run 并记录随机种子和调度；覆盖率可辅助发现漏测，但百分比不替代 §2 的设计保证覆盖；单元层微基准按 assurance.test-specification §6 的条件裁剪，不另立性能章。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构教学宿主命令 `c++ -std=c++20 … && ./frame_decoder_test`，退出码 0 且向量输出 PASS 才算成功；并发 Case 若串行执行从未交错记 INVALID 而非 PASS；重跑生成新 run-id 不覆盖原失败。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：自动化入口能复现每个 Case，并按事实区分失败、阻塞、无效与未运行。</em></span>

- 完整执行命令、单 Case 命令与运行位置：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">c++ -std=c++20 … && ./frame_decoder_test；正式 runner 须提供单 Case 过滤</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 期限、退出码、重跑规则与判定：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">退出码 0 且向量 PASS 才算成功；并发未交错记 INVALID；重跑新 run-id 不覆盖失败</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 覆盖率/变异或反例检查（适用时）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">不适用（教学例无覆盖率工具）</span><!-- STD_TEMPLATE_EXAMPLE_END -->




## 7. 证据、报告与未决项

<span style="color:#1f6feb"><em>**本节目的**：定义证据合同与缺口责任，不预填实际结果。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：Run ID、命令和版本、fixture/seed/向量版本、stdout/stderr、断言失败、原始数据及脱敏/保留方式；正式结果在 reports/<run-id>/ 或共置等价目录；逐项登记无法构造的输入、没有独立 Oracle、缺少注入点或上级合同未定等设计缺口，给 Owner、最晚关闭 Gate 和下一步行动；只有实际 Run 报告才能声明执行结果。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构缺口 G-EX-1“上级协议组合测试入口未定义”，阻断 UT-DEC-001–003 的组合责任，Owner=教学样例评审，最晚 Gate=下次样例修订，关闭条件=指定组合测试文档或批准裁剪；关闭前 NOT_RUN 保留。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：Case 能定位 Run 报告与原始证据；未决设计和未执行测试都不被写成 PASS。</em></span>

| 缺口 ID / 关联来源 | 阻断的 Case 或保证 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|---|
| <!-- TODO；无缺口时写经核对的“无” --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：Run 报告位于 `tests/unit/frame_decoder/reports/<run-id>/`（教学例共置），保存完整命令、编译器版本、源文件 hash、stdout 与退出码。</span>

| 缺口 ID / 关联来源 | 阻断的 Case 或保证 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|---|
| G-EX-1 / FD-R1 | 上级协议组合测试入口未定义，UT-DEC-001–003 的组合责任悬空 | 教学样例评审 / 下次样例修订 | 指定组合测试文档，或明示范围外并批准裁剪 |
| G-EX-2 / FD-R2、FD-R4 | 宿主长寿命、权限、脱敏接收链未实现 | 宿主设计 / 后续教学样例 | 宿主入口实现后补组合验证；当前保留 NOT_RUN |
<!-- STD_TEMPLATE_EXAMPLE_END -->



<!-- 交付自查：另一位作者能否从某个来源 ID 找到可执行 Case；从 Case 找到输入、独立 Expected、测试函数及报告路径；从一个失败找到未覆盖范围，而不把单元测试结果提升为系统验证？ -->
