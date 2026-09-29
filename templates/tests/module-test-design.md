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

<span style="color:#1f6feb"><em>**编写建议**：本模板设计整模块组装后的测试。内部单元全部真实参与，模块测试代码默认与单元测试同住 tests/unit/<module>/（MT- 前缀区分）或共置等价路径；Run 报告保存在 reports/<run-id>/。不要把实际运行结果、批准或系统验收结论填进本设计。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。

> 本设计绑定单一软件模块：模块对象 ID 经 `--design-object-id` 写入 metadata；模块设计 ID/版本与源码修订在 §1 固定，测试代码与 Run 报告路径按 §3、§6、§7 登记。

### 模板定位：单元、模块与相邻测试层的边界

<span style="color:#1f6feb"><em>**编写建议**：本模板的被测对象是"整模块组装后的模块"：内部单元全部真实参与，沿模块设计的对外接口（§9）、内部流程（§6/§7）、规则（§8）与状态转换（§10）验证可观察行为。与单元层的分工：单元隔离 Case 权威在 tests.unit-test-design；与契约/集成层的分工：真实依赖两端互操作由契约与集成测试承担，边界替身不证明真实依赖协议；与模块设计的关系：分母消费 §14.1/§14.2 来源 ID 与 VRC，语义以模块设计为唯一权威，Expected 冲突回溯模块设计。已用通用 test-specification 承载模块级 Case 的项目由本设计取代该职能，不得双写；无多单元组装事实时与单元设计合并并 tailoring 记录。本模板不含性能章（按通用规格 §6 裁剪）、执行规程与运行报告。</em></span>

- **权威分工**：整模块组装后的对外接口与内部流程 Case 以本设计为唯一权威；单元隔离归 `tests.unit-test-design`，真实依赖互操作归契约层，系统组合归 integration/system。
- **测试代码位置**：默认与单元测试同住 `tests/unit/<module>/`（同一模块 Owner 命名空间，Case 前缀 `MT-` 与单元 `UT-` 区分），或项目登记的共置等价路径；如 tailoring 分离为独立目录，须记录到模块的映射，不复制同一测试。
- **单元 PASS 不关闭本层**：单元结果不改写为模块结论；本层 PASS 也不关闭契约、集成或系统目标。

### 状态语义：四种状态分开

<span style="color:#1f6feb"><em>**编写建议**：§2 的覆盖记录、§4 的 Case、§6 的判定和 §7 的证据必须能区分下列四种状态；混用任何两种都视为模板违例。与 tests.unit-test-design 使用同一状态语义。</em></span>

| 状态种类 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| Case 设计状态 | `Designed` / `Gap`（具名缺口）/ `Tailored-N/A` | §2 覆盖记录、§4.N | 未设计写成已设计；N/A 无设计事实依据 |
| 测试代码实现状态 | `Planned` / `Implemented` | §4.N 实现位置 | 计划中的测试函数冒充可执行入口 |
| 执行状态 | `NOT_RUN` / `BLOCKED` / `INVALID` | §6、§7 引用的 Run 报告 | 未运行、被阻断或无效的执行计为通过 |
| 实际判定 Verdict | `PASS` / `FAIL` | 仅 Run 报告 | 本设计文档预填 Actual 或 Verdict |

<span style="color:#1f6feb"><em>**完成条件**：任一 Case 能同时报出四种状态且互不矛盾，如 Designed + Implemented + NOT_RUN（无 Verdict）。</em></span>

## 1. 被测模块与测试边界

