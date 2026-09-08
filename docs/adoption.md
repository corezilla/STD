# 项目采用与升级规范

## 1. 采用模型

项目不通过 RAG“挂载”模板，也不通过软链接引用 STD 工作树。采用流程是：

```text
STD release/tag
    ↓ source manifest + new-design（确定性生成）
候选项目文档 + metadata + std.lock.json
    ↓ Migration Review（不自动升级状态或激活 runtime）
Canonical Promotion
    ↓ Post-Approval Publication
RAG 检索副本
```

STD 管模板；项目管理填写后的设计事实。两者的 authority 不得混合。

## 2. 项目必须提交的文件

项目必须提交`docs/std.lock.json`、`docs/std-source-manifest.json`、已启用的模板实例及其同名`.metadata.json`。不要为未启用的文档类型预建空目录。

混合软硬件项目使用`docs/repository-layout.md`的完整目录规范，纯软件项目使用`docs/software-project-layout.md`。两份规范的每个目录均在目录行后用`#`说明职责，并定义`notes/`、`materials/`、`interfaces/`、`tests/`和本地数据区的边界。

`std.lock.json` 必须通过 `schemas/std-lock.schema.json` 校验，并至少记录：

```json
{
  "schema_version": "std-lock.v1",
  "std_version": "0.1.0-draft.18",
  "source_repository": "corezilla/STD",
  "source_revision": "<full-40-character-commit-sha>",
  "source_tag": "<optional-annotated-tag>",
  "source_manifest_path": "docs/std-source-manifest.json",
  "adopted_at": "YYYY-MM-DD",
  "project_profile": "mixed-system",
  "enabled_domains": ["systems", "software", "hardware", "firmware", "fpga"]
}
```

`project_profile` 只能是 `mixed-system`、`software`、`hardware-fpga` 或
`documentation-only`；`enabled_domains` 表示项目实际启用的工程域。文档 metadata 中的 `domain`
仍描述单份文档，不得拿它替代项目 profile。

`std.lock.json` 只记录采用决定和 immutable revision；`std-source-manifest.json`在迁移开始时独立锁定实际使用的模板、Schema、工具和规范 SHA-256。它不是 RAG ingestion manifest。规划阶段允许 `source_revision=null`；Migration Review Packet 获得 READY、生成候选文档或进入评审前，必须改为完整 40 位 commit SHA，并通过机器校验。`HEAD`、branch 和 tag 名都不能填入 `source_revision`；可选 `source_tag` 必须是 annotated tag，并 peel 到同一个 commit。

```bash
/Users/ben/work/STD/scripts/build-source-manifest \
  --output <project>/docs/std-source-manifest.json
/Users/ben/work/STD/scripts/verify-source-manifest \
  <project>/docs/std-source-manifest.json \
  --std-root <checkout-of-the-locked-STD-revision>
```

完整目录和 Template ID 默认落位见 `docs/repository-layout.md` 与
`templates/path-policy.json`。这是统一默认结构，不否定项目已有且合理的文档组织；偏离项在
tailoring manifest 和项目文档索引中记录即可。

每份文档还必须有同名 `.metadata.json`，记录模板、文档版本、Owner、作者、层级、authority、
状态、repository/path、来源哈希与模板符合方式。Markdown 首页同时显示 `docs/document-control.md` 定义的封面。
封面显示独立 `Template Version`，不显示项目级 `STD Version`。`metadata.std_version` 只保留文档
创建或上次显式升级时的来源审计信息，不要求因项目 lock 或 STD 其他内容更新而改写。
在项目根校验中，`template_version` 只与该 `template_id` 在锁定 catalog 中的独立版本比较，
并同时核对 `template_sha256`；`document_type` 必须等于 `template_id`。

模板符合方式只有三种：

- `native`：直接按当前模板生成；`tailoring_ref` 与 `migration_map_ref` 均为 `null`。
- `tailored`：经批准裁剪；必须填写 `tailoring_ref`。
- `legacy-mapped`：保留既有结构并建立等价章节映射；必须填写 `migration_map_ref`。

`tailoring_ref` 是同一项目内 `management.tailoring` 文档的唯一 Document ID；
`migration_map_ref` 是项目根相对文件路径，禁止绝对路径和 `..`，且目标必须存在。上述引用只有在
`--project-root` 模式下完成解析校验。

## 3. 新建与升级

