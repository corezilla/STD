# ISD 计划位置与机器目录：同一承接行的转换

教学修订 1。这里引用真实存在的 EX-EXPORT 目录记录；计划代码仅为演示，未创建实现、未修改目录、未运行真实 backend。

## 固定输入和人读计划

唯一成员为 `IF-EXPORT#OP01`（prepare），原机器源是
`docs/examples/interfaces/ex-export-v1.schema.json` 的 `/x-operations/prepare`，
version=`EX-EXPORT-01/v1`、revision=`3`，SHA-256见下面完整承接行。
完整成员、签名绑定及消费者范围继续由[原目录](interfaces/catalog.json)维护，本文只摘录其一个downstream对象，不是第二份完整catalog。

| 人读信息 | 设计时的值 |
|---|---|
| 成员及承接者 | IF-EXPORT#OP01 / provider / A-control / real-unix-socket |
| 模块设计与ISD | 两份阅读视图引用同一成员及同一承接者，不创建新的backend |
| Planned位置 | `src/control/prepare.cc` / `control::prepare`（教学计划，尚不存在） |
| 代码状态 | NOT_IMPLEMENTED，不写实际行号 |
| 验证来源 | EX-EXPORT-MAPPING 3.1.0-draft.1 / downstream |
| 原设计验证及Case | EX-V1、EX-V6 / EX-T1、EX-T6；不复制一组ISD Case |

## 设计时的机器承接行

以下JSON逐字段等于原成员的 provider/A-control/real-unix-socket 承接行，回归检查会核对。它不含计划路径，不增加Schema未知字段；既有消费者行仍保留。

```json
{
  "role": "provider",
  "module": "A-control",
  "backend": "real-unix-socket",
  "version": "EX-EXPORT-01/v1",
  "revision": "3",
  "source_sha256": "567a5dd09ddc370772601452701269e43687e57c5750e201c86d25eb2eeb5ed6",
  "implementation": "not_implemented",
  "location": null,
  "symbol": null,
  "verification": "not_run",
  "design_items": ["EX-V1", "EX-V6"],
  "cases": ["EX-T1", "EX-T6"],
  "verification_ref": {
    "repository": "corezilla/STD",
    "path": "docs/examples/interfaces/README.md",
    "document_id": "EX-EXPORT-MAPPING",
    "version": "3.1.0-draft.1",
    "anchor": "downstream"
  },
  "runs": []
}
```

## 实现后如何同步（条件演示，尚未发生）

1. 若该backend代码以后确实存在，检查仓库、文件及实际声明，并从真实入口核对prepare签名与行为。实际位置可能不同于计划；人读表改为实际位置，不移动代码来迎合旧计划。
2. 按成员ID和 `(role,module,backend)` 定位**原行**。例如只有实际发现上述实现时才将location改为 `{ "repository": "corezilla/STD", "path": "src/control/prepare.cc" }`、symbol改为 `control::prepare`，按实际覆盖标partial或implemented。此对象只是条件写法，不是可以现在提交的证据。
3. 保留version/revision/source_sha256、design_items/cases、verification_ref；这里的hash是契约源hash，不是代码hash。保留其他承接者和范围分母，不新建“ISD backend”。实现基线在既有交付记录中绑定真实commit。
4. 有代码但未跑真实backend时verification仍not_run、runs仍为空。执行原EX-T1/EX-T6后记录真实Run，按其覆盖更新状态；Python教学模型PASS不能替代真实socket backend。成员整体状态必须结合全部承接者，不能只凭这一行升为通过。
5. 重跑接口目录检查和正文映射复核。若实际实现要求改变公共行为，先回原authority解决，不能只改ISD或伪造hash通过。

反例：把Planned路径写入not_implemented行、为了模块设计与ISD各加一行、复制Case ID形成两套验证、用教学Run关闭真实backend，均不是有效转换。
