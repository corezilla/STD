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

## 1. Design、Device、Board 与 Toolchain Baseline

<details>
<summary>本节编写建议</summary>

固定 RTL commit、约束文件、目标器件/封装/板卡与工具版本，使后续数值可复现。与设计基线不一致的输入须单列。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

固定 RTL commit、IP version、part/package/speed grade、constraints 和工具版本。

## 2. Build Configuration 与 Reproducibility

<details>
<summary>本节编写建议</summary>

记录构建命令、参数、seed、脚本、环境和输出摘要；另一台受控机器应能重建等价结果。不可复现时说明差异来源。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 3. Synthesis Results

<details>
<summary>本节编写建议</summary>

给 LUT/FF/BRAM/DSP 等实际利用率、推断结构和关键警告，与预算及工具报告相连。只给百分比不写器件与配置不可用。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

| Resource | Used | Available | Utilization | Budget | Margin |
|---|---:|---:|---:|---:|---:|
| <!-- TODO --> | | | | | |

## 4. Implementation、Placement 与 Routing Results

<details>
<summary>本节编写建议</summary>

说明布局布线完成状态、关键区域/拥塞、资源变化和 DRC，附原始报告。综合通过不等于实现成功。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 5. Timing Closure

<details>
<summary>本节编写建议</summary>

列关键时钟、约束覆盖、WNS/TNS、最差路径与未约束路径，解释跨域和例外约束依据。局部时序收敛不得宣称板级性能已验证。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

记录 clocks、WNS/TNS、failing paths、exceptions、unconstrained paths 和 CDC/RDC 结果。

## 6. Power、Thermal 与 Activity Assumptions

<details>
<summary>本节编写建议</summary>

区分工具估算与板级实测，给活动率、负载、温度、风道及电压条件。结果应与上级功热预算在同一边界比较。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 7. DRC、Methodology、Lint、CDC 与 Formal Results

<details>
<summary>本节编写建议</summary>

逐检查类型列版本、覆盖范围、失败/豁免和证据，特别说明未检查的 CDC/RDC 路径。一个检查 PASS 不代表其他检查自动通过。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 8. Bitstream、Hash、Security 与 Programming

<details>
<summary>本节编写建议</summary>

记录 bitstream 摘要、签名/加密、生成来源及可编程目标，说明烧录和回读验证。测试使用的 bitstream 必须与报告绑定。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 9. Simulation、Hardware Test 与 Model Correlation

<details>
<summary>本节编写建议</summary>

分开仿真、软件模型和真实板测的输入、Oracle 和结果，记录不一致及其解释。仿真通过不能替代硬件负载证据。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>

## 10. Waiver、Known Limitation、Risk 与 Release Gate

<details>
<summary>本节编写建议</summary>

列出每个豁免的批准者、限制、到期 Gate 和残余风险。发布结论应明确可用范围与仍需完成的验证。
先固定被测对象及其版本、测试输入和环境条件，再给出独立判据、结果状态与原始证据位置；计划、执行和评审结论必须分开。

完成检查：另一位执行者应能复现或复核本节结论，并能区分 PASS、FAIL、BLOCKED、NOT_RUN 与不适用。
</details>
