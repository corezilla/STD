# LLMTier 软件模块设计实证样板

<a id="std-entry"></a>

本目录收录经用户明确授权的 LLMTier M001、M002 模块设计及其图形资产，用于检验和示范
STD `design.definition` 模板的实际写作效果。STD 的主入口与执行规则见
[STD README](../../README.md#std-entry)。

## 样板

- [M001 HTTP API 模块设计](docs/40_module_design/http-api-design.md)：服务端点型模块，展示端点操作面、
  内部文件调用、服务提供方式、SSE 流程、文件分解与机制承接。
- [M002 Web UI 模块设计](docs/40_module_design/web-ui-design.md)：浏览器端模块，展示页面/抽屉操作面、
  页面结构、导航和交互流程、文件间接口与机制承接。

对应 metadata 与所有被引用的 PNG/SVG 资产一并保存，目录结构保持原相对引用可用。

## 来源与边界

- 来源仓库：`corezilla/LLMTier`
- 来源提交：`62f53a85b67750dc13dfa26248ae6064995d4ddb`
- 原始路径：`docs/40_module_design/{http-api-design.md,web-ui-design.md}`
- 原采用模板：`design.definition` `2.3.0`
- 文档状态：Draft

这些文件是项目实证样板，不是可直接复制的通用业务设计，也不因被 STD 收录而升级状态、改变
LLMTier authority 或替代模板规范。应用到其他项目时只能复用表达方法，必须重新建立本项目的模块
身份、边界、接口、数据、流程、实现位置和验证依据。

样板保留的是 `design.definition` `2.3.0` 字段和 metadata；它们仅示范实际模块设计的表达方法。
新建或升级文档必须以 STD 当前 [模块模板](../../templates/design/design-definition.md)及其项目已采用版本
为准，不得照抄本样板的旧字段、模板版本或 template hash。
