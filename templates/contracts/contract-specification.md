<!-- STD_DOCUMENT_COVER_BEGIN -->
# {{document_title}}

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

## 1. Contract scope 与 authority

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：给实现者一份确定公共行为的约定。用业务输入和结果说明契约用途，再区分本文、机制正文及机器源各自拥有的内容；不另写第二份状态机。

**必须写清楚**：参与方、适用配置/版本、行为范围和非目标。已有字段由原源维护，本文解释前后置、可见性和失败；引用必须打开实际内容，计划路径不是契约。

**抽象示例**：虚构 IF-XFER 定义 Host 提交一块数据及确认完成的规则，不规定 FPGA 内部处理算法。全文可参照 STD 的 `docs/examples/host-fpga-transfer-example.md`，但参数和机制不能照搬为项目事实。

**完成条件**：双方无需另猜共同政策，就能判断本次交接负责什么及不保证什么。

</details>

明确机器可读 contract 和说明文档哪个是字段级权威。

## 2. Operation / Message / Event Catalog

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：列全实际入口与通知，而不是只列成功调用。沿正常、取消、错误、维护路径登记成员，区分操作、响应、事件和共享类型。

**必须写清楚**：固定 ID、发起/提供/消费、签名、同步或异步、关联标识与实际机器源。适用角色从源签名核对，不把响应写成请求、不为单向信号新增响应。

**抽象示例**：SUBMIT 的 ACCEPTED 是准入结果，COMPLETE 是后续异步结果，QUERY 返回既有状态；这三者不能共用一个“成功”含义。

**完成条件**：每项入口可沿 ID 找到全字段及错误，目录与源签名双向一致，未定操作保持可见。

</details>

| ID | Kind | Producer | Consumer | Sync/Async | Idempotency |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

依 `docs/interface-data-mapping-standard.md` 使用目录里的接口族#成员 ID；逐方法定义完整请求、响应、事件及错误类型，关联身份、前置、校验顺序、副作用、确认/完成、期限/重复/取消和合法下一步。

| 成员 ID / 类别 | 机器源 / selector / 版本/revision/hash | request/response/event/error 类型 ID | 正文稳定锚点 | 下游提供/消费 / 实现 / 设计 V → Case |
|---|---|---|---|---|

## 3. Request、Response、Event 与数据对象

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：使双方能够构造和校验完整实例。保留所有适用字段的阅读视图，再用一组有关联的请求、响应和事件解释正常及失败输入；实例不能代替 Schema。

**必须写清楚**：完整类型、长度/范围、默认与可空、身份关联、版本、所有权及跨字段条件。逻辑结构与 wire/Host 布局分开；别名和转换写明损失及校验，不复制公共类型。

**抽象示例**：长度单独合法仍可能超过登记缓冲区；完成事件必须匹配本次设备会话与 request ID。记录中完成长度不能超过冻结提交长度。

**完成条件**：接收方仅凭约定就能定位对象、校验字段组合及决定下一步，并有拒绝实例验证。

</details>

引用 OpenAPI、JSON Schema、Proto、IDL 或 ABI；禁止只给示例不给约束。

## 4. 状态、错误和 blocker catalog

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：固定错误后的外部可观察结果。分别记录受理状态、业务结果、访问安全和资源归还；它们不一定同时终结，不要挤进一个 failed 标志。

**必须写清楚**：错误码/来源、判定事实如何产生、允许调用及阻塞出口；有状态则说明 Guard 和迟到事件。尚无持久化也必须解释在途状态。

**抽象示例**：BUSY 表示未受理；TIMEOUT 表示当前等待结束而结果未知；复位失败时旧缓冲区仍隔离。只有完成或安全停止的依据齐全，才进入对应释放路径。

**完成条件**：逐错误推演后没有只能靠改内部状态才能前进的步骤；未知与失败没有混写。

</details>

## 5. 幂等、并发、事务与一致性

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：说明重复及交叠调用的唯一解释。按实际对象定义并发顺序、原子范围和发布点，不凭“支持事务”推断跨设备原子性。

**必须写清楚**：去重键及作用域/保留期，同键不同参数、取消与完成竞态、旧执行失效、在途数据所有权和可见性。真正不重试的接口也写明重复调用结果。

**抽象示例**：同 request ID 同冻结参数返回既有状态，不重新提交；同 ID 换长度返回 CONFLICT。停止响应尚未证明旧访问结束时，不能给新请求复用缓冲区。

**完成条件**：正常、重复及至少一个交叠顺序可逐步推演，所有参与方对同一生效点达成一致。

</details>

