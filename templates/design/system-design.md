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

> 架构章节参考 arc42 v9.0，并加入软硬件工程、契约、恢复和验证附录。

## 1. 引言与目标

描述业务/研究目标、stakeholder、质量目标和成功标准。

## 2. 架构约束

记录技术、组织、法规、供应链、兼容性和既有实现约束。

## 3. 系统范围与上下文

定义系统边界、外部参与者、相邻系统、数据/控制/物理接口和 authority。

## 4. 解决方案策略

总结关键分解、技术选择、软硬件分工、buy/build 和主要 trade-off。

## 5. 构建块视图

按 system → subsystem → module 递归分解，并为每个块定义 owner、职责、禁止项和接口。

## 6. 运行时视图

至少覆盖主路径、并发路径、失败路径、恢复路径、启动/关闭和升级场景。

## 7. 部署与物理视图

包括进程、主机、容器、板卡、FPGA、GPU、网络/总线、存储和故障域映射。

## 8. 横切概念

覆盖身份权限、配置、日志、时间、错误、幂等、并发、资源管理和兼容性。

## 9. 架构决策

列出 ADR 及其状态，不在此处复制完整决定。

## 10. 质量要求

使用可测量场景定义性能、可靠性、安全、可维护性和可演进性。

## 11. 风险与技术债

## 12. 术语表

## A. 数据模型与状态机

## B. API、Schema、Event、寄存器与错误契约

## C. 持久化、一致性、幂等与恢复

## D. 安全、隐私、Secret 与审计

## E. 可观测性、容量、性能、资源与 SLO

## F. 测试设计与需求 traceability

## G. 集成、部署、迁移、回滚与发布 Gate

## H. 未决问题、外部依赖和后续版本
