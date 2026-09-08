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

## 1. 目标、范围与输入冻结

列出系统需求、接口/ABI、器件与板卡约束，以及输入的冻结状态。

## 2. 设计 authority 与架构不变量

## 3. Top-level、clock domain 与模块 owner

## 4. 数据面、控制面与主运行流

## 5. Host/Device Interface、CSR 与寄存器

## 6. 内部协议、队列、ordering 与 backpressure

## 7. Clock、Reset、CDC/RDC 与时序约束

## 8. Memory、DMA、buffer 与一致性

## 9. 资源预算、频率、吞吐、延迟与功耗

所有预算注明器件、工具版本、约束、利用率假设和证据等级。

## 10. 错误、隔离、恢复与可观测性

## 11. 仿真、形式验证、综合、实现和板级验证

## 12. 软件模型/仿真器对齐与校准

定义共同 contract、golden reference、误差口径和板卡实测回填方式。

## 13. Platform Profile 与可移植边界

## 14. 实现状态、变更控制与 Review Gate
