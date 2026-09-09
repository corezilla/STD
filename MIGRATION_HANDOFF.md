# STD 首批项目迁移 HANDOFF

更新时间：2026-09-09
STD 路径：`/Users/ben/work/STD`  
STD 版本：`0.1.0-draft.25`

适用会话：Slinky、Piko、LLMTier、HIFM

## 1. 任务目标

把当前项目已有设计文档逐步迁移到 STD 模板结构。迁移是结构化整理和缺口补齐，不是重新
发明设计，也不是以公共模板覆盖项目已经冻结的事实、authority、接口 ID 或评审结论。

每个项目会话只修改自己负责的项目仓库；不得借迁移读取、修改或替其他项目批准设计。

## 2. 开始前必须读取

1. 当前项目的 instructions、memory、HANDOFF 和权威文档索引；
2. `/Users/ben/work/STD/README.md`；
3. `/Users/ben/work/STD/docs/template-selection.md`；
4. `/Users/ben/work/STD/docs/adoption.md`；
5. `/Users/ben/work/STD/docs/repository-layout.md`；
6. `/Users/ben/work/STD/docs/document-control.md`；
7. `/Users/ben/work/STD/docs/github-workflow.md`；
8. `/Users/ben/work/STD/docs/versioning.md`、`docs/coding-standard.md` 与
   `docs/design-writing-guide.md`；
9. `/Users/ben/work/STD/templates/catalog.json` 与 `templates/path-policy.json`；
10. 与当前文档类型对应的具体模板；
11. `/Users/ben/work/STD/schemas/document-metadata.schema.json`、
    `schemas/std-lock.schema.json`、`schemas/std-source-manifest.schema.json`与
    `schemas/review-decision.schema.json`。

规划阶段允许项目 `std.lock.json` 的 `source_revision` 暂时为 `null`，并使用
`docs/std-source-manifest.json`独立锁定模板、Schema、工具和规范的 SHA-256。该文件不是 RAG manifest。
但在发出迁移 READY、生成正式候选或进入 Migration Review 前，必须锁定 STD 完整 40 位 commit SHA；
可另记经过机器验证且 peel 到该 commit 的 annotated tag，不能用 `HEAD`、branch 或 tag 名代替 commit SHA；
没有 immutable revision 的 packet 不得进入批准队列。

三类状态必须分离：

```text
Review Verdict = ACCEPTED
≠ Document Status = accepted / Approved
≠ Runtime Activation = true
```

迁移协调的 `Review Verdict = ACCEPTED` 仅表示所评审的标准或计划已达成共识；候选文档仍按项目
批准 Gate 管理，且 `Runtime Activation` 默认为 `false`。

## 3. 不变约束

- 保留当前实现基线、已批准变更、未批准设想三者的区别。
- 保留现有 Requirement、Interface、Error、Test Case、ADR 和 Review ID。
- 保留项目内的单一 authority；公共模板不获得项目业务决策权。
- 不为了匹配模板引入新 runtime mechanism、fallback、config path 或兼容分支。
- 不把估算、模型预测、仿真结果写成实测结果。
- 不把 draft、历史版本或 superseded 文档提升为当前事实。
- 缺少内容时写明确 TODO、Open Gate 或 N/A + rationale，不得编造。
- 原文档在迁移通过 review 前不得删除；优先产生新文件或可审阅 diff。
- 部分迁移按 scope 切换 authority；不得因一个章节迁出就把仍承载其他 current scope 的整份旧文档标为 Superseded。

## 4. 通用迁移步骤

### Step 1：盘点

在 PR 描述、项目既有管理目录或 `docs/00_management/migrations/` 建立
`current-document-inventory.md`，至少记录：路径、文档类型、authority、状态、版本、
上位/下位关系、重复项、冲突项和建议 STD Template ID。

### Step 2：裁剪

