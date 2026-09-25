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

## 1. Board/System Revision、目标与安全边界

<details>
<summary>本节编写建议</summary>

固定首板或整机修订、目标配置和本次允许的上电范围，写清停止阈值与安全责任。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 2. Required Equipment、Firmware、Bitstream 与 Fixture

<details>
<summary>本节编写建议</summary>

列仪器、夹具、校准状态和固件/bitstream 摘要，确保操作针对同一硬件组合。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 3. Visual、BOM、Assembly 与 Resistance Pre-check

<details>
<summary>本节编写建议</summary>

按上电前顺序检查装配、极性、短路和关键电阻值，给预期范围与异常停止动作。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 4. Power Rail Bring-up Sequence

<details>
<summary>本节编写建议</summary>

逐 rail 写输入、使能顺序、测量点、容差和超时，异常时停止后续上电并保留读数。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

| Step | Rail/Signal | Limit | Expected | Actual | Evidence |
|---|---|---:|---|---|---|
| <!-- TODO --> | | | | | |

## 5. Clock、Reset、Boot、JTAG 和 Programming

<details>
<summary>本节编写建议</summary>

说明时钟与复位释放条件、烧录步骤、启动日志及失败恢复，不把 JTAG 可连通等同于系统就绪。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 6. Interface、Memory、PCIe/Network 与 Peripheral Check

<details>
<summary>本节编写建议</summary>

按依赖顺序验证链路、存储和外设，给操作命令、预期状态和错误定位入口。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 7. Firmware/FPGA/Driver Integration

<details>
<summary>本节编写建议</summary>

固定各组件版本和兼容组合，记录加载顺序与共同检查项，局部通过不代表整机集成通过。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 8. Functional、Performance、Thermal 与 Stability Check

<details>
<summary>本节编写建议</summary>

用规定负载、环境和时间窗口检查基本功能及性能/热稳态，区分估算与实际测量。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 9. Failure Isolation、Abort Limit 与 Recovery

<details>
<summary>本节编写建议</summary>

按症状提供安全排查顺序、禁止动作、断电/复位条件与证据收集，避免带故障反复上电。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>

## 10. Calibration、Serialization、Evidence 与 Release Gate

<details>
<summary>本节编写建议</summary>

记录校准系数、序列号、原始测量、操作者和 Gate 结论，保证每块实物可追溯。
按操作者的实际顺序写前置条件、执行入口、预期反馈、失败分支和恢复办法；命令、权限及适用版本应可核对。

完成检查：值班人员不依赖作者口头解释，也能判断能否开始、何时停止以及如何保存操作证据。
</details>
