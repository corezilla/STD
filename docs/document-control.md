# STD 文档封面、版本与状态规范

## 1. 文档封面

每份 Markdown 正式文档必须在一级标题后显示以下字段；不能只存在 sidecar metadata：

| 字段 | 必填 | 规则 |
|---|---|---|
| Document ID | 是 | 项目内永久唯一，重命名文件时不改变 |
| Document Version | 是 | SemVer，格式 `MAJOR.MINOR.PATCH[-prerelease]` |
| Status | 是 | Draft / In Review / Approved / Released / Superseded / Retired |
| Project | 是 | 项目标识 |
| Authority | 是 | 对文档事实负责的项目或组织 |
| Document Owner | 是 | 维护与发起 Review 的责任人/角色 |
| Authors | 是 | 原作者和实质贡献者，可为多人 |
| Created Date | 是 | 首次创建日期，ISO 8601 `YYYY-MM-DD`，不可因迁移重置 |
| Last Modified Date | 是 | 最近一次实质内容变化日期，`YYYY-MM-DD` |
| Project Audit Timestamp | 否 | 项目审计/采集时间，ISO 8601 含秒和时区；不替代创建或修改日期 |
| Template ID | 是 | `templates/catalog.json` 中的稳定 ID |
| Template Version | 是 | 该 Template ID 独立维护的 SemVer |
| Repository | 是 | GitHub `owner/repository` 或批准的内部仓库标识 |
| Canonical Path | 是 | 仓库相对路径 |
| Supersedes | 是 | 无则写 `none` |

Reviewer、Approver、Approval Date 和 Release Tag 在进入 Review/Approved/Released 时填写。
Template Conformance、Tailoring Reference 和 Migration Map Reference 按采用规范填写并与 sidecar 一致。

## 2. 作者、Owner、Reviewer 和 Approver

- Author：实际撰写或实质修改内容的人；Agent 参与时按项目规则记录 Agent 和负责人。
- Document Owner：长期维护责任，不等同于 Git commit author。
- Reviewer：执行技术审查的人，不能因修改格式自动成为 authority。
- Approver：有权批准该文档状态的人或组织。
- Git author/committer：表示某次 repository change，不替代文档封面角色。

## 3. 文档版本

采用 SemVer：

- MAJOR：范围、authority、外部契约或核心行为出现不兼容变化；
- MINOR：增加兼容能力、章节、机制或重要验证内容；
- PATCH：不改变批准语义的澄清、勘误、链接和格式修复；
- prerelease：`draft.N`、`rc.N` 等尚未批准的候选版本。

示例：`0.3.0-draft.2` → `0.3.0-rc.1` → `0.3.0`。

文档版本、Template Version、项目采用的 STD 版本、产品版本和 Git tag 是不同字段，
不得互相代替。项目采用的 STD 版本在 README 和 `docs/std.lock.json` 中管理，不放入单份文档
封面或 sidecar metadata。

## 4. 三类状态必须分离

Review Verdict、Document Status 和 Runtime Activation 是三个独立 Gate，不得互相推导：

| 概念 | 取值 | 含义 |
|---|---|---|
| Review Record State | `PENDING / NOT_REVIEWED` | 非终局记录状态，不得触发 promotion |
| Review Verdict | `ACCEPTED / AMENDMENT / REJECTED / BLOCKED` | 对某一个固定 review packet 的终局审查结论 |
| Document Status | 见下表 | 文档本身的生命周期状态 |
| Runtime Activation | `true / false` | 变更是否已获得单独授权并进入运行基线 |

`Review Verdict = ACCEPTED` 不等于 `Document Status = accepted/Approved`，也不等于
`Runtime Activation = true`。Review verdict 只证明被评审的 packet 按其明示范围通过。文档升级和运行激活各自需要所属项目定义的完整条件。

Markdown 封面与 metadata 使用下列唯一映射：

| metadata `status` | 封面 `Status` |
|---|---|
| `draft` | Draft |
| `review` | In Review |
| `accepted` | Approved |
| `released` | Released |
| `superseded` | Superseded |
| `retired` | Retired |

STD 本身尚未绑定 immutable revision 时，仅“标准或迁移计划协调 review”可以得到
`Review Verdict = ACCEPTED`；项目 Migration Review Packet、正式候选和文档批准队列均不得开始。
锁定并机器核验完整 40 位 STD commit SHA 后，方可进入项目 Migration Review。

终局 review decision 必须至少有一个 reviewer、非空决定时间和理由；`PENDING / NOT_REVIEWED`
的 `decided_at` 必须为 `null`。任何 review record 都不能自行授权 Runtime Activation。

## 5. 文档状态机

```text
Draft → In Review → Approved → Released → Superseded → Retired
            ↘ Amendment → Draft
```

- Draft：可变草稿，不得作为冻结事实。
- In Review：内容和 review commit 已固定，修改后需要重新 Review。
- Approved：authority 已批准，但未必随产品发布。
- Released：绑定产品/repository release tag。
- Superseded：被明确的新文档/version 取代，仍保留历史。
- Retired：不再适用且无当前替代用途。

## 6. 日期规则

- Created Date 保留最初文档创建时间；从旧格式迁移到 STD 不重置。
- Last Modified Date 仅在实质内容变化时更新；纯索引、构建或换行不更新。
- Approved/Released 使用单独日期，不覆盖创建和修改日期。
- Git commit time 是外部证据，不直接写成 Last Modified Date。
- Project Audit Timestamp 只用于项目盘点、迁移采集或自动审计，格式如 `2026-09-07T12:34:56+08:00`；不得据此改写 Created Date 或 Last Modified Date。

## 7. Git commit 的自引用问题

文档无法在自己的内容中可靠记录“包含自己的 commit hash”，因为写入 hash 会产生新 commit。
因此：

- 封面记录 Repository、Canonical Path、Document Version 和 Release Tag；
- 候选文档 sidecar 可记录实际被评审的 `reviewed_commit`；内容变化后必须重新评审；
- merge 后由 publication/RAG manifest 记录不可变 canonical publication commit；
- Released 文档通过 signed/annotated tag 或 GitHub Release 绑定 commit；
- 不在文档或 sidecar 内写入“包含自身的 publication commit”，不得伪造或自引用。

## 8. 文件命名

- Living document 使用稳定、无日期路径，如 `system-design.md`、`recovery-mechanism.md`。
- 不因 PATCH/MINOR 版本每次复制新文件；历史由 Git 保存。
- 只有需要多个并行支持版本的外部契约可在文件名包含 major version，如 `api-v2.openapi.yaml`。
- 日期仅用于会议记录、测试执行报告、审计记录等天然事件型文档。
