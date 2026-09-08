<!-- STD_DOCUMENT_COVER_BEGIN -->
# {{document_title}}

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

固定需求、设计、契约、实现和测试的版本或 commit。

## 2. Traceability Matrix

| Need | Requirement | Design | Interface/Contract | Implementation | Verification/Test | Evidence | Status |
|---|---|---|---|---|---|---|---|
| <!-- TODO --> | | | | | | | |

## 3. Coverage Rules

- `covered` 必须存在可打开且判定有效的 evidence；仅有测试名称不算覆盖。
- `failed/blocked/invalid/not-run` 不得标成通过。
- 上游变化必须能找到受影响的下游设计、实现和测试。

## 4. Orphan、Gap 与冲突

## 5. Review、冻结与更新记录
