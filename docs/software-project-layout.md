# STD 软件项目目录结构

## 1. 使用方法

本profile适用于CLI、SDK、库、服务、Web应用、Agent系统和多服务平台。每个目录在同一行的`#`
之后说明作用。单应用使用`src/`；多服务仓库使用`apps/ + services/ + packages/`，不同时建立两套
表达相同ownership的源码树。每个软件源码根下，有软件子系统时按
`src/<subsystem>/<module>/`组织；模块直接属于软件系统时按`src/<module>/`组织。
`<subsystem>`和`<module>`是稳定的代码目录名，Module ID仍在设计和测试映射中记录，不直接充当目录名。

## 2. 单应用、单服务或单库

```text
<project>/                       # 软件项目仓库根，容纳全局治理、产品源码和交付物
├── .github/                      # PR、Issue、CODEOWNERS、CI和GitHub协作配置
│   ├── PULL_REQUEST_TEMPLATE/    # 不同变更类型的PR说明模板
│   └── workflows/                # 自动构建、检查、测试和发布流水线
├── docs/                         # 项目需求、架构、设计、验证和运维文档
│   ├── 00_management/            # 项目、开发、配置、风险和质量管理
│   │   └── standards/            # 项目自定义规范；README.md为强制总索引
│   ├── 10_requirements/          # 用户需求、ConOps、SRS和追踪关系
│   ├── 15_evaluation/            # 技术选型、PoC、性能和竞品分析
│   ├── 20_system_design/         # 软件系统架构、边界和质量属性
│   │   └── mechanisms/           # 认证、调度、恢复、审计等端到端机制
│   ├── 30_subsystem_design/      # 主要子系统、服务或进程设计
│   ├── 40_module_design/         # 包、模块和组件内部设计
│   ├── 50_implementation_design/ # 类、文件、算法和关键实现单元设计
│   ├── 60_interfaces/            # 接口目录、ICD和机器契约索引
│   ├── 70_verification/          # 测试计划、规格、规程和验收要求；报告随测试保存
│   ├── 80_operations/            # 安装、部署、运行、维护和发布手册
│   ├── 90_decisions/             # ADR和已批准技术决策
│   ├── 91_reviews/               # 正式设计、代码和发布评审记录
│   ├── 98_migration/             # 文档、架构或系统迁移盘点与映射
│   └── 99_reference/             # 外部参考、历史资料和非权威快照
├── notes/                        # 会议、客户、合作方和内部沟通记录
│   ├── meetings/                 # 例会、专题会和评审准备会纪要
│   ├── customers/                # 客户沟通、需求线索和行动项
│   ├── partners/                 # 合作方沟通、依赖和行动项
│   └── internal/                 # 内部讨论、工作记录和临时共识
├── materials/                    # 投资、市场、销售和客户交付材料
├── src/                          # 可发布的软件产品源码；按实际设计层级选择以下路径
│   ├── <subsystem>/              # 有软件子系统时：该子系统的直属模块
│   │   └── <module>/             # src/<subsystem>/<module>/
│   └── <module>/                 # 无子系统时：软件系统的直属模块
├── include/                      # C/C++等项目的公开头文件和公共API
├── interfaces/                   # 多consumer机器可读契约authority
│   ├── docs/                      # 契约导航、边界和人工可读说明
│   ├── openapi/                   # HTTP/REST API定义
│   ├── proto/                     # RPC和消息IDL定义
│   ├── schemas/                   # JSON、YAML和数据Schema
│   ├── events/                    # 事件名称、payload和演进规则
│   ├── error-codes/               # 公共错误码、分类和语义
│   ├── compatibility/             # 版本矩阵、弃用和兼容策略
│   ├── vectors/                   # 小型冻结契约向量和Golden样例
│   └── codegen/                   # 契约驱动的代码和文档生成工具
├── configs/                      # 可提交的配置默认值、示例和Schema
│   ├── defaults/                 # 产品默认配置，不包含secret
│   ├── examples/                 # 用户和开发环境示例配置
│   └── schemas/                  # 配置字段类型、约束和版本
├── tests/                        # 可执行测试、harness、fixture和oracle
│   ├── unit/                     # 函数、类和小模块隔离测试
│   │   └── <module>/             # 稳定模块目录名，内含用例与reports/<run-id>/
│   ├── contract/                 # API、Schema、事件和兼容契约测试
│   │   └── reports/              # 本类报告，按Run ID分开
│   ├── integration/              # 多模块和外部依赖集成测试
│   │   └── reports/              # 集成测试报告，按Run ID分开
│   ├── system/                   # 完整软件系统端到端测试
│   │   └── reports/              # 系统测试报告，按Run ID分开
│   ├── acceptance/               # 用户或客户验收自动化
│   │   └── reports/              # 验收测试报告，按Run ID分开
│   ├── fixtures/                 # 小型、稳定、可提交的测试输入
│   └── common/                   # 公共harness、helper和oracle
├── deploy/                       # 容器、Kubernetes、systemd、IaC和环境模板
├── migrations/                   # 数据库、状态格式或协议迁移及回滚程序
├── scripts/                      # 开发者常用的短命令和任务入口
├── tools/                        # 构建、生成、检查、分析和发布工具
├── examples/                     # 面向用户或开发者的可运行示例
├── benchmarks/                   # 可复现基准场景、runner和统计方法
├── knowledge-base/               # 可选：面向人阅读的静态知识网站
├── third_party/                  # 第三方依赖、许可证和受控patch
├── build/                        # ignored：可由源码重建的编译输出
├── dist/                         # ignored：打包输出，正式发布另行固化
├── .cache/                       # ignored：可重新生成或下载的缓存
└── .local/                       # ignored：本地运行、secret、证据和临时数据
```

