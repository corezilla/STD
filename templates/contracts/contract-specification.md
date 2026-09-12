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

## 1. Contract scope 与 authority

明确机器可读 contract 和说明文档哪个是字段级权威。

## 2. Operation / Message / Event Catalog

| ID | Kind | Producer | Consumer | Sync/Async | Idempotency |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

依 `docs/interface-data-mapping-standard.md` 使用目录里的接口族#成员 ID；逐方法定义完整请求、响应、事件及错误类型，关联身份、前置、校验顺序、副作用、确认/完成、期限/重复/取消和合法下一步。

| 成员 ID / 类别 | 机器源 / selector / 版本/revision/hash | request/response/event/error 类型 ID | 正文稳定锚点 | 下游提供/消费 / 实现 / 设计 V → Case |
|---|---|---|---|---|

## 3. Request、Response、Event 与数据对象

引用 OpenAPI、JSON Schema、Proto、IDL 或 ABI；禁止只给示例不给约束。

## 4. 状态、错误和 blocker catalog

## 5. 幂等、并发、事务与一致性

## 6. Pagination、filter、ordering 与 retention

## 7. 身份、权限、Secret 与多项目隔离

## 8. 版本、兼容性与迁移

绑定消费方的实际 version/revision/hash；ID 不变不等于兼容。字段改名、枚举/错误变化、删除和替代对照旧基线逐项记录，废弃 ID 不回收，多 backend 分别迁移和验证。

## 9. Positive/Negative fixture 与 validator

## 10. Requirement → Contract → Test traceability

## 11. Activation Gate 与未决项