<span style="color:#1f6feb"><em>**本节目的**：固定“整模块组装后”的被测边界——内部单元全部真实参与、边界外依赖的替代位置、本层不证明的组合保证。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：被测 Module ID、正式名称、父对象与设计基线；把模块装配进测试 harness 的构建目标与装配方式；真实内部单元/文件/组件清单（这是与单元测试的根本区别——内部单元不再替身）；模块边界外的依赖（网络、存储、时钟、下游服务）哪些真实、哪些替身，替身不得证明真实依赖协议；本测试和单元、契约、集成、系统各自承担什么。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 EX-MODULE 组装后直接调用真实 select_ids(records, category)，内部 I1 校验、I2 筛选、I3 排序全部真实参与；本层才能证明“完整校验先于筛选”——只测 I2 的单元测试会漏掉非匹配类别中的重复 ID。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：读者能指出模块构建目标、真实内部组成、边界替代位置，以及本设计不能证明的依赖互操作与系统组合保证。</em></span>

- 被测 Module ID、正式名称、父对象与设计基线：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">EX-MODULE/v1 的 M101 DirectorySelector，父对象 S01，设计基线 EX-MODULE/v1</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 模块构建目标与 harness 装配方式：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">教学单二进制 harness，直接链接 M101 目标</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 真实内部单元与边界外依赖/替身：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">I1 校验、I2 筛选、I3 排序全部真实；边界外无依赖，不引入替身</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 不证明的组合保证及承接测试入口：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">宿主并发准入与输入快照（父设计）、真实存储（本例无 I/O）；承接＝宿主组合验证（G-EX-1）</span><!-- STD_TEMPLATE_EXAMPLE_END -->




## 2. 测试依据与正向覆盖

<span style="color:#1f6feb"><em>**本节目的**：把模块设计的对外接口、内部流程、规则与状态来源 ID 转成模块层覆盖分母；组装后才成立的保证必须落在模块级记录，不下放单元层。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：以模块设计的对外 Interface 成员（含错误出口）、主流程与重要过程、Rule、Transition/Invariant 及适用 Constraint 为分母；一个来源 ID 一条覆盖记录，多个来源可复用同一 Case 但分别写独立判据；不从已写好的测试函数反推分母；每条记录的 Case 设计状态按封面后的状态语义填写；未实现与 NOT_RUN 不从分母删除；不适用须给 tailoring 决定及理由。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 EX-CON-2（每次最多 4096 条）→ 恰好 4096 通过、4097 拒绝 → MT-EXM-003/004；“重复 ID 在非匹配类别仍 INVALID_INPUT”（校验先于筛选）→ MT-EXM-002。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：每个适用来源 ID 都有 Case 或具名缺口；组装后才可观察的保证没有下放给单元层，组合责任没有被本层结果代替。</em></span>

| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|
| <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构；一来源一条记录）**：</span>

| 来源 ID / 固定版本 | 要验证的可观察保证 | Case ID / 缺口 | Case 设计状态 | 上级组合验证入口 |
|---|---|---|---|---|
| EX-CON-1 / EX-MODULE v1 | 输入不可变、整批返回 | MT-EXM-001/002 | Designed | 宿主并发准入（父设计，NOT_RUN） |
| 校验先于筛选（模块设计 §7 流程） | 重复 ID 在非匹配类别仍 INVALID_INPUT | MT-EXM-002 | Designed | —（组装后才可观察，不下放单元层） |
| EX-CON-2 / 同基线 | 每次最多 4096 条：恰好通过、超限拒绝 | MT-EXM-003/004 | Designed | — |
<!-- STD_TEMPLATE_EXAMPLE_END -->



## 3. 环境、夹具、隔离与复位

<span style="color:#1f6feb"><em>**本节目的**：让另一位执行者能独立构建 harness、复位和隔离模块实例，并知道每个边界替身未覆盖的真实行为。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：测试语言/runner 及版本、模块构建目标、运行位置、数据和随机种子、受控时钟或调度器；fixture 优先引用项目 interfaces/vectors/ 的冻结契约向量与 tests/fixtures/ 的可提交输入并固定版本，不在本设计复制向量字节；逐个边界替身写清代替的依赖边界、允许模拟的行为和未证明的性质——替身不证明真实依赖协议、事务或时序；给出 harness setup、前次残留检查、每 Case 复位（模块状态经公开入口复位或重建实例，不直改内部状态）、并行隔离键（模块实例/端口/临时目录）和 teardown；环境无法建立时标 BLOCKED，不静默换环境。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 EX-MODULE harness 直接链接教学 C++ 目标，fixture 为冻结构造记录数组；若模块未来接外部存储，边界 fake 只代替返回值——真实存储的原子性不能在模块层用数组 fake 证明，转契约/集成或记缺口。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：另一位执行者能独立构建 harness、复位和隔离模块实例，并知道每个边界替身未覆盖的真实行为。</em></span>

