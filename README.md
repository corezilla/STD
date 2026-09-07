# STD：统一工程文档标准与模板库

STD 面向软件、硬件、固件、FPGA 和软硬件协同项目，提供项目管理、需求、系统设计、
子系统设计、模块设计、接口契约、验证测试、评审、发布和运维所需的版本化模板。

当前 `0.1.0-draft.19` 优先覆盖：

- Slinky，以及与其协作的 Piko、LLMTier；
- HIFM，包括软件、DPU-SIM、FPGA/RTL、板卡和系统验证。

## 核心规则

1. STD 仓库是模板、Schema 和校验工具的权威来源。
2. 项目通过确定性工具生成文档实例，并把实例提交到自己的仓库。
3. 每个实例固定 STD 版本、模板 ID、模板版本和来源哈希。
4. 项目升级模板必须显式执行并评审 diff，禁止静默跟随 STD 更新。
5. RAG 只负责检索，不负责模板分发、版本选择或事实裁决。
6. 系统、子系统、模块和组件使用一致的分层标识，但可选择不同领域 profile。

## 首版模板

模板清单见 [`templates/catalog.json`](templates/catalog.json)，选择方法见
[`docs/template-selection.md`](docs/template-selection.md)。

```text
templates/
├── management/       项目、开发、SEMP、配置、风险、质量、安全计划
├── requirements/     用户需求、ConOps、需求规格与追踪
├── evaluation/       技术分析、备选比较与证据结论
├── design/           系统、跨子系统机制、分层设计、硬件与 FPGA
├── product/          解决方案、SKU 规格与产品路线图
├── interfaces/       接口控制
├── contracts/        API、Schema、事件与错误契约
├── assurance/        V&V、测试计划/步骤/报告、验收和 FPGA 实现报告
├── review/           评审包
├── decisions/        ADR
└── operations/       用户、安装、运维、维护、Bring-up、发布与退役
```

## 在项目中使用

创建文档实例：

```bash
./scripts/new-design \
  --project slinky \
  --template design.system \
  --name system-design \
  --project-root /path/to/project \
  --repository corezilla/slinky \
  --owner system-architecture-team \
  --author "Author Name"
```

校验一个项目的 STD 文档：

```bash
./scripts/validate-design \
  --project-root /path/to/project \
  --require-immutable-std \
  --json /path/to/project/artifacts/std-validation.json
```

生成器会同时创建 Markdown 文档和 `<name>.metadata.json`。项目应提交两者，并保存
`docs/std.lock.json` 与独立的 `docs/std-source-manifest.json`。来源清单用
`scripts/build-source-manifest` 生成、`scripts/verify-source-manifest` 校验；它不是 RAG ingestion
manifest。完整接入规则见 [`docs/adoption.md`](docs/adoption.md)。
该检查覆盖 STD 文档结构，不替代项目契约/Schema 验证或 runtime 与外部依赖证据。

[`docs/repository-layout.md`](docs/repository-layout.md) 给出了完整项目仓库的推荐目录和文档默认落位，
纯软件项目见 [`docs/software-project-layout.md`](docs/software-project-layout.md)；
项目可通过 `--output` 沿用既有结构，并在 tailoring 中记录。封面、版本状态和 GitHub Review 规则分别见
[`docs/document-control.md`](docs/document-control.md) 与
[`docs/github-workflow.md`](docs/github-workflow.md)。

## 上游参考

STD 的覆盖模型参考 ISO/IEC/IEEE 15288、15289 和 42010；系统架构模板参考 arc42 v9.0；
项目/系统/软件工程内容参考 NASA Systems Engineering Handbook 与 NASA Software
Engineering Handbook；硬件、接口和验证文档目录参考 ECSS DRD。

STD 不复制受限标准正文。第三方来源和许可证边界见
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。
