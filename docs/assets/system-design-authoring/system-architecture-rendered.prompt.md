# 系统级架构渲染样例的生成记录

工具：内置 imagegen（非 CLI）。日期：2026-09-10。
输入：仅以下原创虚构文字提示；未输入项目截图、HIFM 技术资料或保密 demo。
输出：`system-architecture-rendered.png`。它是示意渲染，不是机械、电气或接口规格。
与 `system-architecture.svg` 表达相同主要层级，但不是从该 SVG 导出的位图。

最终提示词：

```text
Use case: infographic-diagram.
Asset type: original teaching illustration for a Markdown system architecture design template.
Primary request: a concise, professionally rendered three-dimensional system composition illustration. Emphasize major components and hierarchy, NOT detailed data flow or a flat boxes-and-arrows diagram. Purely fictional generic industrial image capture system.
Composition: landscape white/off-white background, restrained isometric 3D technical visualization. Three major equipment groups read left to right: one industrial camera; a dominant central industrial PC; one customer display showing a simple inspection image (no text on screen). The central PC is a simplified translucent/cutaway gray enclosure, containing exactly one emphasized blue image capture expansion card. Do NOT depict or label chip functions, memory modules, DMA, circuitry internals, or detailed ports.
Above the PC, show a single light transparent floating software tier, clearly visually anchored to the PC rather than a separate external device. On that tier place exactly two elegant rendered software tiles: a small blue driver tile and a gray inspection-application tile. These are software symbols, not hardware boards. Use one discreet vertical grouping cue between the software tier and host, not process arrows. The blue capture card belongs INSIDE the PC, never a freestanding external unit.
Style: polished engineering manual / industrial design visualization, matte gray metal and blue accents, gentle studio shadows, coherent perspective, generous whitespace, large legible labels. Rendered objects must communicate the architecture, no decorative dashboard, no glowing sci-fi circuitry. Customer-supplied equipment is gray; product-supplied capture card and driver are blue.
Text: Only these short Simplified Chinese labels, once each, in readable dark sans-serif: "工业相机" next to camera, "工控机" next to host enclosure, "显示器" next to display, "图像采集卡" with a short leader line to the card inside host, "配套驱动" on blue software tile, "检测应用" on gray software tile, "软件层" by floating tier, "硬件层" by host hardware. No title, no explanatory sentences, no subtitles, no captions, no legend, no numbers, no interface IDs.
Constraints: only major system components, no internal subsystem decomposition. No arrows for data/control flow. Not a deployment instruction, not a detailed physical assembly drawing, not a real product or confidential reference. No logos, no brand names, no watermark.
```
