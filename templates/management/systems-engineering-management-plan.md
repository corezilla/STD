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

## 1. SEMP 目的、范围与项目背景

<details>
<summary>本节编写建议</summary>

说明本计划控制哪些技术决策与交付，引用项目目标和产品边界而不重复系统设计。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 2. 技术组织、职责、authority 与接口

<details>
<summary>本节编写建议</summary>

分配需求、架构、接口、集成与验证的决定权，明确跨团队争议如何裁决。
将每项工作绑定责任人、协作方、触发时点和交付物；有冲突时说明升级与裁决路径。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 3. 生命周期、技术阶段和评审 Gate

<details>
<summary>本节编写建议</summary>

列技术阶段、每个 Gate 的输入/退出标准和批准人，保证阶段结论有证据。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 4. Stakeholder Needs 与 Requirements Management

<details>
<summary>本节编写建议</summary>

说明需要如何转成可验证需求、怎样处理变更和冲突，并保持双向追踪。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 5. Architecture、Design 与 Logical Decomposition

<details>
<summary>本节编写建议</summary>

给系统到软件/固件/硬件的设计层级和约束分配规则，避免各下级独立改写系统政策。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 6. Interface、Configuration 与 Technical Data Management

<details>
<summary>本节编写建议</summary>

规定接口唯一权威、成员 ID、配置基线和数据/图纸保管，说明跨 Owner 变更影响。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. Integration、Verification、Validation 与 Transition

<details>
<summary>本节编写建议</summary>

说明集成顺序、局部到系统的证据承接、用户确认及运营交接责任。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. Decision Analysis、Trade Study 与 Technical Risk

<details>
<summary>本节编写建议</summary>

定义何时需要方案比较、评价指标、失败推演和决策记录，风险如何影响选择。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. Technical Budgets、Measures、Margins 与 Assessment

<details>
<summary>本节编写建议</summary>

将功耗、容量、延迟等总预算分配到下级，包含共同开销和余量并检查可组合性。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 10. Modeling、Simulation、Digital Artifacts 与 Toolchain

<details>
<summary>本节编写建议</summary>

定义模型/仿真用途、版本、假设、校准与工具链，区分 modeled、simulated 和 measured。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 11. Supplier、跨项目和软硬件协同管理

<details>
<summary>本节编写建议</summary>

给外部交付接口、验收基线和跨域变更协调方式，避免依赖方各自使用不同版本。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 12. Tailoring、合规映射与持续改进

<details>
<summary>本节编写建议</summary>

记录裁剪决定、适用依据、合规证据及复审节奏，不能用模板省略代替批准。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
