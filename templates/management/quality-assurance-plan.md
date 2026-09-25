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

## 1. 质量目标、范围与适用标准

<details>
<summary>本节编写建议</summary>

选择与产品风险相称的质量目标和标准版本，说明每项目标如何测量。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 2. 组织独立性、职责与 authority

<details>
<summary>本节编写建议</summary>

定义 QA 与开发/验证的独立性、审计权、阻断权及争议升级路径。
将每项工作绑定责任人、协作方、触发时点和交付物；有冲突时说明升级与裁决路径。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 3. Process、Product 与 Evidence Assurance

<details>
<summary>本节编写建议</summary>

区分流程遵循、产品质量和证据完整性检查，分别给抽查频率与失败处理。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 4. 文档、需求、设计和代码/RTL Review

<details>
<summary>本节编写建议</summary>

规定不同对象的评审入口、清单、批准人和缺陷关闭条件；模板结构通过不等于内容合格。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 5. Verification、Validation 与 Test Assurance

<details>
<summary>本节编写建议</summary>

检查测试计划、独立 Oracle、环境、原始记录和结论一致性，区分验证与确认。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 6. Supplier、器件、工具和第三方质量

<details>
<summary>本节编写建议</summary>

说明供应件、工具链、外包交付的准入、变更监控及不合格处理。
写明检查对象、方法、判定门槛、执行频率和原始证据位置；计划中的检查与已完成的检查分开记录。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. Nonconformance、Defect、CAPA 与 Waiver

<details>
<summary>本节编写建议</summary>

给不符合项从发现、遏制、根因、纠正预防到关闭的流程，豁免须有残余风险批准。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. 配置审计、发布审计与记录保留

<details>
<summary>本节编写建议</summary>

核对发布制品与批准基线、许可证及验证证据，并规定记录摘要和保留期限。
说明谁可以提出和批准变更、受影响对象怎样识别、何时生效以及旧基线如何保留和回退。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. Metrics、抽查、报告和 Gate

<details>
<summary>本节编写建议</summary>

定义少量可用于决策的质量指标及采样方法，报告必须指出未关闭问题和 Gate 影响。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 10. Tailoring 与改进

<details>
<summary>本节编写建议</summary>

逐项记录裁剪依据、批准、复审时间和过程改进反馈，不以“项目小”免除关键质量责任。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
