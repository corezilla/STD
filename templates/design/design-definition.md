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

> 适用于 subsystem、module、component 和 implementation-unit；具体层级写入 metadata。

## 1. 目的、范围与上位输入

## 2. Ownership 与边界

- 负责：<!-- TODO -->
- 不负责：<!-- TODO -->
- authority：<!-- TODO -->
- 上级设计与需求：<!-- TODO -->

## 3. Current Baseline 与 Approved Delta

分别记录当前真实实现、已批准变更和未批准设想，不得混写。

## 4. 设计概览与主流程

用短文和图说明“做什么、怎么做、在整条链路中的位置”。

## 5. 内部分解与依赖

列出组成部分、允许/禁止依赖、调用方向和单一 owner。

## 6. 接口与契约

列出 provided/consumed interface，引用 ICD、API、Schema、ABI 或寄存器定义。

## 7. 数据、状态与生命周期

定义状态 authority、读写者、状态机、持久化、缓存和一致性。

## 8. 控制流、并发与时序

覆盖主路径、分支、排序、并发、timeout、backpressure 和取消。

## 9. 失败、恢复与可观测性

定义错误分类、重试/幂等、部分失败、恢复点、日志、指标和 artifact。

## 10. 资源、容量、性能与限制

## 11. 安全与隔离

## 12. 实现映射与变更范围

列出代码/RTL/原理图/CAD/BOM 等实现位置，以及允许修改的范围。

## 13. Verification、测试义务与证据

| Requirement | Design element | Verification method | Evidence | Status |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 14. Review Checklist、未决项与 Gate
