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

## 1. SKU 标识、状态与目标场景

<details>
<summary>本节编写建议</summary>

给唯一 SKU、修订和面向的工作负载/客户环境，区分规划、可订购和已验证。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 2. 交付范围、包含项与排除项

<details>
<summary>本节编写建议</summary>

列箱内物、软件许可、服务与明确不包含项，避免采购后出现预期差异。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 3. 硬件、固件、软件与许可基线

<details>
<summary>本节编写建议</summary>

固定可订购配置与互相兼容的硬件/固件/软件/许可版本。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 4. 拓扑、容量、配额与扩展上限

<details>
<summary>本节编写建议</summary>

在固定负载、上下文和拓扑下给支持的容量及并发，区分原始算术上限、模型估算和实测产品声明。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 5. 兼容矩阵、选配与禁止组合

<details>
<summary>本节编写建议</summary>

逐选配说明支持版本、插槽/功热限制和明确禁止组合。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 6. 机械、环境、供电与散热要求

<details>
<summary>本节编写建议</summary>

给尺寸、重量、温湿度、输入功率、风道及测量条件，避免只列典型值。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 7. 制造、订购、BOM 与供应链边界

<details>
<summary>本节编写建议</summary>

标注文料、订购号、生产批次与替代器件批准范围，客户不应依据内部实验 BOM 下单。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 8. 性能与容量声明的证据等级

<details>
<summary>本节编写建议</summary>

逐 headline 指标写单位、配置、负载、统计窗口和 modeled/simulated/measured 证据，未测不得宣称支持。
规定原始记录的位置、标识、保留期限和与结论的关联，使摘要可以回到输入和观察事实复核。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 9. 生产、系统与客户验收 Gate

<details>
<summary>本节编写建议</summary>

区分出厂测试、整机验证和客户验收各自的阈值与批准责任。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 10. 版本、发布、替代和退市规则

<details>
<summary>本节编写建议</summary>

说明修订变更通知、兼容替代、最后下单及支持终止时间。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>
