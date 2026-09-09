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

<!--
编写建议：本模板解释数据的业务语义和 ownership；字段类型的机器权威仍是 Schema/IDL。
至少为关键对象给出一条合法示例和一条非法示例。示例值提交前必须替换。
编写规范见 docs/design-writing-guide.md。
-->

## 1. 用途、范围与 authority

说明谁生产和消费这些数据、解决什么歧义，以及对应机器契约的位置。

## 2. 命名、单位与通用规则

| Rule | Requirement | Example |
|---|---|---|
| 时间 | ISO 8601 UTC | `2026-09-09T08:30:00Z` |
| 容量 | 明确 SI 或 binary unit | `512 GiB` |
| ID | 稳定、不可复用 | `doc_01H...` |

## 3. Entity / Object Catalog

| ID | Name | Owner | Lifecycle | Persistence | Schema source |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 4. Field Dictionary

| Object.Field | Type | Required | Unit/Encoding | Range | Default | Meaning |
|---|---|---|---|---|---|---|
| <!-- TODO --> | | | | | | |

## 5. Enum、Status 与 Error Values

| Type | Value | Meaning | Producer | Consumer behavior for unknown value |
|---|---|---|---|---|
| DocumentStatus | `approved` | 已通过 authority 批准 | Review workflow | display as current |

## 6. Identity、Key、Reference 与 Ownership

说明主键、外键、幂等键、租户/项目 scope 和唯一写入 authority。

## 7. 数据关系与数据流

```mermaid
flowchart LR
    P[Producer] -->|Validated object| S[(Canonical store)]
    S -->|Projection| C[Consumer]
```

| Data | Producer | Validation | Store/Transport | Consumer | Derived output |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 8. Serialization、Alignment、Endianness 与 Compatibility

## 9. Persistence、Retention、Migration 与 Deletion

## 10. Validation 与 Examples

合法示例：

```json
{"id":"doc_01H...","status":"approved"}
```

非法示例及预期错误：

```json
{"id":"","status":"unknown-value"}
```

| Example/Test | Valid/Invalid | Expected result | Machine source |
|---|---|---|---|
| minimal valid | Valid | accepted | `fixtures/document.valid.json` |
| unknown status | Invalid | `ERR_STATUS` | `fixtures/document.invalid.json` |

## 11. 实现映射与变更计划

| Data/Schema | Source path | Generated type/code | Migration | Test |
|---|---|---|---|---|
| <!-- TODO --> | | | | |
