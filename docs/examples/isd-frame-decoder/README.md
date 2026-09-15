# FrameDecoder：ISD 可编译教学样例

EX-ISD/v1 · 教学实现修订 2（代码不变） · 不是产品 ABI 或运行验收结论。

同一 M201 的模板图、规则、完整声明和测试在这里相互核对；不新增项目接口或模块。
`frame_decoder.h` 是教学 C++ 类型/签名来源；`frame_decoder.cc` 实现格式行为，
模板是阅读视图。更改头格式、错误顺序或寿命时三者和测试必须同步；正式项目仍绑定自己的 interfaces 目录。

<a id="handoff"></a>

## 模块设计片段 → ISD → 代码与测试

本例在一个文件内模拟两份文档的承接，不另造项目模块或父层级。上游教学基线记为
`EX-FRAME-MODULE` / `1.0.0` / 本节；实现视图记为 `EX-ISD/v1` / 本样例修订2。
这两个是教学标识，不是项目metadata；实际采用还需固定本README及头文件的真实提交或SHA-256，
不把“当前工作树”视为不可变基线。下列规则ID在本教学范围内使用，不加入公共接口catalog。

**上游模块设计片段（行为决定的唯一教学维护处）**：

- `FD-R1`：M201 FrameDecoder为调用者从字节输入中解析首帧；wire头6字节，version=1、kind=1、length为u32大端且0..64。完整头先按version→kind→length拒绝非法，再判断载荷是否齐全；未齐全不消费，成功只消费首帧。
- `FD-R2`：公开C++数据和签名以[frame_decoder.h](frame_decoder.h)为教学机器源。Ok携带借用FrameView及消费数；NeedMore/Invalid消费数为0、无view。调用者必须维持输入不可变及有效直到全部view消费结束；并发调用不共享可变状态。
- `FD-R3`：算法先检查头长，再逐字节读取大端长度，验证头后以剩余输入判断载荷。payload零拷贝、解码器无堆分配，无队列、线程池、I/O或取消接口。不能把长度限制、借用方式和错误顺序留给ISD决定。
- `FD-R4`：该库不认证或授权宿主用户，不写日志，不输出payload诊断文本；只交付结果变体及InvalidReason。宿主在调用前完成自己的访问控制，在调用后消费结构化结果并按其规则做脱敏统计。真实宿主入口尚未在本教学例中实现，不宣称宿主安全/诊断闭环通过。

**独立ISD的承接矩阵**：以下是细化位置，不重复规定另一套wire格式或错误政策。

| 上游项/固定来源 | ISD细化内容 | 权威位置 | 允许自由度 | 验证位置 |
|---|---|---|---|---|
| FD-R1 / EX-FRAME-MODULE 1.0.0 / 本节 | decode_one内的早返回；read_header只读取不决定错误 | R1维护语义；下面实现映射维护函数落实 | 可调整私有helper，不可更换优先级/限长 | FD-V1→C1/C2/C3 |
| FD-R2 / 同基线及frame_decoder.h固定字节 | variant分支构造、span子视图、无view错误返回 | 头文件维护类型；R2维护寿命 | 不改公开类型或引入隐式复制 | FD-V2→C1/v1、C4 |
| FD-R3 / 同基线 | 各字节移位前转uint32_t，先减6后比长度，最后构造subspan | R3维护算法约束；实现说明维护语言步骤 | 可内联helper；不得越界读取或依赖结构体布局 | FD-V1→C3/v4/v5、C4/v1；FD-V2→并发 |
| FD-R4 / 同基线 | decode_one返回InvalidReason而不记录输入；测试宿主main消费返回变体 | R4维护边界；宿主自己的策略不在此定义 | 无权增设鉴权服务、日志或诊断命令 | FD-V3→C3；真实宿主组合NOT_RUN |

## ISD细化：字段与实现映射

下表是上游R1–R4和头文件的阅读投影与实现落点，不是第二个格式authority。修改公共规则先改上游或机器源，再同步本表、模板图文和测试；只调整不改变约束的私有helper时，不重定义R1。

