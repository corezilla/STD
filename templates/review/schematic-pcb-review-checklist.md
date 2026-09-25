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

## 1. Review scope、Revision、Inputs 与 Reviewers

<details>
<summary>本节编写建议</summary>

固定板卡/原理图/PCB/BOM 修订、输入证据和各领域评审者，意见必须绑定同一基线。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 2. Schematic Checklist

<details>
<summary>本节编写建议</summary>

逐电源、时钟、复位、保护、接口和可测试性检查，记录具体页/网名及通过或问题证据。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

- [ ] 电源树、上电/掉电顺序和保护完整
- [ ] Clock、Reset、strap、boot 和 programming 路径完整
- [ ] Interface pin、方向、电平、终端和 reference voltage 正确
- [ ] 器件 P/N、封装、NC/DNI 和未用引脚处理明确
- [ ] Test point、debug、measurement 和 bring-up 能力充分

## 3. PCB Stack-up、Placement 与 Routing Checklist

<details>
<summary>本节编写建议</summary>

检查叠层、阻抗、关键器件布局、回流路径、差分线和制造公差，问题定位到层/区域。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

- [ ] Stack-up、阻抗、参考平面和回流路径已冻结
- [ ] 高速 topology、长度、skew、via 和 loss 满足约束
- [ ] 电源完整性、去耦、铜厚、电流和热路径满足预算
- [ ] BGA breakout、器件 keepout、机械和装配间距可制造
- [ ] DFM/DFT、panelization、fiducial 和测试点满足生产要求

## 4. SI/PI、Thermal、Mechanical 与 EMC Evidence

<details>
<summary>本节编写建议</summary>

核对模型条件、仿真/实测报告及上级预算，不能用局部 PASS 替代整机条件。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 5. BOM、Supply、Lifecycle 与 Alternate Review

<details>
<summary>本节编写建议</summary>

检查关键料号、封装、供货、替代料与软硬件兼容 Gate。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 6. Issue Log

<details>
<summary>本节编写建议</summary>

每项问题写位置、风险、修复责任、目标修订与复核结果，保留原始意见。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

| ID | Severity | Finding | Evidence | Owner | Disposition |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 7. Review Decision 与 Release Gate

<details>
<summary>本节编写建议</summary>

根据开放问题给通过、条件通过或返工结论，指出禁止投板/发布的 blocker。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>
