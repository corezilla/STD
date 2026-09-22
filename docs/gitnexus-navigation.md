# 通过 GitNexus 快速读取 STD

GitNexus 是检索入口，不是新的规范权威或版本采用决定。本页适用于已接入 GitNexus MCP 的
OpenCode、Codex 或其他客户端，不依赖 AGENTS.md、特定会话或新增的检索平台。

## 1. 发现仓库与核对版本

1. 调用 `list_repos`，在返回列表中找到仓库名 `STD`；多页时按返回的分页游标继续查找。
2. 读取资源 `gitnexus://repo/STD/context` 获取概况；`list_repos` 的 `lastCommit` 可用于与项目
   `docs/std.lock.json` 的 `source_revision` 比较。所有后续查询显式指定 `repo: "STD"`。
3. 若项目锁定的STD版本与索引不同，不把当前索引内容当作项目采用版本。回到锁定来源读取原文，
   或按明确授权准备对应版本索引；不要自行升级项目或切换共享STD工作树。

STD索引是本机、当前用户的本地注册，不会随Git push分发。同机且连接同一GitNexus服务/注册表的
客户端可发现它；其他机器或用户须准备授权的STD检出并建立索引。没有工具时应报告缺少连接，
或从项目README的锁定STD入口读文件，不声称已经通过GitNexus核查。

## 2. 优先按路径读取规范，不依赖代码搜索命中

先读取资源 `gitnexus://repo/STD/schema`。本机验证过以下 `cypher` 工具调用可读取Markdown正文：

```json
{
  "repo": "STD",
  "query": "MATCH (f:File) WHERE f.filePath = 'README.md' RETURN f.filePath, f.content"
}
```

读取README中的执行流程后，按任务选择文件。不要把整个仓库全部读入上下文：

| 任务 | 读取的路径 |
|---|---|
| 选择模板与指南 | `docs/template-selection.md`、`docs/ai-authoring-guide.md` |
| 精确模板/指南映射 | `templates/catalog.json`、`docs/ai-authoring-guides.json` |
| 项目规范与强制索引 | `docs/project-standards.md` |
| 目录和测试报告归属 | `docs/repository-layout.md`、`docs/software-project-layout.md` |
| 项目README及开发环境入口 | `templates/_shared/project-readme.md` |
| 当前类型的具体模板/指南 | 按上述目录选定的实际文件路径 |

将查询中的 `README.md` 换成选定路径即可。也可先只检索文件名：

```json
{
  "repo": "STD",
  "query": "MATCH (f:File) WHERE f.filePath STARTS WITH 'templates/design/' AND f.filePath ENDS WITH '.md' RETURN f.filePath ORDER BY f.filePath"
}
```

不确定路径时，可以用 `f.content CONTAINS '关键字'` 限定Markdown文件后查找路径，再定点读取正文。
`query` 工具主要面向代码符号和执行流程，中文规范查询可能无结果或命中测试代码；
这不表示规范不存在。返回内容截断或文件未索引时，按路径读取锁定检出中的原文件。
GitNexus不能代替打开SVG/PNG查看图例，也不能证明规范遵循或设计质量。

## 3. 客户端连接与索引维护

已配置GitNexus MCP的客户端不需要再启动第二套服务。未配置的客户端，可在其MCP配置中建立
本地stdio服务，命令为 `gitnexus`、参数为 `mcp`。命令必须在客户端环境PATH中可用；
具体配置格式以该客户端为准，不在STD中复制或改写用户全局配置。配置后通过 `list_repos` 验证发现STD。

STD维护者在仓库根目录刷新并检查：

```bash
gitnexus analyze --index-only --name STD
gitnexus status
```

纯索引模式不注入AGENTS.md、CLAUDE.md或技能文件；本地索引放在被忽略的 `.gitnexus/` 中，
不提交Git，也不默认生成embeddings或发布远端服务。提交后应刷新索引，并验证实际查询能读到新内容；
仅比较commit不能证明未提交工作树的内容完全一致。
