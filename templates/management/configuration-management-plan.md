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

## 1. 范围、目标与 CM authority

<details>
<summary>本节编写建议</summary>

定义受控配置项范围、基线批准人和变更权，不把所有工作文件都称为发布基线。说明代码、文档、硬件与外部制品分别由谁管理。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 2. Configuration Item Registry

<details>
<summary>本节编写建议</summary>

逐 CI 给唯一 ID、路径/库、Owner、版本方式、依赖及保留要求。列表应能定位实际制品，而非只写类型。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

| CI ID | 类型 | Owner | Repository/Location | Identification | Baseline |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 3. Baseline、版本、标签和命名规则

<details>
<summary>本节编写建议</summary>

定义何时冻结、如何命名 tag/版本、谁批准以及怎样复现基线。文档版本与 Git 提交的关系应明确。
说明谁可以提出和批准变更、受影响对象怎样识别、何时生效以及旧基线如何保留和回退。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 4. Change Request、评估、批准与实施

<details>
<summary>本节编写建议</summary>

写出变更从提出到影响分析、批准、实施、复验和关闭的状态与责任。紧急变更也须保留补审路径。
按触发、输入、责任动作、输出和失败出口组织过程，让执行者可以逐步照做并知道何时停止。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 5. 状态记录、审计与 traceability

<details>
<summary>本节编写建议</summary>

规定 CI 状态、变更记录、需求/测试链接和审计频率，说明如何发现漏登记或版本不一致。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 6. Branch、Build、Release 和 Artifact 保留

<details>
<summary>本节编写建议</summary>

说明分支策略、构建输入、发布制品摘要及回滚保留期限；可从发布号追到源 commit 和工具链。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. Hardware Revision、BOM、Firmware 与校准数据一致性

<details>
<summary>本节编写建议</summary>

定义板卡修订、BOM、固件/bitstream 和设备校准数据的兼容矩阵及识别方法，防止现场混搭。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. Supplier、第三方组件与许可证

<details>
<summary>本节编写建议</summary>

记录外购件与第三方软件来源、版本、许可和替代审查要求，说明供应商变更如何触发复核。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. Access Control、备份和恢复

<details>
<summary>本节编写建议</summary>

定义基线写入/批准权限、凭据保护、备份频率及恢复演练，避免单一仓库或人员成为失效点。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 10. CM Review、度量和异常处理

<details>
<summary>本节编写建议</summary>

给审计项、频率、差异指标、责任人与纠正时限；发布前未关闭的配置异常须有批准决定。
写明检查对象、方法、判定门槛、执行频率和原始证据位置；计划中的检查与已完成的检查分开记录。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
