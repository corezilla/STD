# 完整机制教学案例：有副作用的暂存导出

版本：EX-EXPORT-01/v1 · 日期：2026-09-12 · Target / Planned / NOT_RUN

案例修订：2（补齐取证判定；请求/响应封包不变）。

本例为原创虚构设计，用于试写机制模板，不是项目协议、可部署服务或运行验证证据。
保留[只读 EX-OBS-01/v1](../ai-system-design-authoring-guide.md#88-完整小例两个单元的只读版本核对)作为另一案例；不能把只读重采样规则用于本例写操作。
本文是本例公共规则的唯一维护位置；模板中的接口实例、图和测试是引用视图，不是第二份协议。

## 1. 用途与范围

使用者要把一段文本生成临时导出文件，确认结果后取走，取消或失败时丢弃半成品并归还工作槽位。本文的具体转换就是把 payload 原样编码为 UTF-8 文件，不追加换行或做业务转换；这样调用方可从冻结输入独立计算预期。输出是一次导出结果，或明确的未交付原因与清理状态；不是“启动了一个 Worker”就完成用户任务。

调用者 C 通过管理代理 A 使用本机暂存槽 slot-1，A 内部的 Worker W 只通过 A 的受控写入入口修改该操作私有文件。W 不持有可绕过入口的文件描述符，也不能修改源文件、其他操作或外部业务系统。本例不包含发布文件、跨主机事务、自动重试或第三方副作用补偿。

选择私有暂存范围使取消后的回退可以是丢弃临时产物，而非逆转外部业务。代价是结果交付前必须保留槽位；结果证据丢失时即使看见文件，也不能把半成品推断为已验证结果。本例不适合作为支付、设备动作或生产数据更新的通用重试范本。

## 2. 固定参与方、输入与故障边界

- A 是 operation 记录、槽位占用、写入门禁和终态的 authority；C 负责选择合法分支、保存取得的结果和显式提出下一次任务；W 负责生成及报告结果。
- 本例逻辑接口绑定 UTF-8 JSON Lines 请求/响应，传输为同机 Unix socket `/run/ex-export-demo.sock`；每连接一个请求和一个响应行，不允许重复 JSON key。该路径仅为教学指定值，仓库不创建 socket 或启动服务。
- A 以本机 peer credential 核对已配置调用 UID；operation 绑定首次 prepare 的 UID，后续调用必须相同。正文 JSON 中的身份字段不是凭据；其他 UID 返回 FORBIDDEN，不泄露 operation 状态。
- `agent_instance` 是 A 启动时的不可复用实例标识，C 从已配置的可信部署清单取得；本轮固定为 agent-a1。全部调用先核对它，不能把旧地址上的新实例当原 A。
- 只承诺 A 本次存活期间的记录一致性。W 失联或完成凭据内容丢失/无效可处理，但实例、执行标志、写门禁、在途计数、封口标志和冻结结果这些控制事实必须完整。A 崩溃、控制账本损坏/不可达时不能证明停止，槽位保持隔离，不自动跨实例重试或开放。此类恢复需独立设计，本文不声称已解决。
- 资源预算为每 A 一个工作槽、每输入最多 4096 UTF-8 bytes、最多 16 个 operation 控制记录。这些是教学 Specified 上限，不是测量值。release 归还槽与私有文件，不删除防重放记录；记录满则拒绝新任务，不通过逐出旧 ID 重新执行。

## 3. 唯一规则登记

下表是规范规则；图、状态例和验证项通过 Rule ID 引用。实现状态均 Planned，运行验证均 NOT_RUN。

| Rule ID | 规则与强制位置 |
|---|---|
| EX-R1 | A 先校验调用者、封包及实例，再按 UID + operation_id 查记录。prepare 的同 ID/同 payload/同 slot 返回原操作当前状态；参数不同返回 CONFLICT，绝不分配第二次。同 ID 在 RELEASED 后也不复用。 |
| EX-R2 | W 每次写入先通过 A 的该 operation 写入门禁并计入在途计数。stop 原子关闭新写准入，随后等已准入写入退出；门禁关闭与在途计数归零同时成立才确认 FENCED，同时按 EX-R5 封闭凭据入口并冻结来源快照。仅修改阶段、超时或发出停止请求不是证明。 |
| EX-R3 | stop 不依赖 collect、finalize 或 release，取消 PREPARED 时也可直接执行。关闭的是 W 的写入权限，不撤销 C 的查询/取证/收口控制权限。所有等待均有单次响应期限，未证明安全则留 STOPPING、槽位 HELD。 |
| EX-R4 | 五项分别判断：结果已知性、访问安全、操作终态、资源释放、重新准入。UNKNOWN 可以与 FENCED、FINALIZED、RELEASED 并存；停止不是成功，释放不是恢复原结果。 |
| EX-R5 | collect 仅在 FENCED 后按 §4.2 的来源封口及转换表判定：未执行证明或有效完成凭据保全为 CAPTURED；已封闭的唯一来源确认为缺失/无效才置 UNRECOVERABLE。无法核查来源不等于缺失，保持 PENDING。冻结的结果已知性不改写；不以文件相似或超时代替完成证据。 |
| EX-R6 | finalize 在 FENCED 且 evidence 非 PENDING 时选择且锁定分支。deliver 要求 SUCCEEDED + CAPTURED 且输出内容/长度/摘要校验通过；discard 放弃交付并封结本操作私有产物，不等待“已交付”，物理删除仍由 release 完成。分支选择后不可切换。release 依赖已选分支 FINALIZED，而不依赖未选分支完成。 |
| EX-R7 | release 只删除已收口操作的私有文件并归还槽，不抹掉终态/防重放记录。只有 FENCED + FINALIZED + 槽归还后才可接受用户显式新任务，使用新 operation_id；不能自动重放旧任务、向旧操作再次 execute 或推断外部副作用已补偿。 |
| EX-R8 | 每次响应及凭据绑定 protocol/request_id/agent_instance/operation_id；payload/slot 由 prepare 冻结。C 核对关联及跨字段约束后才消费。旧 W 的迟到写入和结果不能改变停止后冻结的结论，也不能写进新操作。 |

## 4. 完整调用契约

### 4.1 封包与类型

请求恰有 `protocol, request_id, agent_instance, operation_id, op, args` 六项。protocol 固定 EX-EXPORT-01/v1；request_id、agent_instance、operation_id、slot_id 都是 1–64 位 ASCII 字符，首位字母，余位为字母/数字/连字符；request_id 只关联本次响应，不承担幂等性。所有参数都必填，不接受额外字段；字符串不做隐式转换。响应最大 16384 bytes，请求最大 8192 bytes，超限或坏 JSON/重复 key 为 BAD_REQUEST。

成功响应恰有 `protocol, request_id, agent_instance, operation_id, ok:true, state, output`；
错误响应恰有前四个关联字段、`ok:false, error:{code}`，没有 state/output。无法解析关联字段时对应值为 null；错误响应仍使用本协议版本。C 遇到版本、实例、operation 或 request 关联不符时不消费结果，按通信不确定性核查原操作。不存在收到响应就自动新建 operation 的规则。

state 恰有 `phase, result, access, evidence, disposition, resource, admission`，枚举如下：

| 字段 | 取值与含义 |
|---|---|
| phase | PREPARED、EXECUTING、STOPPING、STOPPED、FINALIZED、RELEASED |
| result | NOT_STARTED、UNKNOWN、SUCCEEDED、FAILED；execute 后未确认即 UNKNOWN，stop 安全确认时冻结已知性，之后不回填成功 |
| access | OPEN、CLOSING、FENCED；是 W 写入口状态，不是 C 的控制权限 |
| evidence | PENDING、CAPTURED、UNRECOVERABLE；CAPTURED 可保存成功、失败或未启动的凭据，不能单凭它推断 SUCCEEDED |
| disposition | null、deliver、discard；只在 finalize 选择并冻结 |
| resource | HELD、RELEASED；只计工作槽及私有文件，不包含仍保留的控制记录 |
| admission | BLOCKED、ELIGIBLE；表示本操作的资源阻塞是否解除，不是全局空闲承诺、用户授权或新任务已开始。新 prepare 仍检查此刻槽位和账本容量；旧 RELEASED 快照不会使后来占用的槽变空闲 |

output 仅在成功 deliver 及其后重复 finalize(deliver) 时为 `{encoding:"base64",data,sha256}`；
其他调用为 null。数据为最多 4096 bytes 的完整导出内容，摘要是解码后 bytes 的小写 SHA-256，C 同时验证长度、摘要、与原冻结 payload 的 UTF-8 bytes 一致及 result/evidence/disposition 组合。W 经受控入口完成全部写入及校核后才报告完成凭据；A 未收到有效凭据时，看见与输入相同的暂存 bytes 也不能代替完整完成记录或证明旧写入已经排空。

跨字段约束：STOPPED 及之后必须 FENCED；FINALIZED/RELEASED 必须 evidence 非 PENDING、disposition 非 null；RELEASED 才允许 resource=RELEASED/admission=ELIGIBLE。非 RELEASED 一律 HELD/BLOCKED。PREPARED 为 NOT_STARTED，初始其余 OPEN/PENDING/null；SUCCEEDED 不自动改变访问或资源状态。

### 4.2 操作、失败与后续动作

| op / args 完整形状 | 受理条件与效果 | 失败后合法动作 |
|---|---|---|
| prepare / {"slot_id":"slot-1","payload":"demo"} | UID/实例合法，新 ID、槽空闲、账本未满；冻结参数，创建 PREPARED。payload 可以为空但不超过上限，只支持 slot-1。先查同 ID 再查容量，保证重复 prepare 可返回原记录。 | BUSY 不创建操作，可等待原操作释放；CONFLICT 不覆盖；LEDGER_FULL 不逐出记录 |
| execute / {} | PREPARED 才启动一个 W，并先记录 EXECUTING/UNKNOWN 再交接。EXECUTING 中重复请求只返回当前状态，不再启动；其他阶段 CLOSED。 | 响应丢失以 inspect 查询原 ID，或 stop；不以新 ID 自动重执行 |
| inspect / {} | 返回该操作此刻控制记录，无写副作用；不表示查询与后续操作原子相连 | 不可达仍未知；NOT_FOUND 不证明某个其他实例从未执行 |
| stop / {} | PREPARED/EXECUTING → STOPPING，依 EX-R2 关闭门禁、排空；在同一临界区完成凭据来源封口及结果冻结后到 STOPPED/FENCED。已 FENCED 则返回当前状态，不回退阶段 | 单次至多 2000 ms，未排空仍成功响应 STOPPING/CLOSING（不是停止完成）；可 inspect/再次 stop 或转人工，不能释放 |
| collect / {} | 仅 FENCED；读取封口快照，按下表核对是否执行、有效凭据及内容，保全结论和判定理由。正常可读情况下本次调用即到 CAPTURED/UNRECOVERABLE，不再等待 W；终结后重复返回原记录 | 尚不安全为 NOT_SAFE；来源不可读取/核查或本次检查无法在 2000 ms 内完成则 PENDING，阻塞收口并报告原因。缺失判定必须来自已成功读取的封闭来源，不来自超时 |
| finalize / {"disposition":"deliver"} 或 {"disposition":"discard"} | 仅 STOPPED/FENCED 且 evidence 非 PENDING；按 EX-R6 交付或丢弃。相同已选分支重调幂等；不同分支 CONFLICT | deliver 条件不足为 RESULT_UNAVAILABLE，可由 C 显式选 discard；PENDING 返回 EVIDENCE_PENDING；未安全返回 NOT_SAFE |
| release / {} | 仅 FINALIZED；删除本操作私有文件并回收槽，成功到 RELEASED。已 RELEASED 重调不影响后来操作；保留防重放记录及已交付小结果 | 收口前返回 NOT_FINALIZED；文件清理未完成则留 FINALIZED/HELD/BLOCKED，C 可重调，不伪称资源已释放 |

**取证来源与封口（EX-R5 的唯一详细规则）**

A 的本 operation 内存记录是唯一可采信来源，不另向 W、临时文件、网络备份或日志搜索第二份完成结论。
prepare 记录尚未执行；首次 execute 在交接前记录其 request_id 及已执行标志。W 通过 A 内部的受控完成入口
提交凭据；接收、校验、存入记录和更新结果在 A 的同一 operation 临界区内完成，不存在独立异步投递队列。
凭据绑定 protocol、首次 execute 的 request_id、agent_instance、operation_id、slot_id、冻结 payload 的 SHA-256、
result 及 output；SUCCEEDED 的 output 必须与冻结输入 bytes、长度和摘要相符，FAILED 的 output 为 null。
这些是内部凭据字段，不是新增 C→A 操作；每次对 C 的响应仍关联当前调用的 request_id。

stop 排空写入后，在同一临界区关闭完成入口，将“实例/操作、是否已执行、冻结结果、当前凭据副本或确认为空”
保留为不可变封口快照，再报告 FENCED。先被临界区受理的完成回报纳入快照；后到回报拒绝，不回填旧结果。
封口不需要等 W 自报退出或成功，因此执行中取消时即使从未收到完成凭据也能产生这一事实。
W 可能仍计算，但已无本操作写权和提交完成结论的入口；若实际实现不能证明这两个边界，则不满足本例前提。

collect 在 A 核对封口所属实例/操作和控制记录完整性后，读取此快照并按下表判定。
**UNRECOVERABLE 仅表示按本协议已无法取得可采信的完成凭据，不断言所有物理副本消失，也不证明 W 没执行。**
丢弃私有产物的允许性来自独立的 FENCED 证明，不来自“已不可恢复”这个标签。

| 原取证状态 / 来源事实 | 判定条件与生产者 | 期限与封结动作 |
|---|---|---|
| PENDING；访问未安全 | A 的写入门禁或在途计数尚不满足 EX-R2 | collect 返回 NOT_SAFE；不封结、不释放；先推进 stop |
| PENDING；封口快照确认未执行 | A 的 execute 交接记录不存在，冻结结果为 NOT_STARTED，且完成入口已关 | 本次 collect 内 CAPTURED；理由 NOT_STARTED_AT_SEAL，保全 A 的未执行证明 |
| PENDING；快照有完成凭据 | 关联字段、冻结 result 一致；成功输出通过 bytes/长度/摘要检查，失败输出为 null | 本次 collect 内 CAPTURED；理由 VALID_COMPLETION_AT_SEAL，复制可交付小结果 |
| PENDING；已执行、快照确认为空 | 成功读取已封闭的唯一来源，且无已受理完成凭据；可能中途取消、回报丢失或晚于封口 | 本次 collect 内 UNRECOVERABLE；理由 NO_COMPLETION_AT_SEAL；原结果不改写 |
| PENDING；快照凭据可读但无效 | 关联/冻结结果/内容校验明确失败，且已无其他合法来源 | 本次 collect 内 UNRECOVERABLE；理由 INVALID_COMPLETION_AT_SEAL，保留失败项，不交付内容 |
| PENDING；无法核查来源 | 控制完整性、封口证明或快照读取无法确认，或本次校验无法完成 | 最多 2000 ms 返回 PENDING；记录不可核查原因、阻塞 finalize/release；恢复可读后重调或交责任方，不把期限到达当缺失 |
| CAPTURED 或 UNRECOVERABLE | 已保存本 operation 的封结记录 | 幂等返回；stop/collect 重调不重开来源、重置结论或受理迟到回报 |

这里的检查仅针对至多 4096 bytes 的同实例内存快照；正常完成检查在一次调用内终结。
PENDING 是尚未 collect 或当前无法核查，不是“还等 W 的未知完成时间”。A 保存封口标识、执行标志、凭据存在性、
关联/内容检查结果、reason 和冻结结果作为取证审计；仅读取失败时不得保存伪造的缺失结论。
教学模型以具名故障注入模拟不可读/回报丢失，不能把 receipt 或 evidence 直接设成目标结论代替判定。
真实服务失联或损坏超出本例可保证进展的边界，安全阻塞是合法出口；本例不承诺故障持续时仍强行释放。

错误集合还包括 FORBIDDEN、BAD_REQUEST、INSTANCE_MISMATCH、NOT_FOUND、CLOSED、CONFLICT、
BUSY、LEDGER_FULL、NOT_SAFE、EVIDENCE_PENDING、RESULT_UNAVAILABLE、NOT_FINALIZED。
按鉴权→封包/参数→实例→操作存在/prepare 冻结参数→状态/资源的顺序检查，前一步不通过不执行后续效果。除预定义错误外的连接断开/服务故障视为结果未知，不能暗设“内部错误无副作用”。

每次 C 等待 2500 ms（教学值），控制操作的单次处理上限为 2000 ms；execute/prepare 只确认本步受理，不等待整个导出。无限重试不是合法出口：停止或取证未能推进时报告阻塞、保留记录与槽位并由有权者处置。控制服务不可达时没有靠客户端超时回收资源的捷径。版本不兼容不自动降级。

### 4.3 正常调用实例

以下请求各为一行完整 JSON；逐条等待并校验响应后再执行下一步，不是并发批量发送。

```json
{"protocol":"EX-EXPORT-01/v1","request_id":"q1","agent_instance":"agent-a1","operation_id":"op-001","op":"prepare","args":{"slot_id":"slot-1","payload":"demo"}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q2","agent_instance":"agent-a1","operation_id":"op-001","op":"execute","args":{}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q3","agent_instance":"agent-a1","operation_id":"op-001","op":"inspect","args":{}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q4","agent_instance":"agent-a1","operation_id":"op-001","op":"stop","args":{}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q5","agent_instance":"agent-a1","operation_id":"op-001","op":"collect","args":{}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q6","agent_instance":"agent-a1","operation_id":"op-001","op":"finalize","args":{"disposition":"deliver"}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q7","agent_instance":"agent-a1","operation_id":"op-001","op":"release","args":{}}
```

在本条成功轨迹中，q3 已查到 W 有效完成凭据、q4 已排空、q5 已保全；若实际响应尚未满足前提不能照抄继续。各响应均完整给出状态，即便它与前一条相同。

```json
{"protocol":"EX-EXPORT-01/v1","request_id":"q1","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"PREPARED","result":"NOT_STARTED","access":"OPEN","evidence":"PENDING","disposition":null,"resource":"HELD","admission":"BLOCKED"},"output":null}
{"protocol":"EX-EXPORT-01/v1","request_id":"q2","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"EXECUTING","result":"UNKNOWN","access":"OPEN","evidence":"PENDING","disposition":null,"resource":"HELD","admission":"BLOCKED"},"output":null}
{"protocol":"EX-EXPORT-01/v1","request_id":"q3","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"EXECUTING","result":"SUCCEEDED","access":"OPEN","evidence":"PENDING","disposition":null,"resource":"HELD","admission":"BLOCKED"},"output":null}
{"protocol":"EX-EXPORT-01/v1","request_id":"q4","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"STOPPED","result":"SUCCEEDED","access":"FENCED","evidence":"PENDING","disposition":null,"resource":"HELD","admission":"BLOCKED"},"output":null}
{"protocol":"EX-EXPORT-01/v1","request_id":"q5","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"STOPPED","result":"SUCCEEDED","access":"FENCED","evidence":"CAPTURED","disposition":null,"resource":"HELD","admission":"BLOCKED"},"output":null}
{"protocol":"EX-EXPORT-01/v1","request_id":"q6","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"FINALIZED","result":"SUCCEEDED","access":"FENCED","evidence":"CAPTURED","disposition":"deliver","resource":"HELD","admission":"BLOCKED"},"output":{"encoding":"base64","data":"ZGVtbw==","sha256":"2a97516c354b68848cdbd8f54a226a0a55b21ed138e207ad6c5cbb9c00aa5aea"}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q7","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"RELEASED","result":"SUCCEEDED","access":"FENCED","evidence":"CAPTURED","disposition":"deliver","resource":"RELEASED","admission":"ELIGIBLE"},"output":null}
```

### 4.4 跨字段错误实例

```json
{"protocol":"EX-EXPORT-01/v1","request_id":"q8","agent_instance":"agent-a1","operation_id":"op-001","op":"prepare","args":{"slot_id":"slot-1","payload":"changed"}}
{"protocol":"EX-EXPORT-01/v1","request_id":"q8","agent_instance":"agent-a1","operation_id":"op-001","ok":false,"error":{"code":"CONFLICT"}}
```

同 op-001 不同 payload 必须拒绝，即使槽已空闲。另一个调用若把成功响应 q6 的 operation_id 改成 op-002，C 也必须拒绝消费；字段各自类型正确不代表实例关联正确。

## 5. 完整过程与条件依赖

![暂存导出正常与响应丢失路径](../assets/system-mechanism-authoring/effect-flow.png)

图 E1：[可编辑 SVG](../../templates/diagrams/mechanism/effect-flow.svg)。两条路径都先按 EX-R2/3 安全停止，再取证收口；右路不是自动重试。图不按耗时比例，也不代替 §4 的请求/响应。

正常：prepare 预留私有槽 → execute 受理并生成 → inspect 核对完成 → stop 关闭写入并排空 → collect 保全 → finalize(deliver) 返回完整 bytes → release 回收槽。C 保存收到的结果是其后续义务，release 不意味着外部发布。discard 是放弃交付并封结分支，物理文件统一到 release 删除；这样不会在收口前破坏证据。小型已交付结果随控制记录保留到本次 A 结束，支持丢响应后的同分支取回，但不承诺跨实例持久保存。

取消：PREPARED/EXECUTING 都能直接 stop，不等正常路径完成；安全且来源封口后 collect，选择 discard 再 release。未启动时由 A 的未执行记录保全为 CAPTURED；执行中无已受理凭据时由封口空快照判为 UNRECOVERABLE，不等待 W 补报。回退仅丢弃本操作私有产物，不回滚源数据或补偿外部动作。调用者在 collect 未完成前不能 finalize；不得用提前 release 销毁尚需取证的范围。

![分支与清理依赖](../assets/system-mechanism-authoring/cleanup-dependencies.png)

图 E2：[可编辑 SVG](../../templates/diagrams/mechanism/cleanup-dependencies.svg)。箭头表示前置依赖；“或”表示选定分支完成，不是两个分支都完成。EX-R3 和 EX-R6 是唯一规则。

| 动作 | 依赖适用范围 | 不允许的循环或越界 |
|---|---|---|
| stop / 排空 | 所有已 prepare 操作，不依赖正常执行终结 | stop 等 collect；collect 又等 stop |
| collect / 取证封结 | 访问已 FENCED 且来源已封口；可读取即按 §4.2 判定，不等 W | 把“凭据可恢复”作为安全停止的前提；把不可读取误判为不存在 |
| finalize(deliver) | 仅选择交付的分支，SUCCEEDED + CAPTURED | 要求取消路径也等待交付成功 |
| finalize(discard) | 选择取消/回退的分支，已安全且取证已封结 | 撤销 W 写权时误撤销 C 的 discard 权限 |
| release | 仅依赖已选分支 FINALIZED | 同时等待 deliver 与 discard；取证前销毁私有文件 |

## 6. 响应丢失且证据不可恢复

一次 execute 响应丢失，C 不知道 W 是否完成，先 inspect 原 op-001。若 W 完成凭据可恢复，就按已知结果处理；本反例中凭据确实丢失，但 A 的门禁、在途计数与 operation 控制记录仍完好。

C 发 stop；A 关闭新写准入并确认在途为零，同时封闭完成入口并冻结空凭据快照，返回 STOPPED/FENCED。访问已安全，不必等待旧结果变成已知。collect 成功读取封口快照，核对已 execute 且唯一有效来源无凭据，记录 NO_COMPLETION_AT_SEAL 并返回 UNRECOVERABLE，result 仍 UNKNOWN。C 显式 finalize(discard)，再 release。最后状态如下：

```json
{"protocol":"EX-EXPORT-01/v1","request_id":"lost7","agent_instance":"agent-a1","operation_id":"op-001","ok":true,"state":{"phase":"RELEASED","result":"UNKNOWN","access":"FENCED","evidence":"UNRECOVERABLE","disposition":"discard","resource":"RELEASED","admission":"ELIGIBLE"},"output":null}
```

| 检查轴 | 此分支结论 | 不可推导的结论 |
|---|---|---|
| 结果已知性 | UNKNOWN，旧结果不可恢复 | 不能写 SUCCEEDED 或确定无执行 |
| 访问安全 | FENCED，门禁已关闭且在途为零 | 不能以客户端超时或 Worker 静默替代证明 |
| 操作终态 | FINALIZED(discard)，继而 RELEASED；不再执行旧 ID | 终态不要求虚构旧业务结果 |
| 资源释放 | 私有文件清理确认且槽归还，控制记录保留 | 不表示所有历史证据均删除 |
| 重新准入 | 资源条件 ELIGIBLE，可接受显式新任务/新 ID | 不自动重试旧任务，不承诺外部副作用补偿 |

如果门禁或在途计数无法核查，则停留 STOPPING/CLOSING/HELD/BLOCKED；这才是访问安全未闭合。
如果安全已证明但取证仍 PENDING，只阻塞收口/释放，不重新开放 W 的权限。release 本身清理失败则留 FINALIZED/HELD，重调 release 不再次生成文件。三种阻塞不能混成同一个“失败后重试”。

## 7. 验证项、用例、环境与执行记录

设计验证项回答“哪项保证需要证明”；可执行用例回答“怎样驱动并判定”；环境要求定义哪些控制/观测能力必需；执行记录记录某次实际运行。不能把四者合成一列 PASS。

| 设计验证项 / Rule | 用例设计及独立判据 | 所需环境能力 | 实现/执行与范围 |
|---|---|---|---|
| EX-V1 / R1、R8 | EX-T1：同 ID 相同/不同参数、错实例与串响应；检查无重复启动、拒绝误归属 | EX-ENV-M：可计数的内存逻辑模型 | 教学模型可执行；运行记录见测试输出；不是 IPC 集成证据 |
| EX-V2 / R2、R3 | EX-T2：故意保留在途写，stop 先 CLOSING，release 不可用；清零后才 FENCED | EX-ENV-M；真实版另需 EX-ENV-P 写入门禁命中与排空观察 | 模型仅检查 Guard；真实版未实现/NOT_RUN |
| EX-V3 / R4、R5、R7 | EX-T3：故障注入丢失完成回报，stop 产生来源封口事实，collect 自行判定空/无效凭据；UNKNOWN 保留，discard/release 成功；不可读不能冒充缺失，迟到凭据不重开来源 | EX-ENV-M + 具名回报丢失/来源不可读控制；真实版 EX-ENV-P | 模型可执行；真实停止与文件隔离仍 NOT_RUN |
| EX-V4 / R3、R5、R6 | EX-T4：分别取消 PREPARED 与 EXECUTING；仅从调用入口到 release，不直接改内部判定状态；交付/丢弃互斥，PENDING 不得提前收口 | EX-ENV-M | 模型可执行；并发交叠实际测试 NOT_RUN |
| EX-V5 / R6、R7 | EX-T5：release 清理失败保留占用，重调才归还；迟到旧写拒绝，不影响后来槽所有者 | EX-ENV-M；真实版需要文件错误注入 | 模型可执行；真实文件/进程实现未完成 |
| EX-V6 / R2、R8 | EX-T6：真实 W 不持裸写入口、绕过尝试失败、错误 UID 被拒、实例重启 fail-closed | EX-ENV-P：真实 Unix IPC、peer credential、受控写入口和崩溃夹具 | 未实现；执行 NOT_RUN。环境不可用时 BLOCKED，不能由模型 PASS 关闭 |

EX-ENV-M 由 [教学逻辑模型回归](../../tests/test_mechanism_effect_example.py)在进程内模拟事件，不创建业务文件/服务，不是生产实现。EX-ENV-P 尚未提供；其缺少的接入与隔离能力是实际实施前置条件，不能在文档中假装已存在。

每次执行记录至少绑定 run_id、源 commit/未提交摘要、Case、环境版本、输入/故障命中、观察值、Oracle、结果、原始输出与限制。命令为 `python3 -m unittest discover -s tests -p test_mechanism_effect_example.py -v`，真实 stdout/stderr 和退出码才是本次模型运行证据；本文不预填 PASS。

以下展示 EX-V3 的真实环境覆盖条目如何与用例关联，**不是已执行记录**。没有运行就不编造 Run ID、环境版本或观察值；执行后才新增实际 Run，并保留本条未运行的事实。一次模型 Run 只能填入 EX-ENV-M 的范围，不能替换此条：

```json
{"design_item":"EX-V3","case":"EX-T3","environment_requirement":"EX-ENV-P","environment_version":null,"case_implementation":"NOT_IMPLEMENTED","execution":"NOT_RUN","run_id":null,"source_commit":null,"input":"execute response lost; completion receipt unrecoverable; authority control record intact","oracle_reference":"EX-R2/EX-R4/EX-R5/EX-R7 and section 6 five-axis outcome","fault_hit":null,"observed":null,"raw_evidence":[],"limit":"Real write fencing and file isolation harness is not provided; logical model results do not close this item."}
```

覆盖分开统计：设计项有无承接、用例是否实现、是否执行及结果、是否需要真实系统组合。不适用须有适用性与裁剪依据，不是 NOT_RUN 的别名；本例跨主机分布式恢复不在范围，不用其 N/A 抵消 EX-V6 缺测。即使 EX-T1～5 的逻辑检查通过，EX-V2/3/5 的真实强制点与 EX-V6 仍不关闭。

## 8. 修改后全篇一致性检查示例

例如修改 EX-R6“release 依赖哪条分支”，只在 §3 改规范，再逐项核对：
§4.2 finalize/release 入口与错误，§4.3/§6 响应中的跨字段关系，图 E1/E2，§5 的依赖表，
§6 五轴结论，EX-V4/EX-T4 及其模型断言。逐位置记录“已同步/无影响及理由/仍有旧语义”，不是只全文替换一个词。

规则引用使一致性检查可定位，但不会自动证明一致。未发现某个词不等于旧语义消失；必须实际推演取消、凭据不可恢复和清理失败三条路径。本文的新增模型仅检查教学逻辑，不声称真实协议、安全实现或独立评审已经通过。

本次 EX-R5 回查：§4.2 明确来源封口及转换表；§5/6 和图 E1/E2 的取证节点都引用该规则；
EX-V3/4 与模型改为从原始事件生成判定，不再注入 UNRECOVERABLE 结论。无法读取与确认不存在分开验证。
