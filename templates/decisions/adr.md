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

- Status: proposed / accepted / superseded / rejected
- Date: `{{date}}`
- Decision owners: <!-- TODO -->
- Supersedes: none

## Context

<details>
<summary>本节编写建议</summary>

用当前可观察事实说明必须做决定的原因、固定基线及不决策的后果。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

## Decision Drivers

<details>
<summary>本节编写建议</summary>

列功能、成本、风险、约束和时间等真正影响选项的指标，注明不可谈判条件。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

## Considered Options

<details>
<summary>本节编写建议</summary>

比较可行选项及代表性失败路径；不把明显不可能的稻草人方案当对照。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

## Decision

<details>
<summary>本节编写建议</summary>

明确选定方案、适用条件、禁止事项和生效版本，避免模糊“倾向采用”。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

## Consequences

<details>
<summary>本节编写建议</summary>

列得到的能力、付出的成本、遗留风险与下游必须承接的约束。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

分别记录收益、代价、风险、不可逆项和对上下游的影响。

## Verification and Evidence

<details>
<summary>本节编写建议</summary>

规定怎样证实决定的关键假设，给负责方、测试/分析入口及证据状态。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

## Rollback / Revisit Conditions

<details>
<summary>本节编写建议</summary>

写触发重新评审的事实、可否回退、数据/接口兼容风险和决定人。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>

## Traceability

<details>
<summary>本节编写建议</summary>

关联 Requirement、Constraint、设计章节、实现和验证 ID，不在 ADR 中复制另一份完整规范。
记录待决问题、可行选项、评价准则、采用方案及放弃其他选项的原因，保留生效边界和后续影响。

完成检查：后来者能理解当时为何这样决定，以及什么变化会使该决定失效。
</details>
