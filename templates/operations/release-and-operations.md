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

## 1. Release scope、版本与兼容性

<details>
<summary>本节编写建议</summary>

固定本次交付范围、版本、支持平台与接口/数据兼容边界，区分已发布和候选能力。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 2. 构建、制品、SBOM/BOM 与来源证明

<details>
<summary>本节编写建议</summary>

逐制品绑定源提交、构建环境、摘要、签名及组件清单，保证现场可验证来源。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 3. 部署/安装/烧录/装配步骤

<details>
<summary>本节编写建议</summary>

给明确顺序、命令/工序、参数、预期结果及中止条件，不把“参见 CI”当现场步骤。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 4. 配置、Secret、校准数据与环境

<details>
<summary>本节编写建议</summary>

说明配置和校准数据来源、生效点、权限与敏感信息处理，禁止在文档写实际凭据。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 5. Preflight、Bring-up 与健康检查

<details>
<summary>本节编写建议</summary>

列部署前检查、首次启动顺序、就绪信号与代表请求，区分进程运行和服务可用。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 6. 升级、迁移、回滚和恢复

<details>
<summary>本节编写建议</summary>

写旧版/新版组合、数据备份、转换、失败阈值与回退验证，避免不兼容数据无法回滚。
分别写明故障如何发现、已发生的影响、停止与恢复条件、责任方和可观察证据，不用‘重试即可’代替安全推演。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 7. 操作、监控、告警与 SLO

<details>
<summary>本节编写建议</summary>

给日常指标、统计口径、告警阈值和响应动作，说明适用负载与环境。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 8. 故障诊断、维护与更换

<details>
<summary>本节编写建议</summary>

按症状链接或写出诊断步骤、权限、安全停机和更换后的验证。
分别写明故障如何发现、已发生的影响、停止与恢复条件、责任方和可观察证据，不用‘重试即可’代替安全推演。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 9. 数据保留、备份、审计与安全

<details>
<summary>本节编写建议</summary>

明确保留/删除、备份恢复、访问审计与事件处置责任。
以稳定名称或签名作为主索引，列出取值、约束、输入输出与错误语义；引用唯一机器来源时只补人读意图，不重复维护字段定义。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 10. Acceptance、交接与退役

<details>
<summary>本节编写建议</summary>

列验收证据、开放项、接收方、培训与退役清理，交接前未关闭条件须有 Owner 和期限。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>
