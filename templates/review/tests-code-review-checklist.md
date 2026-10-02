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

固定被审源码的 commit/版本、输入证据（设计/契约/issue 列表）和各领域评审者，意见必须绑定同一基线。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写「已检查」或「通过」。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>


## 2. Naming、Public Contract 与上游契约一致性


<details>
<summary>本节编写建议</summary>

对照设计文档（design.definition §9 / contracts.specification）核对被审源码的公开 API：命名、参数顺序与类型、可空性、返回类型、错误码、可空/非空、并发约束。源码不能脱离设计/契约自行发挥；每条被审证据绑定到上游设计 §/契约条目。

问题包括：定位到 X.Y（文件:行 或 接口 ID）+ 复现路径 + 修复责任 + 关闭条件，禁止只写通过；越界项标 BLOCKED。

完成检查：公开契约每个签名/错误码与上游文档一一对账；私有不暴露；每个公开 API、错误码、并发约束都对应上游条款。
</details>

- [ ] 公开函数/方法名、参数与返回与设计 §9 / contracts 完全一致
- [ ] 错误码 ID、消息、可空性严格遵守设计 §11 错误表/公共错误码（不允许擅自新建错误码）
- [ ] 接口参数顺序、类型、可空与不可空约束一致（不允许 nullable→non-nullable 的隐式放宽）
- [ ] 私有实现细节（内部状态、缓存结构、内部 helper）不暴露在公开契约里
- [ ] 公开方法的可重入/线程安全不证伪：要么文档声明非并发，要么实现真的无共享可变状态
- [ ] 过期/替代签名已删除或显式 deprecate，不存在可被静默调用的旧名
- [ ] 资源所有权/调用顺序与设计 §8 调用链一致
- [ ] 单元测试 Case 列表与方案 §3 VRC 对账（每个 VRC 至少一条对应 Case）


## 3. Error handling、错误路径与边界


<details>
<summary>本节编写建议</summary>

每个公开函数的失败路径必须显式返回或抛出契约中定义的错误，不允许吞错（catch-all + log + 假装成功）。边界输入（空/null/超长/超界/类型错）每种必有一条 Case 覆盖。

问题包括：定位到 函数 + 复现路径 + 修复 + 关闭条件。

完成检查：每个公开方法的错误路径与契约一一对账；吞错或静默 fallback 路径标 BLOCKED。
</details>

- [ ] 每个公开错误路径返回契约中定义的错误码/类型
- [ ] 没有 catch-all + log + 继续 假装成功的吞错写法
- [ ] 空输入/超长输入/类型错误/注入输入各自有对应 Case
- [ ] 资源获取失败时**不**部分初始化即返回错误对象（"部分初始化"是常见 bug）
- [ ] 错误返回路径**不**改变已提交的副作用（roll-forward 风险）
- [ ] panic/异常后残留不再写到调外部接口（assertion 失败不调用外部 API）


## 4. Resource、Concurrency 与副作用清理


<details>
<summary>本节编写建议</summary>

每个拿资源/锁/外部连接的代码路径必须显式释放，异常路径也释放（defer/go defer/finally）。并发路径锁粒度匹配设计 §10 死锁/活锁/超时要求。

问题包括：定位 + 竞态场景 + 死锁路径 + 释放路径不完整 + 不可重入副作用残留。

完成检查：异常路径 + 正常路径都有显式释放；并发路径可复现且不超时丢失更新。
</details>

- [ ] 锁/资源获取和释放配对（RAII/defer/finally）；异常路径也释放
- [ ] 锁粒度匹配设计 §10 死锁/活锁要求（无锁退化或多锁顺序文档化）
- [ ] 跨接口调用的副作用在异常时回滚（事务/补偿）
- [ ] 并发场景可复现：必有一种 Case 暴露竞态/死锁/超时丢失
- [ ] 全局/单例状态在多线程/多进程下的可重入性
- [ ] 资源泄漏的 finally 路径存在（即使正常路径也走到 finally）


## 5. Security 与敏感路径


<details>
<summary>本节编写建议</summary>

鉴权/权限/审计/脱敏/敏感数据路径**禁止借行为**——不能仅靠 review 时"似乎对"就放行；必须有可复现的 Case 覆盖拒绝路径。

问题包括：定位 + 攻击场景 + 越权证据 + 修复责任 + 关闭条件。

完成检查：敏感路径必有一组 Case 覆盖拒绝 + 审计 + 脱敏；绕过敏感检查的写法规为 BLOCKED。
</details>

- [ ] 鉴权/权限边界：调用前必有显式检查，且检查不可被旁路（如直接调用内部函数绕过 wrapper）
- [ ] 权限来源绑定到身份/会话，不绑定到 URL/参数/可被改写对象
- [ ] 敏感数据（密钥/凭据/隐私）**不**进 stdout、不回滚到日志、不出现在 trace
- [ ] prompt/参数注入（LLM 类组件适用）：输入侧隔离指令与数据、输出侧不返原始 prompt
- [ ] 跨接口调用不暴露内部权限范围
- [ ] 失败路径不留下可被重试绕过的半资源


## 6. Testability、可观察性与下游测试钩子


<details>
<summary>本节编写建议</summary>

被审代码必须可被测试覆盖，并为下游测试留出钩子：公开契约可注入替身/可重入；关键路径有对应 unit case（参见设计 §14 VRC）；运行期 + 故障期都可观测、可断言、可重放。

问题包括：定位 + 可测性缺口 + 观测缺口 + 缺钩子 + 修复责任。

完成检查：每个公开契约可被测试覆盖；关键路径在设计 §14 VRC 与方案 §3 清单中；关键路径能在测试中重放且可断言。
</details>

- [ ] 公开契约可注入替身（clock/registry/IO），无需改业务代码
- [ ] 关键路径在设计 §14 VRC 与方案 §3 清单有对应 Case
- [ ] 运行期与失败期都可观测、失败/边界路径可断言（不吞错、不静默 fallback）
- [ ] 单元层可重入（无全局可变状态或状态可重入）
- [ ] 测试 Case 与本 review 同一基线 commit（不是后续 fix 后再补 Case）
- [ ] 并发竞态可由代码 + 测试 case 主动重放


## 7. Issue Log


<details>
<summary>本节编写建议</summary>

每项问题写位置、风险、修复责任、目标修订与复核结果，保留原始意见。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写「已检查」或「通过」。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

| ID | Severity | Finding | Contract Source | Owner | 关闭条件 | Disposition |
|---|---|---|---|---|---|---|
| <!-- TODO --> | | | | | | |


## 8. Review Decision 与 Test Gate


<details>
<summary>本节编写建议</summary>

根据开放问题给通过、条件通过或返工结论，指出禁止开始测试的 blocker（code review 没通过 → plan §3「代码 review 通过」不通过 → 整个测试 BLOCKED）。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写「已检查」或「通过」。

完成检查：每个公开契约可被测试覆盖；code review 通过 → plan §3 可进入；code review 不通过 → 整个 §4 流程 BLOCKED。
</details>

| 项 | 结论 |
|---|---|
| Review Verdict | `PASS` / `CONDITIONAL PASS` / `REWORK` |
| 未关闭 BLOCKED 项数 | |
| 是否允许进入测试（plan §3「代码 review 通过」） | `通过` / `不通过` |
| Reviewer | |
| Approver | |
| Approval Date | |
</content>
