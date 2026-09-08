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

## 1. Review 请求与期望决定

送审前使用 PENDING / NOT_REVIEWED；最终决定只允许：ACCEPTED / AMENDMENT / REJECTED / BLOCKED。

| Gate | 请求/结果 |
|---|---|
| Review Verdict | PENDING / NOT_REVIEWED / ACCEPTED / AMENDMENT / REJECTED / BLOCKED |
| Document Status before review | Draft / In Review / Approved / Released / Superseded / Retired |
| Requested Document Status after review | 填写状态，或`unchanged` |
| Runtime Activation requested | `true / false` |
| Runtime Activation authority | 填写独立授权人或`N/A` |

> `Review Verdict = ACCEPTED` 不会自动将文档升为 Approved，也不会自动激活 runtime 变更。

## 2. Scope、authority 与 reviewers

## 3. 冻结基线

列出 repository、commit、文件、版本和 SHA-256。

## 4. 变更摘要与设计理由

## 5. Requirement、Design、Contract、Test 对齐

## 6. 风险、未决项和不阻塞项

## 7. 验证命令与结果

分开记录 STD structural validation、项目 contract/schema validation 和 runtime/external dependency evidence。每条记录原始命令、原始退出码、关键输出、artifact 路径和执行 commit。

## 8. Review Checklist

- [ ] scope 与 authority 清楚
- [ ] 现状、批准变更和未来设想未混写
- [ ] 接口、错误、状态和恢复已闭合
- [ ] 安全与隔离已评审
- [ ] traceability 和证据可打开
- [ ] 未发生静默 fallback 或兼容性扩张

## 9. 决定、条件与签署