- 新建：使用 `scripts/new-design --project-root <project>` 从固定 STD revision 生成，工具按
  `templates/path-policy.json` 选择推荐目录；使用 `--project-root <project> --output <dir>` 可显式
  沿用项目自定义路径，同时保持封面中的 Canonical Path 为仓库相对路径。
- 具体组件、固件产品或板卡采用Owner共置时，根据`domain_owned_path_patterns`把占位符替换为真实名称，并通过`--output`指定目标目录；生成器的无参默认只代表项目级或领域级文档。
- 修改：只在项目仓库内修改文档实例。
- 升级：只在用户明确要求对齐新 STD 或新模板版本时进行。固定新 revision、重新生成临时候选并人工审阅 diff；禁止直接覆盖项目内容。自动 `upgrade-template` 尚未实现，不得把它写成现有能力。

项目 README 必须在同一行显示 `STD` 和反引号包裹的当前采用版本，并与
`docs/std.lock.json` 一致。STD 发布新版本
不会自动改变项目的采用版本；在用户明确提出升级前，项目继续使用原锁定版本，
日常修改不得顺便执行“最新 STD/模板”对比。
- Review：项目 owner 审阅模板变化与项目自定义内容的合并结果。
- 冻结：accepted/released 文档必须绑定不可变项目 commit。

Review Verdict、Document Status 和 Runtime Activation 必须分开记录，完整映射见`docs/document-control.md`。

## 4. 结构校验范围

推荐从项目根执行，覆盖所有裁剪后启用的文档根、sidecar、ID 和锁文件：

```bash
/Users/ben/work/STD/scripts/validate-design \
  --project-root <project> \
  --require-immutable-std \
  --json <project>/artifacts/std-validation.json
```

遗留仓库可先用 `--write-baseline <file>` 固定既有结构问题，后续用 `--baseline <file>` 区分
`new` 与 `inherited` 错误。该命令只证明 STD structural validation；项目契约和 runtime/外部依赖证据仍是独立 Gate。

Git 项目的 `--project-root` 发现集合为已跟踪文件及未被 `.gitignore` 排除的未跟踪文件；
ignored runtime/build/data 不进入结构校验。非 Git 项目使用带默认目录剪枝的文件遍历。
两种模式都只选择普通文件；名称以 `.md`、`.metadata.json` 或
`.review-decision.json` 结尾的目录不会作为文档读取。发现到的文件若无法读取，validator
必须输出稳定的结构化诊断（例如 `markdown.read`），不得以 traceback 中止，也不得把该问题
写入 baseline 后冒充通过。

封面字段只在 `STD_DOCUMENT_COVER_BEGIN` 与 `STD_DOCUMENT_COVER_END` 标记之间解析。
正文中的表格可以合法使用 `Status`、`Authority` 等同名列或字段，不得覆盖封面值或触发
`cover.mismatch`。

STD source manifest 的生成、独立校验和 project-root 完整性检查使用相同发现边界：Git checkout
只纳入 tracked 与 non-ignored untracked 的普通非 symlink 来源文件；ignored 文件（包括
`.DS_Store` 等平台 metadata）不属于可锁定来源。非 Git checkout 的 fallback 同样排除平台
metadata、`.git`、`__pycache__` 和 symlink。

机器 review decision 统一命名为 `*.review-decision.json`，并通过
`schemas/review-decision.schema.json` 校验。终局 verdict 必须包含 reviewer、决定时间与理由；
请求 runtime activation 时还必须填写独立 activation authority。

## 5. RAG 的正确位置

可以把 STD 规范和项目实例加入 RAG，但必须分 namespace 和 authority：

| 内容 | authority | 用途 |
|---|---|---|
| STD 模板与写作规范 | `std` | 选模板、解释必填项、辅助 review |
| Slinky 项目文档 | `slinky` | 回答 Slinky 当前设计 |
| Piko 项目文档 | `piko` | 回答 Piko 当前设计 |
| LLMTier 项目文档 | `llmtier` | 回答 LLMTier 当前设计 |
| HIFM 项目文档 | `hifm` | 回答 HIFM 当前设计 |

`rag/project-ingestion-manifest.jsonl`只在 canonical promotion 完成后生成。RAG ingestion 必须保存 repository、path、commit、document status、visibility 和 authority；
检索前执行 ACL。RAG 中的模板副本不得替代 Git 中固定版本的模板。
