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

<!--
编写建议：本模板解释数据的业务语义和 ownership；字段类型的机器权威仍是 Schema/IDL。
至少为关键对象给出一条合法示例和一条非法示例。示例值提交前必须替换。
编写规范见 docs/design-writing-guide.md。
-->

## 1. 用途、范围与 authority

<!-- 编写建议：先说明本文解释哪些对象的业务含义、哪些歧义会影响实现，以及唯一 Schema/IDL 的路径和固定版本。数据字典是阅读视图，不改写机器字段；用一条真实业务事件说明这些对象何时产生和何时失效。 -->

说明谁生产和消费这些数据、解决什么歧义，以及对应机器契约的位置。

## 2. 命名、单位与通用规则

<!-- 编写建议：只列全篇反复使用且具有约束力的命名、单位、时间、编码和未知值规则，注明每条规则的来源与适用范围。例子中的容量必须区分 GB 与 GiB；不同边界使用不同单位时写明转换和舍入方法。 -->

| Rule | Requirement | Example |
|---|---|---|
| 时间 | ISO 8601 UTC | `2026-09-09T08:30:00Z` |
| 容量 | 明确 SI 或 binary unit | `512 GiB` |
| ID | 稳定、不可复用 | `doc_01H...` |

## 3. 数据结构设计

<details>
<summary>本章编写建议</summary>


本章是受控字段的阅读视图，不另建数据结构清单，也不拥有操作接口。先按数据性质选择实际适用的类别；每个真实结构以 Data/Type ID 和名称为小节标题，在同一处写完定义、字段、约束、身份、所有权、寿命、合法与拒绝实例及验证。已有 Schema/IDL/头文件等机器来源时固定版本与 selector，并逐字段核对；没有机器来源时标 Proposed、Owner 与形成契约的 Gate，不把草案冒充已可实现的字段权威。

八类入口不是八类都必须填写。项目不适用的类别在本章开头记录理由和 tailoring 决定，成文时删除空类别。以下字段槽位按实际类型展开；状态比较、关系图和转换矩阵可以放在 §4–§7，但不得在那里重新定义同一字段。

</details>

每个结构使用同一固定记录：

- **Data/Type ID、结构名、用途及唯一来源**：机器源路径、版本/revision/hash、selector；或 Proposed 决定引用。
- **完整字段/值定义**：逐字段 ID、名称、类型/引用、必填/可空、单位、范围、枚举、默认值、条件有效性及业务含义；实际二进制/RTL 边界补位宽、端序、对齐与复位值。
- **结构约束**：键、跨字段不变量、未知值与兼容规则；说明生产、修改、唯一写者、可见点、所有权和寿命。
- **实例与验证**：一条完整合法实例和一条边界或拒绝实例，Expected、独立判据、V/Case 及实际证据状态。

### 3.1 公共基础类型与枚举（适用时）

<details>
<summary>本节编写建议</summary>

只定义本文确实拥有的基础类型或枚举；已由公共契约定义的值按原 ID 和固定来源引用。逐值说明含义、范围、保留值与未知值处理，不能把同名但语义不同的状态合并。例：`InspectionState.RUNNING` 仅表示检测已开始，不表示业务结果已完成。

完成检查：读者可从任一值找到唯一机器定义、适用边界和拒绝行为。

</details>

#### 3.1.N `<Data/Type ID> · <真实类型名>`

按本章固定记录填写；逐枚举值补合法/保留/未知值规则。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.1.1 `InspectionState`（公共状态枚举，虚构）**

```text
enum InspectionState { ACCEPTED, RUNNING, SUCCEEDED, FAILED }
```

- **Data/Type ID、含义与来源**：

  `DATA-EX-STATE`；一次检测任务的权威业务状态。示例机器源为 `Proposed: InspectionState`；正式设计须给出实际 Schema/IDL 路径、版本和核对结果，或记录形成契约的 Owner 与 Gate。

- **逐值定义**：

  `ACCEPTED`＝已受理但尚未执行；`RUNNING`＝已开始执行但无最终结果；`SUCCEEDED`＝结果已发布；`FAILED`＝执行终止且未发布成功结果。未知值拒绝，不映射为 `FAILED`。

