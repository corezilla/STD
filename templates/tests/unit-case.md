<!-- STD_DOCUMENT_COVER_BEGIN -->
# {{document_title}}

> STD 使用入口：[STD 主说明与执行流程](../../README.md)。这是工程文档标准模板；作者先读入口，再按项目已采用版本读取适用规范和专项指南。

| 文档字段 | 值 |
|---|---|
| Document ID | `{{document_id}}` |
| Document Version | `{{document_version}}` |
| Status | `{{document_status}}` |
| Project | `{{project}}` |
| Authority | `{{authority}}` |
| Document Owner | {{document_owner}} |
| Authors | {{authors}} |
| Created Date | `{{created_at}}` |
| Last Modified Date | `{{last_modified_at}}` |
| Template ID | `{{template_id}}` |
| Template Version | `{{template_version}}` |
| Template Conformance | `{{template_conformance}}` |
| Tailoring Reference | {{tailoring_ref}} |
| Migration Map Reference | {{migration_map_ref}} |
| Repository | `{{source_repository}}` |
| Canonical Path | `{{source_path}}` |
| Supersedes | {{supersedes}} |

> Reviewer、Approver、Approval Date 和 Release Tag 在进入相应状态时填写。Git commit/tag 是
> 外部不可变证据；不要在文档内容中伪造包含自身的 commit hash。
<!-- STD_DOCUMENT_COVER_END -->

<span style="color:#1f6feb"><em>**编写建议**：本文档是单个单元测试 Case 的完整设计，一 Case 一文档，与 design.implementation 阶段的测试方案（tests.unit-test-scheme）清单一一对应；测试脚本按本文档编写；LLM/智能体组件的输入构造、独立判据、统计口径与预算安全方法见 [LLM 测试方法](../../docs/ai-guides/llm-testing.md)。</em></span>

> **格式说明**：蓝色斜体为编写建议（指导如何填写，生成实例后保留）；灰色文字为虚构教学示例（以 `STD_TEMPLATE_EXAMPLE` 标记包裹，`new-design` 生成实例时自动剥离，不得当作项目事实或运行证据）；`<!-- TODO -->` 为待填槽位。颜色在 GitHub 等严格渲染器中降级为斜体/普通字，语义不变。
> 本文档对设计验证项（VRC/V-xxx）的引用规则：只引用 ID 与状态，不复制定义/判据；Case 文档若需细化执行断言需在变更时回溯设计修订并记录。

> 本 Case 文档绑定：模块对象 ID 经 `--design-object-id`、所属方案经 `--parent-document-id` 写入 metadata；Document ID＝Case ID。

### 模板定位：方案、用例与计划的边界

<span style="color:#1f6feb"><em>**编写建议**：单元层 Case；方案清单行持有设计状态，本文档持有实现状态；模块组装层 Case 归 tests.module-case。</em></span>

- **一 Case 一文档**：本文档只展开一个 Case；Document ID＝Case ID（UT-<对象>-<NNN>）；责任摘要、分类与优先级以 `tests.unit-test-scheme` 清单行为准，不在本文档重复维护。
- **测试脚本的唯一依据**：编码者按本文档写测试代码，不需要回读方案或设计正文猜测意图。
- **不预填结果**：本文档持有实现状态；执行状态与 Verdict 只在 Run 报告。

### 状态语义：实现状态

<span style="color:#1f6feb"><em>**编写建议**：本文档只持有实现状态；用例状态在方案清单，执行状态与 Verdict 只在 Run 报告；三层混用即违例。</em></span>

| 状态 | 取值 | 唯一权威记录处 | 禁止 |
|---|---|---|---|
| 测试代码实现状态 | `Planned` / `Implemented` | 本文档 §7 | 计划中的测试函数冒充可执行入口 |
| 执行状态 | `NOT_RUN` / `BLOCKED` / `INVALID` | Run 报告 | 在本文档预填执行或判定 |
| 实际判定 Verdict | `PASS` / `FAIL` | 仅 Run 报告 | 在本文档预填 Actual 或 Verdict |

