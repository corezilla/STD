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

## 1. Security scope、资产与信任边界

<details>
<summary>本节编写建议</summary>

列需保护的资产、部署拓扑、攻击者可触达边界和项目安全责任，不用笼统“系统安全”代替范围。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 2. 威胁模型、攻击面与假设

<details>
<summary>本节编写建议</summary>

按入口和资产推演具体威胁、能力假设、影响及缓解；假设失效时必须复审控制。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 3. 身份、认证、授权与最小权限

<details>
<summary>本节编写建议</summary>

定义身份来源、授权判定点、角色/资源作用域和拒绝行为，避免只在 UI 隐藏操作。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 4. Secret、Key、Credential 与轮换

<details>
<summary>本节编写建议</summary>

说明生成、存储、分发、使用、轮换、撤销和泄露处置，禁止把凭据写进文档或构建产物。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 5. 数据分类、隐私、加密与隔离

<details>
<summary>本节编写建议</summary>

按数据级别给传输/静态保护、访问范围、保留删除及租户隔离要求。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 6. 软件、Firmware、FPGA、Hardware 和供应链安全

<details>
<summary>本节编写建议</summary>

分配各技术层的启动信任、接口防护、器件/依赖来源和漏洞处理责任。
逐项描述触发条件、影响范围、预防与发现手段、处置责任和关闭证据，不以风险名称代替措施。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 7. Secure Build、签名、更新与 Rollback Protection

<details>
<summary>本节编写建议</summary>

固定构建来源、签名链、版本单调性、升级失败回退和供应链证据。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 8. Logging、Audit、Detection 与 Incident Response

<details>
<summary>本节编写建议</summary>

定义安全事件、关联字段、脱敏、告警阈值、取证保留和响应职责。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 9. Security Verification、Pen Test 与 Evidence

<details>
<summary>本节编写建议</summary>

逐控制指定可执行验证和独立判据，说明渗透测试范围、环境及未覆盖的攻击面。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>

## 10. Vulnerability、Exception、Residual Risk 与 Gate

<details>
<summary>本节编写建议</summary>

记录漏洞分级、修复期限、例外批准和残余风险，明确何种开放项阻断发布。
把本节从原则落成可执行的安排：给出对象、适用条件、责任方、产物和决策门槛，避免只有岗位名或抽象承诺。

完成检查：读者应能据此确定下一步由谁在何时做什么、用什么证据判断完成；未决事项写明 Owner、最晚关闭 Gate 和引用。
</details>
