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

## 1. 产品愿景、范围与时间边界

<details>
<summary>本节编写建议</summary>

说明要服务的客户任务、产品边界和规划期限，区分已批准承诺与探索性方向。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 2. 当前基线与已批准承诺

<details>
<summary>本节编写建议</summary>

固定当前发布版本、已实现能力及正式承诺来源，不把目标能力写成现状。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 3. 阶段、里程碑与可交付结果

<details>
<summary>本节编写建议</summary>

每阶段写用户可见结果、前置 Gate、决定人及可验收证据，避免只列日期。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 4. 能力、SKU 和解决方案演进

<details>
<summary>本节编写建议</summary>

按能力和 SKU 说明新增、变更、淘汰及适用场景，明确兼容关系。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 5. 依赖、前置 Gate 与责任人

<details>
<summary>本节编写建议</summary>

列技术、供应、验证与外部合作依赖，注明 Owner 和依赖失败时的调整路径。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 6. 兼容、弃用、替代和迁移计划

<details>
<summary>本节编写建议</summary>

给旧用户/数据/接口的过渡期、替代方案与最终停止支持条件。
将工作绑定责任人、协作方、触发时点、产物与冲突裁决路径，明确资源不足时的调整门槛。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 7. 验证、发布与运行准入条件

<details>
<summary>本节编写建议</summary>

说明性能、可靠性、安全及运行证据达到什么程度才能对外承诺。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 8. 风险、不确定性与决策时点

<details>
<summary>本节编写建议</summary>

把未知量、调查任务、影响和最晚裁决时间写清，不把待定项硬塞进发布日期。
为每项风险或保护要求写出触发条件、受影响资产、执行位置、拒绝或缓解动作和验证方法。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 9. 需求、ADR、项目计划和发布追踪

<details>
<summary>本节编写建议</summary>

连接产品意图与正式需求、设计决定、计划和发布记录，不让 roadmap 成为唯一技术权威。
将工作绑定责任人、协作方、触发时点、产物与冲突裁决路径，明确资源不足时的调整门槛。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>
