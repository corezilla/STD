# STD RAG 产物

本目录保存由 Git 权威内容确定性派生的索引输入和本地索引状态，不是模板权威来源。

- `std-ingestion-manifest.jsonl`：跨 RAG 实现可用的 ingestion manifest。
- `../meta/rag/rag.sqlite`：本次使用当前 Slinky Artifact-aware RAG 生成的本地索引数据库；
  实际文件名可由现有 Slinky 环境配置覆盖。
- `../meta/rag/`：本地运行生成的索引、检索记录和来源 manifest；属于可重建产物，不提交 Git。

重新生成 manifest：

```bash
./scripts/build-rag-manifest
```

当前 Slinky RAG 是 project/workspace scoped。其他项目采用 STD 时，应从 STD Git revision
生成项目文档，再由项目自己的 RAG 索引项目实例。不得把 STD RAG 中的模板内容当作项目设计事实。
