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

## 1. 目标、范围与交付产品

<details>
<summary>本节编写建议</summary>

列最终产品、主要工程交付和不在开发范围的工作，关联项目目标而非泛写“按期交付”。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

注明 software / firmware / FPGA / mixed domain。

## 2. 生命周期模型与开发方法

<details>
<summary>本节编写建议</summary>

说明阶段、迭代、冻结与反馈方式，哪类证据允许回到前一阶段修订。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 3. 组织、职责和 authority

<details>
<summary>本节编写建议</summary>

对需求、设计、实现、验证与发布分别指定负责、评审和批准人，避免 Owner 与 Approver 混淆。
将每项工作绑定责任人、协作方、触发时点和交付物；有冲突时说明升级与裁决路径。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 4. 工作分解、里程碑、依赖与资源

<details>
<summary>本节编写建议</summary>

把交付物拆为可检查任务，列前置条件、负责人、设备/人员资源和里程碑出口。
将每项工作绑定责任人、协作方、触发时点和交付物；有冲突时说明升级与裁决路径。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 5. 需求、设计、实现与集成方法

<details>
<summary>本节编写建议</summary>

解释各层文档和代码如何承接，公共接口何时冻结、如何集成以及设计缺口如何反馈。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 6. Coding/RTL/Documentation Standards

<details>
<summary>本节编写建议</summary>

列项目采用的强制规范、版本和索引位置，并说明豁免流程；不要复制规范全文。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. Toolchain、环境、版本与可重复构建

<details>
<summary>本节编写建议</summary>

写开发/CI 环境、工具版本、容器或设备、构建命令和产物摘要，使新 Agent 可复现。
说明谁可以提出和批准变更、受影响对象怎样识别、何时生效以及旧基线如何保留和回退。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. Review、Verification、Validation 与 Gate

<details>
<summary>本节编写建议</summary>

定义各阶段评审输入、独立验证、批准人和阻断条件；结构校验不能替代设计内容评审。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. 配置、变更、问题和缺陷管理

<details>
<summary>本节编写建议</summary>

引用唯一 CM/Issue 流程并说明开发阶段如何提交、分诊、修复、回归和关闭。
说明谁可以提出和批准变更、受影响对象怎样识别、何时生效以及旧基线如何保留和回退。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 10. 安全、质量、供应链与第三方依赖

<details>
<summary>本节编写建议</summary>

列安全/质量活动与第三方交付的检查点，包括 SBOM、许可、漏洞和器件替代。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 11. 发布、维护、迁移与退役

<details>
<summary>本节编写建议</summary>

说明交付后谁维护、版本兼容、数据迁移、回滚和退役责任，避免只计划首次发布。
说明谁可以提出和批准变更、受影响对象怎样识别、何时生效以及旧基线如何保留和回退。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 12. 度量、报告、风险与 Tailoring

<details>
<summary>本节编写建议</summary>

选与项目决策相关的指标、报告节奏和风险复审；裁剪须有明确决定而非自行省略。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
