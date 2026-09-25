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

## 1. 解决的用户问题与场景

<details>
<summary>本节编写建议</summary>

从客户任务、实际使用者和痛点写起，给现状后果和目标结果。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 2. 范围、假设与非目标

<details>
<summary>本节编写建议</summary>

明确交付边界、部署前提与不承诺能力，重要假设须有验证方式。
先用一段话指出对象、场景与结果，再交代排除项和适用边界；不能让读者靠后续章节猜测本节目的。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 3. 解决方案概览与系统构成

<details>
<summary>本节编写建议</summary>

画逻辑组成和责任连接，逐组件说明作用；不要把内部芯片细节当解决方案架构。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 4. 部署拓扑、规模与选配

<details>
<summary>本节编写建议</summary>

给典型/最大部署、节点/网络、客户可选项及资源限制。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 5. 产品、客户与合作方责任边界

<details>
<summary>本节编写建议</summary>

说明安装、配置、数据、运维、支持由谁承担，跨边界失败时谁先响应。
将工作绑定责任人、协作方、触发时点、产物与冲突裁决路径，明确资源不足时的调整门槛。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 6. 接口、依赖和兼容性

<details>
<summary>本节编写建议</summary>

列外部接口与第三方依赖的版本、能力假设和失效行为，引用唯一契约。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 7. 容量、性能、功耗与成本边界

<details>
<summary>本节编写建议</summary>

在固定场景和配置下给可交付指标及证据级别，说明超限后的行为。
把用户任务与交付能力连接起来，写清适用场景、容量或性能边界及不承诺的情形；数字区分估算、仿真和实测。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 8. 安装、运行、升级和恢复

<details>
<summary>本节编写建议</summary>

概述客户从部署到日常运行、故障恢复和升级的关键流程与责任。
按触发、前提、执行动作、观察结果和异常出口展开一条代表路径，必要时附图或命令示例供读者核对。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 9. 验证、验收与交付物

<details>
<summary>本节编写建议</summary>

给场景对应的验收判据、证据和交付清单，避免只说“按合同验收”。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>

## 10. 风险、未决项与路线图关系

<details>
<summary>本节编写建议</summary>

列影响方案承诺的未知、Owner、关闭 Gate 及未来版本依赖。
为每项风险或保护要求写出触发条件、受影响资产、执行位置、拒绝或缓解动作和验证方法。

完成检查：读者能判断谁在何种条件下获得什么价值，以及该结论由哪些需求或证据支撑。
</details>