使用 `management.tailoring` 生成 tailoring manifest，逐项决定 keep、simplify 或 omit，并说明
理由和风险。不要要求每个项目启用全部模板。

### Step 3：锁定 STD 来源

把 `/Users/ben/work/STD/examples/std.lock.example.json` 复制为项目 `docs/std.lock.json`，填写单值
`project_profile` 和 `enabled_domains`，并锁定本 HANDOFF 指定的 immutable STD revision。另外生成并校验独立来源清单：

```bash
/Users/ben/work/STD/scripts/build-source-manifest \
  --output <project>/docs/std-source-manifest.json
/Users/ben/work/STD/scripts/verify-source-manifest \
  <project>/docs/std-source-manifest.json \
  --std-root <checkout-of-the-locked-STD-revision>
```

`std-source-manifest.json`在 Migration Review 开始前生成；
`rag/project-ingestion-manifest.jsonl`只在 Canonical Promotion 完成后生成。两者不得共用文件名或 Gate。

### Step 4：生成候选文档

示例：

```bash
/Users/ben/work/STD/scripts/new-design \
  --project <project> \
  --template design.definition \
  --name <document-name> \
  --project-root <project> \
  --repository <owner/repository> \
  --owner <responsible-role-or-person> \
  --author <author-name> \
  --level subsystem \
  --domain software
```

生成器按 STD 项目级或领域级推荐目录自动落位。具体软件组件、固件产品或板卡的Owner文档，应按
`templates/path-policy.json` 的`domain_owned_path_patterns`替换真实名称，并同时使用 `--project-root` 和 `--output` 显式落位。
推荐结构不是对其他路径的
禁用规则；若项目保留自定义路径，应在 tailoring manifest 中记录。生成器不会覆盖已有文件。
若文档已经存在，应人工建立结构映射并生成可审阅 diff，不得强制覆盖。
直接按模板生成使用 `template_conformance=native`；经 tailoring 合并使用 `tailored` 并填写
`tailoring_ref`；保留既有结构使用 `legacy-mapped` 并填写 `migration_map_ref`。不得把只有标题相似的
遗留文档声明为 native conformance。

### Step 5：迁移内容

先搬运已确认事实和原有 ID，再补缺失章节。所有新增判断标出依据；重大设计变化单独写 ADR，
不要藏在格式迁移 diff 中。

### Step 6：校验与评审

```bash
/Users/ben/work/STD/scripts/validate-design \
  --project-root <project> \
  --require-immutable-std \
  --json <project>/artifacts/std-validation.json
/Users/ben/work/STD/scripts/verify-source-manifest \
  <project>/docs/std-source-manifest.json
```

验证必须分为三层，不得把 `validate-design` 的成功表述为完整验收：

1. **STD structural validation**：所有裁剪后启用根目录中的封面/sidecar 完整性与一致性、模板
   catalog/hash/version/type、Document ID 唯一性、conformance 引用、review decision、路径、链接、
   std.lock 和来源清单。已有仓库使用 baseline
   区分 inherited 与 new 问题。
2. **Project contract/schema validation**：ABI、IDL、OpenAPI、Schema、错误码、兼容性和 traceability。
3. **Runtime/external dependency evidence**：实际依赖、恢复流程、外部系统、硬件或运行时行为证据。

Migration Review Packet 提交 changed files、旧→新映射、未迁移内容、三层验证、traceability、blockers 和 review 请求。每项验证记录原始命令、原始退出码、关键输出、artifact 路径和执行 commit；不得以 `|| true` 等包装命令的退出码代替原始结果。

项目 owner 对 packet 给出 `Review Verdict = ACCEPTED / AMENDMENT / REJECTED / BLOCKED`。该 verdict 不自动改变 Document Status 或 Runtime Activation。

### Step 7：Canonical Promotion

只有在 review verdict、独立文档批准 Gate 和 immutable project commit 都满足后，才能用一个可审查变更完成 authority 切换：