- **约束与生命周期**：

  状态键为 `task_id`；只有任务状态的权威持有者可改变值，发布后读者才可观察。`RUNNING → SUCCEEDED` 必须已有可定位的结果；终态不得再回到 `RUNNING`。任务保留期限由系统级策略决定，此例不虚构期限。

- **合法/拒绝实例**：

  已发布结果 `result_id=res-7` 后置 `SUCCEEDED` 合法；只有执行开始记录、没有结果时置 `SUCCEEDED` 必须拒绝。

- **验证**：

  设计向量 `V-EX-STATE-01` 检查终态前提和未知值拒绝；本例 `NOT_RUN`，不表示验证通过。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.2 业务与操作数据结构（适用时）

<details>
<summary>本节编写建议</summary>

以真实业务对象或操作载荷为单位写一份完整定义，不按输入和输出重复建类型。说明字段如何共同表达一次业务事实、哪些组合无效，以及何时产生或失效。例：`InspectionRequest` 的 `request_id` 非空且代表一次业务操作。

完成检查：接口签名中的类型名能直接定位到本节的完整字段、约束与实例。

</details>

#### 3.2.N `<Data/Type ID> · <真实结构名>`

按本章固定记录填写；逐字段补业务含义及跨字段约束。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.2.1 `InspectionRequest`（业务对象，虚构）**

```text
InspectionRequest {
  request_id: string,
  image_uri: string,
  policy_version: uint32
}
```

- **Data/Type ID、用途与来源**：

  `DATA-EX-REQUEST`；代表一次待受理的检测请求，示例机器源为 `Proposed: InspectionRequest`。正式项目需绑定实际类型定义和固定版本。

- **`request_id`**：

  必填、非空字符串，作为同一业务请求的稳定身份；实际编码及长度上限由 Schema 确定。

- **`image_uri`**：

  必填、非空字符串，指向待检图像而非图像字节副本；URI 方案和访问权限由图像存储契约确定。

- **`policy_version`**：

  必填、正整数，指定本次请求采用的已发布规则版本。

- **跨字段与寿命**：

  同一 `request_id` 重放时，`image_uri` 与 `policy_version` 必须保持一致；冲突值不得创建第二任务。受理方创建任务记录后保留请求身份；原图的所有权与释放期限另由图像存储契约决定。

- **合法/拒绝实例**：

  `{request_id:"req-7", image_uri:"asset://image/7", policy_version:3}` 在引用和版本均存在时合法；同一 `request_id` 携带另一个图像 URI 应拒绝并返回已定义的冲突错误。

- **验证**：

  `V-EX-REQUEST-01` 覆盖合法构造、缺字段和同 ID 冲突；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.2.2 `InspectionSubmission`（受理结果，虚构）**

```text
InspectionSubmission {
  request_id: string,
  task_id: string,
  disposition: ACCEPTED | EXISTING
}
```

- **Data/Type ID、用途与来源**：

  `DATA-EX-SUBMISSION`；表示请求已受理或同请求重放找到了原任务，不表示检测已经完成。示例机器源为 `Proposed: InspectionSubmission`。

- **`request_id`**：

  必填，等于输入 `InspectionRequest.request_id`；用于把响应绑定到原请求。

- **`task_id`**：

  必填、非空；`ACCEPTED` 指向本次新建任务，`EXISTING` 指向相同请求身份下已存在的原任务。

- **`disposition`**：

  必填；`ACCEPTED` 表示首次受理，`EXISTING` 表示同一请求内容重放且未新增执行；未知值拒绝。

- **约束与生命周期**：

  受理责任单元在任务身份持久确定后构造结果；响应丢失时仍可凭原 `request_id` 查询。任务何时完成由 §3.1 的 `InspectionState` 表达，不能从 `InspectionSubmission` 推断成功检测。

- **合法/拒绝实例**：

  `{request_id:"req-7", task_id:"t-7", disposition:ACCEPTED}` 在确实新建 `t-7` 后合法；没有持久任务身份却返回 `ACCEPTED` 必须拒绝。

