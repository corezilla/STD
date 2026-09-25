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

## 1. 产品 Variant、Revision 与 BOM authority

<details>
<summary>本节编写建议</summary>

固定产品变体、板卡修订、批准 BOM 和生效批次，避免混用试制与量产物料。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 2. BOM

<details>
<summary>本节编写建议</summary>

逐料位列正式 P/N、封装、用量、制造商与版本，并与原理图和装配图互相核对。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

| Item | RefDes | Manufacturer | MPN | Description | Qty | Lifecycle | Approved alternatives |
|---|---|---|---|---|---:|---|---|
| <!-- TODO --> | | | | | | | |

## 3. 关键器件选型依据

<details>
<summary>本节编写建议</summary>

用电气、热、性能、供货与生命周期约束比较可行器件，说明推荐项的代价。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

记录电气/机械/热需求、derating、qualification、封装和工具支持。

## 4. Supply、Lead Time、MOQ、Cost 与 Lifecycle Risk

<details>
<summary>本节编写建议</summary>

记录来源、交期、起订量、成本及停产风险和证据日期，给采购备选 Gate。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 5. Alternate、Second Source 与 Compatibility Gate

<details>
<summary>本节编写建议</summary>

逐替代料定义引脚、电气、固件/驱动、热和认证兼容检查，未经 qualification 不自动等同。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 6. Compliance、Material Declaration 与 Counterfeit Control

<details>
<summary>本节编写建议</summary>

列适用法规、材料声明、来料检验和防假货追溯要求。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 7. Firmware/FPGA/Driver Compatibility

<details>
<summary>本节编写建议</summary>

把器件修订与可用固件、bitstream、驱动版本绑定，指出禁止组合和识别方法。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 8. Approved Vendor、Quote Evidence 与变更历史

<details>
<summary>本节编写建议</summary>

保存批准供应商、报价/样品证据、批准人和 BOM 变更原因，便于生产批次追溯。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>