## 6. Pagination、filter、ordering 与 retention

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：确定集合查询及记录寿命的行为。只对实际具有分页、过滤或排序的操作展开这些属性；没有分页仍需检查状态、去重和迟到事件是否依赖保留记录。

**必须写清楚**：快照/游标一致性、稳定顺序、边界及失效结果，保留对象、回收触发和上限。没有某项能力按事实解释，不新增查询服务来填模板。

**抽象示例**：IF-XFER 单次查询没有分页；已释放请求的终态仍保留到当前设备会话关闭，用于辨认迟到响应。若采用有界去重窗口，应另定义窗口外查询和重试结果。

**完成条件**：读者知道旧 ID 何时失效、记录回收是否影响安全，以及真正不适用的集合能力。

</details>

## 7. 身份、权限、Secret 与多项目隔离

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：让权限成为可实施、可测试的规则。定义主体、对象与动作的关系，以及认证、授权和操作状态校验的先后，不以网络隔离替代对象授权。

**必须写清楚**：身份来源、租户/会话范围、凭据撤销、调试/复位权限、越权返回及信息泄露边界。示例仅用虚构凭据，不放真实 token 或用户数据。

**抽象示例**：另一个会话持有相同数值句柄也不能查询或释放本会话缓冲区；全设备复位只由维护权限发起，并报告受影响范围。

**完成条件**：正常授权、越权、旧身份和撤销交叠均有判据与验证责任，不靠调用者自觉遵守。

</details>

## 8. 版本、兼容性与迁移

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：解释契约变化对实际消费者的影响。对比固定旧基线逐项列新增、改义、删除和默认行为变化，不能只更新 version/revision。

**必须写清楚**：兼容组合、迁移顺序、拒绝/回退边界和剩余旧消费者。公共规则改变后同步接口实例、状态、流程、测试与消费基线；无协商能力就明确固定版本。

**抽象示例**：新增完成状态不能假定旧消费者会安全忽略；先证明旧新向量的解释，必要时做破坏性版本升级，由原 authority 决定。

**完成条件**：每个受影响 backend 都有采用或不适用依据，未迁移者没有从覆盖分母消失。

</details>

绑定消费方的实际 version/revision/hash；ID 不变不等于兼容。字段改名、枚举/错误变化、删除和替代对照旧基线逐项记录，废弃 ID 不回收，多 backend 分别迁移和验证。

## 9. Positive/Negative fixture 与 validator

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：用具体反例验证规则而非只演示格式。给一组合法输入，以及单字段合法但组合错误、重复、迟到、版本不匹配的代表输入。

**必须写清楚**：向量固定基线、预期返回/状态、独立 Oracle、适用端及验证命令。结构、原生编码、模型和真实设备检查分别标范围；不复制转换后的协议来迁就工具。

**抽象示例**：错误 epoch 的完成记录结构合法，但不能完成当前请求；JSON/目录检查通过不能证明设备已经停止 DMA。

**完成条件**：每个关键规则至少有能暴露违反行为的检查；未运行项没有伪造 PASS 或 Run。

</details>

## 10. Requirement → Contract → Test traceability

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：让共同保证能交给下游实现和验证。用需求/Constraint、规则或成员 ID 对应设计验证项，再连接 Case、所需环境和实际 Run，复用原追踪记录。

**必须写清楚**：提供/消费及 backend、本地与组合验证、尚未实现/运行的部分；承接范围来自固定输入，不由剩余通过项推导。

**抽象示例**：X-R3→X-V3→X-T3 约束复位后安全复用；参考模型和真实板卡是不同环境，模型通过仍保留板卡 NOT_RUN。

**完成条件**：从任一共同保证能找到全部责任方及证据去向，单方成功不会关闭整体目标。

</details>

| 需求/Constraint | 规则/成员 ID | 设计 V | 承接方/backend | Case / 环境 | Run/状态/缺口 |
|---|---|---|---|---|---|

## 11. Activation Gate 与未决项

<details>
<summary>编写建议、规范与示例</summary>

**本节目的**：区分契约设计可用、实现完成和运行许可。记录尚未形成共同决定的事项及其影响；不把静态检查、作者自审或模板填完视为上线授权。

**必须写清楚**：未决成员、冲突及 Owner、所需输入/实验、选择与关闭判据；哪些独立内容可以继续，哪些保证还不能交下游。适用 Gate 沿用项目，不增加逐段审批。

**抽象示例**：尚未确定设备停止确认的可信来源，阻塞安全释放方案；可以继续定义独立的数据校验，但不能声称只待硬件测试。

**完成条件**：关键机制不再仅写 TBD；设计、实现、验证和激活的状态及依据明确分开。

</details>