- **验证**：

  `V-EX-SUBMISSION-01` 检查首次受理、同请求重放、响应丢失后查询和无重复任务；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.3 配置与规则数据结构（适用时）

<details>
<summary>本节编写建议</summary>

定义配置字段、来源、默认值的批准依据、版本、校验及生效点。区分保存成功、发布成功与运行目标实际使用，不在数据字典里自创新的配置 fallback。例：`DetectionPolicy.threshold` 只对新受理任务生效，旧任务保留原快照。

完成检查：错误配置可以被明确拒绝，读者知道值对哪个对象、从何时开始生效。

</details>

#### 3.3.N `<Data/Type ID> · <真实配置或规则名>`

按本章固定记录填写；补版本、作用域、校验和生效条件。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.3.1 `config/inspection-policy.yaml`（配置文件，虚构）**

```yaml
schema_version: 1
policy_version: 3
enabled: true
score_threshold: 0.75
```

- **Data/Type ID、用途与来源**：

  `DATA-EX-POLICY-FILE`；这是一份决定检测任务是否准入及其判定阈值的 YAML 文件，不是单独的内存对象。示例路径和内容均为虚构；真实项目须指定受控文件路径、唯一配置 Schema、版本及部署责任方。

- **`schema_version`**：

  必填整数，本例只接受 `1`；用于选择文件格式，未知版本拒绝加载。

- **`policy_version`**：

  必填正整数，标识本次加载的规则版本；发布后不复用。

- **`enabled`**：

  必填布尔值；`false` 表示不受理新的检测任务，不改变既有任务的终态。

- **`score_threshold`**：

  必填数值，闭区间 `[0, 1]`，单位为无量纲得分；`enabled=false` 时仍须通过格式校验，避免下次启用时读取无效值。

- **文件级约束与生效**：

  本例由进程在启动时读取并整份校验；缺字段、重复键、未知键、类型错误或越界值均使启动失败，不静默使用默认值。启动成功后进程固定一份已校验快照；编辑磁盘文件不会热更新，只有按启动过程重启并确认新版本后才生效。运行中任务的恢复规则由系统恢复设计决定。

- **合法/拒绝实例**：

  上面的完整文件在受控路径且通过 Schema 校验时合法；将 `score_threshold` 改为 `1.2` 或增加未知键 `fallback_mode` 时必须拒绝整份文件，不能部分采用。

- **验证**：

  `V-EX-POLICY-FILE-01` 覆盖完整加载、缺字段/未知键/越界拒绝、修改文件但未重启时版本不变；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.4 通信报文结构（适用时）

<details>
<summary>本节编写建议</summary>

逐消息、事件、流或文件载荷说明字段、编码、关联身份、顺序标识和兼容边界；投递、确认、重试等操作行为仍由接口定义。例：`FrameReadyEvent` 包含 `frame_id` 与来源内递增的 `sequence`。

完成检查：双方能按同一机器来源解码，且迟到、重复或未知字段有确定处理。

</details>

#### 3.4.N `<Data/Type ID> · <真实报文名>`

按本章固定记录填写；补编码、长度/计数来源和版本兼容。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.4.1 `FrameReadyEvent`（通信报文，虚构）**

| 报文内 bit 位置 | 0–15 | 16–23 | 24–31 | 32–63 | 64–127 | 128–191 | 192–255 |
|---|---|---|---|---|---|---|---|
| 字段 | `magic` | `version` | `flags` | `source_id` | `frame_id` | `sequence` | `image_ref_id` |
| 类型 | `u16` | `u8` | `u8` | `u32` | `u64` | `u64` | `u64` |

图 EX-DATA-4 · `FrameReadyEvent` 的线传布局；表格从左到右为报文顺序，编号为从报文起始位置计算的 bit offset。图仅展示虚构教学格式，不是项目的机器权威。该固定报文共 256 bit／32 byte，多字节整数字段按网络字节序（大端）编码；没有隐含填充或可变长尾部。

