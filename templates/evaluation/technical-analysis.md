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

## 1. 决策问题与目标

<details>
<summary>本节编写建议</summary>

把要回答的问题写成可比较的选项与判据，说明不分析会影响什么设计决定。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 2. 范围、边界与当前基线

<details>
<summary>本节编写建议</summary>

固定当前版本、拓扑、负载和排除项，防止不同条件的数据混用。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 3. 备选方案与对比维度

<details>
<summary>本节编写建议</summary>

列真正可行的方案、统一指标和硬约束，不能只对推荐方案详细分析。
给出候选、比较维度、固定假设和证据来源，再解释取舍及其代价；不要仅列优缺点或结论。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 4. 方法、数据源与可复现性

<details>
<summary>本节编写建议</summary>

给公式、脚本、原始输入、版本与复算步骤；引用来源而非只放最后数字。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 5. 假设、单位、拓扑与证据等级

<details>
<summary>本节编写建议</summary>

逐假设说明来源与敏感性，统一 SI/binary 单位、per-device/aggregate 范围，区分 modeled、simulated、measured。对会改变结论的假设给出替代值或区间，并展示结果对它的敏感程度；引用外部数据时保留版本和原始单位。

完成检查：读者能按相同拓扑、单位和证据等级复算关键数字，未测量的数据不会被误认为产品已验证指标。
</details>

对 modeled、simulated、estimated 和 measured 结果明确分类。

## 6. 结果与敏感性

<details>
<summary>本节编写建议</summary>

在相同条件下比较结果，并改变关键输入检验结论是否翻转；图表注明单位与误差。
给出候选、比较维度、固定假设和证据来源，再解释取舍及其代价；不要仅列优缺点或结论。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 7. 不确定性、限制和反例

<details>
<summary>本节编写建议</summary>

列模型未覆盖的机制、可推翻结论的反例及所需补测，不能把估算当实测。
给出候选、比较维度、固定假设和证据来源，再解释取舍及其代价；不要仅列优缺点或结论。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 8. Trade-off 与建议

<details>
<summary>本节编写建议</summary>

根据已声明判据解释推荐方案、代价及被放弃方案何时可能更好。
给出候选、比较维度、固定假设和证据来源，再解释取舍及其代价；不要仅列优缺点或结论。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 9. 验证 Gate 与后续行动

<details>
<summary>本节编写建议</summary>

把关键未知量转成测试/采购/评审任务，给 Owner、截止 Gate 和通过条件。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>

## 10. 需求、ADR、设计和证据追踪

<details>
<summary>本节编写建议</summary>

将分析结论映射到正式决定与下游约束，避免分析报告本身变成未经批准的设计 authority。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：读者可以按相同前提复算判断，并知道哪些新证据会触发复审。
</details>
