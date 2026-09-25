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

## 1. 目标、范围与风险 appetite

<details>
<summary>本节编写建议</summary>

说明哪些风险类型在本计划内、可接受程度和需要升级的损失边界，区分风险与已发生问题。
写出适用对象、明确排除项和可判定的目标，说明本节结论将约束哪一阶段或哪一类决策。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 2. 角色、authority 与升级机制

<details>
<summary>本节编写建议</summary>

明确发现、评估、处理和接受残余风险的不同责任及升级时限，高风险不能由实施者自行关闭。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 3. 识别、分析、排序和复审方法

<details>
<summary>本节编写建议</summary>

说明如何从设计、测试、供应和运行证据识别风险，按统一尺度排序并定期复审。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 4. 评分与阈值

<details>
<summary>本节编写建议</summary>

定义概率、影响、可探测性或其他评分维度的具体等级及行动阈值，避免只有颜色没有决策。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

定义 likelihood、impact、detectability、时间窗口和聚合规则。

## 5. Risk Register

<details>
<summary>本节编写建议</summary>

每项风险写事件、原因、后果、触发指标、Owner、状态和证据，不把解决方案当成风险描述。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

| Risk ID | Cause | Event | Consequence | Score | Response | Trigger | Owner | Status |
|---|---|---|---|---:|---|---|---|---|
| <!-- TODO --> | | | | | | | | |

## 6. Mitigation、Contingency 与 Residual Risk

<details>
<summary>本节编写建议</summary>

区分降低发生概率的措施、事件发生后的应急动作和措施后仍存的风险，分别给验证与批准。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. 技术、进度、成本、安全和供应风险

<details>
<summary>本节编写建议</summary>

按项目真实威胁覆盖跨领域风险，特别记录同一原因对多条计划的共同影响。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. 与 Issue、Assumption、Decision 和 Gate 的关系

<details>
<summary>本节编写建议</summary>

说明风险何时转为问题、假设怎样被验证、决策如何改变评分及何时阻断 Gate。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. 报告、审计和关闭标准

<details>
<summary>本节编写建议</summary>

规定复审频率、报告对象、关闭证据与重新打开条件，残余风险接受须可追溯。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