- **Data/Type ID、用途与来源**：

  `DATA-EX-FRAME-EVENT`；通知采集图像已可读取。示例机器源为 `Proposed: FrameReadyEvent`；正式项目须固定消息 Schema、版本和实际传输绑定，不从图推导 topic 或部署事实。

- **`magic`（bit 0–15）**：

  必填 `u16`，固定值 `0xA55A`；不匹配则按格式错误拒绝，不继续解析其他字段。

- **`version`（bit 16–23）**：

  必填 `u8`，本教学格式仅接受 `1`；未知版本拒绝，不猜测字段兼容。

- **`flags`（bit 24–31）**：

  必填 `u8`，本版必须为 `0`；非零保留位拒绝。

- **`source_id`（bit 32–63）**：

  必填 `u32`，非零，标识采集来源。

- **`frame_id`（bit 64–127）**：

  必填 `u64`，非零，标识该来源的一帧。

- **`sequence`（bit 128–191）**：

  必填 `u64`，非零，在同一来源内递增；不得据此跨来源排序，耗尽前须停止该来源的新报文而非回绕复用。

- **`image_ref_id`（bit 192–255）**：

  必填 `u64`，非零，引用该来源已发布且可读取的图像；引用的解析与授权由图像存储契约确定，报文本身不携带图像字节。

- **约束与寿命**：

  `(source_id, sequence)` 是去重键；同键不同 `frame_id` 或 `image_ref_id` 为冲突。报文只在图像可读取后发布；事件被消费不等于图像资源可删除。传输确认、重试和背压属于对应接口，不在此重复定义。

- **合法/拒绝实例**：

  `magic=0xA55A, version=1, flags=0, source_id=2, frame_id=7, sequence=42, image_ref_id=9` 按图编码为 32 byte 且引用已发布图像时合法；将 `flags` 改为 `1` 或同键改用另一个 `image_ref_id` 应拒绝，不覆盖原记录。

- **验证**：

  `V-EX-FRAME-01` 覆盖逐字段编码/解码、长度与端序、版本/保留位拒绝、重复与冲突报文；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.5 设备与 FPGA 表项结构（适用时）

<details>
<summary>本节编写建议</summary>

只记录真实存在的寄存器、描述符或 RTL 表项。引用固定 register map/RTL 来源，逐字段写位宽、复位值、读写权限、写入确认和生效条件；纯软件项目不得为填模板虚构硬件布局。

完成检查：驱动和 RTL 能按同一布局解释数据，错误指示可追到负责转换的边界。

</details>

#### 3.5.N `<Data/Type ID> · <真实表项名>`

按本章固定记录填写；补位域、时钟/复位及读写副作用。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.5.1 `CaptureStatusRegister`（设备寄存器，虚构）**

假设设备暴露一个 `CAPTURE_MMIO` 控制地址空间。下表偏移均相对该地址空间基址；基址由实际平台分配，不在本例编造物理地址。所有寄存器均按 32-bit 对齐、小端字节序访问；不支持非对齐或非 32-bit 访问。未列出的偏移为保留区，访问返回总线拒绝，不得作为兼容扩展的隐式空间。

| 偏移 | 寄存器名称 | 宽度/访问 | 复位或初值 | 用途与访问副作用摘要 |
|---|---|---|---|---|
| `0x00` | `CAP_ID` | 32-bit / RO | `0x43415031` | 设备身份常量 `CAP1`；读取无副作用，不表示设备已就绪。 |
| `0x04` | `CAP_VERSION` | 32-bit / RO | `0x00010000` | 高 16 位主版本、低 16 位次版本；软件先核对兼容范围。 |
| `0x10` | `CAP_CONTROL` | 32-bit / RW | `0x00000000` | 受控启停入口；写入可能触发动作，不能按普通内存变量处理。 |
| `0x20` | `CAP_STATUS` | 32-bit / RO | `0x00000000` | 本例下方完整展开的状态寄存器；原子读取，无读清副作用。 |
| `0x24` | `CAP_FRAME_COUNT` | 32-bit / RO | `0x00000000` | 已完成帧数；达到最大值后饱和，设备复位时清零。 |
| `0x28` | `CAP_DROPPED_COUNT` | 32-bit / RO | `0x00000000` | 因输入溢出而丢弃的帧数；达到最大值后饱和，设备复位时清零。 |
| `0x2C` | `CAP_IRQ_STATUS` | 32-bit / RW1C | `0x00000000` | 中断状态；读取得到当前锁存位，写 `1` 清对应位，写 `0` 不改变该位。 |

