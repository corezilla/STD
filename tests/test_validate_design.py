#!/usr/bin/env python3
"""Regression tests for validate-design discovery and read diagnostics."""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
import re
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_script(module_name: str, script_name: str):
    loader = importlib.machinery.SourceFileLoader(
        module_name, str(ROOT / "scripts" / script_name)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def load_validator():
    return load_script("std_validate_design", "validate-design")


class ValidateDesignDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_suffix_directory_is_not_discovered_as_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime" / "case-design.md").mkdir(parents=True)
            actual = root / "docs" / "actual.md"
            actual.parent.mkdir()
            actual.write_text("# Actual\n")
            excluded = root / "node_modules" / "ignored.md"
            excluded.parent.mkdir()
            excluded.write_text("# Ignored\n")

            self.assertEqual(self.validator.discover(root, ".md"), [actual])

    def test_markdown_read_failure_becomes_structured_issue(self):
        path = Path("unreadable.md")
        with mock.patch.object(Path, "read_text", side_effect=OSError("denied")):
            issues = self.validator.validate_markdown(path, None)

        self.assertEqual(issues[0]["code"], "markdown.read")
        self.assertIn("denied", issues[0]["message"])

    def test_cover_fields_are_read_only_between_cover_markers(self):
        metadata = {
            "document_id": "example",
            "document_version": "0.1.0-draft.1",
            "status": "review",
            "project": "example",
            "authority": "example",
            "document_owner": "Example Owner",
            "authors": ["Example Author"],
            "created_at": "2026-09-08",
            "last_modified_at": "2026-09-08",
            "template_id": "design.definition",
            "template_version": "1.0.0",
            "template_conformance": "legacy-mapped",
            "tailoring_ref": None,
            "migration_map_ref": "docs/migration-map.json",
            "source_repository": "example/repository",
            "source_path": "docs/example.md",
            "supersedes": None,
        }
        cover_rows = {
            field: self.validator.expected_cover_value(field, metadata)
            for field in self.validator.COVER_MAP
        }
        cover = "\n".join(f"| {field} | {value} |" for field, value in cover_rows.items())

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            path.write_text(
                "<!-- STD_DOCUMENT_COVER_BEGIN -->\n"
                "# Example\n\n"
                f"{cover}\n"
                "<!-- STD_DOCUMENT_COVER_END -->\n\n"
                "## Runtime result\n\n"
                "| Status | FAIL |\n"
            )
            issues = self.validator.validate_markdown(path, metadata)

        self.assertFalse([item for item in issues if item["code"] == "cover.mismatch"])

    def test_template_versions_are_independent_and_complete(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())

        self.assertEqual(set(catalog["templates"]), set(catalog["template_versions"]))
        for version in catalog["template_versions"].values():
            self.assertRegex(version, r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")

    def test_compact_cover_and_end_control_are_validated_together(self):
        fields = self.validator.COMPACT_COVER_FIELDS
        metadata = {key: "example" for key in self.validator.COVER_MAP.values()}
        metadata.update(status="draft", authors=["Example Author"])
        rows = {
            field: f"| {field} | {self.validator.expected_cover_value(field, metadata)} |"
            for field in self.validator.COVER_MAP
        }
        front = "\n".join(rows[field] for field in rows if field in fields)
        back = "\n".join(rows[field] for field in rows if field not in fields)
        cover = f"<!-- STD_DOCUMENT_COVER_BEGIN -->\n# Example\n{front}\n<!-- STD_DOCUMENT_COVER_END -->"
        control = f"<!-- STD_DOCUMENT_CONTROL_BEGIN -->\n{back}\n<!-- STD_DOCUMENT_CONTROL_END -->"
        document = f"{cover}\n\n## Design\n\n| Status | FAIL |\n\n## Control\n\n{control}\n"
        cases = [
            ("valid", document, None),
            ("missing-field", document.replace(rows["Authors"], ""), "cover.missing"),
            ("mismatch", document.replace(rows["Authors"], "| Authors | Wrong |"), "cover.mismatch"),
            ("duplicate", document.replace(back, rows["Status"] + "\n" + back), "cover.duplicate"),
            ("missing-end", document.replace("<!-- STD_DOCUMENT_CONTROL_END -->", ""), "cover.markers"),
            ("repeated-block", document + control, "cover.markers"),
            ("reversed", document.replace(control, "<!-- STD_DOCUMENT_CONTROL_END -->\n" + back + "\n<!-- STD_DOCUMENT_CONTROL_BEGIN -->"), "cover.markers"),
            ("nested", cover.replace("<!-- STD_DOCUMENT_COVER_END -->", control + "\n<!-- STD_DOCUMENT_COVER_END -->"), "cover.markers"),
            ("missing-front-field", document.replace(rows["Template ID"], "").replace(back, rows["Template ID"] + "\n" + back), "cover.missing"),
            ("body-cannot-supply-control", cover + "\n" + back, "cover.missing"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.md"
            for name, content, expected_code in cases:
                with self.subTest(case=name):
                    path.write_text(content)
                    issues = self.validator.validate_markdown(path, metadata)
                    if expected_code is None:
                        self.assertEqual(issues, [])
                    else:
                        self.assertIn(expected_code, [item["code"] for item in issues])

    def test_system_markdown_opening_is_short_and_control_is_at_end(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        front, body = system.split("<!-- STD_DOCUMENT_COVER_END -->", 1)
        expected = {
            "Document ID", "Document Version", "Status", "Project", "Document Owner",
            "Last Modified Date", "Template ID", "Template Version",
        }
        fields = set(re.findall(r"^\| ([^|]+?) \|", front, re.MULTILINE)) - {"文档字段"}
        self.assertEqual(fields, expected)
        self.assertEqual(fields, self.validator.COMPACT_COVER_FIELDS)
        self.assertLessEqual(len(front.splitlines()), 14)
        self.assertTrue(body.lstrip().startswith("## 1. 文档说明\n"))
        headings = re.findall(r"^#{2,3} (.+)$", system, re.MULTILINE)
        self.assertEqual(headings[:4], [
            "1. 文档说明", "1.1 目的与读者", "1.2 范围、非目标与设计层级", "2. 产品应用与设计目标",
        ])
        self.assertLess(system.index("## 2. 产品应用"), system.index("## 3. 系统概览"))
        for heading in (
            "## 附录 A.", "### A.1 修订记录", "### A.2 目录、表目录与图目录",
            "## 附录 B.", "### B.1 参考资料与术语", "### B.2 适用 profile 与章节裁剪",
            "### B.3 适用基线、视图状态与证据规则", "### B.4 设计约束与关键假设", "## 附录 C.",
        ):
            self.assertGreater(system.index(heading), system.index("## 17."))
        self.assertNotRegex(system, r"§1\.[3-6]|### 1\.[3-6]")
        self.assertIn("EX-SCENE-01｜流水线视觉检测的逻辑应用场景", system)

    def test_system_outline_matches_adopted_product_first_structure(self):
        # Freeze the agreed generic outline; CI must not depend on a project checkout.
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        expected = """1. 文档说明
1.1 目的与读者
1.2 范围、非目标与设计层级
2. 产品应用与设计目标
2.1 问题与业务背景
2.2 用户与使用场景
2.3 应用环境与系统边界
2.4 设计目标与成功条件
3. 系统概览
3.1 系统架构
3.2 组成与职责
3.3 物理与逻辑对应关系
3.4 系统机制清单与文档映射
4. 功能与需求实现概览
4.1 功能总表
4.2 关键功能原理与边界
4.3 需求追溯
5. 重要过程
5.1 重要过程总览与工作模式
5.2 一次业务处理怎样完成
5.3 系统启动过程
5.4 配置加载与生效过程
5.5 停止与重启过程
5.6 异常、过载与恢复过程
5.7 模式切换与状态迁移
6. 硬件实现方案
6.1 硬件架构与板卡组成
6.2 板间与器件接口
6.3 时钟、复位、电源与信号完整性
6.4 器件选型与容量依据
6.5 硬件可靠性与开发平台
7. 软件实现方案
7.1 软件架构
7.2 模块设计与代码映射
7.3 通信、配置与状态管理
7.4 页面与交互（如适用）
7.5 软件可靠性与开发平台
7.6 部署与运行环境
8. 可编程逻辑与专用处理单元
8.1 内部模块框图
8.2 模块处理说明
8.3 时序、资源与跨域设计
8.4 开发、仿真与调试平台
9. 数据、描述符与存储结构
9.1 业务数据流
9.2 描述符与元数据流
9.3 状态表、缓存与持久化
9.4 容量与带宽计算
10. 接口与通信协议
10.1 接口总表
10.2 数据面接口
10.3 控制与管理接口
10.4 维护与调试接口
10.5 公共数据结构与编码
10.6 硬件连接与项目选项
10.7 配置与启动环境接口
10.8 接口组合与兼容性
11. 可靠性、维护与升级
11.1 故障模型与可靠性机制
11.2 运行统计、日志与故障定位
11.3 升级与回滚
12. 性能、扩展与兼容性
12.1 性能模型与预算
12.2 瓶颈与资源余量
12.3 扩容方案与兼容矩阵
13. 可测试性与验收设计
13.1 主要测试方法与结果判定
13.2 测试控制、故障注入与恢复验证
13.3 测试环境的快速部署与复位
13.4 并发测试与环境隔离
13.5 自动化执行与复现
13.6 验证覆盖与验收矩阵
14. 信息安全架构
14.1 资产、入口与信任边界
14.2 身份认证与授权
14.3 密钥、凭据与敏感数据
14.4 控制面、管理面与调试面防护
14.5 启动、升级、回滚与供应链信任
14.6 威胁、审计与安全验证
15. 结构、热、工艺与安全设计
15.1 结构与造型
15.2 功耗与热设计
15.3 工艺与制造测试
15.4 安全与电磁兼容
16. 实现计划
17. 设计决策、风险与未决项
17.1 设计决策
17.2 下级详细设计与验收任务
附录 A. 文档控制与导航
A.1 修订记录
A.2 目录、表目录与图目录
附录 B. 设计输入与适用性
B.1 参考资料与术语
B.2 适用 profile 与章节裁剪
B.3 适用基线、视图状态与证据规则
B.4 设计约束与关键假设
附录 C. 编写与交付检查""".splitlines()
        self.assertEqual(re.findall(r"^#{2,3} (.+)$", system, re.MULTILINE), expected)
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        self.assertEqual(catalog["template_versions"]["design.system"], "8.1.0")

    def test_system_reordering_keeps_business_preconditions_and_risk_handoff(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        business = system.split("### 5.2 一次业务处理怎样完成\n", 1)[1].split("\n### ", 1)[0]
        guidance, body = business.split("</details>", 1)
        for term in ("就绪、准入和配置前提", "§5.3", "§5.4", "§5.5", "§5.6", "§5.7"):
            self.assertIn(term, guidance)
        self.assertIn("**业务主线与结果边界**", body)
        handoff = system.split("### 17.2 下级详细设计与验收任务\n", 1)[1].split("\n## ", 1)[0]
        for term in ("§3.2", "§13.6", "§16", "Constraint ID", "预设计", "技术债",
                     "本地与系统组合验收", "机制未定不判设计完成", "具体下一步", "关闭证据/Gate"):
            self.assertIn(term, handoff)
        guidance, body = handoff.split("</details>", 1)
        self.assertIn("**下级详细设计与验收任务**", body)
        self.assertIn("**关联风险、技术债与未决项**", body)

    def test_cover_sync_preserves_both_system_blocks_and_other_templates(self):
        sync = load_script("std_sync_covers", "sync-template-covers")
        cover = (ROOT / "templates/_shared/document-cover.md").read_text().strip()
        front, back = sync.split_cover(cover)
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        self.assertIn(front, system)
        self.assertIn(back, system)
        self.assertEqual(sync.COMPACT_FIELDS, self.validator.COMPACT_COVER_FIELDS)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "templates/_shared").mkdir(parents=True)
            (root / "templates/_shared/document-cover.md").write_text(cover)
            (root / "templates/catalog.json").write_text(json.dumps({
                "templates": {"design.system": "system.md", "design.hardware": "hardware.md"},
            }))
            hardware = (ROOT / "templates/design/hardware-design.md").read_text()
            system_path, hardware_path = root / "templates/system.md", root / "templates/hardware.md"
            system_path.write_text(system)
            hardware_path.write_text(hardware)
            with mock.patch.object(sync, "ROOT", root):
                sync.main()
                self.assertEqual(system_path.read_text(), system)
                self.assertEqual(hardware_path.read_text(), hardware)
                system_path.write_text(system.replace("| Authors | {{authors}} |", "| Authors | stale |"))
                sync.main()
                self.assertEqual(system_path.read_text(), system)
                self.assertEqual(hardware_path.read_text(), hardware)

    def test_template_covers_use_template_version_not_std_version(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())

        for relative in catalog["templates"].values():
            content = (ROOT / "templates" / relative).read_text()
            self.assertIn("| Template Version | `{{template_version}}` |", content)
            self.assertNotIn("| STD Version |", content)

    def test_design_templates_include_guidance_examples_and_implementation_content(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())
        design_ids = [
            "design.system", "design.system-mechanism", "design.definition",
            "design.hardware", "design.fpga", "design.data-dictionary",
        ]

        for template_id in design_ids:
            content = (ROOT / "templates" / catalog["templates"][template_id]).read_text()
            self.assertIn("编写建议", content, template_id)
            self.assertIn("示例", content, template_id)

        system = (ROOT / "templates" / catalog["templates"]["design.system"]).read_text()
        required_sections = (
            "文档说明", "系统概览", "产品应用与设计目标", "功能与需求实现概览",
            "重要过程", "硬件实现方案", "软件实现方案",
            "可编程逻辑与专用处理单元", "数据、描述符与存储结构", "接口与通信协议",
            "可靠性、维护与升级", "性能、扩展与兼容性", "可测试性与验收设计",
            "信息安全架构", "结构、热、工艺与安全设计", "实现计划", "设计决策、风险与未决项",
        )
        for heading in required_sections:
            self.assertIn(heading, system)
        self.assertEqual(system.count("<summary>编写建议、规范与示例</summary>"), len(required_sections))

        lines = system.splitlines()
        headings = [
            index for index, line in enumerate(lines)
            if line.startswith(("## ", "### ", "#### ", "##### "))
        ]
        self.assertGreater(len(headings), len(required_sections))
        for position, index in enumerate(headings):
            next_heading = headings[position + 1] if position + 1 < len(headings) else len(lines)
            cursor = index + 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if lines[cursor].strip() == "<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->":
                sample_end = lines.index("<!-- STD_TEMPLATE_EXAMPLE_END -->", cursor + 1)
                self.assertLess(sample_end, next_heading, lines[index])
                cursor = sample_end + 1
                while cursor < len(lines) and not lines[cursor].strip():
                    cursor += 1
            self.assertLess(cursor, next_heading, lines[index])
            self.assertEqual(lines[cursor].strip(), "<details>", lines[index])

            closing = lines.index("</details>", cursor + 1)
            self.assertLess(closing, next_heading, lines[index])
            guidance = "\n".join(lines[cursor:closing + 1])
            self.assertTrue(
                "**本章目的**" in guidance or "**本节目的**" in guidance,
                lines[index],
            )
            for required in ("**必须写清楚**", "**编写规范**", "**抽象示例**", "**完成条件**"):
                self.assertIn(required, guidance, lines[index])

    def test_system_executable_subsections_have_guidance_and_body_slots(self):
        """Check reusable scaffold coverage, not whether a real design is correct."""
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        expected = {
            "3.3.1": "对象身份与拓扑", "3.3.2": "管理诊断访问与共享故障域",
            "5.1.1": "跨组件操作与统筹", "5.1.2": "参与方确认与异常收敛",
            "10.2.1": "单项操作与消息定义", "10.4.1": "用户命令逐项定义",
            "10.5": "公共数据结构与编码", "10.6": "硬件连接与项目选项",
            "10.7": "配置与启动环境接口", "10.8": "接口组合与兼容性",
            "11.2.1.1": "检查项目与适用范围", "11.2.1.2": "依赖顺序与路径覆盖",
            "11.2.1.3": "结果汇总与退出恢复", "11.2.2": "指标与日志契约",
            "11.2.3": "跨组件关联、时间与快照",
            "13.2.1": "测试控制点与确认协议", "13.2.2": "支持范围与清理恢复",
        }
        for number, title in expected.items():
            with self.subTest(section=number):
                marker = "#" * (number.count(".") + 2) + f" {number} {title}\n"
                self.assertEqual(system.count(marker), 1)
                section = re.split(r"\n#{2,5} ", system.split(marker, 1)[1], maxsplit=1)[0]
                help_text, body = section.split("</details>", 1)
                for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
                    self.assertIn(f"**{label}**", help_text)
                advice = help_text.split("**编写规范**：", 1)[1].split("**抽象示例**", 1)[0]
                self.assertGreater(len(advice.strip()), 100)
                self.assertTrue(body.strip().startswith(("|", "<!--")), title)
        tailoring = system.split("### B.2", 1)[1].split("### B.3", 1)[0]
        for condition in ("§10.6", "纯软件", "单组件", "不新增通用平台", "不能因机制尚未实现"):
            self.assertIn(condition, tailoring)

    def test_shared_contracts_and_runtime_coordination_are_not_deferred(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text().replace("\n", "")
        mechanism = (ROOT / "templates/design/system-mechanism-design.md").read_text().replace("\n", "")
        for term in ("Document Owner 不等于运行时统筹者", "参数全集", "没有机器源",
                     "不手工维护第二份真相", "系统协作方案未定", "实际技术条款已核对"):
            self.assertTrue(term in system, f"Missing system rule: {term}")
        for term in ("运行时统筹与确认责任", "总体成功判据", "部分完成", "统筹者退出",
                     "公共字段", "全部提供方和消费者", "不能断言任务不存在"):
            self.assertIn(term, mechanism)
        for path in ("docs/ai-system-design-authoring-guide.md",
                     "docs/design-writing-guide.md", "docs/architecture-design-authoring-guide.md"):
            content = (ROOT / path).read_text().replace("\n", "")
            self.assertNotIn("参数全集仍由唯一的下级定义维护", content)
            self.assertNotIn("参数全集及实现细节才由下级承接", content)
            self.assertIn("公共", content)
            self.assertIn("完整", content)

    def test_ai_guide_capability_work_packages_distinguish_design_from_execution(self):
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        package = guide.split("### 4.8", 1)[1].split("## 5.", 1)[0].replace("\n", "")
        for term in ("适用条件", "通用", "虚构", "已有局部技术定义", "旧契约",
                     "共同判据", "尚未实现或验证", "双方设计输入", "系统验收", "独立的设计仍可继续"):
            self.assertTrue(term in package, f"Missing capability workflow: {term}")
        audit = guide.split("### 6.7", 1)[1].split("## 7.", 1)[0]
        self.assertIn("打开", audit)
        self.assertIn("实际技术", audit)
        review = guide.split("### 13.2", 1)[1].split("### 13.3", 1)[0].replace("\n", "")
        self.assertIn("全部适用能力子项", review)
        self.assertIn("一个代表请求不能替代", review)
        self.assertIn("实际有不同协作/清理机制", review)

    def test_ai_guide_complete_example_keeps_operations_failures_and_handoff(self):
        """Prevent the worked example degrading to names or a success-only diagram."""
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        example = guide.split("### 8.8", 1)[1].split("## 9.", 1)[0].replace("\n", " ")
        self.assertEqual(re.findall(r"\| (EX-OP\d+) /", example), ["EX-OP1", "EX-OP2"])
        self.assertEqual(re.findall(r"\| (EX-T\d+) ", example), ["EX-T1", "EX-T2", "EX-T3", "EX-T4"])
        for term in ("EX-OBS-01/v1", "NOT_RUN", "运行时统筹者", "唯一公共契约", "字段均必选",
                     "Result 成功分支", "Result 失败分支", "DEADLINE_EXCEEDED", "IDENTITY_MISMATCH",
                     "M 中途退出", "PARTIAL", "FAILED", "非原子", "单调时钟", "迟到",
                     "只读", "不得把只读可重试推广", "sys-inspect revisions", "退出 64", "EX-C1/C2"):
            self.assertIn(term, example)
        self.assertIn("不改变业务状态和无槽位泄漏", example)

    def test_system_recovery_guidance_distinguishes_readonly_sampling(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        recovery = system.split("#### 5.1.2", 1)[1].split("### 5.2", 1)[0].replace("\n", "")
        for term in ("有副作用的重新执行或在途资源复用", "旧执行权限已停止或隔离",
                     "幂等/去重", "无跨请求资源预留", "新的观测上下文",
                     "旧查询的清理期限", "新采样不是原操作恢复"):
            self.assertIn(term, recovery)
        self.assertNotIn("取消比赛", system)
        self.assertIn("命中并发时的裁决和最终结果", system)
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text().replace("\n", "")
        self.assertIn("不要求不同组件共用启动代次", guide)
        self.assertIn("可验证的关联或转换规则", re.sub(r"\s+", "", guide),
                      "Cross-object identity mapping must be explicit and verifiable")
        self.assertNotIn("双方目标身份和代次相同", guide)

    def test_readonly_example_defines_freshness_deadlines_and_cleanup(self):
        """Guard written contract boundaries; this does not execute the fictional service."""
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        example = guide.split("### 8.8", 1)[1].split("## 9.", 1)[0].replace("\n", "")
        for term in ("Cache-Control: no-store", "不跟随 `Location`", "禁止使用缓存",
                     "响应不使用内容压缩", "超过大小限制即停止读取", "0～1499",
                     "优先于此刻到达的其他结果", "截止时刻之前完成验证",
                     "非阻塞", "处理及响应写出最多 700 ms", "最迟在单元处理期限内释放",
                     "3xx 不产生第二次请求", "旧缓存不参与本轮", "HTTP 状态与合法 Error 代码对应"):
            self.assertIn(term, example)

    def test_document_metadata_schema_excludes_project_std_version(self):
        schema = json.loads((ROOT / "schemas" / "document-metadata.schema.json").read_text())

        self.assertNotIn("std_version", schema["required"])
        self.assertNotIn("std_version", schema["properties"])

    def test_system_application_scene_has_environment_user_and_task(self):
        template = ROOT / "templates/design/architecture-design.md"
        section = template.read_text().split("### 2.3 应用环境与系统边界\n", 1)[1].split("### 2.4", 1)[0]
        sample = section.split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertNotIn("<details>", sample)
        image_match = re.search(r"!\[[^]]+\]\(([^)]+)\)", sample)
        self.assertIsNotNone(image_match)
        self.assertLess(image_match.start(), sample.index("*EX-SCENE-01｜"))
        self.assertLess(sample.index("*EX-SCENE-01｜"), sample.index("工厂在自动流水线"))
        self.assertLess(sample.index("工厂在自动流水线"), sample.index("**怎样借鉴这页**"))
        for term in ("客户提供", "PCIe", "不承担", "供电和散热", "虚构", "NOT_RUN",
                     "操作人员坐在工作台前", "桌面显示器", "不新增自动剔除", "使用任务",
                     "逻辑应用场景", "不表示实际距离", "简化人形"):
            self.assertIn(term, sample)
        image_path = (template.parent / image_match[1]).resolve()
        self.assertTrue(image_path.is_relative_to(ROOT))
        png = image_path.read_bytes()
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(image_path.name, "application-scene-logical.png")
        # Preserve the exact application-scene asset selected by the user.
        self.assertEqual(hashlib.sha256(png).hexdigest(), "35042b31c8150da9ca816b40e0924f084e71f6f06e606d4da605162ceadd3225")
        self.assertGreater(int.from_bytes(png[16:20], "big"), 1000)
        self.assertTrue(image_path.with_suffix(".prompt.md").is_file())

    def test_system_architecture_sample_stays_at_system_composition_level(self):
        """Check the teaching scaffold and assets, not engineering correctness."""
        template = ROOT / "templates/design/architecture-design.md"
        section = template.read_text().split("### 3.1 系统架构\n", 1)[1].split("### 3.2", 1)[0]
        sample = section.split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertNotIn("<details>", sample)
        image_match = re.search(r"!\[[^]]+\]\(([^)]+)\)", sample)
        self.assertIsNotNone(image_match)
        self.assertLess(image_match.start(), sample.index("*EX-ARCH-01｜"))
        self.assertLess(sample.index("*EX-ARCH-01｜"), sample.index("系统由工业相机"))
        self.assertLess(sample.index("系统由工业相机"), sample.index("**怎样借鉴这页**"))
        for term in ("主机", "配套驱动", "逻辑层次", "下级设计", "短名称", "Owner",
                     "不把原理段落", "Target / Planned / NOT_RUN"):
            self.assertIn(term, sample)
        image_path = (template.parent / image_match[1]).resolve()
        self.assertTrue(image_path.is_relative_to(ROOT))
        png = image_path.read_bytes()
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(image_path.name, "system-architecture-light.png")
        # The user-selected architecture image is unchanged by the scene/roles update.
        self.assertEqual(hashlib.sha256(png).hexdigest(), "92ad577a8426935dcbee47d24a0642696b3ee851a840ac3ed686657f53c7925e")
        for connection in ("采集接口", "PCIe", "驱动 API", "显示输出"):
            self.assertIn(connection, sample)
        self.assertGreater(int.from_bytes(png[16:20], "big"), 1000)
        self.assertTrue(image_path.with_suffix(".prompt.md").is_file())
        svg = (image_path.parent / "system-architecture.svg").read_text()
        self.assertIn('viewBox="0 0 1280 620"', svg)
        self.assertNotIn("<script", svg)
        self.assertNotIn("<image", svg)
        for term in ("工业相机", "图像采集卡", "检测应用", "配套驱动", "显示器", "软件层", "硬件层"):
            self.assertIn(term, svg)
        for detail in ("DMA", "接收与校验", "卡上配置与状态", "IF-01"):
            self.assertNotIn(detail, svg)
        parsed = ET.fromstring(svg)
        ns = {"s": "http://www.w3.org/2000/svg"}
        self.assertIsNotNone(parsed.find('.//s:g[@id="host"]/s:g[@id="software-layer"]/s:g[@id="driver"]', ns))
        card = parsed.find('.//s:g[@id="host"]/s:g[@id="hardware-layer"]/s:g[@id="capture-card"]', ns)
        self.assertIsNotNone(card)
        self.assertEqual(card.findall("s:g", ns), [])

    def test_software_architecture_example_stays_logical_and_has_roles(self):
        template = ROOT / "templates/design/architecture-design.md"
        section = template.read_text().split("### 7.1 软件架构\n", 1)[1].split("### 7.2", 1)[0]
        sample = section.split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertNotIn("<details>", sample)
        image_match = re.search(r"!\[[^]]+\]\(([^)]+)\)", sample)
        self.assertIsNotNone(image_match)
        self.assertLess(image_match.start(), sample.index("*EX-SW-01｜"))
        for term in ("操作界面", "检测流程", "图像分析", "驱动 API", "设备管理", "采集控制",
                     "图像交付", "状态读取", "不是进程", "不是一条依次执行", "NOT_RUN", "§7.6",
                     "应用层", "驱动层", "定制操作系统（按需）", "普通操作系统不在本软件组成图", "删除整个底层",
                     "无图标、无连接线", "层底色用浅色", "调用关系和数据流另图表达"):
            self.assertIn(term, sample)
        image_path = (template.parent / image_match[1]).resolve()
        self.assertTrue(image_path.is_relative_to(ROOT))
        self.assertEqual(image_path, ROOT / "templates/diagrams/software-layered-architecture.svg")
        svg = ET.parse(image_path).getroot()
        ns = {"s": "http://www.w3.org/2000/svg"}
        self.assertEqual(svg.attrib["viewBox"], "0 0 1344 720")
        self.assertIsNotNone(svg.find("s:title", ns))
        self.assertIsNotNone(svg.find("s:desc", ns))
        for tag in ("script", "image", "foreignObject", "line", "polyline", "polygon", "path", "use"):
            self.assertEqual(svg.findall(f".//s:{tag}", ns), [], tag)
        ids = [node.attrib["id"] for node in svg.iter() if "id" in node.attrib]
        self.assertEqual(len(ids), len(set(ids)))
        for group, expected in (
            ("application-layer", {"operator-interface", "inspection-workflow", "image-analysis"}),
            ("driver-layer", {"driver-api", "device-management", "acquisition-control", "image-delivery", "status-readout"}),
            ("system-customization-layer", {"custom-operating-system"}),
        ):
            layer = svg.find(f'.//s:g[@id="{group}"]', ns)
            self.assertIsNotNone(layer)
            modules = {node.attrib["id"] for node in layer.findall(".//s:g", ns)
                       if node.find('s:text[@class="module-label"]', ns) is not None}
            self.assertEqual(modules, expected)
            self.assertIsNotNone(layer.find('s:text[@class="layer-label"]', ns))
        style = svg.find("s:defs/s:style", ns).text
        for selector in (".neutral .layer-panel", ".neutral .module", ".accent .layer-panel", ".accent .module",
                         ".module-label", ".layer-label", ".accent .interface"):
            self.assertIn(selector, style)
        visible_labels = ["".join(node.itertext()) for node in svg.findall(".//s:text", ns)]
        for removed_label in ("客户检测应用", "配套驱动", "系统支撑层", "操作系统 / 设备接口"):
            self.assertNotIn(removed_label, visible_labels)
        self.assertIn("系统定制层", visible_labels)
        self.assertIn("定制操作系统（按需）", visible_labels)
        self.assertIn("不是本采集案例已确定的组成", svg.find("s:desc", ns).text)
        self.assertNotIn("@import", style)
        self.assertNotRegex(style, r"url\(\s*[^#]")
        self.assertTrue(image_path.with_name("README.md").is_file())
        self.assertIn("可复用 SVG 模板", sample)

    def test_ai_guide_reuse_instructions_match_native_svg_sources(self):
        """Keep copy/edit examples usable; this does not certify design quality."""
        guide_path = ROOT / "docs/ai-system-design-authoring-guide.md"
        guide = guide_path.read_text()
        section = guide.split("### 7.9 Agent 如何直接复用 STD 图形样式\n", 1)[1].split("## 8.", 1)[0]
        ns = {"s": "http://www.w3.org/2000/svg"}
        edit_targets = {
            "software-layered-architecture": ("application-layer", "driver-layer", "system-customization-layer"),
            "fpga-program-architecture": ("own-rtl", "input-boundary", "output-boundary", "main-data-direction"),
            "board-top-layout": ("pcb-outline", "fpga-device", "power-region", "functional-connections"),
        }
        for name, ids in edit_targets.items():
            relative = f"../templates/diagrams/{name}.svg"
            self.assertIn(f"]({relative})", section)
            svg = ET.parse(guide_path.parent / relative).getroot()
            for group_id in ids:
                self.assertIn(f"`{group_id}`", section)
                self.assertIsNotNone(svg.find(f'.//s:g[@id="{group_id}"]', ns))

        # The documented fragment replaces a module in the existing style scope.
        fragment = re.search(r"```xml\n(.*?)\n```", section, re.S)
        self.assertIsNotNone(fragment)
        module = ET.fromstring(f'<svg xmlns="{ns["s"]}">{fragment[1]}</svg>')[0]
        svg = ET.parse(ROOT / "templates/diagrams/software-layered-architecture.svg").getroot()
        layer = svg.find('.//s:g[@id="driver-layer"]', ns)
        self.assertEqual(layer.attrib["class"], "accent")
        parent = layer.find('s:g[@id="product-driver"]', ns)
        old_module = parent.find('s:g[@id="device-management"]', ns)
        self.assertEqual(module.attrib["transform"], old_module.attrib["transform"])
        parent.remove(old_module)
        parent.append(module)
        ids = [node.attrib["id"] for node in svg.iter() if "id" in node.attrib]
        self.assertEqual(len(ids), len(set(ids)))
        width = int(module.find("s:rect", ns).attrib["width"])
        self.assertEqual(width, (1032 - 24 * (4 - 1)) / 4)
        for label in module.findall("s:text/s:tspan", ns):
            self.assertEqual(int(label.attrib["x"]), width / 2)
        self.assertIn("按 §7.9 选用已有图形样式", guide.split("## 14.", 1)[1])

    def test_ai_guide_template_mapping_and_readme_version_agree(self):
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        readme = (ROOT / "README.md").read_text()
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        version = re.search(r"^版本：([^ ·]+)", guide, re.M)[1]
        self.assertIn(f"`{version}`", readme)
        table = guide.split("| 方法来源 | 本版核对版本 |", 1)[1].split("\n\n", 1)[0]
        for template_id in ("design.system", "design.definition", "design.hardware",
                            "design.fpga", "design.system-mechanism"):
            row = next(line for line in table.splitlines() if f"`{template_id}`" in line)
            self.assertIn(catalog["template_versions"][template_id], row.split("|")[2])
        self.assertRegex(guide, r"本轮修订输入基线：STD commit `[0-9a-f]{40}`")
        self.assertNotIn("复核本版方法仍以页首固定 commit 为准", guide)

    def test_ai_guide_separates_review_scope_asset_kinds_and_states(self):
        """Guard against contradictory workflow wording, not content approval."""
        guide = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        scope = guide.split("### 4.1", 1)[1].split("### 4.2", 1)[0]
        self.assertIn("不重跑 S0～S7", scope)
        self.assertIn("直接依赖", scope)
        self.assertIn("完成条件后交付", scope)
        common = (ROOT / "docs/ai-authoring-guide.md").read_text()
        state = common.split("## 6.", 1)[1].split("## 7.", 1)[0]
        self.assertIn("ai-authoring-guide.md#6-", guide.split("### 9.1", 1)[1].split("### 9.2", 1)[0])
        template = (ROOT / "templates/design/architecture-design.md").read_text()
        for vocabulary in ("Current / Target / Transitional", "Planned / Partial / Implemented",
                           "NOT_RUN / BLOCKED / FAIL / PARTIAL / Verified"):
            self.assertIn(f"`{vocabulary}`", state)
            self.assertIn(f"`{vocabulary}`", template)
        self.assertNotIn("Planned / Implemented / Verified", guide)
        assets = common.split("### 7.2", 1)[1].split("## 8.", 1)[0]
        self.assertIn("ai-authoring-guide.md#72-", guide.split("### 7.3", 1)[1].split("### 7.4", 1)[0])
        for text in ("原生工程图保留", "生成式插画保留原始位图", "不存在的 SVG/三维源"):
            self.assertIn(text, assets)
        entry = guide.split("## 14.", 1)[1].split("## 15.", 1)[0]
        for text in ("局部任务不重跑", "既有合格图不强制换格式", "实现和验证状态分开填写"):
            self.assertIn(text, entry)

    def assert_approved_native_diagram(self, image_path, name, svg_sha, png_sha, dimensions):
        self.assertEqual(image_path, ROOT / f"templates/diagrams/{name}.svg")
        self.assertEqual(hashlib.sha256(image_path.read_bytes()).hexdigest(), svg_sha)
        svg = ET.parse(image_path).getroot()
        ns = {"s": "http://www.w3.org/2000/svg"}
        self.assertIsNotNone(svg.find("s:title", ns))
        self.assertIsNotNone(svg.find("s:desc", ns))
        for tag in ("script", "image", "foreignObject", "use"):
            self.assertEqual(svg.findall(f".//s:{tag}", ns), [], tag)
        ids = [node.attrib["id"] for node in svg.iter() if "id" in node.attrib]
        self.assertEqual(len(ids), len(set(ids)))
        png = (ROOT / f"docs/assets/system-design-authoring/{name}.png").read_bytes()
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(hashlib.sha256(png).hexdigest(), png_sha)
        self.assertEqual((int.from_bytes(png[16:20], "big"), int.from_bytes(png[20:24], "big")), dimensions)
        return svg, ns

    def test_board_layout_example_keeps_approved_image_and_layout_boundary(self):
        template = ROOT / "templates/design/architecture-design.md"
        section = template.read_text().split("### 6.1 硬件架构与板卡组成\n", 1)[1].split("### 6.2", 1)[0]
        sample = section.split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertNotIn("<details>", sample)
        image = re.search(r"!\[[^]]+\]\(([^)]+)\)", sample)
        self.assertIsNotNone(image)
        self.assertLess(image.start(), sample.index("*EX-HW-01｜"))
        for term in ("EX-CAP-FPGA-01", "Target / Planned / NOT_RUN", "不是 PCB 走线", "教学假设",
                     "相机接口及接口适配与保护", "**FPGA**", "**帧缓存**", "**配置 Flash**", "**参考时钟**",
                     "**电源区**", "**JTAG 调试接口**", "**PCIe 板边接口**", "§8.1", "SI/PI"):
            self.assertIn(term, sample)
        svg, ns = self.assert_approved_native_diagram(
            (template.parent / image[1]).resolve(), "board-top-layout",
            "90ad9801671ec87d2794454a34616381bdadcf10b7d4961383b3984d7e8043fb",
            "92b3624a634dc8b688cc37dcb595ef125f75a67d6acc9b22c63f5165d20634ed", (2880, 1760),
        )
        for group in ("pcb-outline", "camera-connector", "input-adaptation", "fpga-device", "frame-memory",
                      "configuration-flash", "reference-clock", "power-region", "debug-connector", "host-board-edge"):
            self.assertIsNotNone(svg.find(f'.//s:g[@id="{group}"]', ns), group)
        fpga = svg.find('.//s:g[@id="fpga-device"]', ns)
        self.assertEqual(fpga.findall("s:g", ns), [])  # One device, not a nested RTL diagram.

    def test_fpga_program_example_keeps_approved_image_and_logic_boundary(self):
        template = ROOT / "templates/design/architecture-design.md"
        section = template.read_text().split("### 8.1 内部模块框图\n", 1)[1].split("### 8.2", 1)[0]
        sample = section.split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertNotIn("<details>", sample)
        image = re.search(r"!\[[^]]+\]\(([^)]+)\)", sample)
        self.assertIsNotNone(image)
        self.assertLess(image.start(), sample.index("*EX-FPGA-01｜"))
        for term in ("EX-CAP-FPGA-01", "Target / Planned / NOT_RUN", "不是 FPGA 芯片内部资源", "接口边界",
                     "**输入解析**", "**帧组装**", "**帧队列**", "**传输调度**", "**采集控制**",
                     "**配置寄存器**", "**状态与错误统计**", "**复位与初始化**", "**调试与自检**",
                     "存储访问/控制器", "集成 IP", "不能仅凭本图宣称设计已经闭合"):
            self.assertIn(term, sample)
        svg, ns = self.assert_approved_native_diagram(
            (template.parent / image[1]).resolve(), "fpga-program-architecture",
            "ffe4b0fa19bdf7a82b7f9b11a74825a6da2f94c94a286b5d497acfc37701f9fa",
            "9627b7ecb92e7a1b9d0ff219fbf147ec3648a7d8ce2167488ac6f296a74997db", (2880, 1720),
        )
        own_rtl = svg.find('.//s:g[@id="own-rtl"]', ns)
        self.assertIsNotNone(own_rtl)
        for group in ("input-parser", "frame-assembler", "frame-queue", "transfer-scheduler",
                      "acquisition-controller", "configuration-registers", "status-error-counters",
                      "reset-initialization", "debug-self-test"):
            self.assertIsNotNone(own_rtl.find(f's:g[@id="{group}"]', ns), group)
        for boundary in ("input-boundary", "output-boundary"):
            self.assertIsNotNone(svg.find(f's:g[@id="{boundary}"]', ns))
            self.assertIsNone(own_rtl.find(f'.//s:g[@id="{boundary}"]', ns))

    def test_architecture_is_followed_by_each_component_responsibility(self):
        """Protect the readable example, not a claim about engineering completeness."""
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        section = system.split("### 3.2 组成与职责\n", 1)[1].split("### 3.3", 1)[0]
        sample = section.split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertNotIn("<details>", sample)
        self.assertIn("以下接续 EX-ARCH-01", sample)
        self.assertEqual(re.findall(r"^\*\*([^*]+)\*\*：", sample, re.MULTILINE)[:6], [
            "工业相机", "图像采集卡", "工控机", "配套驱动", "检测应用", "显示器",
        ])
        for term in ("图像", "输入", "运行环境", "接口", "不负责", "不承担", "采集卡设计", "职责"):
            self.assertIn(term, sample)
        self.assertNotIn("| Block ID", sample)
        self.assertNotIn("DMA", sample)
        self.assertIn("**逐组件职责说明**", section.split("</details>", 1)[1])

    def test_system_repeatable_units_have_narrative_slots_outside_help(self):
        """Protect the authoring scaffold, not a claim about design quality."""
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        units = {
            "F-XXX：功能名称": (
                "场景、问题与适用范围", "对象、输入与正常处理原理",
                "方案理由、代价与配置边界", "边界输入、异常与外部结果", "验收与未决事项",
            ),
            "MODE-XXX：模式名称": (
                "适用场景、基线与模式差异", "本模式流程图与编号步骤",
                "工作原理与方案理由", "配置、容量与适用限制", "代表失败与恢复衔接",
            ),
            "BLK-XXX：模块名称": (
                "职责、存在理由与输入输出对象", "处理过程与状态变化",
                "上下游协作、缓存与流控", "取舍、正常与失败推演",
            ),
        }
        for heading, slots in units.items():
            with self.subTest(unit=heading):
                section = system.split(f"#### {heading}\n", 1)[1].split("\n### ", 1)[0]
                help_block, body = section.split("</details>", 1)
                self.assertIn("**抽象示例**", help_block)
                for slot in slots:
                    self.assertIn(f"**{slot}**", body)

        self.assertEqual(system.count("<details>"), system.count("</details>"))
        # Keep the seventeen main chapters; document-control appendices are unnumbered.
        chapters = [line for line in system.splitlines() if line.startswith("## ")]
        numbered = [line.split(" ", 2)[1] for line in chapters if line.split(" ", 2)[1][0].isdigit()]
        self.assertEqual(numbered, [f"{number}." for number in range(1, 18)])

    def test_system_testability_keeps_maintenance_and_debug_boundaries(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        testing = system.split("## 13. 可测试性与验收设计\n", 1)[1].split("\n## ", 1)[0]
        headings = [line for line in testing.splitlines() if line.startswith("### ")]
        self.assertEqual(headings, [
            "### 13.1 主要测试方法与结果判定",
            "### 13.2 测试控制、故障注入与恢复验证",
            "### 13.3 测试环境的快速部署与复位",
            "### 13.4 并发测试与环境隔离",
            "### 13.5 自动化执行与复现",
            "### 13.6 验证覆盖与验收矩阵",
        ])
        maintenance = system.split("## 11. 可靠性、维护与升级\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("### 11.2 运行统计、日志与故障定位", maintenance)
        self.assertIn("#### 11.2.1 自检与诊断设计", maintenance)
        self.assertIn("### 11.3 升级与回滚", maintenance)
        self.assertNotIn("### 12.4", maintenance)
        self.assertLess(
            maintenance.index("#### 11.2.1 自检与诊断设计"),
            maintenance.index("### 11.3 升级与回滚"),
        )
        debugging = system.split("### 10.4 维护与调试接口\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("替代依赖/旁路/环回", debugging)
        self.assertIn("指示灯", debugging)
        self.assertIn("责任模块", debugging)
        for required in (
            "状态、版本与资源查询", "配置查看与校验", "运行统计", "日志与证据获取",
            "自检与诊断", "跟踪与捕获", "测试注入、替代与环回", "恢复与维护操作",
            "命令运行位置与入口", "被控对象/选择方式", "执行身份与前置条件",
            "关键调用/执行流程", "返回与失败判定", "运行影响/退出",
        ):
            self.assertIn(required, debugging)
        self.assertIn("统计口径", maintenance)
        self.assertIn("§13.4", debugging)
        self.assertIn("§11.2", testing)
        self.assertIn("§11.2.1", testing)
        self.assertIn("§10.4", testing)

    def test_system_engineering_guidance_retains_decision_and_failure_scaffolds(self):
        """Guard required authoring prompts; humans still review design correctness."""
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        prompts = {
            "3.3 物理与逻辑对应关系": ("故障类型", "共享", "进程退出", "共同故障"),
            "5.6 异常、过载与恢复过程": ("在途对象", "结果未知", "权威结果", "人工处置"),
            "6.3 时钟、复位、电源与信号完整性": ("就绪信号", "等待上限", "运行中失锁", "通道预算"),
            "7.3 通信、配置与状态管理": (
                "发布点", "部分目标失败", "多进程", "重启结果", "进程内副本", "持久化版本的保留与删除",
            ),
            "7.4 页面与交互（如适用）": ("线框图", "结果未知", "取消", "刷新", "服务端授权"),
            "8.3 时序、资源与跨域设计": ("单侧复位", "数据与描述符", "在途数据", "业务恢复"),
            "10.3 控制与管理接口": ("调用位置", "部分成功", "响应丢失", "无法查到结果"),
            "11.1 故障模型与可靠性机制": ("共同失效点", "误判", "保护机制自身失效", "选择理由"),
            "11.3 升级与回滚": ("不可逆点", "控制者中途退出", "旧版无法读取", "逐阶段失败"),
            "12.1 性能模型与预算": ("共享资源", "吞吐上界", "排队", "内存峰值", "可复算推导"),
            "15.2 功耗与热设计": ("转换损耗", "传感器失效", "回差", "状态转换", "负载限制"),
        }
        for heading, required in prompts.items():
            with self.subTest(section=heading):
                section = system.split(f"### {heading}\n", 1)[1]
                guidance = section.split("</details>", 1)[0]
                for prompt in required:
                    self.assertIn(prompt, guidance)

    def test_system_important_processes_cover_lifecycle_and_data_plane(self):
        """Keep lifecycle guidance and its narrative slots in the generated scaffold."""
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        processes = system.split("## 5. 重要过程\n", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(
            [line for line in processes.splitlines() if line.startswith("### ")],
            [
                "### 5.1 重要过程总览与工作模式",
                "### 5.2 一次业务处理怎样完成",
                "### 5.3 系统启动过程",
                "### 5.4 配置加载与生效过程",
                "### 5.5 停止与重启过程",
                "### 5.6 异常、过载与恢复过程",
                "### 5.7 模式切换与状态迁移",
            ],
        )
        self.assertIn("| Process ID |", processes)
        self.assertIn("#### MODE-XXX：模式名称", processes)
        prompts_and_slots = {
            "5.3 系统启动过程": (
                ("执行方", "超时", "部分启动失败", "并发启动", "旧执行者", "所有启动入口", "平台自动启动"),
                ("启动流程与就绪判据", "启动失败与再次启动"),
            ),
            "5.4 配置加载与生效过程": (
                ("初始配置", "重启生效", "在途任务", "保存成功", "超时", "静默采用"),
                ("配置来源、加载与生效时序", "并发、失败与恢复分支"),
            ),
            "5.5 停止与重启过程": (
                ("入口与权限", "在途任务", "强制停止", "结果未知", "临时资源", "排空超时"),
                ("停止、资源释放与重启时序",),
            ),
        }
        for heading, (prompts, slots) in prompts_and_slots.items():
            with self.subTest(section=heading):
                section = processes.split(f"### {heading}\n", 1)[1].split("\n### ", 1)[0]
                guidance, body = section.split("</details>", 1)
                for prompt in prompts:
                    self.assertIn(prompt, guidance)
                for slot in slots:
                    self.assertIn(f"**{slot}**", body)

    def test_system_process_cross_references_follow_new_section_numbers(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        data_plane = system.split("### 5.2 一次业务处理怎样完成\n", 1)[1].split("</details>", 1)[0]
        for target in ("§5.1", "§5.3", "§5.4", "§5.5", "§5.6", "§5.7"):
            self.assertIn(target, data_plane)
        reliability = system.split("### 11.1 故障模型与可靠性机制\n", 1)[1].split("</details>", 1)[0]
        self.assertIn("通过 Failure ID 引用 §5.6", reliability)
        self.assertNotIn("§5.4", reliability)
        self.assertNotIn("## 6. 工作模式与端到端流程", system)
        self.assertNotIn("### 6.2 正常数据流", system)
        hardware_startup = system.split("### 6.3 时钟、复位、电源与信号完整性\n", 1)[1].split("</details>", 1)[0]
        self.assertIn("由 §5.3 串入完整系统启动过程", hardware_startup)
        configuration = system.split("### 7.3 通信、配置与状态管理\n", 1)[1].split("</details>", 1)[0]
        self.assertIn("§5.4 的 Process ID", configuration)

    def test_system_examples_do_not_claim_unconditional_isolation_or_throughput(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        self.assertNotIn(
            "两个逻辑处理实例共享一个物理缓存控制器，但分别属于独立故障隔离域。", system,
        )
        self.assertNotIn(
            "持续吞吐支持值取输入链路、处理流水、存储和输出四阶段能力的最小值。", system,
        )
        performance = system.split("### 12.1 性能模型与预算\n", 1)[1].split("</details>", 1)[0]
        self.assertIn("资源独立或共享影响已计入", performance)
        self.assertIn("不能直接当作支持承诺", performance)
        self.assertIn("50 requests/s", performance)
        self.assertIn("两种上界都不是", performance)

    def test_system_numbered_references_resolve_to_unique_sections(self):
        for name in (
            "architecture-design.md", "design-definition.md", "system-mechanism-design.md",
            "hardware-design.md", "fpga-design.md",
        ):
            with self.subTest(template=name):
                content = (ROOT / "templates/design" / name).read_text()
                headings = re.findall(r"^#{2,5} (?:附录 )?((?:\d+|[A-C])(?:\.\d+)*)(?:\.)? ", content, re.MULTILINE)
                self.assertEqual(len(headings), len(set(headings)))
                references = set(re.findall(r"§((?:\d+|[A-C])(?:\.\d+)*)", content))
                self.assertTrue(references)
                self.assertEqual(references - set(headings), set())

    def test_design_constraint_handoffs_have_sources_freedom_and_composition(self):
        """Guard both ends of the handoff, not whether a filled design satisfies it."""
        sections = {
            "architecture-design.md": ("### 3.2 组成与职责", (
                "来源基线与决定状态", "适用条件", "承接单元/Owner", "分配预算或行为保证",
                "下游可自行决定/不可改变", "组合校核", "变更影响/裁决责任", "共享项", "待承接/待验证",
            )),
            "design-definition.md": ("### 1.1 继承的上级约束与落实方式", (
                "上级基线与决定状态", "继承预算或行为保证", "可自行选择/不可改变",
                "本地落实/内部再分配", "验证方法与结果/证据", "差距/变更影响/反馈责任", "组合校核",
            )),
            "system-mechanism-design.md": ("### 3.1 系统约束与参与方承接", (
                "上级基线与决定状态", "系统保证/分配", "参与方承接与自由度",
                "流程/协议/下级落实位置", "组合验证与证据状态", "差距/变更影响/裁决责任",
            )),
            "hardware-design.md": ("### 1.1 继承的上级约束与落实方式", (
                "Document ID", "上级基线与决定状态", "适用条件与测量边界", "继承预算或行为约束",
                "可自行选择/不可改变", "本地落实/内部再分配", "本地验证与系统组合验证/责任",
                "差距/变更影响/证据状态", "转换损耗", "公共开销", "组合校核", "裁决责任",
            )),
            "fpga-design.md": ("### 1.1 继承的上级约束与落实方式", (
                "Document ID", "上级基线与决定状态", "适用条件与计量边界", "继承预算或行为约束",
                "可自行选择/不可改变", "本地落实/内部再分配", "本地验证与系统组合验证/责任",
                "差距/变更影响/证据状态", "RTL block", "公共开销", "共享存储", "原决定责任方",
            )),
        }
        for name, (heading, prompts) in sections.items():
            with self.subTest(template=name):
                content = (ROOT / "templates/design" / name).read_text()
                section = re.split(r"\n#{2,3} ", content.split(heading + "\n", 1)[1], maxsplit=1)[0]
                guidance, body = section.split("</details>", 1)
                for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
                    self.assertIn(f"**{label}**", guidance)
                self.assertIn("| Constraint ID /", body)
                for prompt in prompts:
                    self.assertIn(prompt, section)

    def test_design_predesign_requires_resolution_and_writeback_not_just_pending(self):
        for name in ("architecture-design.md", "design-definition.md", "system-mechanism-design.md"):
            with self.subTest(template=name):
                content = (ROOT / "templates/design" / name).read_text().replace("\n", "")
                for prompt in ("预设计", "evaluation.technical-analysis", "约束", "选项", "推演", "推荐", "代价", "回写", "未实现", "未实测"):
                    self.assertTrue(prompt in content, f"Missing authoring prompt {prompt!r} in {name}")
                self.assertIn("不能判", content)
                self.assertIn("可继续", content)
                self.assertIn("口号", content)
        guide = (ROOT / "docs/architecture-design-authoring-guide.md").read_text()
        self.assertIn("## 11. 从章节预设计到下游承接", guide)
        self.assertIn("不凑两个虚假选项", guide)
        self.assertIn("不伪造签收", guide)

    def test_constraint_handoffs_reach_verification_in_all_design_layers(self):
        for name, heading, source_section, column in (
            ("architecture-design.md", "### 13.6 验证覆盖与验收矩阵", "§3.2", "| Target/Constraint ID 与能力范围 |"),
            ("design-definition.md", "## 14. 测试与验收", "§1.1", "| Function/Rule/Constraint |"),
            ("system-mechanism-design.md", "## 15. 验证、上线与回滚", "§3.1", "| 设计验证项 / Scenario/Invariant/Constraint |"),
            ("hardware-design.md", "## 12. Verification 与验收", "§1.1", "| Function/Requirement/Constraint ID |"),
            ("fpga-design.md", "## 12. Verification 与验收", "§1.1", "| Function/Invariant/Constraint ID |"),
        ):
            with self.subTest(template=name):
                content = (ROOT / "templates/design" / name).read_text()
                verification = content.split(heading + "\n", 1)[1].split("\n## ", 1)[0]
                for prompt in (source_section, "Constraint ID", "组合", column):
                    self.assertIn(prompt, verification)

    def test_specialist_templates_keep_local_and_system_acceptance_distinct(self):
        """Check constraint handoff prompts, not electrical or RTL correctness."""
        for name in ("hardware-design.md", "fpga-design.md"):
            with self.subTest(template=name):
                content = (ROOT / "templates/design" / name).read_text()
                self.assertIn("不必另建 `design.definition` 文档", content)
                self.assertIn("项目明确采用后重新评估", content)
                verification = content.split("## 12. Verification 与验收\n", 1)[1].split("\n## ", 1)[0]
                for prompt in (
                    "§1.1", "本地/系统组合范围", "验证责任", "两类结果分开",
                    "局部 PASS 不关闭系统目标", "原约束责任方", "NOT_RUN",
                ):
                    self.assertIn(prompt, verification)
        selection = (ROOT / "docs/template-selection.md").read_text()
        for prompt in ("专项模板 §1.1", "专项模板 §12", "不必再创建 `design.definition`"):
            self.assertIn(prompt, selection)
        system = (ROOT / "templates/design/architecture-design.md").read_text().replace("\n", "")
        self.assertIn("`design.definition` 或硬件/FPGA", system)
        self.assertIn("不为专项设计另建通用文档", system)

    def test_mechanism_retry_requires_authoritative_recovery_and_fencing(self):
        """Prevent the unsafe example returning; this is not a distributed-system proof."""
        content = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        self.assertNotIn("新 lease/同 generation", content)
        self.assertNotIn("| generation matches |", content)
        state_machine = content.split("## 8. 状态机与不变量\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("执行/写入授权有效", state_machine)
        recovery = content.split("## 9. 失败传播、重试与恢复\n", 1)[1].split("\n## ", 1)[0]
        guidance, body = recovery.split("</details>", 1)
        for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
            self.assertIn(f"**{label}**", guidance)
        for prompt in (
            "结果未知并核对权威状态", "旧执行者停止或已被隔离", "满足幂等/去重条件",
            "副作用接收方强制执行", "如何拒绝旧写入", "无法确认时保持阻塞或转人工",
            "由唯一契约明确", "旧 Worker 恢复", "迟到结果", "新旧执行交叠",
        ):
            self.assertIn(prompt, guidance.replace("\n", ""))
        for prompt in ("已有结果则不重试", "停止或隔离且幂等/去重成立", "unknown/blocked", "拒绝旧写入"):
            self.assertIn(prompt, body)
        verification = content.split("## 15. 验证、上线与回滚\n", 1)[1].split("\n## ", 1)[0]
        for prompt in ("FAIL-001", "旧 Worker 恢复", "副作用不重复", "无法确认则阻塞或转人工"):
            self.assertIn(prompt, verification)

    def test_mechanism_every_section_has_paragraph_guidance_and_body(self):
        content = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        headings = list(re.finditer(r"^#{2,3} (.+)$", content, re.MULTILINE))
        self.assertEqual(len(headings), 32)
        self.assertEqual(re.findall(r"^## (\d+)\.", content, re.MULTILINE),
                         [str(n) for n in range(1, 17)])
        for index, heading in enumerate(headings):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
            section = content[heading.end():end]
            with self.subTest(heading=heading[1]):
                self.assertEqual(section.count("<details>"), 1)
                self.assertEqual(section.count("</details>"), 1)
                guidance, body = section.split("</details>", 1)
                for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
                    self.assertIn(f"**{label}**", guidance)
                rules = guidance.split("**编写规范**：", 1)[1].split("**抽象示例**", 1)[0]
                self.assertGreater(len(rules.strip()), 75)
                body = re.sub(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->.*?<!-- STD_TEMPLATE_EXAMPLE_END -->",
                              "", body, flags=re.DOTALL)
                self.assertTrue(body.strip(), "Teaching material cannot be the only body")
        self.assertIn("不能只填表", content)
        self.assertNotIn("新 lease/同 generation", content)

    def test_mechanism_executable_topics_are_not_only_generic_checklists(self):
        content = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        checks = {
            "3.3": ("地址不等于身份", "共享故障/复位域", "映射"),
            "5": ("accepted", "durable", "released", "每个成功和错误"),
            "4.3": ("节点断电", "持久", "所有权", "安全复用"),
            "6.1": ("启动未就绪", "在途", "并发裁决"),
            "8.1": ("联合资源", "安全复用", "排空确认"),
            "10": ("推导", "共享开销", "背压", "不等于"),
            "11": ("身份 tuple 不是授权", "撤权", "强制点"),
            "12.1": ("窗口", "时间源", "清零", "丢失"),
            "12.2": ("完整语法", "执行位置", "施加/回读点", "软件 echo"),
            "13": ("installed", "active", "verified", "回滚前提"),
            "14": ("旧契约冲突", "全部提供方和消费者", "组合验证"),
            "15.1": ("LLM", "arm→hit→release", "独立", "real/simulated"),
            "15.2": ("就绪", "复位", "隔离测试", "竞争测试", "自动化"),
            "15.3": ("实际授权", "唯一流程", "NOT_RUN"),
        }
        for number, terms in checks.items():
            match = re.search(r"^#{2,3} " + re.escape(number) + r"[. ]+[^\n]+\n", content, re.MULTILINE)
            self.assertIsNotNone(match, number)
            section = re.split(r"\n#{2,3} ", content[match.end():], maxsplit=1)[0]
            for term in terms:
                self.assertIn(term, section, f"{number}: {term}")

    def test_mechanism_figures_have_visible_prose_safe_svg_and_bound_exports(self):
        content = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        blocks = re.findall(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->(.*?)<!-- STD_TEMPLATE_EXAMPLE_END -->",
                            content, re.DOTALL)
        readonly = {"usage-overview", "collaboration", "objects", "sequence", "state-lifecycle", "failure-recovery", "test-path"}
        effects = {"effect-flow", "cleanup-dependencies"}
        names = readonly | effects
        self.assertEqual(len(blocks), 12)
        seen = set()
        for block in blocks:
            self.assertNotIn("<details>", block)
            self.assertIn("Target / Planned / NOT_RUN", block)
            self.assertIn("不是第二份协议", block)
            paths = re.findall(r"!\[[^]]*\]\(([^)]+\.png)\)", block)
            if not paths:  # API, five-axis and verification teaching blocks are text/tables.
                self.assertIn("mechanism-side-effect-example.md", block)
                continue
            self.assertEqual(len(paths), 1)
            png = (ROOT / "templates/design" / paths[0]).resolve()
            self.assertTrue(png.is_file())
            seen.add(png.stem)
            self.assertIn(f"../diagrams/mechanism/{png.stem}.svg", block)
            self.assertIn("#88-完整小例两个单元的只读版本核对" if png.stem in readonly
                          else "mechanism-side-effect-example.md", block)
        self.assertEqual(seen, names)
        exports = json.loads((ROOT / "docs/assets/system-mechanism-authoring/exports.json").read_text())
        self.assertEqual((exports["width"], exports["height"]), (1440, 840))
        self.assertEqual(len(exports["exports"]), 9)
        self.assertEqual({Path(item["svg"]).stem for item in exports["exports"]}, names)
        for item in exports["exports"]:
            svg_bytes = (ROOT / item["svg"]).read_bytes()
            png_bytes = (ROOT / item["png"]).read_bytes()
            self.assertEqual(hashlib.sha256(svg_bytes).hexdigest(), item["svg_sha256"])
            self.assertEqual(hashlib.sha256(png_bytes).hexdigest(), item["png_sha256"])
            self.assertEqual(png_bytes[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual((int.from_bytes(png_bytes[16:20], "big"),
                              int.from_bytes(png_bytes[20:24], "big")), (1440, 840))
            svg = ET.fromstring(svg_bytes)
            self.assertEqual(svg.attrib["viewBox"], "0 0 1440 840")
            ids = [node.attrib["id"] for node in svg.iter() if "id" in node.attrib]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue({"title", "desc", "legend"}.issubset(ids))
            for node in svg.iter():
                self.assertNotIn(node.tag.rsplit("}", 1)[-1], ("script", "image", "foreignObject"))
                for key, value in node.attrib.items():
                    self.assertFalse(key.lower().startswith("on"))
                    if key.endswith("href"):
                        self.assertTrue(value.startswith("#"))
                    for reference in re.findall(r"url\(#([^)]+)\)", value):
                        self.assertIn(reference, ids)
            self.assertIn("EX-OBS-01/v1" if Path(item["svg"]).stem in readonly
                          else "EX-EXPORT-01/v1", svg_bytes.decode())

    def test_mechanism_example_preserves_test_order_and_volatile_boundary(self):
        content = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        sample = content.split("图 6：", 1)[1].split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        positions = [sample.index(text) for text in ("arm B", "协议路径调用后", "已 hit", "撤销延迟")]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("不保留 CLOSED 记录", content)
        self.assertIn("新观测", content)
        state = (ROOT / "templates/diagrams/mechanism/state-lifecycle.svg").read_text()
        self.assertIn("不保存 CLOSED 记录", state)
        self.assertNotIn("取消 / 进程退出", state)
        sequence = (ROOT / "templates/diagrams/mechanism/sequence.svg").read_text()
        for term in ("先后", "700 ms", "1500 ms", "2000 ms", "CLI 校验后退出 0"):
            self.assertIn(term, sequence)
        self.assertLess(sequence.index('id="query-a"'), sequence.index('id="query-b"'))

    def test_mechanism_guide_routes_same_assets_without_forcing_whole_system(self):
        guide_path = ROOT / "docs/ai-guides/system-mechanism.md"
        entry = guide_path.read_text()
        system = (ROOT / "docs/ai-system-design-authoring-guide.md").read_text()
        stub = system.split("### 14.1 系统机制写作入口", 1)[1].split("## 15.", 1)[0]
        self.assertIn("ai-guides/system-mechanism.md", stub)
        self.assertNotIn("**这六图如何复用**", stub)
        for term in ("不要求", "16", "预设计", "独立 Oracle", "不要求六图全画", "900 px",
                     "SVG 是维护源", "作者自审", "实际字段/行为定义", "未实际开展独立评审"):
            self.assertIn(term, entry)
        self.assertEqual(len(re.findall(r"\]\(../../templates/diagrams/mechanism/[^)]+\.svg\)", entry)), 9)
        for reference in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", entry):
            self.assertTrue((guide_path.parent / reference).resolve().is_file(), reference)

    def test_generated_mechanism_keeps_compact_controls_but_not_teaching_assets(self):
        source = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        sync = load_script("std_sync_mechanism_covers", "sync-template-covers")
        front, back = sync.split_cover((ROOT / "templates/_shared/document-cover.md").read_text().strip())
        self.assertIn(front, source)
        self.assertIn(back, source)
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run([str(ROOT / "scripts/new-design"), "--project", "example",
                            "--template", "design.system-mechanism", "--name", "mechanism",
                            "--output", directory, "--repository", "example/repo",
                            "--owner", "Example Owner", "--author", "Example Author"],
                           check=True, capture_output=True, text=True)
            content = (Path(directory) / "mechanism.md").read_text()
            for marker in ("STD_TEMPLATE_EXAMPLE", "../../docs/assets/", "../diagrams/", "!["):
                self.assertNotIn(marker, content)
            cover = content.split("<!-- STD_DOCUMENT_COVER_BEGIN -->", 1)[1].split("<!-- STD_DOCUMENT_COVER_END -->", 1)[0]
            self.assertEqual(len(re.findall(r"^\| [^|]+ \|", cover, re.MULTILINE)), 9)  # header + 8 fields
            self.assertEqual(content.count("<details>"), 32)
            self.assertIn("<!-- STD_DOCUMENT_CONTROL_BEGIN -->", content)
            validation = subprocess.run([str(ROOT / "scripts/validate-design"), directory, "--json"],
                                        capture_output=True, text=True)
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            self.assertEqual(json.loads(validation.stdout)["issues"], [])

    def test_system_plan_separates_review_implementation_and_integration_gates(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        planning = system.split("## 16. 实现计划\n", 1)[1].split("\n## ", 1)[0].replace("\n", "")
        self.assertNotIn("契约测试通过后才能并行开发两端", planning)
        example = planning.split("**抽象示例**：", 1)[1].split("**完成条件**", 1)[0]
        stages = ("接口语义、错误行为和测试向量完成评审后", "两端可并行实现", "分别通过契约测试后", "进入集成", "端到端验证通过后")
        positions = [example.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("不冒充真实生产者、消费者的实现测试", example)
        self.assertIn("没有循环依赖", planning)

    def test_product_scenarios_and_manufacturing_have_design_outputs(self):
        system = (ROOT / "templates/design/architecture-design.md").read_text()
        for heading, prompts in {
            "### 2.2 用户与使用场景": (
                "客户类别", "实际使用者", "主要业务任务", "部署及维护条件",
                "维护操作不能代替", "固定场景", "隔离", "可靠性",
            ),
            "### 15.3 工艺与制造测试": (
                "缺陷", "输入位置与方法", "观测/判定及未覆盖", "装配前", "装配后",
                "测试点", "烧录", "校准", "原理图", "PCB", "结构", "固件",
                "工装异常", "返修重测", "Constraint ID", "出厂禁用",
            ),
        }.items():
            with self.subTest(section=heading):
                section = system.split(heading + "\n", 1)[1].split("\n### ", 1)[0]
                for prompt in prompts:
                    self.assertIn(prompt, section)

    def test_system_mechanism_selection_preserves_readable_summary_and_unique_detail(self):
        paths = (
            "docs/template-selection.md", "docs/design-writing-guide.md",
            "docs/architecture-design-authoring-guide.md", "templates/design/architecture-design.md",
            "templates/design/system-mechanism-design.md",
        )
        for path in paths:
            with self.subTest(path=path):
                content = (ROOT / path).read_text().replace("\n", "")
                for prompt in ("端到端原理", "关键阶段", "系统级约束", "代表失败", "详细状态转换", "协议", "Constraint ID"):
                    self.assertTrue(prompt in content, f"Missing boundary prompt {prompt!r} in {path}")
        selection = (ROOT / "docs/template-selection.md").read_text()
        self.assertNotIn("保存系统全景、子系统分解、全局策略和机制目录。", selection)
        self.assertIn("系统模板 §3.2", selection)
        self.assertIn("机制模板 §3.1", selection)
        self.assertIn("单元模板 §1.1", selection)

    def test_readme_adoption_is_checked_against_project_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (root / "README.md").write_text(
                "This project adopts STD `0.1.0-draft.18`.\n"
            )
            (docs / "std.lock.json").write_text(json.dumps({
                "schema_version": "std-lock.v1",
                "std_version": "0.1.0-draft.18",
                "source_repository": "corezilla/STD",
                "source_revision": None,
                "source_tag": None,
                "source_manifest_path": "docs/std-source-manifest.json",
                "adopted_at": "2026-09-09",
                "project_profile": "software",
                "enabled_domains": ["software"],
            }))

            issues, _, _ = self.validator.validate_project_control(root, False)

            (root / "README.md").write_text(
                "This project adopts STD `0.1.0-draft.17`.\n"
            )
            mismatch, _, _ = self.validator.validate_project_control(root, False)

        self.assertFalse([item for item in issues if item["code"] == "readme.std-version"])
        self.assertTrue([item for item in mismatch if item["code"] == "readme.std-version"])

    def test_new_design_renders_independent_template_version(self):
        catalog = json.loads((ROOT / "templates" / "catalog.json").read_text())
        expected_version = catalog["template_versions"]["design.system"]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            subprocess.run([
                str(ROOT / "scripts" / "new-design"),
                "--project", "example",
                "--template", "design.system",
                "--name", "system-design",
                "--output", str(output),
                "--repository", "example/repository",
                "--owner", "Example Owner",
                "--author", "Example Author",
            ], check=True, capture_output=True, text=True)

            markdown = (output / "system-design.md").read_text()
            metadata = json.loads((output / "system-design.metadata.json").read_text())
            validation = subprocess.run([
                str(ROOT / "scripts" / "validate-design"), str(output), "--json",
            ], capture_output=True, text=True)
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            report = json.loads(validation.stdout)
            self.assertEqual(report["issues"], [])
            self.assertEqual(report["checked_metadata"], 1)
            self.assertEqual(report["checked_markdown"], 1)

        self.assertIn(f"| Template Version | `{expected_version}` |", markdown)
        self.assertIn("| Design Level | `system` |", markdown)
        self.assertIn("| Domain | `mixed` |", markdown)
        self.assertIn("| Visibility | `project` |", markdown)
        self.assertNotIn("| STD Version |", markdown)
        self.assertEqual(metadata["template_version"], expected_version)
        template = ROOT / "templates" / catalog["templates"]["design.system"]
        self.assertEqual(metadata["template_sha256"], hashlib.sha256(template.read_bytes()).hexdigest())
        self.assertEqual(metadata["design_level"], "system")
        self.assertNotIn("std_version", metadata)
        self.assertNotIn("{{", markdown)
        self.assertNotIn("STD_TEMPLATE_EXAMPLE", markdown)
        self.assertNotIn("EX-DEPLOY-01", markdown)
        self.assertNotIn("EX-SCENE-01", markdown)
        self.assertNotIn("EX-ARCH-01", markdown)
        self.assertNotIn("EX-SW-01", markdown)
        self.assertNotIn("EX-HW-01", markdown)
        self.assertNotIn("EX-FPGA-01", markdown)
        self.assertNotIn("EX-CAP-FPGA-01", markdown)
        self.assertNotIn("../../docs/assets/", markdown)
        self.assertNotIn("../diagrams/", markdown)
        self.assertIn("### 2.3 应用环境与系统边界", markdown)
        self.assertIn("提供逻辑应用场景/上下文图、上下游及责任边界", markdown)
        self.assertIn("填入项目系统架构图", markdown)
        self.assertIn("**逐组件职责说明**", markdown)
        self.assertIn("#### MODE-XXX：模式名称", markdown)
        self.assertIn("#### BLK-XXX：模块名称", markdown)
        self.assertIn("## 5. 重要过程", markdown)
        self.assertIn("### 5.3 系统启动过程", markdown)
        self.assertIn("### 5.4 配置加载与生效过程", markdown)
        self.assertIn("### 5.2 一次业务处理怎样完成", markdown)

    def test_new_design_preserves_explicit_level_and_other_template_default(self):
        for template_id, level, expected in (
            ("design.system", "cross-level", "cross-level"),
            ("design.definition", "module", "module"),
            ("design.system-mechanism", None, "cross-level"),
        ):
            with self.subTest(template=template_id, level=level), tempfile.TemporaryDirectory() as directory:
                command = [
                    str(ROOT / "scripts" / "new-design"), "--project", "example",
                    "--template", template_id, "--name", "level-example", "--output", directory,
                    "--repository", "example/repository", "--owner", "Example Owner",
                    "--author", "Example Author",
                ]
                if level is not None:
                    command.extend(["--level", level])
                subprocess.run(command, check=True, capture_output=True, text=True)
                metadata = json.loads((Path(directory) / "level-example.metadata.json").read_text())
                self.assertEqual(metadata["design_level"], expected)

    def test_generated_design_handoffs_validate_in_all_design_layers(self):
        catalog = json.loads((ROOT / "templates/catalog.json").read_text())
        for template_id, heading in (
            ("design.system", "**系统约束分配与下游承接**"),
            ("design.definition", "### 1.1 继承的上级约束与落实方式"),
            ("design.system-mechanism", "### 3.1 系统约束与参与方承接"),
            ("design.hardware", "### 1.1 继承的上级约束与落实方式"),
            ("design.fpga", "### 1.1 继承的上级约束与落实方式"),
        ):
            with self.subTest(template=template_id), tempfile.TemporaryDirectory() as directory:
                output = Path(directory)
                subprocess.run([
                    str(ROOT / "scripts/new-design"), "--project", "example", "--template", template_id,
                    "--name", "handoff-design", "--output", directory, "--repository", "example/repository",
                    "--owner", "Example Owner", "--author", "Example Author",
                ], check=True, capture_output=True, text=True)
                content = (output / "handoff-design.md").read_text()
                metadata = json.loads((output / "handoff-design.metadata.json").read_text())
                self.assertIn(heading, content)
                self.assertIn("| Constraint ID /", content)
                self.assertNotIn("{{", content)
                self.assertEqual(metadata["template_version"], catalog["template_versions"][template_id])
                template = ROOT / "templates" / catalog["templates"][template_id]
                self.assertEqual(metadata["template_sha256"], hashlib.sha256(template.read_bytes()).hexdigest())
                result = subprocess.run([
                    str(ROOT / "scripts/validate-design"), directory, "--json",
                ], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["issues"], [])
                self.assertEqual(report["checked_markdown"], 1)
                self.assertEqual(report["checked_metadata"], 1)


class SourceManifestDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_script("std_build_source_manifest", "build-source-manifest")
        cls.verifier = load_script("std_verify_source_manifest", "verify-source-manifest")
        cls.validator = load_validator()

    def test_git_ignored_platform_metadata_is_not_a_source_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(".DS_Store\n")
            template = root / "templates" / "kept.md"
            template.parent.mkdir()
            template.write_text("# Kept\n")
            ignored = root / "templates" / ".DS_Store"
            ignored.write_bytes(b"platform metadata")
            guide = root / "docs" / "guide.md"
            guide.parent.mkdir()
            guide.write_text("# Guide\n")
            subprocess.run(["git", "-C", str(root), "add", ".gitignore", "templates/kept.md"], check=True)

            expected = {"docs/guide.md", "templates/kept.md"}
            excluded = root / "outside-manifest.json"
            built = {path.relative_to(root).as_posix() for path in self.builder.source_paths(root, excluded)}

            self.assertEqual(built, expected)
            self.assertEqual(self.verifier.expected_paths(root), expected)
            self.assertEqual(self.validator.expected_source_paths(root), expected)

    def test_non_git_fallback_excludes_platform_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guide = root / "docs" / "guide.md"
            guide.parent.mkdir()
            guide.write_text("# Guide\n")
            (root / "docs" / ".DS_Store").write_bytes(b"platform metadata")
            cached = root / "scripts" / "__pycache__" / "cached.pyc"
            cached.parent.mkdir(parents=True)
            cached.write_bytes(b"cache")

            expected = {"docs/guide.md"}
            excluded = root / "outside-manifest.json"
            built = {path.relative_to(root).as_posix() for path in self.builder.source_paths(root, excluded)}

            self.assertEqual(built, expected)
            self.assertEqual(self.verifier.expected_paths(root), expected)
            self.assertEqual(self.validator.expected_source_paths(root), expected)


class RagManifestVersionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_script("std_build_rag_manifest", "build-rag-manifest")

    def test_catalog_template_uses_its_independent_version(self):
        catalog = {
            "templates": {"design.system": "design/system-design.md"},
            "template_versions": {"design.system": "2.3.4"},
        }

        self.assertEqual(
            self.builder.versions_for(
                "templates/design/system-design.md", "9.9.9", catalog
            ),
            ("2.3.4", "2.3.4"),
        )

    def test_guidance_uses_std_version(self):
        catalog = {"templates": {}, "template_versions": {}}

        self.assertEqual(
            self.builder.versions_for("docs/versioning.md", "9.9.9", catalog),
            ("9.9.9", "9.9.9"),
        )

if __name__ == "__main__":
    unittest.main()