库项目通常启用`include/`和compatibility checks；服务项目通常启用`deploy/`、配置Schema、数据库
迁移、运行手册和SLO/可观测性设计。

## 3. 多应用、多服务或平台仓库

```text
<project>/                       # 软件平台仓库根，容纳多Owner应用、服务、包和公共治理
├── .github/                      # 全仓Owner、Review、CI和发布配置
├── docs/                         # 平台级需求、架构和跨服务机制
├── notes/                        # 平台会议及客户、合作方、内部沟通记录
├── materials/                    # 平台投资、市场、销售和对外交付材料
├── interfaces/                   # 跨应用、服务和SDK的公共契约authority
│   ├── docs/                      # 契约导航、边界和人工可读说明
│   ├── openapi/                   # HTTP/REST API定义
│   ├── proto/                     # RPC和消息IDL定义
│   ├── schemas/                   # 数据、配置和artifact Schema
│   ├── events/                    # 跨服务事件契约和演进规则
│   ├── error-codes/               # 跨Owner错误码注册和语义
│   ├── compatibility/             # 兼容矩阵、弃用和升级规则
│   ├── vectors/                   # 小型冻结契约向量和Golden样例
│   └── codegen/                   # 公共契约生成器和一致性检查
├── apps/                         # Web、CLI、Desktop、Mobile等用户入口
│   └── <app>/                    # 一个可独立构建或发布的前端应用
│       ├── docs/                 # 该应用专属需求、设计和运行资料
│       ├── src/                  # 该应用源码；按子系统/模块或直属模块组织
│       └── tests/                # 该应用局部单元和组件测试
├── services/                     # 可独立部署的后端服务集合
│   └── <service>/                # 单个服务的Owner和发布边界
│       ├── docs/                 # 服务专属设计、接口消费和运行资料
│       ├── src/                  # 服务源码；按子系统/模块或直属模块组织
│       ├── tests/                # 服务内部单元、组件和契约测试
│       ├── configs/              # 服务默认配置、示例和Schema
│       └── deploy/               # 服务独立部署定义
├── packages/                     # 可复用、可版本化的软件包和SDK
│   └── <package>/                # 单个包的Owner、API和兼容边界
│       ├── docs/                 # 包API、使用方法和内部设计
│       ├── src/                  # 包源码；按子系统/模块或直属模块组织
│       └── tests/                # 包单元、兼容和发布验证
├── tests/                        # 跨Owner和平台级可执行测试
│   ├── contract/                 # 跨Owner公共契约测试
│   │   └── reports/              # 公共契约测试报告，按Run ID分开
│   ├── integration/              # 多服务集成和依赖联调测试
│   │   └── reports/              # 集成测试报告，按Run ID分开
│   ├── system/                   # 平台端到端测试
│   │   └── reports/              # 系统测试报告，按Run ID分开
│   └── acceptance/               # 平台用户或客户验收自动化
│       └── reports/              # 验收测试报告，按Run ID分开
├── deploy/                       # 平台级环境、网络、编排和IaC
├── experiments/                  # 可复现实验manifest、runner和分析代码
├── knowledge-base/               # 可选：项目或产品的静态知识网站
├── tools/                        # 仓库级构建、生成、检查和发布工具
├── third_party/                  # 全仓第三方依赖、许可证和patch
└── .local/                       # ignored：本地数据、secret和运行输出
```