此表只示范**寄存器列表**的覆盖方式，不是其余六个寄存器的完整字段定义。真实设计应为 `CAP_CONTROL`、`CAP_IRQ_STATUS` 等每个实际使用的寄存器另设同名小节，固定具体位域、合法写序列、清除时机、并发及异常行为；若下级 register map/RTL 是机器权威，本表须从同一固定基线生成或逐项核对。

| 寄存器逻辑位 | 31–3 | 2 | 1 | 0 |
|---|---|---|---|---|
| 字段 | `reserved` | `overflow` | `busy` | `ready` |

图 EX-DATA-5A · 表格从左到右是寄存器高位到低位，表头直接给出逻辑位编号；位域布局不表示总线的字节传输顺序。本例假设设备寄存器空间偏移 `0x20`、32-bit 对齐访问、小端字节序；均为虚构教学条件。

- **Data/Type ID、用途与来源**：

  `DATA-EX-CAPTURE-STATUS`；供控制单元读取采集状态。示例机器源为 `Proposed: CaptureStatusRegister`；正式设计须用固定版本 register map/RTL 逐位核对。

- **`reserved`（bit 31–3）**：

  只读，复位和正常读取均为零；读到非零视为格式/版本不匹配，不按已知字段解释。

- **`overflow`（bit 2）**：

  只读、复位值 `0`；发生输入溢出后锁存为 `1`，本教学例子中只在设备复位时清零。

- **`busy`（bit 1）**：

  只读、复位值 `0`；采集操作正在进行时为 `1`。

- **`ready`（bit 0）**：

  只读、复位值 `0`；初始化完成且可接收新操作时为 `1`。`ready` 与 `busy` 不得同时为 `1`。

- **访问与生命周期**：

  一次 32-bit 读取返回同一时刻的原子快照；写此只读地址返回总线拒绝，不改变状态。复位全零不等于已经就绪；何时从复位进入 `ready=1` 由设备启动过程定义。

- **合法/拒绝实例**：

  读取 `0x00000001` 表示就绪且不忙；`0x00000003` 同时声明就绪与忙，违反不变量，控制单元须报告设备状态异常，不能凭其中一个位继续执行。

- **验证**：

  `V-EX-REGISTER-01` 覆盖复位值、位域、只读拒写、原子读取和互斥状态；本例 `NOT_RUN`，不代表 RTL 仿真或上板结果。

<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.5.2 `RouteTableEntry`（FPGA 数据表项，虚构）**

| 表项逻辑位 | 15–12 | 11–0 |
|---|---|---|
| 字段 | `target` | `route_id` |

图 EX-DATA-5B · 表格从左到右是表项高位到低位，表头直接给出逻辑位编号。本例假设 `route_table[0..63]` 共 64 项，基址偏移 `0x100`，每项占 2 byte、步长 2 byte；第 `i` 项位于 `0x100 + 2i`。16-bit 表项按小端字节序读写，图不是字节传输时序。

- **Data/Type ID、用途与来源**：

  `DATA-EX-ROUTE`；表项给 FPGA 路由查找提供目标。示例布局为 `Proposed`；真实设计须以固定版本 RTL/register map 为机器权威，逐位核对容量、地址和生效规则。

- **`target`（bit 15–12）**：

  无符号 4 位，范围 0–15，选择输出目标。

- **`route_id`（bit 11–0）**：

  无符号 12 位，运行有效值 1–4095；`0` 表示空项，不参加有效路由查找。

- **索引、约束与生命周期**：

  表索引为 0–63，索引与 `route_id` 是不同概念；复位后 64 项全零。只有获授权的控制单元可在停止路由查找后以 16-bit 原子写入表项，硬件写入确认后，重新启动的查找才采用新值；在途查找不得混用旧新值。停止/确认/重启的调用条件由表项写入接口定义，本节只固定数据布局和生效边界。

