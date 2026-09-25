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

## 1. 执行摘要与结论

<details>
<summary>本节编写建议</summary>

先给被测范围、通过/失败/阻断的真实结论以及是否满足本层 Gate。结论必须与后文逐项结果和未关闭缺陷一致。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 2. 被测基线与实际环境

<details>
<summary>本节编写建议</summary>

固定实际代码/制品/硬件版本、拓扑、数据和工具，与计划环境的差异单列。不同基线的结果不可直接合并统计。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 3. 执行记录

<details>
<summary>本节编写建议</summary>

逐 Case/Run 给执行时间、输入、Expected、Actual、判定、原始日志或测量链接。未运行、无效和环境阻断不能算通过。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

| Case ID | Run ID | Start/End | Result | Evidence | Defect/Blocker |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 4. 偏差、无效执行与重测

<details>
<summary>本节编写建议</summary>

说明每次偏离 procedure 的原因、批准、影响范围及重测用的新基线。保留无效或失败的原始记录。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 5. 缺陷、逃逸问题与风险

<details>
<summary>本节编写建议</summary>

将失败追到缺陷 ID、严重度、修复状态和残余风险，明确是否影响发布或上级验证。
为每项风险或保护要求写出触发条件、受影响资产、执行位置、拒绝或缓解动作和验证方法。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 6. 覆盖与 traceability

<details>
<summary>本节编写建议</summary>

由实际 Run 结果复算需求/接口/状态覆盖，列出缺口、孤儿用例和未测失败路径。计划覆盖不等于已执行覆盖。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 7. 测量结果、不确定度与限制

<details>
<summary>本节编写建议</summary>

对每个数值给单位、条件、样本量、不确定度和证据等级，说明适用边界及不能推断的性能。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 8. Release/Review Gate 建议

<details>
<summary>本节编写建议</summary>

基于明确阈值和开放问题给接受、条件接受或拒绝建议，列责任人和关闭证据；测试报告不越权替代批准决定。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
