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

## 1. Safety scope、目标与适用法规

<details>
<summary>本节编写建议</summary>

界定人员、设备和环境的安全目标、产品边界、法规及适用版本。信息安全另按相应安全架构/计划处理，不相互替代。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 2. Safety roles、独立性与 authority

<details>
<summary>本节编写建议</summary>

指定危险分析、设计措施、独立复核和残余风险接受的责任及资格。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 3. Hazard Identification and Analysis

<details>
<summary>本节编写建议</summary>

从使用、故障、维护和误操作场景识别危险源、后果和触发条件，保持 Hazard ID 可追溯。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

| Hazard ID | Cause | Hazardous state | Consequence | Severity | Control | Verification |
|---|---|---|---|---|---|---|
| <!-- TODO --> | | | | | | |

## 4. Safety Requirements 与 Architecture Controls

<details>
<summary>本节编写建议</summary>

把危险控制转为可验证需求和系统级防护，写明预防、检测、隔离和安全状态。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 5. Fault、Failure、FMEA/FTA 与安全状态

<details>
<summary>本节编写建议</summary>

分析单点与共同原因故障、检测覆盖及转入安全状态的时间和条件。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 6. Hardware、Software、Firmware 和操作安全

<details>
<summary>本节编写建议</summary>

分配各技术域及操作人员的控制责任，确保保护链和维护操作不互相抵消。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. Safety Verification、Evidence 与 Case

<details>
<summary>本节编写建议</summary>

逐 Hazard/Requirement ID 指定分析、仿真、测试和独立证据，说明安全论证的未关闭缺口。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. Incident、变更影响与残余风险接受

<details>
<summary>本节编写建议</summary>

定义事故报告、遏制、根因、设计变更复评和残余风险批准，保留原始事实。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. 生命周期 Gate、签署与记录保留

<details>
<summary>本节编写建议</summary>

列关键 Gate 的安全输入、签署人和阻断条件，并规定记录保留与审计路径。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
