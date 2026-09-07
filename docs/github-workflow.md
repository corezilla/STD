# STD GitHub 文档协作规范

## 1. Repository 与 Branch

- 默认分支保存当前 canonical 文档，不直接提交未经 Review 的设计变化。
- 文档修改使用短生命周期分支：`docs/<document-id>-<topic>`。
- STD 迁移推荐使用分支和 PR；临时迁移目录不是默认的长期文档结构。
- release/default branch 建议启用保护规则，限制 force-push 和删除。

## 2. Commit

STD 约定提交标题：

```text
docs(<scope>): <imperative summary>
```

每个 commit 保持单一可审阅目的。机械路径迁移与语义设计修改尽量拆分，避免 reviewer 无法判断
内容变化。发布基线建议使用 GitHub 可验证的 signed commit/tag。

## 3. Pull Request

PR 必须包含：

- Document ID 和旧/新 Document Version；
- changed files 与 path move；
- Current Baseline、Approved Delta 和明确非目标；
- Requirement/Interface/Test/ADR 影响；
- 兼容性、安全、恢复和迁移影响；
- validator 命令与结果；
- blockers、open questions 和期望决定。

使用 `.github/PULL_REQUEST_TEMPLATE/document-change.md`。Draft PR 可用于早期协作；进入正式
Review 前固定候选版本和完整 evidence。

## 4. CODEOWNERS 与 Ruleset

- 在 `.github/CODEOWNERS` 为系统设计、硬件、FPGA、接口、安全和测试路径指定 owner。
- CODEOWNERS 文件自身也必须有 owner。
- 默认分支 ruleset 至少要求 Pull Request、CODEOWNER/授权 reviewer approval、required status
  checks、conversation resolution，并禁止未授权 bypass。
- 新提交使已审 diff 变化时，应撤销或重新要求 approval。

GitHub 支持通过 CODEOWNERS 自动请求相应 owner Review，并可在 protected branch/ruleset 中
要求 Code Owner approval 和 status checks。

## 5. Required Checks

最低检查：

```text
std-validate
link-check
schema-contract-check
traceability-check
```

涉及硬件/FPGA/软件时按需增加 BOM、ERC/DRC、lint、CDC/RDC、synthesis、unit/contract/system
tests。检查结果必须对应 PR head commit。

## 6. Merge、Tag 与 Release

- 只有 Approved 文档才能随产品 release 合并/标记为 Released。
- Review Verdict、Document Status 和 Runtime Activation 是独立 Gate；PR approved 或
  `Review Verdict = ACCEPTED`不自动升级文档状态，也不自动激活 runtime 变更。
- Canonical promotion 必须在一个可审查变更中同时更新新文档、索引、旧文档
  Superseded/historical 状态与 RAG inclusion/exclusion，并验证不存在两份 current authority。
- 部分迁移必须按明确 scope 切换 authority。只迁出旧文档的一部分时，旧文档继续作为未迁移
  scope 的 current authority，并在旧、新文档及 migration map 中写清 scope 边界；只有全部 scope
  都已迁移且索引/RAG 不再把旧文档解释为 current，才可把整份旧文档标为 Superseded。
- 项目版本 tag 使用项目既有规则；STD 发布建议使用 `std-vMAJOR.MINOR.PATCH`。
- Release tag 指向包含相应文档版本的 commit，推荐 annotated/signed tag。
- merge 后 RAG 只索引 default/release branch 的 canonical commit，不索引未保存编辑器内容。

## 7. 大型和二进制工程文件

原理图、PCB、CAD、波形、bitstream 和大型测试数据若无法有效文本 diff，应：

- 同时提交可审查的文本导出、版本/hash 和生成工具信息；
- 按项目策略使用 Git LFS；
- PR 中说明 GitHub 无法直接渲染的内容如何本地 Review；
- 不以截图替代机器可校验的源文件和报告。
