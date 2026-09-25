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

## 1. Release identity、日期与状态

<details>
<summary>本节编写建议</summary>

给唯一版本号、发布日期、候选/正式状态和适用产品配置。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 2. Included Configuration Items

<details>
<summary>本节编写建议</summary>

列代码、文档、硬件、固件、模型和数据迁移项的精确版本与摘要。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

| Item | Version/Revision | Commit/Hash | Build ID | Compatibility |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 3. 新功能、修复与行为变化

<details>
<summary>本节编写建议</summary>

按用户可观察结果说明变化、适用范围和对应需求/缺陷，不只列提交号。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 4. Breaking Change、Migration 与 Deprecation

<details>
<summary>本节编写建议</summary>

逐破坏性变化给旧行为、新行为、迁移步骤、期限及失败回退。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 5. Known Issues、限制与 Workaround

<details>
<summary>本节编写建议</summary>

列已知问题触发条件、影响、暂避动作和计划解决版本，不能把暂避写成修复。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 6. Build、Package、Bitstream、BOM 与 Provenance

<details>
<summary>本节编写建议</summary>

记录制品路径、签名/哈希、构建来源和物料组合，确保可复现发布包。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 7. Verification、Security、License 与 Release Evidence

<details>
<summary>本节编写建议</summary>

列测试范围、未测项目、漏洞/许可检查与批准证据，区分计划和实测。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 8. Install/Upgrade/Rollback Reference

<details>
<summary>本节编写建议</summary>

链接与此版本匹配的安装升级回滚指南，指出最低可升级版本和数据限制。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>