- **合法/拒绝实例**：

  索引 `5` 写入 `target=2, route_id=7`，逻辑值为 `0x2007`、小端字节为 `07 20`，重启查找后有效；`target=2, route_id=0` 不可作为有效路由，读取时应按空项处理，不能把它当作已配置目标。

- **验证**：

  `V-EX-ROUTE-01` 覆盖地址步长、大小端编码、复位空项、无效值和写入后生效边界；本例 `NOT_RUN`，不代表 FPGA 仿真或上板结果。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.6 运行状态数据结构（适用时）

<details>
<summary>本节编写建议</summary>

定义跨步骤保留的状态字段、唯一写者、允许转移、可见点和恢复事实；状态名称不能代替进入条件。区分内存态、持久态和派生视图，说明并发观察到旧值时如何解释。

完成检查：正常、失败及重启路径都能定位哪个状态有效，且不会出现两个未裁决的权威写者。

</details>

#### 3.6.N `<Data/Type ID> · <真实状态结构名>`

按本章固定记录填写；补转移条件、持久/易失边界及恢复证据。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.6.1 `InspectionRuntimeState`（运行状态，虚构）**

```text
InspectionRuntimeState {
  task_id: string,
  generation: uint32,
  state: InspectionState,
  result_uri: string?
}
```

- **Data/Type ID、用途与来源**：

  `DATA-EX-RUNTIME`；表示一项任务当前权威状态。示例机器源为 `Proposed: InspectionRuntimeState`；`InspectionState` 指向 §3.1 的同名教学类型，真实项目须改用自己的唯一来源。

- **`task_id`**：

  必填、非空字符串，作为任务状态键。

- **`generation`**：

  必填、正整数，标识该任务状态的更新代次。

- **`state`**：

  必填，取 §3.1 `InspectionState` 的已定义值。

- **`result_uri`**：

  可空字符串，仅在 `SUCCEEDED` 时必填，其他状态必须为空；URI 方案由结果存储契约确定。

- **约束与生命周期**：

  任务状态持有者是唯一写者，更新以 `(task_id, generation)` 防止旧完成覆盖新状态。状态读者可见点是权威更新提交后；进程内副本可失效，但不得将其直接当作持久事实。保留与恢复规则由系统策略明确。

- **合法/拒绝实例**：

  `{task_id:"t-7", generation:2, state:SUCCEEDED, result_uri:"result://7"}` 在结果已发布时合法；`state:SUCCEEDED, result_uri:null` 必须拒绝。

- **验证**：

  `V-EX-RUNTIME-01` 覆盖终态不变量和旧代次更新拒绝；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.7 数据库表结构（适用时）

<details>
<summary>本节编写建议</summary>

仅定义本文实际拥有的持久表；外部数据库引用其唯一 Schema。逐列写类型、键、索引、约束与版本，说明事务提交点、崩溃恢复、旧版数据转换和删除传播。例：受理返回前必须完成约定的 `inspection_jobs` 提交。

完成检查：读者能判断冲突、迁移中断与不可读旧库的处理，不以“有表”代替持久保证。

</details>

#### 3.7.N `<Data/Type ID> · <真实表名>`

按本章固定记录填写；补键/索引、事务边界及迁移版本。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.7.1 `inspection_jobs`（数据库表，虚构）**

```sql
CREATE TABLE inspection_jobs (
  task_id TEXT PRIMARY KEY,
  generation INTEGER NOT NULL CHECK (generation >= 1),
  state TEXT NOT NULL,
  result_uri TEXT NULL,
  CHECK ((state = 'SUCCEEDED' AND result_uri IS NOT NULL)
      OR (state <> 'SUCCEEDED' AND result_uri IS NULL))
);
```

- **Data/Type ID、用途与来源**：

  `DATA-EX-JOBS-TABLE`；保存任务的可恢复事实，示例 DDL 状态为 `Proposed`。真实系统须以受控迁移文件/Schema 的固定版本为机器权威，并说明数据库产品与约束支持情况。

