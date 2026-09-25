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

## 1. Procedure ID、目的与适用 Case

<details>
<summary>本节编写建议</summary>

固定 procedure 与 Case ID 的关系，说明这套步骤验证的具体行为和不适用范围。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 2. 被测版本、环境与安全前置条件

<details>
<summary>本节编写建议</summary>

写出执行前必须确认的版本、拓扑、权限和安全状态；前置不满足时不得继续，并记录原因。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 3. Equipment、Tool、Fixture 与数据

<details>
<summary>本节编写建议</summary>

列仪器校准状态、工具版本、夹具连接和输入数据摘要，保证他人能重放同一条件。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 4. Setup 与 Preflight

<details>
<summary>本节编写建议</summary>

按执行顺序给环境部署、配置加载、健康检查和初始状态确认，附可观察的通过条件。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

| Step | Action/Command | Expected observation | Evidence |
|---|---|---|---|
| <!-- TODO --> | | | |

## 5. Execution Steps

<details>
<summary>本节编写建议</summary>

每一步写操作者动作、输入、等待/超时、应见输出和证据采集点，不让执行者猜下一步。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

每一步都记录输入、操作、预期结果、实际结果和证据位置。

## 6. Cleanup、Restore 与可重复性

<details>
<summary>本节编写建议</summary>

说明正常和异常结束后的资源释放、状态复位、数据清理和再次运行前的检查。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 7. Abort、Failure 与异常处置

<details>
<summary>本节编写建议</summary>

定义安全停止阈值、失败时保留的证据和恢复顺序；禁止为了完成步骤忽略危险信号。
分别写明故障如何发现、已发生的影响、停止与恢复条件、责任方和可观察证据，不用‘重试即可’代替安全推演。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 8. Data Reduction、计算和判定

<details>
<summary>本节编写建议</summary>

写明原始测量如何换算为结果、单位/舍入/不确定度及 Pass/Fail Oracle，避免只填主观结论。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 9. 执行者、见证人、时间与签署

<details>
<summary>本节编写建议</summary>

记录实际执行人、见证人、时间、环境偏差和签署范围，保证记录可审计。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
