# STD 软件项目目录结构

## 1. 使用方法

本profile适用于CLI、SDK、库、服务、Web应用、Agent系统和多服务平台。每个目录在同一行的`#`
之后说明作用。单应用使用`src/`；多服务仓库使用`apps/ + services/ + packages/`，不同时建立两套
表达相同ownership的源码树。

## 2. 单应用、单服务或单库

```text
<project>/                       # 软件项目仓库根，容纳全局治理、产品源码和交付物
├── .github/                      # PR、Issue、CODEOWNERS、CI和GitHub协作配置
│   ├── PULL_REQUEST_TEMPLATE/    # 不同变更类型的PR说明模板
│   └── workflows/                # 自动构建、检查、测试和发布流水线
├── docs/                         # 项目需求、架构、设计、验证和运维文档
│   ├── 00_management/            # 项目、开发、配置、风险和质量管理
│   ├── 10_requirements/          # 用户需求、ConOps、SRS和追踪关系
│   ├── 15_evaluation/            # 技术选型、PoC、性能和竞品分析
│   ├── 20_system_design/         # 软件系统架构、边界和质量属性
│   │   └── mechanisms/           # 认证、调度、恢复、审计等端到端机制
│   ├── 30_subsystem_design/      # 主要子系统、服务或进程设计
│   ├── 40_module_design/         # 包、模块和组件内部设计
│   ├── 50_implementation_design/ # 类、文件、算法和关键实现单元设计
│   ├── 60_interfaces/            # 接口目录、ICD和机器契约索引
│   ├── 70_verification/          # 测试计划、规格、步骤、报告和验收
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
├── src/                          # 可发布的软件产品源码
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
│   ├── contract/                 # API、Schema、事件和兼容契约测试
│   ├── integration/              # 多模块和外部依赖集成测试
│   ├── system/                   # 完整软件系统端到端测试
│   ├── acceptance/               # 用户或客户验收自动化
│   ├── fixtures/                 # 小型、稳定、可提交的测试输入
│   └── common/                   # 公共harness、helper和oracle
├── deploy/                       # 容器、Kubernetes、systemd、IaC和环境模板
├── migrations/                   # 数据库、状态格式或协议迁移及回滚程序
├── scripts/                      # 开发者常用的短命令和任务入口
├── tools/                        # 构建、生成、检查、分析和发布工具
├── examples/                     # 面向用户或开发者的可运行示例
├── benchmarks/                   # 可复现基准场景、runner和统计方法
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
│       ├── src/                  # 该应用产品源码
│       └── tests/                # 该应用局部单元和组件测试
├── services/                     # 可独立部署的后端服务集合
│   └── <service>/                # 单个服务的Owner和发布边界
│       ├── docs/                 # 服务专属设计、接口消费和运行资料
│       ├── src/                  # 服务实现源码
│       ├── tests/                # 服务内部单元、组件和契约测试
│       ├── configs/              # 服务默认配置、示例和Schema
│       └── deploy/               # 服务独立部署定义
├── packages/                     # 可复用、可版本化的软件包和SDK
│   └── <package>/                # 单个包的Owner、API和兼容边界
│       ├── docs/                 # 包API、使用方法和内部设计
│       ├── src/                  # 包实现源码
│       └── tests/                # 包单元、兼容和发布验证
├── tests/                        # 跨Owner和平台级可执行测试
│   ├── contract/                 # 跨Owner公共契约测试
│   ├── integration/              # 多服务集成和依赖联调测试
│   ├── system/                   # 平台端到端测试
│   └── acceptance/               # 平台用户或客户验收自动化
├── deploy/                       # 平台级环境、网络、编排和IaC
├── experiments/                  # 可复现实验manifest、runner和分析代码
├── tools/                        # 仓库级构建、生成、检查和发布工具
├── third_party/                  # 全仓第三方依赖、许可证和patch
└── .local/                       # ignored：本地数据、secret和运行输出
```

平台级`docs/20_system_design/mechanisms/`管理认证、授权、任务调度、消息流、重试恢复、审计、
配额和RAG等跨服务机制。服务内部算法和类设计放在`services/<service>/docs/`，不在平台文档复制。

## 4. 关键边界

- `docs/70_verification/`保存测试计划和正式报告；`tests/`保存可执行测试。
- `interfaces/`保存机器可读公共契约；consumer只引用，不复制Schema。
- 组件内部单元测试随组件共置；根`tests/`只保存跨Owner契约、集成、系统和验收测试。
- `configs/`和`deploy/`不保存token、证书和生产secret。
- `migrations/`是软件数据/状态迁移，不是文档迁移。
- `.local/`、`build/`、`dist/`和`.cache/`不进入Git。
- 项目可按语言生态调整`src/`内部结构，但不得改变顶层Owner和authority边界。