平台级`docs/20_system_design/mechanisms/`管理认证、授权、任务调度、消息流、重试恢复、审计、
配额和RAG等跨服务机制。服务内部算法和类设计放在`services/<service>/docs/`，不在平台文档复制。

## 4. 静态知识库

项目需要的若主要是可浏览的静态页面，正式名称使用 Knowledge Base，仓库或目录名使用
`knowledge-base`；代码标识符需要时使用 `knowledge_base`。不使用顶层 `web/` 表示知识库，
避免与 `webui/` 或 `apps/<webui>/` 的产品用户界面混淆。

推荐的最小结构为：

```text
knowledge-base/
├── docs/                         # Markdown或其他页面正文
├── assets/                       # 图片、附件和样式素材
├── site/                         # 按需：静态站点配置和模板
└── README.md                     # 内容边界、本地预览和发布方法
```

问答、RAG、向量库、外部检索后端和复杂 ACL 不是该目录的默认要求；只有项目明确
启用相应能力时才增加。纯静态知识站不强制建立独立 `tests/`；可在构建命令或 CI 中
执行站点构建、内部链接、资源存在性和重复页面路径检查。

## 5. 关键边界

项目规范放在 `docs/00_management/standards/`，其中README.md为强制总索引。
根README靠前链接总索引，每份规范开头反向链接，详见[项目规范强制索引](project-standards.md)。

- `docs/70_verification/`保存计划、规格和规程；每类测试保存自己的代码与报告，例如 `tests/system/reports/<run-id>/`，不集中到根 `tests/reports/`。
- `interfaces/`保存机器可读公共契约；consumer只引用，不复制Schema。
- 多服务项目的组件内部单元测试默认随组件共置；采用集中测试布局时，也可放在根
  `tests/unit/<module>/`，但须明确Owner和源码映射。根`tests/`还保存跨Owner契约、集成、系统和验收测试。
- `configs/`和`deploy/`不保存token、证书和生产secret。
- `migrations/`是软件数据/状态迁移，不是文档迁移。
- `.local/`、`build/`、`dist/`和`.cache/`不进入Git。
- `src/`、`apps/<app>/src/`、`services/<service>/src/`和`packages/<package>/src/`均以各自的
  `src/`为起点：有子系统用`src/<subsystem>/<module>/`，没有子系统用`src/<module>/`。
  同一模块只保留一处源码；语言生态需要不同物理路径时，在tailoring中记录到该设计对象的映射。

模块单元测试可集中为 `tests/unit/<module>/`，或随实际服务/应用/库共置为
`services/<service>/tests/unit/<module>/` 等；各自保留 `reports/<run-id>/`，不复制同一测试。
`<module>`与源码模块目录名对应，并在测试规格中映射稳定Module ID；同一测试Owner内目录名须唯一。
混合项目目录中的 `<component>` 指构建/交付单元，不是设计模块；目录须映射实际 Module ID。
多服务布局中各级 `tests/` 也遵循这套报告归属规则。
正式Markdown报告和metadata可入Git，机器输出默认放各Run下 `artifacts/` 或CI制品库，
不要忽略整个报告目录。完整文件样例、Case与Run关联及保留规则见
[测试目录与报告分工](repository-layout.md#411-按测试类型保存报告)和[系统测试示例](repository-layout.md#412-系统测试的文件级示例)。
