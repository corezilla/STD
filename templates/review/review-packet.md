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

## 1. Review 请求与期望决定

<details>
<summary>本节编写建议</summary>

开篇写清请审什么、需要批准/修改/拒绝哪项决定，以及不在本次评审范围的动作。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

送审前使用 PENDING / NOT_REVIEWED；最终决定只允许：ACCEPTED / AMENDMENT / REJECTED / BLOCKED。

| Gate | 请求/结果 |
|---|---|
| Review Verdict | PENDING / NOT_REVIEWED / ACCEPTED / AMENDMENT / REJECTED / BLOCKED |
| Document Status before review | Draft / In Review / Approved / Released / Superseded / Retired |
| Requested Document Status after review | 填写状态，或`unchanged` |
| Runtime Activation requested | `true / false` |
| Runtime Activation authority | 填写独立授权人或`N/A` |

> `Review Verdict = ACCEPTED` 不会自动将文档升为 Approved，也不会自动激活 runtime 变更。

## 2. Scope、authority 与 reviewers

<details>
<summary>本节编写建议</summary>

列文档/代码范围、唯一权威和所需专业评审人，避免遗漏接口另一侧 Owner。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 3. 冻结基线

<details>
<summary>本节编写建议</summary>

固定提交、文件清单、摘要、STD 模板版本和测试环境，保证意见对应同一候选。
固定可复查的来源、版本与配置条件，分清已确认事实和工作假设；变化时列出需要重新检查的项目。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

列出 repository、commit、文件、版本和 SHA-256。

## 4. 变更摘要与设计理由

<details>
<summary>本节编写建议</summary>

按重要决定说明旧状、候选方案、取舍和下游影响，不用提交路径清单代替设计解释。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 5. Requirement、Design、Contract、Test 对齐

<details>
<summary>本节编写建议</summary>

抽样或逐项检查需求到设计、机器契约、实现和验证的追踪，特别标出无承接项。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 6. 风险、未决项和不阻塞项

<details>
<summary>本节编写建议</summary>

区分必须修复的 blocker、可附条件接受项和后续改进，逐项给 Owner 与 Gate。
为每项风险或保护要求写出触发条件、受影响资产、执行位置、拒绝或缓解动作和验证方法。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

## 7. 验证命令与结果

<details>
<summary>本节编写建议</summary>

给可复现命令、工作目录、基线、exit code 和证据位置，失败不得被摘要掩盖。
把每项检查连到对象与独立判据，列出环境、代表输入、预期与结果证据；局部通过不能推导总体通过。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

分开记录 STD structural validation、项目 contract/schema validation 和 runtime/external dependency evidence。每条记录原始命令、原始退出码、关键输出、artifact 路径和执行 commit。

## 8. Review Checklist

<details>
<summary>本节编写建议</summary>

用针对本类文档的可判定问题检查内容质量；打勾须指向具体章节或证据。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>

- [ ] scope 与 authority 清楚
- [ ] 现状、批准变更和未来设想未混写
- [ ] 接口、错误、状态和恢复已闭合
- [ ] 安全与隔离已评审
- [ ] traceability 和证据可打开
- [ ] 未发生静默 fallback 或兼容性扩张

## 9. 决定、条件与签署

<details>
<summary>本节编写建议</summary>

记录批准/修订/拒绝、适用摘要、条件、批准人和时间，不能把 PENDING 当 ACCEPTED。
围绕固定版本的被审对象记录检查方法、观察事实、判定和关闭责任，避免只写‘已检查’或‘通过’。

完成检查：评审意见可定位、可复现；每项未关闭问题有 Owner、关闭条件和再次审查入口。
</details>
