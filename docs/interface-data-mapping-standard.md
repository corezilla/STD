# 接口与数据规格映射规范

版本：2.0.0-draft.1 · 日期：2026-09-12 · 状态：待发布方法；不自动升级项目采用基线

## 1. 双读者与唯一来源

设计交付面向人和 Agent：人从正文理解用途、机制、取舍及失败边界；Agent 从稳定成员 ID
定位完整字段/操作，再找到同一基线的实现责任和验证。只交链接、名称或一条请求示例均不完整。
[设计文档编写规范](design-writing-guide.md)规定交付质量，本规范唯一维护映射模型；
模板提供正文栏目，[通用 AI 指南](ai-authoring-guide.md)及专项说明执行方法。

机器契约拥有结构、类型、签名及适用的编码；正文拥有前后置条件、顺序、并发、失败和寿命。
正文保留完整阅读视图，可由源生成或逐项核对，记录基线；禁止独立改两套字段。
机器行为摘要回链正文，不另立状态机。既有 Proto/OpenAPI/JSON Schema/RTL/YAML 原位保留，
不为统一扩展名迁移文件或重造协议。公共类型引用原 ID；别名/投影/转换须说明逐字段映射、
新增与损失语义及验证责任。Proposed 契约可先在设计中提出，但下游实现基线必须含实际机器定义。

## 2. 稳定身份与目录

建议在现有接口根保留人读 README 和机器 catalog；路径由项目映射决定，不强制新增顶层目录。
接口族 ID 与成员 ID 组合为 `IF-EXPORT#OP01`，字段为 `IF-EXPORT#TYPE01.operation_id`
或既有字段号。ID 不依赖章节、路径或实现函数名，不因移动重编号、回收或复用；历史带版本的 ID
保留。契约 version/revision 与文档版本单独固定；ID 不变不代表兼容。

[interface-catalog.schema.json](../schemas/interface-catalog.schema.json)是模型 2.0.0 的格式 authority。
2.0.0 新增必填的独立下游范围输入，与 1.0.0 不兼容；只有项目明确采用本修订时才迁移，
不把旧清单静默当成新格式通过。原成员 ID、契约版本、正文身份和源文件位置不因此改变。
对象禁止额外字段；字符串非空、ID/路径/摘要按 Schema 限制；revision 保留源的字符串或整数类型，
不把 JSON 整数修订号强改为字符串。必填项及条件如下：

| 记录 | 必填内容与实际写法 |
|---|---|
| 顶层 | schema_version、repository、families、members；repository 是稳定仓库名，不是本机路径 |
| family | id/name/purpose、providers/consumers、source、coverage、downstream_inventory；目的写使用任务，不只写接口名称 |
| source | repository、根相对 path、selector、version/revision 及其 selector、SHA-256、semantic_scope |
| member | id/family/kind/name、source、prose、bindings、status、evolution、downstream、reading_view |
| prose | repository/path、Document ID/version、显式稳定 anchor；身份复用同名 metadata 与受控封面 |
| bindings | role、target 成员 ID、相对本成员定义的 selector；alias/conversion 另需 mapping 说明 |
| downstream | 提供/消费 role、module/backend、version/revision/source_sha256、实现和验证状态、location/symbol、design_items/cases、verification_ref/runs |

正文身份沿用同名 `.metadata.json` 的 `document_id/document_version/source_repository/source_path`，
并与 `STD_DOCUMENT_COVER_BEGIN/END` 封面及可选 `STD_DOCUMENT_CONTROL_BEGIN/END` 文末控制区核对。
检查器复用 `validate-design` 的封面校验和现有 document-metadata Schema，再与目录比对；
不扫描示例表格冒充封面，不要求项目追踪新模板版本。显式 `<a id="contract-data"></a>` 只定位章节，
一个正文可给多个成员共用锚点。不得新建独立的隐藏文档 ID/版本；旧 `Document ID/Version` 注释若仍保留，
只能是 metadata 的唯一且一致的镜像，冲突即失败，缺失 metadata 也不能退回注释验证。
代码 location 只含 repository/path，symbol 为实际声明；未实现时二者为 null，不创建空代码。
verification_ref 定位既有验证表，design_items、Case 和 Run 是不同 ID；未实现 Case 仍保留在
该表的分母中，NOT_RUN 不得填伪造 Run。目录只索引任务/证据，不另复制全项目测试平台。

