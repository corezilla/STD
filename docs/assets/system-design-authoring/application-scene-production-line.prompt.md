# 自动流水线应用场景图生成记录

工具：内置 imagegen，编辑模式（非 CLI）。日期：2026-09-10。
输入：用户本轮提供的第二张图片，即此前原创虚构的三维设备示意；未使用保密 demo。
输入附件 SHA-256：`ac3259de4990d01a41b4d2ae93624bb89bc2f13a5b80efe9cb2303d1377220c1`。
输出：`application-scene-production-line.png`，图号 EX-SCENE-01。
修改内容：将设备放入自动流水线和操作工作台的实际使用场景，移除软件层悬浮图块。
图为虚构教学示意；相机视场、机箱透视、屏幕结果和现场布置均不是实测、安全或安装依据。

最终提示词：

```text
Use case: compositing.
Edit target: the attached original fictional industrial camera / PC / display illustration. Transform it into an APPLICATION-SCENARIO illustration for an engineering system design document, not another architecture diagram. Preserve the general design identity of the industrial camera, industrial PC with a blue internal capture card, and gray monitor. Make the actual use environment immediately understandable.

Scene: a clean automatic production conveyor line carrying a few repeated generic machined metal parts, with the industrial camera firmly mounted on a gantry/bracket above the conveyor, its lens pointing down at a part in the inspection position. Beside the line, a separate ordinary workstation desk stands outside the moving equipment area. The monitor is ON THE DESK with a keyboard and mouse. One adult operator is SEATED on a chair in front of the desk, seen in comfortable three-quarter side/back view looking at the monitor; the screen displays an enlarged image of one of those metal parts with a restrained inspection outline and a small result indicator, no dense UI text. The industrial PC rests on a ventilated shelf under or beside that desk, not on the conveyor. A small subtle cutaway in the PC may reveal the one blue capture card, but keep it secondary to the overall scene.
Camera to PC and PC to monitor have a few orderly, restrained physical cable connections, routed safely along the equipment, not across the walking area. The PC supplies the display output; do not imply the capture card directly operates the display or controls the conveyor.

Composition: landscape 16:9, broad readable three-quarter technical illustration, the conveyor and mounted camera in the left/background, workstation with desk, monitor, seated operator and PC on right/foreground. All key items visible without overlap. A simple pale factory floor and uncluttered neutral background establish a workplace without unnecessary machines.
Style: professional explanatory rendered illustration, soft gray materials with a restrained blue accent on the capture card, coherent scale and soft lighting; enough realism to recognize the setup, not glossy promotional art, no futuristic dramatic lighting. Maintain the reference equipment character but adjust scale to the actual scene.
Text: Only five small readable Simplified Chinese labels placed near the corresponding item without occluding it: "自动流水线", "工业相机", "工控机", "显示器", "操作人员". No title, no paragraphs, no legends, no floating software icons, no software/hardware tier labels. Remove the original floating glass software tier, driver and application tiles, and their dotted grouping connector entirely.
Constraints: exactly one camera, one PC, one monitor, one seated adult operator. No internal subsystem labels, no DMA/cache/chip specifications, no software architecture overlays, no robotic rejector, no conveyor-control relationship, no logo or watermark. Purely fictional teaching example; not a production safety/installation specification.
```