- Runner、版本、模块构建与运行命令：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">教学 C++ 宿主；无 seed、无受控时钟</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- Fixture / seed / 向量来源及版本：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">冻结构造记录数组（含重复 ID、边界 4096/4097 条）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 边界替身、受控时钟/调度与未覆盖行为：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">本例无替身；若接外部存储，fake 只代返回值，不证明真实存储协议</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- Setup、复位确认、并行隔离和 Cleanup：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">每 Case 新建输入数组天然复位；无并行共享</span><!-- STD_TEMPLATE_EXAMPLE_END -->




## 4. 用例设计

<span style="color:#1f6feb"><em>**本节目的**：把覆盖记录落成模块层逐 Case 设计，编码者不需要猜测测试意图。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：沿“对外接口 × 正常/边界/错误”与“内部流程 × 交错/故障”建立 4.N Case，不堆两份泛泛列表；每例先给被测入口的完整代码式声明（公开 API、命令或事件入口）；逐输入写构造方法、字段/范围、初态和触发动作——状态型初态必须经公开入口构造；逐输出或错误写互斥条件、副作用与终态；Expected 在执行前固定，由独立来源或可手算规则推导，不得调用被测实现复算期望；对边界替身的调用序可作断言，但该断言不证明真实依赖协议；为每例写清可执行测试函数/文件、状态和所需上级组合用例。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 Case MT-EXM-002：select_ids(records, category) 输入两条同 ID 记录且类别均不匹配目标，Expected=INVALID_INPUT、整批拒绝、输入逐字节不变——校验先于筛选，手算依据模块校验规则，不调用 select_ids 复算。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：每个 Case 可按输入、调用、独立 Expected 和失败出口实施，不需要编码者猜测测试意图。</em></span>

### 4.N `MT-<MODULE>-<NNN>` · <对外接口或内部流程与条件>

<span style="color:#1f6feb"><em>**编写建议**：一个 Case 一个小节，标题为 `MT-<MODULE>-<NNN>` 加对外接口或内部流程与条件；按下列槽位逐项填写，状态型初态必须经公开入口构造，状态按封面后的状态语义分列。</em></span>

- **来源 ID / 被测行为 / 适用基线**

  <!-- TODO：写来源版本、接口成员或流程，不复制第二份权威定义。 -->

- **被测接口声明与输入构造**

  ```text
  <真实公开入口签名>
  ```

  <!-- TODO：每个输入参数单独描述类型、取值、fixture、初态；状态型初态说明经哪个公开入口形成。 -->

- **执行、观察点与独立 Oracle**

  <!-- TODO：写实际调用或事件、观测对象（公开返回、公开查询或权威记录）、Expected 的独立推导、允许误差或精确比较方法。 -->

- **成功、错误、副作用与清理判据**

  <!-- TODO：写互斥返回/异常、错误字段、边界副作用；失败时确认没有半成品或错误释放。 -->

- **实现位置、自动化入口与状态**

  <!-- TODO：tests/unit/<module>/ 下的测试文件与测试名（MT- 前缀）。按封面后的状态语义分列：实现状态 Planned/Implemented；执行状态 NOT_RUN/BLOCKED/INVALID；PASS/FAIL 只出现在 Run 报告。 -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
### 4.1 `MT-EXM-002` · 校验先于筛选（虚构示例）