path 必须为 POSIX 仓库根相对普通文件路径：禁止绝对路径、`..`、反斜线、URL、符号链接。
跨仓库通过 CLI 显式 `--repository-root ID=PATH` 映射已经取得的固定副本；检查器不联网、不读默认相邻项目。
来源 version/revision 的 selector 必须实际可读取且值相等，SHA-256 绑定完整文件字节；
绑定工作树摘要不等于已提交，发布时另记录实际包含这些字节的不可变 commit。

selector.kind 支持 `json_pointer`（RFC 6901，根为 `""`，`~0/~1` 转义）与 `literal`
（原生格式中的唯一完整声明行，非任意代码/查询）。JSON 指针直接解析值；literal 只证实精确定位，
不能据此宣布原生字段或 ABI 校验。原生版本亦可选唯一版本声明行，此时 version/revision 保存完整行。
原生 Proto/RTL 等内容语义须由项目现有解析器/适配检查完成，记录实际命令及覆盖，不通过改扩展名伪装 JSON。

## 3. 数据和操作的设计深度

每个公共类型写用途、生产/消费、完整字段、身份/版本、所有权、可见时点及寿命；逐字段给
名字、类型/位宽、单位、大小/长度/计数来源、含义、范围/枚举、必填/缺省/可空、条件有效性、
引用目标和跨字段约束。可变长度有上限及溢出处理。逻辑宽度、序列化长度、Host sizeof 和 wire
offset 分开；只有实际二进制 ABI 才规定端序、对齐、padding/reserved、校验覆盖，不虚构 packed 布局。

逐操作写提供/调用方、同步/异步、完整请求/响应/事件/错误类型、身份权限、前置及校验顺序、
副作用、accepted/completed/effective/released 保证、重复/幂等、取消/超时和每个错误后的合法动作。
目录的 role 必须与源签名语义一致，所有适用槽位恰好映射一次，不能漏响应、重复请求或用 alias 掩盖错配。
本检查器支持源 JSON 对象中命名的 `request/response/event/error` 类型引用及 `args`（role=field），
包括这些槽位内嵌的 `$ref`；从源枚举角色与 selector，再核对目录和目标类型。单向操作只映射源实际声明的
槽位，不强加不存在的响应。未知签名布局报未支持并阻止本项通过，由项目解析器适配；不把 OpenAPI/Proto 等
其他布局默认为此形状，也不为适配工具重写原协议。转换应另由实际类型/转换定义承载，不能替代操作的真实签名。
CLI 同时给命令 ID、参数类型/范围/默认/互斥、stdout/stderr/退出码及执行环境。
硬件边界给标准号/版本/适用部分和项目绑定；自定义信号按实际写方向、位宽、时钟/时序、电气条件。
标准链接不能代替未被标准决定的项目选项。不存在的信号或故障控制不为填模板新增。

## 4. 覆盖、演进与下游

coverage.level 为 entry_only（只有接口族）、selected_members（指定子集）、complete（声明范围全集）。
scope 必须解释分母，excluded_scope 解释未覆盖部分，不能把目录遗漏解释成接口不存在。
complete 的 inventory 是实际机器源字典容器列表，检查器枚举每个直接子定义，与成员来源集合双向比较；
不能用目录自身的 ID 列表充当独立分母。原生不可枚举来源不得靠 literal 声称本工具完成全集验证。

status.design 为 proposed/in_review/approved/deprecated；implementation 为 not_implemented/partial/implemented；
verification 为 not_run/blocked/fail/pass。文档批准不等于实现，结构检查 PASS 不得填作运行验证 PASS。
多 backend 分别登记；成员整体通过必须覆盖全部承接 backend，不能静默移除未实现或未执行者。

### 4.1 独立的承接范围分母

family.downstream_inventory 使用 source 格式绑定一份已有设计/采用范围的结构化投影，
固定 repository/path、version/revision/selectors 和完整文件 hash。其内容遵循
[downstream-scope.schema.json](../schemas/downstream-scope.schema.json) 1.0.0：

- participants 固定每个参与方 ID 及 role/module/backend；ID 与三元组都不得重复。
- members 以接口族#成员 ID 为键；每项 required 列出必须承接者，not_applicable 列出
  participant 与非空理由。每个已规划参与方在每个成员下必须恰有一种归属，不能遗漏、重复或交叠。
- 实际 member.downstream 的三元组集合必须与 required 双向相等。未实现者仍有承接行，
  implementation=not_implemented、verification=not_run；不允许删除消费者或 backend 后通过。
- complete 编目范围要求 scope 与成员全集精确一致；selected_members 可引用更大的同族
  scope，但所有入选成员必须在 scope 内；范围外成员不被此批宣告已承接。

