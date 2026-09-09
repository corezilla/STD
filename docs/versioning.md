# STD 版本规范

## 1. 目标

版本用于固定可审阅输入，不用于强迫项目追随 STD 的每次变更。项目、模板、文档、产品、
机器契约和 Git revision 是不同版本域，不得相互代替。

## 2. 版本域

| 版本域 | 记录位置 | 变更条件 |
|---|---|---|
| STD Version | STD `VERSION`；项目 README 和 `docs/std.lock.json` | 项目只在用户明确要求时升级 |
| Template Version | `templates/catalog.json.template_versions[template_id]`；文档封面和 sidecar | 对应模板自身变更时独立升级 |
| Document Version | 文档封面和 sidecar | 文档业务内容、状态或边界变更 |
| Product/Release Version | 产品和发布文档 | 产品发布流程决定 |
| Contract/Schema Version | 机器契约自身 | 兼容性和契约规则决定 |
| Git Commit/Tag | Git | 不可变证据，不是语义版本 |

## 3. 项目采用 STD

1. 项目 README 必须以人可读方式写明当前采用的 STD Version；`STD` 和反引号包裹的版本号
   必须出现在同一行，以便本地校验器核对。
2. `docs/std.lock.json` 是同一采用决定的机器可读记录，包含 immutable commit 和可选 annotated tag。
3. README 和 lock 必须一致；不得只改其中一处声称升级完成。
4. STD 发布新版本时，项目不自动跟随、不自动重生成文档、不自动重跑迁移。
5. 只有用户明确要求对齐新 STD 版本时，才开始升级评估、diff、验证和评审。
6. 日常修改项目文档时，使用项目已锁定的 STD 和模板；不查询或自动对比“最新版本”。

项目 README 推荐写法：

```markdown
## Engineering Standard

This project adopts STD `<adopted-version>`, locked by `docs/std.lock.json`.
STD upgrades are performed only when explicitly requested by the user.
```

## 4. 模板独立版本

每个 Template ID 有自己的 SemVer。`catalog_version` 只是 catalog 数据结构和发布版本，
不再作为所有模板的共享版本。

模板版本变更规则：

- MAJOR：删除必填信息、改变 authority/责任边界，或引入不兼容结构；
- MINOR：新增兼容章节、字段、checklist 或写作指导；
- PATCH：不改变要求语义的勘误、措辞、格式和链接修复。

只有被修改的模板才升级自身版本。STD 文档、Schema、工具或其他模板变更，不得连带升级
未变模板的 Template Version。

每份生成文档必须保存：

- 封面：`Template ID` 和 `Template Version`；
- sidecar：`template_id`、`template_version` 和 `template_sha256`。

单文档封面和 sidecar 都不得保存 `std_version`。项目级 STD 来源只在 README、
`docs/std.lock.json` 和来源清单中固定。

`template_sha256` 锁定精确 bytes，Template Version 表达语义版本，两者都要保留。

## 5. 文档版本

文档使用 SemVer：

- MAJOR：范围、authority、外部契约或核心行为不兼容变更；
- MINOR：新增兼容能力、章节、机制或重要验证内容；
- PATCH：不改变已批准语义的澄清、勘误、链接或格式修复；
- prerelease：`draft.N`、`rc.N` 等尚未批准的候选。

更新 Template Version 不会自动更新 Document Version。只有项目实际采用新模板并产生文档
差异时，才按差异的语义影响决定文档版本。

## 6. 验证与升级

默认验证只检查：

1. 项目已锁定的 STD 来源是否完整；
2. 文档记录的 Template Version 是否与已锁定 catalog 中该 Template ID 的版本一致；
3. `template_sha256` 是否与锁定来源中该模板一致。

默认验证不访问网络、不查询 STD 最新版本、不把项目与未锁定的新模板比较。

用户明确要求升级时，才执行：选定目标 STD revision、评估受影响 Template ID、生成候选、
审阅 diff、更新 README/lock，并保存验证证据。
