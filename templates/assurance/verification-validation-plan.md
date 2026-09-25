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

## 1. 目标、范围与 V&V authority

<details>
<summary>本节编写建议</summary>

区分 Verification 是否按设计实现与 Validation 是否满足用户场景，固定各自范围和批准权。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 2. 被验证基线与环境

<details>
<summary>本节编写建议</summary>

列需求、设计、代码、硬件及数据的固定版本，以及环境拓扑和偏差处理。不同基线证据不能无条件合并。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

固定需求、设计、实现、硬件 revision、工具链、模型/数据和 commit。

## 3. Verification 方法

<details>
<summary>本节编写建议</summary>

逐要求选择分析、检查、仿真、演示或测试，说明独立判据和可接受证据。方法选择要与风险和可观测性相称。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

| Requirement | Analysis | Inspection | Demonstration | Test | Owner | Evidence |
|---|---:|---:|---:|---:|---|---|
| <!-- TODO --> | | | | | | |

## 4. Validation 场景与用户目标

<details>
<summary>本节编写建议</summary>

用实际角色、业务任务、部署条件和期望结果构造端到端场景；内部单元测试不能替代用户目标验证。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 5. 测试层级和责任边界

<details>
<summary>本节编写建议</summary>

分配模块、子系统、系统和验收层的用例与责任，说明局部证据如何承接但不自动关闭组合目标。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

Unit、Contract、Module、Subsystem、System、Recovery、Security、Performance、Qualification、Acceptance。

## 6. 环境、fixture、oracle 与数据治理

<details>
<summary>本节编写建议</summary>

定义可快速部署/复位的环境、受控替身、独立 Oracle、数据来源与敏感数据处理。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 7. 覆盖、采样、统计和判定规则

<details>
<summary>本节编写建议</summary>

规定需求/接口/状态/风险覆盖口径、样本与置信要求、通过阈值及缺口报告方法。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 8. 故障注入、恢复和非正常路径

<details>
<summary>本节编写建议</summary>

从依赖边界或受控时钟/调度制造故障，核对安全停止、结果已知性、恢复与资源释放。
分别写明故障如何发现、已发生的影响、停止与恢复条件、责任方和可观察证据，不用‘重试即可’代替安全推演。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 9. 偏差、waiver、问题与重测

<details>
<summary>本节编写建议</summary>

记录偏差/豁免批准、原失败、修复基线、重测和相邻回归范围，避免覆盖历史证据。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 10. Evidence package、traceability 与签署

<details>
<summary>本节编写建议</summary>

定义证据包目录、原始记录、摘要、追踪链和签署人；Gate 结论须能由逐项状态复算。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
