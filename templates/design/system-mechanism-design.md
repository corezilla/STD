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
<!--
编写建议：本模板只用于跨越两个或更多组件/子系统、具有独立流程或恢复语义的机制。重点是把参与方、
消息、状态变化和失败传播串成一条可实现链路。单一模块内部逻辑按领域使用 design.definition
或硬件/FPGA 专项模板，不重复建文。
编写规范见 docs/design-writing-guide.md；所有示例必须替换。
-->

## 1. 机制摘要：解决什么问题

系统设计仍保留端到端原理、关键阶段、系统级约束和代表失败；本文唯一维护该机制的详细
状态转换、参与方协议和恢复规则，字段级定义仍引用机器契约。固定上级系统基线及对应
Process/Step/Constraint ID，说明本文范围；细节变化时核对系统摘要，不能维护两套不同流程。

| 项目 | 内容 |
|---|---|
| 触发者 | <!-- TODO --> |
| 当前问题 | <!-- TODO --> |
| 可观察结果 | <!-- TODO --> |
| 为什么需要多个参与方 | <!-- TODO --> |
| Non-goals | <!-- TODO --> |

## 2. 使用场景与功能

| Scenario ID | 触发条件 | 参与方 | 预期结果 | 验收条件 |
|---|---|---|---|---|
| SC-001 | 用户提交任务 | UI、API、Worker、Store | 任务终态可查询 | 重复提交不产生第二个任务 |

## 3. 参与方、责任和 authority

| Participant | 负责 | 不负责 | Owned data/state | Provided/Consumed interface | 实现位置 |
|---|---|---|---|---|---|
| API | 鉴权和创建命令 | 执行任务 | request record | HTTP / queue | `src/api/` |

### 3.1 系统约束与参与方承接

<details>
<summary>本节编写建议、规范与示例</summary>

**本节目的**：把系统分配给本机制的政策和预算落实到参与方，使跨单元协作满足同一组约束。

**必须写清楚**：上级基线、Constraint ID、决定状态和条件，参与方必须提供的保证、允许的
实现自由度、组合规则、各方落实位置、验证及变更影响。

**编写规范**：固定系统分配和所引用的契约版本，以来源文档与约束 ID 联合定位；细分项关联
父约束，拟议输入仍标为拟议。机制 Owner 只在系统授权范围内细化，不能自行改变超限行为、
重试政策或总预算。已有系统分配直接引用；需要细分时说明参与方及公共开销，避免一份资源
被重复承诺。把生产方保证与消费方前提接起来，检查
正常及失败路径；各方独立通过并不证明协作闭合。下级通用单元或硬件/FPGA 专项设计用同一约束 ID
说明实现与验证，冲突返回原决定责任方，不由某一参与方单方修改；系统摘要同步反映已采用
的变化，但不复制本文的完整状态机或协议。

**抽象示例**：虚构系统要求校验失败时当前目录不变。机制据此规定校验方只交付整批通过的
候选，写入方拒绝失败或检查不完整的结果；双方可选择内部算法，但不能改为跳过错误行后发布。
验证先构造上游校验失败，检查输出及编排不调用写入入口；再直接向写入接口注入未通过的
候选，检查其拒绝且旧快照未变。两类检查分别验证正常交接和边界防护，不能相互代替。
此例仅示范约束怎样跨参与方落实，不代表已有契约、实现或测试结果。

**完成条件**：系统约束可追到参与方责任、详细流程与组合验证，自由度和反馈边界明确；
未验证或不满足的项保持可见，不因接口表已填或单方 PASS 而判整体闭合。

</details>

| Constraint ID / 上级基线与决定状态 | 适用条件 | 系统保证/分配 | 参与方承接与自由度 | 流程/协议/下级落实位置 | 组合验证与证据状态 | 差距/变更影响/裁决责任 |
|---|---|---|---|---|---|---|

## 4. 输入、输出与共享对象

| Object | Producer | Consumer | Contract | Identity/key | 生命周期 | Authority |
|---|---|---|---|---|---|---|
| TaskCommand | API | Worker | `schemas/task.json` | task_id | accepted→terminal | API |

## 5. 正常端到端流程

```mermaid
sequenceDiagram
    participant U as User/UI
    participant A as API
    participant Q as Queue
    participant W as Worker
    participant S as State Store
    U->>A: Request + idempotency key
    A->>S: Create accepted state
    A->>Q: Validated command
    Q->>W: Delivery
    W->>S: Terminal result
    S-->>U: Observable status/result
```

| Step | Sender → Receiver | 输入 | 校验/处理 | 状态变化 | 输出/timeout |
|---:|---|---|---|---|---|
| 1 | UI → API | request | auth + schema | none | accepted/error |

## 6. 分支和替代流程

| Branch ID | 条件 | 与主流程不同之处 | 最终结果 | 是否允许 fallback |
|---|---|---|---|---|
| BR-001 | queue unavailable | 不创建可执行任务 | explicit unavailable | No |

## 7. 状态机与不变量

| From | Event | Guard | To | Writer | Side effect | 非法转换结果 |
|---|---|---|---|---|---|---|
| accepted | worker-start | 权威状态允许且执行/写入授权有效（按唯一契约核验） | running | Worker | start timestamp | reject |