<span style="color:#1f6feb"><em>**完成条件**：本 Case 能报出实现状态，且沿 Case ID 可追到方案清单行与 Run 报告。</em></span>

## 1. Case 概述与责任

<span style="color:#1f6feb"><em>**本节目的**：把方案清单里这行责任摘要展开成可实施的边界。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：Case ID、来源 ID、设计验证项、分类与优先级引用方案清单行；要测什么、明确不测什么；本 Case 的失败意味着什么。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD-003：头非法时按优先级拒绝——不证明组装后流程。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：读者不回读方案也知道本 Case 的责任与边界。</em></span>

- Case ID / 来源 ID / 设计验证项 / 分类 / 优先级（引用方案清单）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">UT-FD-003 / FD-R1 / VRC-EX-ISD-DECODE-01 / negative / P0（引用方案清单行）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 要测什么（责任展开）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">头非法时按 version→kind→length 优先级拒绝且不等待载荷</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 明确不测什么 / 失败含义：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">不测组装后流程（属于模块层）；失败含义＝校验顺序实现错误</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 2. 被测入口与前置

<span style="color:#1f6feb"><em>**本节目的**：固定被测入口与前置状态。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：被测入口完整声明；状态型初态必须经公开入口构造，不直改内部状态；fixture/向量引用其版本，不复制字节；替身/夹具/受控时钟等测试资产链接其 `tests.asset-design` 文档，契约以该文档为唯一 authority。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD-003：单次调用 decode_one，冻结向量。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：另一位执行者能独立建立前置。</em></span>

- 被测入口声明与位置：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">decode_one(std::span&lt;const std::uint8_t&gt;) noexcept，frame_decoder.h</span><!-- STD_TEMPLATE_EXAMPLE_END -->

```text
<真实公开入口签名>
```

- 初态构造（经公开入口）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">无状态，无需初态构造</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 环境类型 + ENV 实例编号（引用 tests.unit-test-plan §4 分配）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">ENV-1 独立子程序编译产物（clang17 编译产物） / ENV-2 受控时钟 fake（HARNESS-FD-CLOCK） / ENV-3 冻结向量集（docs/examples/isd-frame-decoder/）（契约见 tests.asset-design）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 依赖的测试资产（tests.asset-design 文档）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">HARNESS-FD 教学宿主 / VEC-FD 冻结向量集（契约与自检见 asset 文档）</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 3. 输入构造

<span style="color:#1f6feb"><em>**本节目的**：逐参数固定输入。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：每个参数的类型、取值、构造方法; stream/time-domain mock 设置（流式/事件驱动/SSE 用例）：用例 §2 的 fake 须提供 advance(time_ms) / emit(event) / drain() 接口；测试代码 §4 用 advance 推进时间、用 emit 触发事件；用例 §5 用 drain() 后判断言 (避免 sleep 真实时钟)。；冻结值或生成规则；非法与边界值的取舍理由；规模（数量、分页、复杂度）与时间域（wall/CPU、观测开销）按目标预算写清。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD-003：单参数冻结向量。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：输入可复现，无隐含依赖。</em></span>

- 逐参数输入构造：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">input＝hex 02 02 ff ff ff ff（version、kind 均非法，声明 length=0xffffffff）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 边界/非法取值及理由：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">同时含多项非法以暴露优先级；边界正常对照见 UT-FD-001</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 规模 / 时间域（数量、分页、复杂度、观测开销）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">单帧 8 字节级解析，O(1)；无规模与计时判据（正式项目按 ISD 预算）</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 4. 执行步骤与观察点

<span style="color:#1f6feb"><em>**本节目的**：固定动作序列与观察点。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：按序写动作与观察对象（公开返回、公开查询、权威记录、边界替身调用序）；替身调用序可断言但不证明真实协议。；执行超时与中断（单 Case 单线程超时（默认 30s，可调）+ 替身调用次数上限（默认 1000 次，超限视为 Invalid 而非 Pass）+ 观察点轮询间隔（默认 10ms，单点等待不超过 5s）；FAKE 注入未命中或超时视为该 Case 失败；Case 内中断不应改变被测全局状态、需用 RAII 风格恢复/或回滚到基线）。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：见下表灰字。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：执行者不猜下一步。</em></span>