| 规则/对象 | 定义与执行点 | 独立验证 |
|---|---|---|
| version:u8=1、kind:u8=1 | wire 偏移 0、1；read_header 读取，decode_one 依次检查 | C3/v2、v3 同时非法时仍固定错误优先级 |
| length:u32 大端，0..64 | wire 偏移 2..5；各字节先转 uint32_t 再移位，不把指针强转成 u32 | C3/v1/v4/v5：65、0xffffffff、256 均 LENGTH |
| 完整头先校验，再等载荷 | size>=6 后做减法；长度限界后才计算 consumed | C2 空/短输入；C3 仅头非法无需等体 |
| FrameView | 头文件中 kind + span；OK 才包含 view | C1/v1 指针等于原输入+6，字节为 41 42 |
| DecodeResult | variant<Ok,NeedMore,Invalid>；后两者 consumed=0 且没有 view | C1–C3 检查变体、消费数和错误 |
| 只解析首帧 | 成功 consumed=6+length；尾部交给 caller | C1/v3 追加 FF 仍只消费 8 |
| 借用及可重入 | 所有栈对象归调用；无共享可变状态或堆工作区 | C4 未对齐输入、并发只读及输入不变 |

read_header 位于匿名 namespace，前提是至少 6 字节；它只解码，不判断业务有效性。
decode_one 唯一维护 version→kind→length 的检查顺序。模板时序中的 INVALID 由入口检查产生，
不能让 helper 与入口维护不同的错误顺序。逐字节读取不依赖机器端序或对齐，移位前提升避免有符号溢出。
wire 字节数与 sizeof(Header) 无关，不用结构体内存布局序列化。

返回视图在函数返回后仍借用输入；caller 必须保持底层存储有效且不可变，直到所有视图使用结束。
无视图返回时借用在调用结束后终止。并发测试中主线程等待两个线程退出后才销毁输入。
悬空指针和数据竞争是调用前提违约，不通过故意触发 UB 来模拟合法错误路径。

## 从一个决定走到测试

FD-R1的“完整头先拒绝”落在 `decode_one`：调用前检查6字节足够；`read_header`将
`02 02 ff ff ff ff`解成字段，但不自行决定错误；入口先发现version非法，直接构造Invalid(Version)，
不等待那段不存在的巨大payload。`frame_decoder_test.cc` 的 `invalid` helper从公开入口调用，
独立期待Version及consumed=0，对应原C3/v2，不能改成调用被测解析器生成expected。
私有helper名称不是新成员ID；模块与ISD的两张表也不是两个实现。

| 设计验证项 | 原Case/向量与代码入口 | 本例证明范围 | 仍需其他验证 |
|---|---|---|---|
| FD-V1 格式与优先级 | C1/C2/C3 → frame_decoder_test.cc 的main、invalid、need_more | 固定输入的结果/消费数/错误；含u32高位 | 实际产品协议与真实宿主集成 |
| FD-V2 ownership与重入 | C1/v1、C4/v1/v2 → main中的指针/非对齐/并发检查 | 借用地址、并发只读、输入不变 | 调用者长时寿命、真实峰值与期限 |
| FD-V3 安全诊断边界 | C3 → invalid检查结构化InvalidReason；人工核对库实现不含日志输出 | 库错误不携带payload、无库内日志调用 | 宿主身份/授权/脱敏/统计接收入口未提供，NOT_RUN |

不为ISD复制C1–C4，增加实现边界时在原Case内追加向量。Run记录绑定实际编译器、源字节、命令与结果；
表中预期和固定测试定义不是运行记录。这里的教学标识不冒充公共目录成员；真实目录的Planned转换另见
[现有IF-EXPORT成员示例](../isd-planned-mapping.md)。

## 构建和装配

目标：C++20 命令行教学测试；公开头为 frame_decoder.h，私有 read_header 不导出。
没有全局初始化、动态库、独立线程池、安装或服务部署。std::thread 只在测试宿主用于并发演练。
从 STD 根目录执行（产物写独立临时目录）：

```sh
frame_build=$(mktemp -d)
c++ -std=c++20 -Wall -Wextra -Werror -pedantic -pthread \
  docs/examples/isd-frame-decoder/frame_decoder.cc \
  docs/examples/isd-frame-decoder/frame_decoder_test.cc -o "$frame_build/frame_decoder_test"
"$frame_build/frame_decoder_test"
```

可用实际编译器绝对路径替换 c++，记录 `--version`、平台、完整命令和退出码。自动回归使用 CXX
或当前可用编译器；无编译器明确 skip，不报告该项运行通过。测试输出固定向量及并发检查 PASS 才算本例运行成功。
可附加 `-fsanitize=address,undefined -fno-omit-frame-pointer` 运行同一向量，仍不替代完整产品验证。

本例解析时间为 O(1)、不复制 payload、不分配堆空间；测试 vector 和线程分配不属于解码器。
没有独立启动/停止或 LLM 调用，宿主的启动、排队、时间期限和额度由宿主设计承担。
本例不提供产品延迟、容量、真实宿主装配或实时性证据，不据此关闭上级预算。
