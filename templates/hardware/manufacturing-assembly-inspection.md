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

## 1. 产品、Revision、范围与制造基线

<details>
<summary>本节编写建议</summary>

固定制造对象、板卡修订、批次和批准图纸/BOM，说明试制与量产工艺差异。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 2. Applicable Drawings、BOM、工艺和标准

<details>
<summary>本节编写建议</summary>

列受控图纸、装配文件、工艺规范与版本，禁止使用未批准副本。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 3. Material、器件、来料检验与可追溯性

<details>
<summary>本节编写建议</summary>

定义关键器件批次、真伪、来料检验和序列号追踪，说明不合格隔离。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 4. 制造与装配流程

<details>
<summary>本节编写建议</summary>

按工序给输入、设备、参数、检查点和放行条件，特别标出装配后不可再接触的部位。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

| Step | 输入 | 工装/参数 | 操作 | In-process check | Record |
|---|---|---|---|---|---|
| <!-- TODO --> | | | | | |

## 5. 焊接、清洁、防护和特殊工艺

<details>
<summary>本节编写建议</summary>

给温度/时间、清洁、防护和返工限制，关键参数需可记录。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 6. ESD、Safety 与环境控制

<details>
<summary>本节编写建议</summary>

规定静电、安全、温湿度及人员资格，给异常停止和纠正方法。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 7. Inspection、AOI/X-ray、尺寸与电气检查

<details>
<summary>本节编写建议</summary>

从典型缺陷反推检测方法、可达测试点、判退阈值及故障定位。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 8. Programming、Calibration 与 Serialization

<details>
<summary>本节编写建议</summary>

写烧录/校准顺序、版本校验、唯一序列号与结果回写，失败设备不能混入合格品。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 9. Nonconformance、Rework、Repair 与 Deviation

<details>
<summary>本节编写建议</summary>

定义偏差批准、返工次数、复验和报废条件，保留原始不合格记录。
以具体器件、板卡或制造对象为单位描述参数、约束、替代方案与验收方法，区分设计值、仿真值和实测值。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>

## 10. Acceptance、包装、存储、运输和交付记录

<details>
<summary>本节编写建议</summary>

给出厂判据、防护包装、环境限制和批次证据包，确认交付物可追溯。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：下游能够据此选择或制作对象，并知道超出限制时如何判退或提交变更。
</details>
