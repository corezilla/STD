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

## 1. 目的与范围

<details>
<summary>本节编写建议</summary>

说明收集的是哪类相关方的需要、适用产品阶段和决策用途，不提前把需要写成实现方案。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

说明需要解决的问题、产品边界和本文件不构成设计实现的部分。

## 2. Stakeholder 与使用者

<details>
<summary>本节编写建议</summary>

区分购买/批准者、实际使用者、运维者和受影响者，记录各自任务和 authority。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

| ID | Stakeholder | 目标 | 责任/authority | 成功表现 |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 3. 使用场景与痛点

<details>
<summary>本节编写建议</summary>

用真实业务情境描述谁在何时遇到什么障碍及其后果，避免只写“提高效率”。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

## 4. Needs

<details>
<summary>本节编写建议</summary>

逐 Need ID 表述期望的可观察结果与优先级，保留原始来源和冲突，不把偏好直接变成设计决定。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

| Need ID | Need statement | 来源 | Priority | Rationale | Acceptance signal |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

Needs 使用业务或用户语言，不提前规定不必要的实现方案。

## 5. 运行环境与生命周期期望

<details>
<summary>本节编写建议</summary>

记录部署环境、负载、人员技能、培训、维护和退役条件，说明它们如何影响使用。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

## 6. 质量、成本、进度与合规期望

<details>
<summary>本节编写建议</summary>

给期望范围、限制条件、来源及可谈判空间；数值目标区分愿望和已批准约束。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

## 7. 假设、依赖、冲突与未决问题

<details>
<summary>本节编写建议</summary>

逐项写影响、责任方、验证或裁决方法和截止 Gate，避免在后续需求中掩盖分歧。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

## 8. Need → Requirement 映射

<details>
<summary>本节编写建议</summary>

把每条需要映射到具体 Requirement ID 或说明尚待转化，检查无来源需求和无承接需要。
说明划分依据、每个对象的责任及相互关系，让对象能从名称追到唯一来源，不以目录或名词堆叠代替关系。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>