该输入复用项目现有的采用/责任分配记录，可由其生成检查投影，不新设平行审批平台。
先按真实设计及配置确定范围，再填写实际承接，禁止从 downstream 行反向生成分母。
调整范围需记录旧新差异、原因和有权决定；检查器能发现 hash 漂移、删行和错配，但不能
证明 scope 已获批准、理由合理或现实中没有遗漏消费者，这些必须内容复审。
正文 Approved 不代表产品已实现；不过即使只有设计获批，承接行也不能少于固定 required 集合。
全体在该成员下确实不适用时可以显式逐项说明，不因此产生运行 PASS。

完整例见 [EX-EXPORT 独立范围](examples/interfaces/downstream-scope.json)。采用 2.0.0 时先
核对原有参与方及每个 backend，建立该输入并补缺失承接，最后重跑目录正反例；不能只改
schema_version，不能让工具自动为旧项目扩大编写或实现范围。

evolution 记录 active/deprecated、replaced_by（无替代为 null）及 compatibility 理由。
废弃 ID 保留为可追溯条目；删除字段、改名、范围/枚举/错误变化均需比较旧固定基线、更新兼容/替代关系，
由原 authority 决定破坏性版本及消费方迁移。只改版本字符串不能证明兼容；checker 检查绑定，语义兼容仍需
对照历史差异和项目向量。新接口源、正文投影、目录、下游消费基线与验证映射须同次同步。

## 5. 先登记机制，再逐份编写

系统设计保留一份机制清单：Mechanism ID、上级 Mechanism ID、Document ID、预定仓库相对文件名、用途/范围、
关联能力/Process/Constraint、参与单元、相关接口族、Owner、前置依赖、写作状态和已成文基线。
上级 Mechanism ID 表示设计分解与约束继承，顶层填 none；前置依赖表示写作或行为的先决条件并注明类别，
可以跨分支，不能替代父子归属，也不从父子关系推断运行时调用顺序。每个机制只有一个直接上级且上级须已登记
（可为 Planned），禁止自指、循环或悬空；被多处使用时引用原机制，不复制多个身份。子机制写明承接范围，
由上级保留组合约束；跨仓库上级须使用明确的仓库/机制 ID 定位。父子树与依赖图分别做内容走查。
可以先定稳定 ID 和文件名，不要求先创建空文件。待编写路径用代码文字，不能用会误导读者的断链；
成文后改为真实相对链接并绑定文档版本/锚点。状态区分 Planned、Draft、In Review、Approved、Retired；
Planned 行的已成文版本为 none，不能当作已存在接口来源、已接收的下游实现输入或审批依据。

一个机制只有一个详细规范来源；移动文件更新映射，拆分/合并另登记 ID 去向。系统仍保留端到端原理、
关键阶段、共同约束和代表失败；有清单不等于系统正文只剩索引。逐份写作时先承接清单中的同一 ID、
边界及约束，发现交叠或缺口先修正清单，不另开同义文件。未完成依赖保持可见，不阻止独立章节推进。

## 6. 工具、完整示例与检查边界

运行 `python3 scripts/validate-interface-catalog --project-root . --catalog docs/examples/interfaces/catalog.json`。
依赖与已有文档检查器一致：Python 3 + jsonschema；工具只读，无网络、无动态插件执行。
新[完整映射示例](examples/interfaces/README.md)复用虚构 EX-EXPORT-01/v1，结构从真实 Schema
投影，行为仍在既有案例。`--print-view 'IF-EXPORT#OP01'` 只向 stdout 输出所选定义，方便更新阅读视图。

本工具检查格式/重复 ID、hash 与版本、来源定位、封面/metadata/目录身份、正文稳定锚点、JSON `$ref` 与签名映射完整性、
逐字投影视图、声明全集、废弃指向及下游基线/状态。reading_view 不为 null 时，正文使用
`<!-- CONTRACT_VIEW IF-EXPORT#OP01 BEGIN -->` + JSON fenced 完整投影 +对应 END 标记，
由工具确定性排序输出后核对。普通解释段落不能被自动证明与契约一致，须内容走查。
非 JSON 原生字段语义、跨字段行为、真实代码语义、Run 真实性、跨仓库兼容及运行互操作明确不由此工具证明；
输出 not_checked 和 runtime_validation，不把静态通过扩大为独立评审、产品验收或 Runtime Activation。

先按新读者复述用途/正常及失败过程，再按 Agent 做 OP→请求/响应→字段→行为→下游→验证的双向走查。
记录具体错配位置和修正，作者模拟不冒充独立评审。采用步骤和本轮逐项落实见
[变更与验收记录](interface-data-mapping-review.md)。旧项目不主动跟随，用户要求时才选定新 STD/模板基线。
