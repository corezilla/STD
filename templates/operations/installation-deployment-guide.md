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

## 1. 范围、版本与目标环境

<details>
<summary>本节编写建议</summary>

固定适用产品版本、平台、部署拓扑和权限，列不支持的环境。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 2. Architecture、Topology 与依赖

<details>
<summary>本节编写建议</summary>

画安装涉及的节点、网络和外部服务，说明启动顺序及依赖失效时的行为。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 3. Hardware/Software/Firmware Prerequisites

<details>
<summary>本节编写建议</summary>

列最低资源、系统版本、固件和访问要求，并给实际检查命令。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 4. Package、Image、Bitstream 与 Integrity Check

<details>
<summary>本节编写建议</summary>

列获取位置、版本、签名/摘要及校验步骤，未通过不得继续安装。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 5. 安装、部署、烧录或装配步骤

<details>
<summary>本节编写建议</summary>

按可执行顺序写命令、参数、预期输出和超时，区分首次安装与覆盖升级。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 6. 配置、Secret、Certificate 与权限

<details>
<summary>本节编写建议</summary>

说明配置来源、受保护凭据的注入方式、权限检查和生效点，不在文档填写真实密钥。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 7. 数据初始化、Migration 与 Compatibility

<details>
<summary>本节编写建议</summary>

写空数据与旧数据两条路径、备份、转换、拒绝和失败回滚。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 8. Verification、Smoke Test 与 Acceptance

<details>
<summary>本节编写建议</summary>

给可执行健康检查、代表请求、Expected 和失败处置，不能只写“启动成功”。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 9. Upgrade、Rollback 与 Disaster Recovery

<details>
<summary>本节编写建议</summary>

固定可升级/可回退版本、数据兼容、触发阈值及恢复验证，避免回退程序却保留不兼容数据。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 10. Uninstall、Cleanup 与交付记录

<details>
<summary>本节编写建议</summary>

说明停止、卸载、保留/删除数据和凭据、环境恢复以及交接记录。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>