<span style="color:#6e7681">- **来源 ID / 被测行为 / 适用基线**</span>

<span style="color:#6e7681">  模块设计 §7 流程 / EX-MODULE v1：完整校验必须先于筛选，非匹配类别中的重复 ID 也要检出。</span>

<span style="color:#6e7681">- **被测接口声明与输入构造**</span>

  ```text
<span style="color:#6e7681">  select_ids(records: span<const Record>, category: Category) -> vector<Id> | InvalidInput</span>
  ```

<span style="color:#6e7681">  `records`：两条同 ID 记录，类别均不匹配目标 `category`（冻结向量）。</span>

<span style="color:#6e7681">- **执行、观察点与独立 Oracle**</span>

<span style="color:#6e7681">  单次调用；观察返回变体与输入字节。Expected=InvalidInput、整批拒绝、输入逐字节不变——按校验规则人工判定，不调用 select_ids 复算。</span>

<span style="color:#6e7681">- **成功、错误、副作用与清理判据**</span>

<span style="color:#6e7681">  仅 InvalidInput 分支；无部分结果；无需清理。对照 Case：合法且无重复输入返回确定顺序 IDs（MT-EXM-001）。</span>

<span style="color:#6e7681">- **实现位置、自动化入口与状态**</span>

<span style="color:#6e7681">  教学 harness 的 invalid 输入段；Implemented / NOT_RUN。</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->



## 5. 状态、并发与故障测试（条件适用）

<span style="color:#1f6feb"><em>**本节目的**：按模块事实裁决状态、并发与故障测试的适用性；模块级的特点是内部单元真实、交错由真实并发或受控时钟驱动、故障注入落在模块边界。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：先按模块事实表逐行裁决适用性，不适用必须引用模块设计章节中的事实并给 tailoring 依据，并区分“不适用”与“尚未设计”（后者是 Gap，登记到 §7）；适用时沿 Transition/Invariant ID 选择代表交错；故障注入落在模块边界（依赖错误、超时、乱序、重复、迟到事件）且必须有命中证明（替身注入计数或可观察的边界事件）；初态经公开入口构造；终态经公开查询或权威记录独立观察，不直改内部状态伪造流程通过；同步只读模块不虚构恢复协议，但并发只读交错仍按 §4 覆盖。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构异步导出模块：完成通知前经受控时钟注入取消，终态走公开 status 与产物目录观察；完整行见本章正文示例。</em></span>

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
<span style="color:#6e7681">**示例（虚构；无状态模块的事实表写法）**：</span>

| 模块事实（引用设计章节） | 第 5 章最低要求 |
|---|---|
| EX-MODULE §10：同步只读、无跨调用状态、无 I/O/线程/取消 | Tailored-N/A，事实如左；不设计恢复协议 |
| EX-CON-1：输入不可变 | 并发只读交错按 §4 覆盖（两线程同输入只读），不构成恢复协议要求 |

<span style="color:#6e7681">**示例（虚构；有状态异步导出模块的 Transition 行）**：</span>

| Transition / Invariant ID | 前置事实及可控交错或注入 | Case ID | 独立观测与退出条件 |
|---|---|---|---|
| 状态转换：提交→执行→完成/取消 | 初态经公开 submit 构造；受控时钟推进执行阶段；完成通知前注入取消 | MT-EXP-101 | 公开 status 查询终态=已取消且无残留产物；句柄释放 |
| 迟到完成不复活任务 | 取消后受控时钟送达完成事件 | MT-EXP-102 | status 仍为已取消；迟到结果被拒绝且可观察，不写半成品文件 |
| 边界依赖故障：存储写入失败 | 存储替身注入一次写错误（注入计数=1 为命中证明） | MT-EXP-103 | 终态=失败且错误字段指明存储；无部分文件残留；替身不证明真实存储协议 |
<!-- STD_TEMPLATE_EXAMPLE_END -->



## 6. 自动化执行与判定

