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

## 1. 范围、版本、安全与维护权限

<details>
<summary>本节编写建议</summary>

界定适用版本、可维护对象、人员资格和危险操作的批准边界。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 2. System Health、Indicators 与 Diagnostic Entry

<details>
<summary>本节编写建议</summary>

列指示灯、状态页、日志、统计和诊断命令的执行位置、正常值和采样条件。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 3. Preventive Maintenance

<details>
<summary>本节编写建议</summary>

按使用时长或状态触发预防维护，给步骤、工具、阈值与完成验证。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 4. Symptom → Cause → Action Matrix

<details>
<summary>本节编写建议</summary>

从用户可见症状出发按安全顺序排查可能原因，每个动作给判定分支而非盲目替换。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

| Symptom/Error | Evidence to collect | Probable cause | Safe action | Escalation |
|---|---|---|---|---|
| <!-- TODO --> | | | | |

## 5. Software、Firmware、FPGA 与 Hardware Diagnostics

<details>
<summary>本节编写建议</summary>

按层级给检查入口、期望结果和故障隔离边界，注明不会更改现场证据的只读步骤。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 6. Replace、Repair、Reflash、Reconfigure 与 Calibration

<details>
<summary>本节编写建议</summary>

写更换和修复的授权、版本匹配、备份、校准与复验步骤。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 7. Data Protection、Backup 与 Recovery

<details>
<summary>本节编写建议</summary>

说明维护前后保护哪些数据、备份校验、恢复顺序及敏感信息处理。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 8. Known Issues、Workaround 与 Prohibited Actions

<details>
<summary>本节编写建议</summary>

逐已知问题给适用版本、暂避条件、风险和绝对禁止动作；不能把 workaround 写成永久修复。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 9. Post-maintenance Verification 与 Service Record

<details>
<summary>本节编写建议</summary>

给功能/安全复测、测量值、部件序列号和维修记录，确认设备可重新交付。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 10. Escalation、RMA、Log Package 与 Closure

<details>
<summary>本节编写建议</summary>

定义本地无法处理时的升级条件、脱敏日志包、RMA 资料与关闭确认人。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>