1. 确认新文档的 canonical path、Document ID 和版本。
2. 将 metadata 与封面升级到已授权状态；sidecar 的 `reviewed_commit`指向实际被评审候选，merge 后
   canonical publication commit 由 publication/RAG manifest 记录，不在自引用文档中伪造。
3. 更新 README、文档索引、authority registry 和追踪关系。
4. 按 scope 把已完全迁出的旧 authority 标记为 Superseded/historical，并链接新 canonical artifact；
   若只迁移部分 scope，旧文档继续负责残余 scope 并明确边界。是否移入 archive 由 tailoring 决定。
5. 执行单一 authority 检查，确认同一范围不存在两份 current 文档。
6. Runtime Activation 如需发生，使用独立授权和证据 Gate，不从文档 verdict 推导。

### Step 8：Post-Approval Publication 与项目 RAG

只在 Canonical Promotion 完成后，才生成`rag/project-ingestion-manifest.jsonl`并由项目现有 RAG 机制索引。发布包必须记录 canonical commit、索引范围、新文档 inclusion、旧文档 exclusion、索引结果和重复 authority 检查。STD 的 RAG 只帮助查模板，不能替代项目实例或项目 commit。

## 5. Slinky 迁移重点

建议映射：

| 当前内容 | STD Template |
|---|---|
| `spec/10_system_design/` | `design.system` |
| `spec/20_system_mechanisms/` | `design.system-mechanism`，每个机制一份文档 |
| `spec/30_subsystem_design/` | `design.definition`，level=`subsystem` |
| `spec/40_module_design/` | `design.definition`，level=`module` |
| `spec/50_isd_design/` | `design.definition`，level=`implementation-unit` |
| Interface 文档 | `interfaces.control` |
| `test/design/` | `assurance.vv-plan` / `assurance.test-specification` |
| Review 和 blocker ledger | `review.packet` / `assurance.test-report` |

必须保留 Current Implementation Baseline、Approved Delta、source boundary、single owner、
recovery、可测试性和 requirement→suite→case→execution evidence 链。

## 6. Piko 迁移重点

- Piko Agent Runtime 总体：`design.system`；
- Runtime 内部子系统：`design.definition`，`level=subsystem`；
- CollaborationBridge 端到端通信、身份、幂等、恢复和 Element/Slinky 路由机制：优先 `design.system-mechanism`；
- Bridge 内部组件和实现单元：`design.definition`，选择 `level=component` 或 `implementation-unit`；
- OpenAPI、JSON Schema、Event、error catalog：`contracts.specification`；
- fixture 和 validator：作为 contract evidence 保留机器可读文件，不转写进 Markdown；
- QA：`assurance.vv-plan` + `assurance.test-specification`；
- 跨项目 review：`review.packet`。

必须保留多 room/cursor、resolution summary、authority boundary、Element route、fail-closed、
幂等/恢复和 activation gate 的精确契约。

## 7. LLMTier 迁移重点

- 系统/服务设计：`design.system` 或 `design.definition`；
- Piko data plane、Slinky observation 和 management contract：`interfaces.control` +
  `contracts.specification`；
- compatibility manifest 继续保持机器可读 authority；
- capacity、quota、idempotency、recovery fixture 和 QA 分别映射到 contract 与 assurance 模板。

必须保留 Model ID 精确大小写、provider 能力边界、Responses/Embeddings 责任、兼容矩阵和
不得静默 fallback 的约束。

## 8. HIFM 迁移重点

建议使用 `project_profile=mixed-system`，并启用
`systems/software/hardware/firmware/fpga/mixed` domains：

