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

## 1. 接口目的、范围与双方 authority

## 2. 接口注册表

| Interface ID | Provider | Consumer | 类型 | Version | Status |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

按 `docs/interface-data-mapping-standard.md` 注册族和成员，不另编与机器目录不同的编号。编目范围说明 entry_only、selected_members 或 complete 的分母及遗漏；状态不等于实现通过。

| 接口族#成员 ID / 类别 | 机器源 / selector / 版本/revision/hash | 正文 Document ID / 版本 / 稳定锚点 | 编目范围/缺口 | 下游提供/消费 / 模块 / 设计 V / Case |
|---|---|---|---|---|

## 3. 传输与物理边界

按需描述 function call、HTTP、message、file、PCIe、AXI、pin、connector 或 mechanical datum。

## 4. 数据、命令与 Schema

逐对象保留完整机器源阅读视图及类型/字段 ID，给类型、单位、范围、必填/默认/null、条件有效性、数组计数及兼容；真实二进制 ABI 才补 endianness/alignment。标准接口注明标准号/版本/适用部分和项目绑定，不能仅贴标准链接。

## 5. 状态机、顺序和时序

## 6. 错误、timeout、重试、幂等和恢复

## 7. 并发、流控、容量与性能

## 8. 安全、身份、权限和隔离

## 9. 版本协商、兼容矩阵与弃用

## 10. Contract fixture、验证与证据

## 11. 未决项与双方批准