<span style="color:#1f6feb"><em>**本节目的**：提供含模块组装步骤的可复现自动化入口，并按事实区分失败、阻塞、无效与未运行。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：从全新工作区可复现的构建（含模块组装目标）和测试入口、选择模块或单 Case 的命令、环境前检、超时、退出码、失败现场与清理顺序；PASS/FAIL/BLOCKED/INVALID/NOT_RUN 的判定条件——断言与设计不符是 FAIL，依赖环境缺失是 BLOCKED，边界故障注入未命中是 INVALID，尚未运行是 NOT_RUN；flaky 不通过重跑覆盖原失败，保存每次 Run 并记录随机种子和调度；覆盖率可辅助发现漏测，但百分比不替代 §2 的设计保证覆盖；模块级性能断言按 assurance.test-specification §6 的条件裁剪，不另立性能章。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构组装目标 `c++ … module_harness.cc` 全量执行，单 Case 用 runner 过滤参数选择；边界注入计数=0 记 INVALID 而非 PASS；组装失败或环境缺失记 BLOCKED。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：自动化入口能复现每个 Case（含模块组装步骤），并按事实区分失败、阻塞、无效与未运行。</em></span>

- 完整执行命令（含组装）、单 Case 命令与运行位置：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">c++ … module_harness.cc 全量执行；正式 runner 用过滤参数选单 Case</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 期限、退出码、重跑规则与判定：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">边界注入计数=0 记 INVALID；组装失败记 BLOCKED；重跑新 run-id 不覆盖失败</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 覆盖率/变异或反例检查（适用时）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">不适用（教学例）</span><!-- STD_TEMPLATE_EXAMPLE_END -->




## 7. 证据、报告与未决项

<span style="color:#1f6feb"><em>**本节目的**：定义证据合同与缺口责任，不预填实际结果。</em></span>

<span style="color:#1f6feb"><em>**必须写清楚**：Run ID、命令和版本、fixture/seed/向量版本、stdout/stderr、断言失败、原始数据及脱敏/保留方式；正式结果在 reports/<run-id>/ 或共置等价目录；逐项登记无法构造的输入、没有独立 Oracle、缺少注入点或上级合同未定等设计缺口，给 Owner、最晚关闭 Gate 和下一步行动；只有实际 Run 报告才能声明执行结果，模块层 PASS 不关闭契约、集成或系统目标。</em></span>

<span style="color:#1f6feb"><em>**抽象示例**：虚构 G-EX-1“宿主并发准入组合入口未定义”阻断宿主并发结论，Owner=父设计，最晚 Gate=子系统评审；模块层各 Run 保存在 reports/<run-id>/，计划与设计均不得预填结果。</em></span>

<span style="color:#1f6feb"><em>**完成条件**：Case 能定位 Run 报告与原始证据；未决设计和未执行测试都不被写成 PASS。</em></span>

| 缺口 ID / 关联来源 | 阻断的 Case 或保证 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|---|
| <!-- TODO；无缺口时写经核对的"无" --> | | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">**示例（虚构）**：Run 报告位于 `tests/unit/directory_selector/reports/<run-id>/`（教学例共置），保存组装命令、编译器版本、源 hash、stdout 与退出码。</span>

| 缺口 ID / 关联来源 | 阻断的 Case 或保证 | Owner / 最晚 Gate | 关闭所需事实或决定 |
|---|---|---|---|
| G-EX-1 / 宿主并发准入 | 宿主并发场景的组合结论悬空 | 父设计 / 子系统评审 | 父设计定义并发准入入口后补组合验证；当前 NOT_RUN 保留 |
<!-- STD_TEMPLATE_EXAMPLE_END -->



<!-- 交付自查：另一位作者能否从某个来源 ID 找到可执行 Case；从 Case 找到输入、独立 Expected、测试函数及报告路径；从一个失败找到未覆盖范围，而不把模块测试结果提升为契约或系统验证？ -->