| Invariant ID | 必须始终成立的规则 | Enforcement | 违反后的结果 |
|---|---|---|---|
| INV-001 | 一个 idempotency key 只对应一个 payload digest | API + Store | conflict |

## 8. 失败传播、重试与恢复

<details>
<summary>本节编写建议、规范与示例</summary>

**本节目的**：在失联、部分成功或结果未知时维持单一有效执行与可追踪结果，不把探活失败
误当作执行失败，也不因重试制造重复副作用。

**必须写清楚**：谁确认权威任务状态，旧执行者可能仍执行什么、其执行/写入权限如何失效，
迟到写入和已发生副作用如何核对，重试的幂等/去重条件、阻塞或转人工出口及证据。

**编写规范**：失联先标记结果未知并核对权威状态；若结果已确认，按契约返回或恢复该结果，
不重新执行。只有确认旧执行者停止或已被隔离，且满足幂等/去重条件时才允许重试。说明隔离
由哪个资源或副作用接收方强制执行、如何拒绝旧写入；仅更新调度记录或等待 lease 到期不等于
旧 Worker 已停止或所有旧权限已失效。核对外部副作用；无法确认时保持阻塞或转人工，不盲目
重派。任务身份与执行代次、lease、generation 等规则由唯一契约明确，不从本模板推导固定
的“同代次”或“换代次”策略，也不新增项目尚未批准的重试机制。

**抽象示例**：Worker 的完成响应丢失，监控先记录 UnknownOutcome。若权威记录已有结果，
返回原结果；否则按契约确认旧执行者已停止或隔离，并核对副作用去重证据，才进入获准的重试
路径。若无法阻止旧 Worker 继续写入，或副作用无法判明，任务保持阻塞并移交指定责任方。
测试应覆盖旧 Worker 恢复、迟到结果和新旧执行交叠，检查旧写入被拒绝且副作用不重复。

**完成条件**：能够从失败点推演到结果确认、安全重试或阻塞处置；执行授权、副作用及状态
收敛都有明确依据和验证，不以“重新发 lease”代替安全前提。

</details>

| Failure ID | 失败点 | 谁检测 | 向上游返回/传播 | 重试规则 | 数据处理 | 最终状态 |
|---|---|---|---|---|---|---|
| FAIL-001 | Worker 失联 | 契约指定的监控方 | 结果未知，核对权威状态 | 已有结果则不重试；否则须确认旧执行者停止或隔离且幂等/去重成立 | 保留日志，核对副作用，拒绝旧写入 | 结果已确认则按契约收敛；否则 unknown/blocked，不伪造终态 |

必须覆盖 timeout、取消、重复投递、部分成功、重启和 UnknownOutcome。

## 9. 并发、排序与容量

明确 writer、锁/lease、generation、queue、ordering、backpressure、公平性和资源耗尽行为。

## 10. 安全、权限与信任边界

描述每一跳的身份、鉴权、授权、敏感数据、跨租户/跨项目隔离和 fail-closed 行为。

## 11. 可观测性与证据

| Signal | Writer | Correlation fields | Consumer | Retention | Alert/Debug use |
|---|---|---|---|---|---|
| task transition | State Store | task_id、generation | Operator | 30 days | stuck task |

## 12. 配置、兼容与部署

列出配置 Owner、默认值、作用域、版本兼容、部署位置和故障域。任何 fallback 必须显式、
可观察、可测试。

## 13. 各参与方实现清单

| 顺序 | Participant | 变更 | 文件/模块 | Contract | 完成条件 |
|---:|---|---|---|---|---|
| 1 | API | 接收幂等键 | `src/api/tasks.ts` | Task API | contract tests pass |
| 2 | Worker | 执行和终态写入 | `src/worker/run.ts` | TaskCommand | recovery tests pass |

## 14. 验证、上线与回滚

将 §3.1 的 Constraint ID 与场景、不变量一并映射，既验证各方承接，也验证组合后的正常和
失败行为。固定相同输入及配置；局部 PASS 不关闭协作验证，未运行的检查保留 NOT_RUN，
发现差距回传原约束责任方，不能只调整测试预期使其通过。

| Scenario/Invariant/Constraint | 测试 | Oracle | Evidence | 状态 |
|---|---|---|---|---|
| SC-001 / INV-001 | duplicate submission | single task | <!-- TODO --> | Planned |
| FAIL-001 | 失联后旧 Worker 恢复、迟到结果、重试交叠与不可确认分支 | 旧写入被拒绝；副作用不重复；已有结果不重做；无法确认则阻塞或转人工 | NOT_RUN | Planned |

写明启用条件、灰度、兼容窗口、回滚点和旧机制退出方式。

## 15. 风险、未决问题与决定

若关键协作机制或验证判据未定，先列必须解决的问题，按输入与约束、选项、正常/失败推演、
推荐方案及代价、未决项形成预设计；复杂分析复用 `evaluation.technical-analysis`。选择后
回写状态/流程及 §3.1，并核对系统摘要与各方承接。关键机制未定不能判设计完成；不相关工作
可继续，未实现/未实测另行标注。逐节检查实际决定、依据、下游约束、自由度及承接检查位置，
不把登记未决项或复制统一口号当作设计结果。

| ID | 问题 | 影响 | Owner | 截止 Gate | 状态/ADR |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |
