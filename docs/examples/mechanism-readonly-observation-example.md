# 虚构案例：跨单元只读版本观测机制

版本：0.1.0-draft.1 · 日期：2026-09-23 · Target / Planned / NOT_RUN

本例是公开、独立构造的教学设计，用同一代表输入贯通用途、责任、对象、调用、状态、失败和验证。
它不是任何项目的既有协议、实现或测试证据。项目只能复用写法和图形样式，不能复用虚构事实。

## 1. 使用场景和边界

运维者在维护或变更前查询目标 A、B 的运行版本。汇总单元 M 读取固定目标清单，依次采样并返回
逐目标结果，使调用者能区分完整、部分、无成功采样和入口拒绝。机制只做只读观测，不升级配置、
不保存历史，也不证明两个目标在同一瞬间一致。

![使用场景、处理范围和输出结果](../assets/system-mechanism-authoring/usage-overview.png)

[可编辑 SVG](../../templates/diagrams/mechanism/usage-overview.svg)。图只回答何时使用、处理什么和得到什么；
责任与 authority 由下一节定义。

## 2. 参与方与 authority

![参与方和协作边界](../assets/system-mechanism-authoring/collaboration.png)

[可编辑 SVG](../../templates/diagrams/mechanism/collaboration.svg)。运维者通过既有管理入口调用 M；M 负责本轮
汇总，不建立版本数据库。A、B 各自拥有本地版本事实。工程 Owner 相同也不改变运行责任边界。

| 参与方 | 拥有的事实或决定 | 明确不负责 |
|---|---|---|
| 调用者 | 是否发起新观测、怎样消费 Report | 不决定目标真实版本 |
| M | 本轮身份、顺序、截止时间和汇总 outcome | 不替 A/B 产生版本事实 |
| A、B | 各自的版本 tuple 与本地采样错误 | 不决定整轮 outcome |

## 3. 对象及寿命

![事实、采样副本和汇总对象](../assets/system-mechanism-authoring/objects.png)

[可编辑 SVG](../../templates/diagrams/mechanism/objects.svg)。目标短时持锁复制本地 tuple；M 完整校验后才接纳
Sample，并按 A、B 固定顺序组合 Report。错误项保留 ERROR 位置，不伪造 Sample。Report 标记
`non_atomic=true`，轮次关闭后释放临时对象，不建立持久历史。

## 4. 代表输入的完整调用演练

本节是硬性设计演练，不是单个 happy-path 样本。冻结输入：调用者 `operator-7` 发起
`observe(targets=[A,B])`，M 分配 `observation_id=obs-42`；A 返回 `version=3.2.1`，B 在 700 ms
内未响应。逐步走查如下：

1. 调用者提交身份、固定目标集合和调用 UID；M 先校验授权、目标集合及并发槽。
2. M 创建 `obs-42`，调用 A；A 返回带目标身份和版本 tuple 的成功响应，M 校验后接纳。
3. M 调用 B；期限到后将 B 记为 `DEADLINE_EXCEEDED`，不补造版本，也不把超时解释为 B 已失效。
4. M 生成 `PARTIAL` Report：A=OK/3.2.1，B=ERROR/DEADLINE_EXCEEDED，`non_atomic=true`。
5. 调用者收到 Report 和退出码 2；随后轮次关闭、I/O 与槽位释放。迟到 B 响应只能记诊断，不能改写已关闭 Report。

调用者由此知道 A 的一次可信采样以及 B 本轮没有结果；不知道 B 是否仍在运行，也不能用新观测证明旧
请求的结果。若任何一步仍需口头补充目标身份、字段、错误或合法下一步，公共设计尚未完成。

![正常调用时序](../assets/system-mechanism-authoring/sequence.png)

[可编辑 SVG](../../templates/diagrams/mechanism/sequence.svg)。图示完整成功路径；上述具体输入演练故意选择
部分结果，用于核对同一操作在失败分支中的可观察语义。

## 5. 状态、失败和清理

![轮次状态和资源寿命](../assets/system-mechanism-authoring/state-lifecycle.png)

[可编辑 SVG](../../templates/diagrams/mechanism/state-lifecycle.svg)。只有入口校验和槽位获取都成功才创建轮次；
汇总根据成功数决定 outcome。M 本地关闭不能证明目标已停，但本例没有业务写入，目标调用受独立期限约束。

![部分结果与未知结果](../assets/system-mechanism-authoring/failure-recovery.png)

[可编辑 SVG](../../templates/diagrams/mechanism/failure-recovery.svg)。A 成功、B 超时时，M 仍可返回 PARTIAL；
M 在响应前退出时，调用者只知道通信失败，旧 Report 没有持久副本。以后经授权的新观测使用新 ID，
不是恢复或重放旧轮次。

## 6. 测试路径和独立判据

![测试控制和独立判据](../assets/system-mechanism-authoring/test-path.png)

[可编辑 SVG](../../templates/diagrams/mechanism/test-path.svg)。测试先固定 A/B tuple 和可信身份，再 arm B 的
受控延迟；真实入口调用后确认指定请求 hit，才把超时计为目标故障覆盖。独立 Oracle 核对 A 的预置事实、
B 的错误、PARTIAL outcome 和退出码 2。结束时 release 延迟、终止残留连接并确认槽位归还。

模拟目标只能证明模拟范围；图、样例和结构测试均不能改称生产验证。

## 7. 与其他教学路径的选择

- 有业务副作用、取证和资源收口时，使用[暂存导出案例](mechanism-side-effect-example.md)，不要套用本例“新观测即可”的前提。
- Host、驱动、FPGA 和板卡能力交接时，使用[Host—驱动—FPGA 案例](host-fpga-transfer-example.md)，并保留原生布局与真实停止/排空验证边界。
- 项目机制文档仍按模板完整说明自己的 §1–16；本例只展示设计方法，不是可复制的项目正文。