| 当前内容 | STD Template |
|---|---|
| HIFM 系统与 DPU 子系统 | `design.system` / `design.definition` |
| DPU-SIM 与 Validation | `design.definition` |
| FPGA 总体和模块设计 | `design.fpga` + `design.definition` |
| 板卡、原理图、PCB、BOM、供电和散热 | `design.hardware` |
| ABI、IDL、CSR、register map、设备/Host 接口 | `interfaces.control` + `contracts.specification` |
| 模型测算、方案评估、竞品和trade-off | `evaluation.technical-analysis`；最终选择另写 `decisions.adr` |
| 验证设计、首验规格和测试计划 | `assurance.vv-plan` / `assurance.test-specification` |
| 解决方案、SKU和路线图 | `product.solution-definition` / `product.sku-specification` / `product.roadmap` |
| 发布、bring-up 和验收 | `operations.release` + `review.packet` |

必须保留 unit/topology/placement scope，严格区分 GB/GiB、逻辑/物理放置、单设备/单副本/
节点聚合、持续容量/临时峰值，以及 modeled/simulated/estimated/measured 证据等级。DPU-SIM、
FPGA RTL 和板卡实测共享 contract，但互不冒充对方的证据。

## 9. 两阶段交付

### 9.1 Migration Review Packet

1. 文档 inventory 和旧→新模板映射；
2. tailoring manifest；
3. `docs/std.lock.json` 和 `docs/std-source-manifest.json`；
4. 迁移后的候选文档及 `.metadata.json`；
5. traceability 与三层验证的原始结果；
6. 保留/删除/归档建议，但本阶段不直接删除旧文档；
7. blockers、需要用户决定的设计问题和期望 Review Verdict。

### 9.2 Post-Approval Publication Packet

1. canonical path、Document Status 和 immutable project commit；
2. README、authority index 和 traceability 切换；
3. 旧文档 Superseded/historical 处理和 archive 决定；
4. `rag/project-ingestion-manifest.jsonl`、新文档 inclusion 和旧文档 exclusion；
5. RAG indexing 结果和单一 current authority 检查；
6. 独立 Runtime Activation 决定及其证据，如不适用则记录 `false / N/A`。

每份迁移后的正式文档还必须在首页填写 Document ID、Document Version、Status、Project、
Authority、Document Owner、Authors、Created Date、Last Modified Date、Template ID、Template Version、
Repository、Canonical Path 和 Supersedes。项目采用的 STD Version 只记录在项目 README 和
`docs/std.lock.json`。迁移不得重置原始 Created Date；无法确认时应从 Git
历史或旧文档恢复最早可验证日期，并在迁移记录中注明证据边界，不得把迁移日期伪装成创建日期。

## 10. 第二批生命周期模板

`0.1.0-draft.2` 已补充 Stakeholder Needs、ConOps、独立 Traceability Matrix、Development
Plan、SEMP、配置/风险/质量/安全/信息安全计划、分层 Test Plan、Test Procedure、Acceptance、
User/Installation/Operations/Maintenance/Bring-up Manual、Version Description、Data Dictionary、
制造装配检验、BOM/器件选型、原理图/PCB Review 和 FPGA Implementation Report。

迁移会话应按项目实际需要启用，不能仅因模板存在就机械生成空文档。允许按 tailoring 合并，
但必须记录合并后的章节映射，保证信息项没有丢失。

## 11. 跨子系统机制设计

`0.1.0-draft.3` 新增 `design.system-mechanism`。Artifact Flow、Recovery、RAG、Role Routing、
KV 分层、PES、X800-CR 等跨越两个或更多子系统的机制，应各自形成独立文档。系统设计只保留
机制目录、定位和引用；机制文档负责端到端流程、公共状态、参与方责任、接口、失败恢复、
容量性能、配置、验证和证据闭环。机制文档不得成为第二个子系统 authority。

## 12. GitHub 迁移协作

推荐在短生命周期 `docs/<document-id>-<topic>` 分支中完成迁移，并使用
`.github/PULL_REQUEST_TEMPLATE/document-change.md` 描述版本、路径、影响和验证结果。项目可按
实际情况配置 CODEOWNERS、default branch ruleset、required checks 和 signed release tag；完整
规则见 `docs/github-workflow.md`。
