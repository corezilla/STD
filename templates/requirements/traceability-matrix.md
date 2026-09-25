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

## 1. 范围与基线

<details>
<summary>本节编写建议</summary>

固定参与追踪的需求、设计、实现和验证基线及版本，说明哪些对象不在矩阵内。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

固定需求、设计、契约、实现和测试的版本或 commit。

## 2. Traceability Matrix

<details>
<summary>本节编写建议</summary>

逐 ID 映射来源、上/下游对象和验证入口，保持双向可查；引用唯一权威，不在矩阵重写定义。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

| Need | Requirement | Design | Interface/Contract | Implementation | Verification/Test | Evidence | Status |
|---|---|---|---|---|---|---|---|
| <!-- TODO --> | | | | | | | |

## 3. Coverage Rules

<details>
<summary>本节编写建议</summary>

规定什么算已设计、已实现、已验证及何时允许 N/A，明确多对多映射的计数口径。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

- `covered` 必须存在可打开且判定有效的 evidence；仅有测试名称不算覆盖。
- `failed/blocked/invalid/not-run` 不得标成通过。
- 上游变化必须能找到受影响的下游设计、实现和测试。

## 4. Orphan、Gap 与冲突

<details>
<summary>本节编写建议</summary>

列出无来源需求、未承接需要、未验证约束和互相矛盾的链接，给 Owner 与关闭动作。
把期望转成可识别的主体、触发条件、行为、边界和验收观察，说明来源与优先级；不要把主观形容词当作可验证要求。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>

## 5. Review、冻结与更新记录

<details>
<summary>本节编写建议</summary>

记录复核人、冻结版本、变更原因和受影响链接，确保矩阵可与对应提交和评审证据重建。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：下游能够分配责任与验证项，冲突或未决定的要求能追到责任人和裁决入口。
</details>