| Step | 动作 | 观察点 |
|---|---|---|
| <!-- TODO --> | | |

<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->
<span style="color:#6e7681">| 1 | 以冻结向量单次调用 decode_one | 返回变体、consumed、输入字节 |</span>
<!-- STD_TEMPLATE_EXAMPLE_END -->

## 5. 独立 Oracle 与预期结果

<span style="color:#1f6feb"><em>**本节目的**：固定独立 Oracle 与互斥预期。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：Expected 由独立来源或可手算规则推导，不得调用被测实现复算；输出互斥（成功/各错误分支无第三态）；允许误差或精确比较方法；数值/模型输出分项判据——reference 重复性、真实输入回放、整模型比较分别判定，误差门限来自目标算法要求而非统一常数；判据语义以设计验证项（VRC）为唯一权威，本文细化为可执行断言但不改写，冲突回溯设计修订。</em></span>

> 同一 Case 不混多个负向条件或异常分支；每个条件/分支独立 Case（独立判定、独立复跑、独立 Run 记录）。需验证多条件同时非法的优先级时用专属 Case。
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD-003：手算推导。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：预期独立且互斥，可判定。</em></span>

- 独立 Oracle 来源与推导：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">FD-R1 规则＋人工计数，不调用 decode_one 复算</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 互斥预期（成功 / 各错误分支）：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">仅 Invalid(Version)：consumed=0、无视图；Ok/NeedMore/Invalid(Kind|Length) 均为失败</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 6. 错误路径、副作用与清理

<span style="color:#1f6feb"><em>**本节目的**：固定错误路径、副作用与清理。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：每个错误出口的触发与表现；副作用断言（输入不变、无半成品、资源释放）；清理与失败现场保留。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD-003：无副作用。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：失败可观察、清理可确认。</em></span>

- 错误出口与表现：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">无其他错误出口（输入长度≥6 已由 UT-FD-002 覆盖）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 副作用断言与清理：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">输入逐字节不变；无堆分配、无 I/O；无需清理</span><!-- STD_TEMPLATE_EXAMPLE_END -->

## 7. 自动化位置与状态

<span style="color:#1f6feb"><em>**本节目的**：固定自动化位置与实现状态。</em></span>
<span style="color:#1f6feb"><em>**必须写清楚**：测试文件（`tests/unit/cases/UT-<对象>-<NNN>.py`，文件名＝Case ID＋语言后缀，与本文档 Document ID 同 stem）与测试函数名（描述性）；被本模块 Case 复用的辅助函数放可执行 cases 树的 `tests/unit/cases/support/`（跨模块工具走 `tests/common/`）；单 Case 执行命令；实现状态 Planned/Implemented；执行与 Verdict 归 Run 报告。</em></span>
<span style="color:#1f6feb"><em>**抽象示例**：虚构 UT-FD-003：invalid_header_rejected。</em></span>
<span style="color:#1f6feb"><em>**完成条件**：可从本文档定位测试代码与命令。</em></span>

- 测试文件 / 测试函数：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">tests/unit/cases/UT-FD-003.py 的 invalid_header_rejected</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 单 Case 执行命令：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">正式 runner：--filter UT-FD-003（教学宿主无过滤，全量跑）</span><!-- STD_TEMPLATE_EXAMPLE_END -->
- 实现状态：<!-- TODO --><!-- STD_TEMPLATE_EXAMPLE_BEGIN --><span style="color:#6e7681">Implemented；执行与 Verdict 归 Run 报告</span><!-- STD_TEMPLATE_EXAMPLE_END -->

<!-- 交付自查：编码者能否只凭本文档写出测试脚本；预期是否独立推导（不调用被测实现复算）；失败出口与清理是否可观察？ -->
