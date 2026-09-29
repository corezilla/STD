# STD 单元测试设计模板续写 handoff（OpenCode）

日期：2026-09-28。此文件是临时交接记录，不是已发布标准；用完可删除。开始工作时仍须阅读仓库 `README.md`、当前 `AGENTS.md` 和项目已采用的规范，不能仅凭本 handoff 修改正式模板或项目采用状态。

## 当前状态

- 仓库：`/Users/ben/work/STD`，`main` 与 `origin/main` 一致；已提交 HEAD 为 `46e0806ec56ca0c41fa6ac62a6b755af70dacf36`。
- STD 已提交版本为 `0.1.0-draft.43`；软件模块设计模板 `design.definition` 为 `3.4.0`。
- 新草稿：`templates/tests/unit-test-design.md`，已正式登记为 `tests.unit-test-design` `0.1.0`（2026-09-28 用户裁决归放与独立模板定位；随后完成 catalog/path-policy/new-design/选择规则/AI 指南/README/VERSION 全部登记与实例校验，252 tests PASS）。
- 当前另有未跟踪 `.claude/`、`AGENTS.md`、`CLAUDE.md`；这些不是本轮草稿，不得为清理工作树而删除或顺带提交。
- 草稿写成后运行 `python3 -m unittest discover -s tests -p 'test_*.py'`：252 tests PASS。草稿尚未经过真实模块试写或内容质量评审；测试通过不代表模板已可发布。

## 用户意图与已确定的边界

用户要求先拟一份“单元测试设计”模板草稿，之后在 OpenCode 继续 STD 工作。本轮只起草，不注册为正式模板、不升级 STD 版本、不修改项目文档、不提交或推送。

现有 `templates/assurance/test-specification.md` 是通用测试规格，支持 unit、contract、integration、system 等层级；草稿聚焦**一个软件模块的隔离测试设计**。它不是测试计划、执行规程或运行报告：设计中固定 Case 输入与独立 Expected；Actual、Run 证据和最终 Verdict 属于执行报告。单元 PASS 不代替契约、集成或系统验证。

代码和报告路径按 `docs/software-project-layout.md`：默认 `tests/unit/<module>/`，或项目已登记的服务/包内共置路径；各自的 `reports/<run-id>/` 保存运行证据。`<module>` 是稳定代码目录名，不是 Module ID。多服务布局与例外必须明确 Owner、源码映射和隔离单位。

## 草稿结构

1. 被测模块与测试边界：真实代码、被替代依赖、固定设计和不证明的组合保证。
2. 测试依据与正向覆盖：从 Function、Constraint、Rule、Interface、Transition、Invariant、关键错误等来源 ID 逐项映射 Case 或具名缺口；一个来源 ID 一条覆盖记录。
3. 环境、夹具、隔离与复位：runner、fixture、seed、受控时钟/调度、真实依赖与替身的证明边界、并行隔离。
4. 用例设计：逐 Case 给完整函数声明、逐参数输入、初态、动作、独立 Oracle、互斥输出/错误、副作用、清理、测试代码位置及状态。草稿有一个虚构 `FrameDecoder` 反例。
5. 状态、并发与故障测试（条件适用）：沿 Transition/Invariant ID 从公开入口构造交错和故障，不直接改业务终态凑测试通过。
6. 自动化执行与判定：命令、前检、期限、退出码，区分 PASS/FAIL/BLOCKED/INVALID/NOT_RUN；重跑不覆盖失败证据。
7. 证据、报告与未决项：只定义证据合同及缺口责任，不预填实际结果。

每个主章已有折叠的“编写建议、示例与完成条件”，符合现有模板结构回归；正文槽位尚需试写验证。

## 下一步应先决定的问题

1. **~~独立模板还是通用模板的 unit profile？~~（已解决，2026-09-28）** 用户已裁决：放 `templates/tests/`，一个目录对应一种文档，肯定是独立模板。已完成的对比结论保留在草稿"模板定位"块：与 `assurance.test-specification` 权威分工、与 `design.definition` §14 的承接关系、不得双写、不强制空壳。剩余工作只是正式化时登记。
2. **设计深度是否能指导写测试代码？** 用一个真实但获准使用的模块，或 STD 虚构的有状态模块，试填从来源 ID → Case → fixture → 独立 Oracle → 测试函数 → Run 报告路径的全链。特别检查依赖替身是否错误地证明了事务/原子性、故障是否真的命中、失败和清理是否可观察。
3. **适用性与状态语义。** 同步只读函数不应被迫设计恢复协议；有状态、异步、持久化或共享资源模块不能以一句 N/A 省略第 5 章。区分 Case 设计状态、代码实现状态、执行状态与实际 Verdict。
4. **正式化时才处理登记。** 若确定为新模板，再决定 Template ID/Version、封面/metadata Schema、catalog、`new-design`、模板选择规则、验证 AI 指南、README/VERSION 与项目路径，并按 STD 版本规则升级。既有项目不自动采用。

## 续写与验证注意

- 先读 `templates/assurance/test-specification.md`、`test-plan.md`、`test-procedure.md`、`test-report.md`，以及 `docs/ai-guides/verification.md`、`docs/software-project-layout.md` 和 `templates/design/design-definition.md` 的 §14。避免复制计划、规程、报告或模块设计中的同一权威内容。
- 所有新增示例保持虚构，不把 Piko/HIFM/LLMTier 的私有项目设计直接搬入 STD；若选真实样本需核对使用授权和来源边界。
- 修改代码函数/类/方法前按 `AGENTS.md` 运行 GitNexus `impact` 并报告影响；提交前运行 `detect_changes()`。不要把上述未跟踪本地辅助文件自动纳入提交。
- 若决定提交，先完成内容复审、生成实例检查、相关测试及全套测试、`git diff --check`、精确暂存与版本一致性检查。提交/推送只在用户明确要求时执行。
