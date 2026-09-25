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

> 项目计划模板。所有不适用项必须写 `N/A` 并说明理由。

## 1. 目标、范围与成功标准

<details>
<summary>本节编写建议</summary>

给产品/项目边界、主要交付及可检验成功条件；将未承诺的工作列为非目标。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

- 业务/研究目标：<!-- TODO -->
- 范围内：<!-- TODO -->
- 范围外：<!-- TODO -->
- 可验证成功标准：<!-- TODO -->

## 2. Stakeholder、组织与 authority

<details>
<summary>本节编写建议</summary>

区分需求提出者、交付 Owner、审查者与批准者，说明跨组织争议由谁裁决。
将每项工作绑定责任人、协作方、触发时点和交付物；有冲突时说明升级与裁决路径。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

| 角色 | 责任 | 决策 authority | 升级路径 |
|---|---|---|---|
| <!-- TODO --> | | | |

## 3. 生命周期、里程碑与 Gate

<details>
<summary>本节编写建议</summary>

列每个 Gate 的输入、输出、签署人与阻断项，保证里程碑不是只有日期。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

| 阶段 | 输入 | 交付物 | Exit criteria | Owner |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 4. 工作分解、依赖与计划

<details>
<summary>本节编写建议</summary>

按可交付结果拆分工作、关键依赖、资源及缓冲，说明延期时的重排规则。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

记录 WBS、关键依赖、并行边界、关键路径和外部交付。

## 5. 工程与管理计划

<details>
<summary>本节编写建议</summary>

索引开发、质量、安全、配置与验证计划的唯一版本，并说明彼此的适用范围。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

引用需求、架构、接口、V&V、安全、质量、配置、供应链和数据管理计划。

## 6. 风险、问题与机会

<details>
<summary>本节编写建议</summary>

把具体风险/问题绑定影响、Owner、处理策略和复审时间；不要只给颜色评分。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

| ID | 描述 | 可能性 | 影响 | 处置 | Owner | Gate |
|---|---|---:|---:|---|---|---|
| <!-- TODO --> | | | | | | |

## 7. 配置、变更与版本

<details>
<summary>本节编写建议</summary>

说明项目基线、变更批准、版本标识及发布制品追踪，引用 CM 详细规则。
说明谁可以提出和批准变更、受影响对象怎样识别、何时生效以及旧基线如何保留和回退。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

定义配置项、基线、审批者、变更流程、版本规则和回退要求。

## 8. 沟通、评审与报告

<details>
<summary>本节编写建议</summary>

规定会议/评审产物、报告频率、接收者及需升级的事件，避免消息没有责任闭环。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

定义例会之外的正式记录、评审包、决策记录及跨项目通信渠道。

## 9. 资源、成本、采购与供应

<details>
<summary>本节编写建议</summary>

列关键人员、设备、预算和长交期采购，明确供应变化对里程碑的影响。
将每项工作绑定责任人、协作方、触发时点和交付物；有冲突时说明升级与裁决路径。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

包括人员、设备、算力、器件、长交期项、替代料和预算假设。

## 10. Tailoring 与未决项

<details>
<summary>本节编写建议</summary>

逐裁剪和未决决定写依据、批准人、影响与关闭 Gate；不能把缺失输入当作 N/A。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

引用 tailoring manifest，并列出尚未关闭的关键决定。
