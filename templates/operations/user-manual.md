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

## 1. 产品简介、目标读者与适用版本

<details>
<summary>本节编写建议</summary>

用用户语言说明产品解决什么任务、适合谁使用、适用版本及不支持的用途。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 2. Safety、Security 与使用限制

<details>
<summary>本节编写建议</summary>

把用户必须先知道的危险、权限和数据保护边界放在操作前，给明确禁止动作。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 3. 系统要求、包装内容与准备工作

<details>
<summary>本节编写建议</summary>

列最低设备/浏览器/网络条件、随附物和准备清单，说明如何确认满足。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 4. 安装、连接、登录与首次配置

<details>
<summary>本节编写建议</summary>

按新用户实际顺序写操作、画面/命令反馈与常见失败处理，不假设读者知道内部架构。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 5. Quick Start

<details>
<summary>本节编写建议</summary>

用一条最短且安全的真实任务从准备走到可见结果，标出输入样例和成功判据。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 6. 主要任务与工作流

<details>
<summary>本节编写建议</summary>

逐主要业务任务写触发、步骤、预期输出、取消和错误恢复，必要时配截图或流程图。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

按用户目标组织步骤，不按内部模块组织。

## 7. 配置、输入、输出和数据管理

<details>
<summary>本节编写建议</summary>

说明用户可改配置、输入格式、输出位置、保留/删除和权限边界。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 8. 状态、通知、错误和恢复

<details>
<summary>本节编写建议</summary>

将每种用户可见状态/错误映射到含义和可执行下一步，不暴露不稳定内部异常文本。
分别写明故障如何发现、已发生的影响、停止与恢复条件、责任方和可观察证据，不用‘重试即可’代替安全推演。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 9. 日常维护、升级和备份

<details>
<summary>本节编写建议</summary>

给普通用户可执行的维护动作、备份验证和升级前后的兼容检查。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 10. Troubleshooting 与 Support

<details>
<summary>本节编写建议</summary>

按症状给安全排查顺序和升级支持时需提供的脱敏信息。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 11. 权限、隐私、合规和注意事项

<details>
<summary>本节编写建议</summary>

解释账户角色、数据可见范围、隐私处理和需要用户承担的合规责任。
为每项风险或保护要求写出触发条件、受影响资产、执行位置、拒绝或缓解动作和验证方法。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 12. Glossary、FAQ 与 Reference

<details>
<summary>本节编写建议</summary>

只收录用户实际遇到的术语和常问问题，外部参考链接应指向当前版本。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>
