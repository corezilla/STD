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

## 1. Acceptance scope、合同/需求基线与双方 authority

<details>
<summary>本节编写建议</summary>

固定验收对象、合同/需求版本与双方的决定权，区分供应方自测和客户验收。说明哪些结果构成接受，哪些超出本次范围。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 2. Deliverables 与 Configuration Baseline

<details>
<summary>本节编写建议</summary>

逐交付物列名称、版本、摘要及配置项关系，保证现场测试和签署针对同一套制品。缺失或替换制品时写明重新确认方式。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 3. Acceptance Criteria

<details>
<summary>本节编写建议</summary>

将每条验收条件绑定 Requirement ID、测量条件、阈值及判定方法，避免“功能正常”一类不可判定表述。未满足的条件不得靠口头解释转为通过。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

| Criterion ID | Requirement | Method | Threshold | Evidence | Approver |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 4. 环境、现场条件、设备和数据

<details>
<summary>本节编写建议</summary>

记录现场拓扑、设备校准、软件/固件版本、测试数据及环境范围。说明这些条件偏离时结果是否有效和谁批准例外。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 5. Test Sequence、Procedure 与责任分工

<details>
<summary>本节编写建议</summary>

按依赖顺序引用可执行 procedure，列出执行者、见证人和客户确认点。说明中断、重启及现场资源冲突时如何恢复。
将工作绑定责任人、协作方、触发时点、产物与冲突裁决路径，明确资源不足时的调整门槛。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 6. Deviation、Waiver、Failure 与 Retest

<details>
<summary>本节编写建议</summary>

分别定义偏差、豁免、失败及重测的处理和批准权，保留原失败证据。重测须说明修复基线和需回归的相邻范围。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 7. 数据、记录、交付和保留

<details>
<summary>本节编写建议</summary>

指定原始数据、日志、测量结果和签署记录的保存位置、格式、校验值及保留期限。报告结论应能追到原始记录。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 8. Acceptance Gate、签署与条件

<details>
<summary>本节编写建议</summary>

列出 Gate 的进入条件、开放项、条件接受限制和双方签署动作。未完成条件必须有 Owner、期限和关闭证据。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