- **`task_id`**：

  非空主键，对应任务身份。

- **`generation`**：

  正整数，用于防止旧更新覆盖。

- **`state`**：

  非空，采用 §3.1 枚举的持久编码；实际编码映射须固定。

- **`result_uri`**：

  可空，仅在成功终态非空。此例没有声称存在查询索引，真实查询路径应决定索引。

- **事务与生命周期**：

  唯一写入责任单元在承诺“任务已受理”前提交首条记录；状态与结果引用在同一事务中更新。崩溃后以已提交行恢复，不以页面缓存推断提交。保留期限、删除权限和数据迁移版本必须由项目确定。

- **合法/拒绝实例**：

  `('t-7', 2, 'SUCCEEDED', 'result://7')` 在结果已发布时合法；`('t-8', 1, 'SUCCEEDED', NULL)` 违反约束，应拒绝且不得提交部分终态。

- **验证**：

  `V-EX-JOBS-01` 覆盖约束拒绝、提交失败与崩溃恢复；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

### 3.8 错误码与错误结构（适用时）

<details>
<summary>本节编写建议</summary>

系统公共错误沿用系统设计逐码定义及机器来源；本词典只解释其数据视图，不重新分配码值或改变调用方动作。私有异常单独标范围，越过系统边界前必须映射。逐码说明唯一含义、触发事实、载荷、结果状态、未知码行为与验证。

完成检查：接口失败出口引用存在的 Error ID，同码异义和未定义错误不能进入交付。

</details>

#### 3.8.N `<Data/Type/Error ID> · <真实错误名>`

按本章固定记录填写；公共码引用系统来源，私有码注明映射边界。

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.8.1 `InspectionErrorCode`（公共错误码枚举，虚构）**

```text
enum InspectionErrorCode { INVALID_REQUEST, REQUEST_CONFLICT, PERMISSION_DENIED, QUEUE_FULL }
```

- **Data/Type/Error ID、来源**：

  枚举 `DATA-EX-ERROR-CODE`；各值分别为 `ERR-EX-INVALID-REQUEST`、`ERR-EX-REQUEST-CONFLICT`、`ERR-EX-PERMISSION-DENIED`、`ERR-EX-QUEUE-FULL`。示例机器源为 `Proposed: InspectionErrorCode`。正式项目须固定实际 Error enum/Schema 的代码值、版本和核对结果，不把教学名称当作已分配码。

- **`INVALID_REQUEST`**：

  必填字段缺失、值不合法或引用不可读取；校验在创建任务前结束，调用方修正输入，不得原样重试。

- **`REQUEST_CONFLICT`**：

  已有相同 `request_id`，但图像或规则版本不同；不创建第二任务，调用方核对原请求身份，不得换 ID 绕过冲突。

- **`PERMISSION_DENIED`**：

  当前身份无权提交该请求；在创建任务前拒绝，调用方取得授权后才可重新提交。

- **`QUEUE_FULL` 的含义与边界**：

  受理队列达到确定上限，本次请求未受理且未创建任务；不表示已受理任务执行失败，也不表示结果未知。其他未知码不得擅自映射为 `QUEUE_FULL`。

- **触发、结果与副作用**：

  权限与输入校验先于冲突和容量判定；受理责任单元在入队前依据权威队列容量事实判定 `QUEUE_FULL`。以上错误均不得创建新任务或占用其执行资源；仅 `QUEUE_FULL` 可在接口规定的期限内按同一请求身份重试，不能把重试理解为已有任务恢复。

- **下级承接与载荷**：

  受理模块产生这些码，边界适配模块可透传，界面按错误码提示修正、授权、核对原请求或稍后重试；错误响应使用下方同节定义的 `InspectionError`，其中 `task_id` 必须为空。

- **合法/拒绝实例与验证**：

  队列满且无新任务时返回 `QUEUE_FULL` 合法；任务已创建却返回此码必须拒绝。`V-EX-QUEUE-01` 核对触发事实、错误码和无副作用，本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
**3.8.2 `InspectionError`（错误载荷结构，虚构）**

