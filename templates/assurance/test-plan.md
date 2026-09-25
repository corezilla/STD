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

> 通过 metadata/profile 指明 system、subsystem、module、unit、contract 或其他测试层级。

## 1. 目标、范围与测试层级

<details>
<summary>本节编写建议</summary>

说明本计划验证哪些对象和需求，属于单元、集成、系统还是验收层，且明确不覆盖什么。测试层级不能互相冒充。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 2. 被测基线、排除项与依赖

<details>
<summary>本节编写建议</summary>

固定代码/文档/硬件配置和外部依赖的版本，列出排除项及批准依据。基线变化时定义需重跑的范围。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 3. Test Strategy 与 Coverage Model

<details>
<summary>本节编写建议</summary>

说明如何从需求、接口、状态与风险导出测试集合，哪些采用分析、仿真或实测。覆盖模型应能发现孤儿需求和未测失败路径。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 4. Test Item、Feature 与 Requirement Matrix

<details>
<summary>本节编写建议</summary>

逐测试项绑定 Requirement/Function ID、测试层级、责任和验证方法。矩阵只索引，不替代具体用例与判据。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 5. 环境、设备、拓扑、数据和工具

<details>
<summary>本节编写建议</summary>

列出足以复现的硬件、软件、网络拓扑、数据规模、工具版本和隔离方式。指出受共享资源或外部服务影响的条件。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 6. Test Types 与 Case Families

<details>
<summary>本节编写建议</summary>

按正常、边界、负向、并发、性能、恢复等分类说明代表输入和目的。每类应能落到具体 Case ID，不能只列测试类型名称。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

包括 normal、boundary、negative、concurrency、recovery、security、performance 和 endurance。

## 7. Entry、Exit、Pass、Fail、Blocked 和 Invalid Criteria

<details>
<summary>本节编写建议</summary>

定义开始/结束门槛及各结果状态的可判定条件，区分产品失败、环境阻断和执行无效。未运行不得以计划状态计通过。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 8. 组织、职责、排期和资源

<details>
<summary>本节编写建议</summary>

安排用例设计、环境提供、执行、见证和裁决的责任及时间，写明关键设备或人员冲突的处理。
将工作绑定责任人、协作方、触发时点、产物与冲突裁决路径，明确资源不足时的调整门槛。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 9. Defect、Deviation、Rerun 与 Regression

<details>
<summary>本节编写建议</summary>

定义缺陷登记、偏差批准、修复基线、重测及邻近回归规则。保留首轮失败和后续重测的关联。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 10. Evidence、Traceability、Reporting 与 Gate

<details>
<summary>本节编写建议</summary>

规定原始日志、测量、配置快照、报告和需求追踪的命名与保存方式。Gate 结论应能复算覆盖和未关闭问题。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 11. 风险、安全与清理恢复

<details>
<summary>本节编写建议</summary>

识别危险测试、敏感数据、资源耗尽和环境污染风险，写停止阈值、回滚/复位步骤及责任。
分别写明故障如何发现、已发生的影响、停止与恢复条件、责任方和可观察证据，不用‘重试即可’代替安全推演。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
