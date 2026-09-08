# Knowledge Base 静态站点命名与 Git 迁移 HANDOFF

更新时间：2026-09-08
STD 路径：`/Users/ben/work/STD`
状态：可由后续会话按本 handoff 直接初始化或迁移 Knowledge Base

## 1. 目标

将现有以 `web` 命名的知识库改为清晰的 Knowledge Base，避免与产品 `webui`
混淆。正式名称和路径统一为：

- 展示名称：`Knowledge Base`；
- Git 仓库或顶层目录：`knowledge-base`；
- 代码标识符确实不能使用连字符时：`knowledge_base`；
- 产品用户界面继续使用 `webui` 或 `apps/<webui>/`。

Knowledge Base 默认是面向人阅读的静态知识网站，不默认启用问答、RAG、向量库、
外部检索服务或复杂 ACL。

## 2. 推荐最小结构

```text
knowledge-base/
├── docs/                         # Markdown或其他页面正文
├── assets/                       # 图片、附件和样式素材
├── site/                         # 静态站点配置和模板
└── README.md                     # 内容边界、本地预览和发布方法
```

初始化新的 Knowledge Base 根目录时，必须创建并纳入 Git 的 `README.md`、`docs/`、
`assets/` 和 `site/`。暂时没有实际内容的子目录使用 `.gitkeep` 跟踪；首个实际文件进入后
可以删除同目录的 `.gitkeep`。只有项目已有明确 tailoring 并记录理由时，才可以省略其中
一个子目录。纯静态站点不强制建立独立 `tests/`；最低验证为：

1. 站点能成功构建；
2. 内部链接有效；
3. 被引用的图片和附件存在；
4. 没有重复页面路径。

### 2.1 新目录直接初始化

没有旧知识站点内容需要移动时，后续会话直接建立以下可提交骨架，不创建问答、RAG、
向量库或外部索引：

```text
knowledge-base/
├── docs/.gitkeep
├── assets/.gitkeep
├── site/.gitkeep
└── README.md
```

如果用户或项目明确要求代码标识符形式，则把根目录名替换为 `knowledge_base/`，内部结构
保持不变。`README.md` 至少说明内容边界、本地预览/构建状态、发布状态，以及它与产品
`webui`、RAG 和 Runtime Activation 的边界。

该初始化应作为独立 commit；不得夹带既有 dirty 修改。提交前至少核对：

```bash
git status --short
git diff --cached --name-status
git diff --cached --check
```

如果此时只有目录骨架、尚无页面和站点配置，则站点构建、链接、资源和重复页面检查记录为
`N/A (empty skeleton)`；首批实际内容进入时必须把这些检查升级为真实执行结果。

## 3. Git 迁移原则

本迁移不通过 `cp`、`rsync` 或手工复制文件建立新结构。迁移必须保留原 Git 历史，
并避免旧路径和新路径同时成为 current authority。

通用规则：

- 执行前记录 `HEAD`、branch、remote、dirty、untracked、ignored、submodule 和 worktree 状态；
- 任何需要保留的内容必须先进入 Git commit 并成功 push；
- 未跟踪或 ignored 文件不会由 GitHub 保留，不得在未决定其处置前删除旧 checkout；
- 目录搬迁和正文修订分成不同 commit，便于 Git rename detection 和 review；
- 不创建空的新 GitHub 仓库来替换原仓库，除非用户另行批准历史迁移。

## 4. 仓库内部目录改名

如果 `web/` 是现有仓库内的顶层目录，使用 Git 原生移动：

```bash
git status --short
git mv web knowledge-base
git diff --cached --summary
git diff --cached --find-renames=90%
git diff --cached --check
```

该 commit 只允许路径移动，不同时修改页面正文、站点样式或链接。移动 commit 通过后，
再用第二个 commit 修改配置、路径引用、CI 和文档。

Git 不在 commit 中存储独立的“重命名对象”，而是在比较时根据内容相似度识别 rename。
因此，机械移动 commit 应尽量保持文件 bytes 不变。

## 5. 独立项目根目录从 `web` 改为 `knowledge-base`

如果 `web` 是整个项目 checkout 的根目录，不使用文件复制来构造新项目。以已推送的原
GitHub repository 为唯一来源，执行全新 clone：

```bash
git -C <old-web-checkout> status --short
git -C <old-web-checkout> fetch origin
git -C <old-web-checkout> rev-parse HEAD
git -C <old-web-checkout> rev-parse origin/main
git -C <old-web-checkout> ls-files --others --exclude-standard
git clone <existing-github-url> <new-parent>/knowledge-base
git -C <new-parent>/knowledge-base rev-parse HEAD
```

必须验证新 checkout 的 commit SHA 与已推送的目标 branch 一致，并重跑站点构建、链接和
资源检查。如果使用 Git LFS、submodule 或 linked worktree，必须分别完成额外验证。

旧 checkout 先移入可恢复的废纸篓，不直接执行 `rm -rf`。只有新 checkout、GitHub branch、
构建和引用都验证通过后，才能决定是否永久删除旧目录。

## 6. Codex 和工具路径

Git 文件迁移与 Codex 任务路径切换是两个独立 Gate。新 checkout 验证通过后，再更新：

- Codex 保存的 project/workdir；
- 本地脚本、CI 和发布配置中的绝对路径；
- 已授权协作 profile 中的 canonical cwd（如适用）。

不为兼容旧任务默认长期保留两个可写 checkout。需要短期过渡时，兼容方案必须有明确的
删除条件，且不得使旧目录变成第二个可写 authority。

## 7. 完成条件

同时满足以下条件才能声明 Knowledge Base 改名完成：

1. 当前权威路径中不再使用顶层 `web/` 表示知识库；
2. Git history、branch、tag 和原 remote 保持可追溯；
3. 未跟踪或 ignored 内容已有明确保留或丢弃决定；
4. 站点构建、链接、资源和页面路径检查通过；
5. 新目录的 `HEAD` 与 GitHub 目标 branch 一致；
6. Codex 和其他工具不再把旧目录当作可写项目根；
7. 旧路径不再与 `knowledge-base` 并行承担 current authority；
8. `README.md`、`docs/`、`assets/` 和 `site/` 均已纳入 Git；空目录使用 `.gitkeep`。

## 8. 边界

本 handoff 的范围只覆盖生成可审阅的命名和 Git 迁移方案；文档本身不构成下列操作的授权：

- 删除未提交内容；
- 创建或替换 GitHub repository；
- 强制 push、改写历史或删除 branch/tag；
- 启用问答、RAG、向量库或外部索引；
- 修改产品 WebUI 的责任边界或运行时行为。

需要上述操作时，必须另行获得用户明确批准。
