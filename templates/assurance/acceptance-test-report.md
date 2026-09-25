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

## 1. Acceptance 结论

<details>
<summary>本节编写建议</summary>

先给本次验收通过、条件通过或未通过的明确结论及适用范围，引用决定人和证据。不要用摘要掩盖未关闭条件。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

结论：accepted / conditionally-accepted / rejected / blocked。

## 2. 实际交付与 Configuration Baseline

<details>
<summary>本节编写建议</summary>

记录实际到场制品、硬件/软件/固件版本及摘要，与计划基线逐项比对。替换或现场修改须留下批准记录。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 3. 实际环境、参与者和执行时间

<details>
<summary>本节编写建议</summary>

写实际现场条件、仪器、数据、执行者/见证人及时间窗口，与计划的偏差单列。环境不足导致的无效执行不能计作失败或通过。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 4. Criteria Results

<details>
<summary>本节编写建议</summary>

逐验收条件列原始测量、Expected、Actual、判定和证据链接，引用相应 Requirement ID。汇总数必须能由逐项结果复算。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

| Criterion ID | Result | Measurement/Observation | Evidence | Deviation |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 5. Failure、Deviation、Waiver 与 Retest

<details>
<summary>本节编写建议</summary>

保留首轮失败、偏差/豁免批准、修复版本及重测结果的完整链条。重测通过不删除原始失败记录。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 6. Open Conditions、责任人和 Deadline

<details>
<summary>本节编写建议</summary>

每项开放条件写影响、Owner、最晚关闭时间、确认人和可验证的关闭证据。条件接受还要写未关闭前的使用限制。
将工作绑定责任人、协作方、触发时点、产物与冲突裁决路径，明确资源不足时的调整门槛。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 7. 交付物、记录和签署

<details>
<summary>本节编写建议</summary>

列出提交的报告、原始数据、配置快照、签署页和存档位置。签署范围须与第 1 节结论及开放条件一致。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