```text
InspectionError {
  code: InspectionErrorCode,
  request_id: string?,
  task_id: string?
}
```

- **Data/Type ID、用途与来源**：

  `DATA-EX-ERROR`；表示一次请求的错误响应。示例机器源为 `Proposed: InspectionError`；正式设计须固定错误载荷 Schema 及其版本。

- **`code`**：

  必填，取本节 `InspectionErrorCode` 的已定义值；本结构不重新分配错误码。

- **`request_id`**：

  字段必填、值可空；输入有合法 `request_id` 时原样返回，输入缺失或 ID 自身无效导致 `INVALID_REQUEST` 时为 `null`。其他三个错误码必须携带非空原请求 ID。

- **`task_id`**：

  可空字符串；上述四种错误都表示本次未创建任务，因此必须为空。响应丢失造成的结果未知不是本错误载荷，须用原 `request_id` 查询权威结果。

- **约束与生命周期**：

  错误响应由边界适配单元构造，并随本次请求返回；日志可保留关联身份，但敏感信息不得未经授权复制到载荷。实际编码与长度由 Schema 固定。

- **合法/拒绝实例**：

  `{code:QUEUE_FULL, request_id:"req-7", task_id:null}` 在确实未受理时合法；本次任务已创建却返回任何上述错误码都属语义错误，必须阻断。

- **验证**：

  `V-EX-ERROR-01` 检查字段条件、关联身份和敏感信息边界；本例 `NOT_RUN`。

<!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 跨结构身份、键与关联

<details>
<summary>本节编写建议</summary>

本节只分析两个或更多结构之间的关系，不重复 §3 的字段定义。给出主键、外键、幂等键、租户/项目作用域与引用失效的关系图或短表，说明对象删除和并发写入时如何维持关联；每条边都引用 §3 的稳定 Data/Type ID。

完成检查：读者可从一个对象追到其引用对象及唯一写入 authority，而不是靠同名字段猜测关系。

</details>

## 5. 跨结构数据流与投影

<details>
<summary>本节编写建议</summary>

画出生产者、校验点、权威存储、派生投影和消费者，并以 Data/Type ID 标注每条箭头。正文解释创建、更新、消费和失败回退时哪些副本可信；本节描述关系，不成为第二份结构字段来源。

完成检查：每个派生对象能追到输入和转换责任，缓存或投影没有被画成第二个权威源。

</details>

## 6. 编码、布局与兼容边界

<details>
<summary>本节编写建议</summary>

只汇总跨多个结构共用的编码和版本规则；单个结构特有的布局仍回到 §3 对应记录。实际跨语言、网络、存储或 RTL 时说明字节序、对齐、padding、长度与校验覆盖；逻辑类型不虚构 C ABI。旧版读取、新版未知字段和拒绝行为要与固定机器源一致。

完成检查：两个实现方不会因默认字节序、单位或未知值策略不同而得到相反解释。

</details>

## 7. 跨结构实例与验证追踪

<details>
<summary>本节编写建议</summary>

§3 每个关键结构已有完整合法和拒绝实例；本节只给同时涉及多个结构的业务场景，并索引各自 V/Case、固定 fixture 和实际 Run。明确 Expected 与独立判据，区分未实现、未执行和不适用，不能用同一错误实例在两个对象上重复计为完整覆盖。

完成检查：从场景能双向追到参与结构的字段来源、接口成员与原始验证证据。

</details>

## 8. 实现映射与变更计划

<details>
<summary>本节编写建议</summary>

将每个 Data/Schema ID 映射到真实或 Planned 的生成类型、代码位置、转换函数和测试入口。变更时先改唯一机器权威，再列出需要重新生成或核对的消费者；未实现位置不得填成已有 symbol，也不要在映射中重写字段语义。

完成检查：编码者能找到实际落点与变更顺序，审查人能区别计划路径和现存实现。

</details>

| Data/Schema ID | 唯一来源及版本 | 实现位置/状态 | 转换与迁移 | V/Case |
|---|---|---|---|---|
| <!-- TODO --> | | | | |
