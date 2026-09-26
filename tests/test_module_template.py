"""Module scaffold regressions; these do not certify an authored module design."""

import hashlib
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/design/design-definition.md"
GUIDE = ROOT / "docs/ai-guides/unit-design.md"


class ModuleTemplateTests(unittest.TestCase):
    def test_recovery_semantics_align_across_software_design_chain(self):
        for filename in ("software-system-design.md", "subsystem-design.md", "design-definition.md"):
            text = (ROOT / "templates/design" / filename).read_text()
            with self.subTest(template=filename):
                for term in ("状态查询", "同请求重放", "执行者接管", "新业务重试",
                             "权威幂等记录", "完整参数", "不新增执行", "参数冲突" if filename != "design-definition.md" else "冲突参数"):
                    self.assertIn(term, text)
                self.assertNotIn("只有确认旧执行者停止或已隔离，并满足幂等/去重条件才可重试", text)
                self.assertNotIn("先确认旧执行者停止或隔离，满足幂等/去重条件才重试", text)
        guide = (ROOT / "docs/ai-guides/software-system.md").read_text()
        self.assertIn("重放无需先停止", guide)
        self.assertNotIn("确认旧执行者停止/隔离和副作用条件后才决定重试", guide)

    def test_new_module_rejects_invalid_level_and_domain_before_writes(self):
        for options in (("--level", "system"), ("--domain", "hardware"),
                        ("--domain", "software", "--domain", "hardware")):
            with tempfile.TemporaryDirectory() as directory:
                result = subprocess.run([str(ROOT / "scripts/new-design"), "--project", "example",
                    "--template", "design.definition", "--name", "bad", "--project-root", directory,
                    "--repository", "example/repo", "--owner", "Owner", "--author", "Author", *options],
                    capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("level=module", result.stderr)
                self.assertEqual(list(Path(directory).iterdir()), [])

    def test_identity_algorithm_and_original_request_guidance(self):
        text = TEMPLATE.read_text()
        for term in ("模块编号 / 正式英文名称", "直属父对象编号 / 名称",
                     "docs/software-object-identifiers.md", "英文名称（稳定编号）",
                     "每个重要算法必须有算法图", "具体输入推演",
                     "validate_all (I1)", "DirectorySelector (M101)"):
            self.assertIn(term, text)
        diagram = text.split("**接口调用图例", 1)[1].split("<!-- STD_TEMPLATE_EXAMPLE_END -->", 1)[0]
        self.assertIn("E->>V: 原始 request（只读借用，未拆字段）", diagram)
        self.assertNotIn("E->>V: records, kind", diagram)
        self.assertLess(diagram.index("else 校验成功"), diagram.index("从已校验 request 读取"))
        for case in ("缺少 records", "额外字段", "非对象输入", "INVALID_INPUT/index=null"):
            self.assertIn(case, diagram)
        guide = GUIDE.read_text()
        self.assertNotIn("../../templates/diagrams/software-layered-architecture.svg", guide)
        self.assertIn("检查请求形状、缺失和额外字段时必须取得原始请求", guide)

    def test_replay_build_and_environment_requirements(self):
        text = TEMPLATE.read_text()
        for phrase in ("状态查询只读原操作", "同请求重放", "原执行者可继续运行", "执行者接管",
                       "新业务重试", "重试不得重置总期限", "并发启动峰值", "共享额度扣减",
                       "最大输出规模", "构建目标", "编译/链接条件", "初始化及销毁",
                       "docs/examples/module-async-export-example.md"):
            self.assertIn(phrase, text)

    def test_existing_fifteen_chapters_and_paragraph_guidance(self):
        text = TEMPLATE.read_text()
        numbers = re.findall(r"(?m)^## (\d+)\. ", text)
        self.assertEqual(numbers, [str(n) for n in range(1, 16)])
        sections = re.split(r"(?m)^## ", text)[1:]
        self.assertEqual(len(sections), 17)  # 15 chapters, mechanism appendix, teaching appendix
        for section in sections:
            with self.subTest(heading=section.splitlines()[0]):
                main = section.split("\n### ", 1)[0]
                self.assertEqual(main.count("<details>"), 1)
                self.assertEqual(main.count("</details>"), 1)
                for label in ("本节目的", "必须写清楚", "编写规范", "抽象示例", "完成条件"):
                    self.assertIn(f"**{label}**", main)
                norm = main.split("**编写规范**：", 1)[1].split("\n\n", 1)[0]
                self.assertGreater(len(norm), 55)
                self.assertTrue(section.split("</details>", 1)[1].strip())

    def test_software_scope_and_actual_design_not_just_responsibilities(self):
        text = TEMPLATE.read_text()
        for term in ("《软件模块设计说明书》", "内部函数、类和算法", "不自动新增正式模块层级",
                     "职责表不能代替方案正文", "代表输入与失败推演", "文件/symbol",
                     "预设计", "不能判设计完成", "可继续", "独立 Oracle"):
            self.assertIn(term, text)
        for stale in ("适用于 subsystem、module、component", "模块/类/RTL block",
                      "相同 key 可重试", "src/document/service.ts"):
            self.assertNotIn(stale, text)
        self.assertLess(text.index("## 5. 内部结构"), text.index("## 7. 主流程"))

    def test_required_processes_and_condition_production_are_explicit(self):
        text = TEMPLATE.read_text()
        for term in ("每个重要流程都要有流程图或时序图", "连续正文和异常分支", "图文核对",
                     "每个等待", "判定来源", "合法出口", "Stage DAG 不能替代过程图",
                     "Guard 的事实来源", "公开入口", "输入不可变", "可重入范围"):
            self.assertIn(term, text)
        guide = GUIDE.read_text()
        for term in ("软件模块执行分支", "先试写一条公开调用", "不要套用上述子系统章号",
                     "此前模板反馈的复发检查", "不是关键词打勾表", "回写唯一规则位置"):
            self.assertIn(term, guide)

    def test_side_effect_rules_are_conditional_and_read_only_case_is_not_overextended(self):
        text = TEMPLATE.read_text()
        for term in ("结果已知性", "访问安全", "操作终态", "资源释放", "重新准入",
                     "旧执行者已停止或被可靠隔离", "幂等/去重条件", "不能换 key",
                     "有副作用、取证及资源收口的机制才演练", "调用者超时不等于本模块结束",
                     "没有独立 UI、线程或取消 API", "不直接篡改内部状态"):
            self.assertIn(term, text)

    def test_interface_roles_identity_and_verification_obligations(self):
        text = TEMPLATE.read_text()
        for term in ("request/response/error", "封面/metadata", "漏掉 response",
                     "规格未定义是设计缺口", "NOT_IMPLEMENTED", "NOT_RUN",
                     "§6 数据、§13 实现任务及 §14 验证", "backend", "独立 Oracle",
                     "设计验证要求 VRC", "Case", "环境/配置", "Run/证据", "并行隔离"):
            self.assertIn(term, text)
        self.assertIn("接口语义、错误行为和测试向量完成评审后两端可并行实现", text)

    def test_teaching_diagrams_and_vectors_are_one_explicitly_bounded_case(self):
        text = TEMPLATE.read_text()
        begin = "<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->"
        end = "<!-- STD_TEMPLATE_EXAMPLE_END -->"
        self.assertEqual(text.count(begin), text.count(end))
        self.assertGreaterEqual(text.count(begin), 9)
        samples = re.findall(re.escape(begin) + r"(.*?)" + re.escape(end), text, re.S)
        sample = next(block for block in samples if "EX-MODULE/v1" in block and "O1：" in block)
        self.assertEqual(sample.count("```mermaid"), 0)  # figures live alongside each subject
        self.assertEqual(text.count("```mermaid"), 11)
        for term in ("EX-MODULE/v1", "M-C1", "M-S1", "M-P1", "M101", "Target", "Planned",
                     "IF-SELECT/v1", "request=SelectRequest", "response=SelectResult",
                     "R-VALID", "R-ORDER", "候选索引为 [0,1]", '"ids":["a1","b2"]',
                     '"index":2', "E-UNIT / NOT_RUN", "O1：", "O2："):
            self.assertIn(term, sample)
        # The concrete request is independently hand-checkable; do not pretend this runs the module.
        request = json.loads(re.search(r"```json\n(.*?)\n```", sample, re.S).group(1))
        self.assertEqual(request["kind"], "A")
        self.assertEqual([r["id"] for r in request["records"]], ["b2", "a1", "c3"])
        self.assertEqual([r["priority"] for r in request["records"]], [3, 3, 9])
        self.assertIn("不是执行记录", sample)
        self.assertIn("不虚构现有机器 hash", sample)

    def test_detailed_figures_are_at_their_chapters_not_only_in_appendix(self):
        text = TEMPLATE.read_text()
        expected = {
            4: ("M-C1",), 5: ("M-S1",), 6: ("M-D1", "M-D2", "M-D3"), 7: ("M-P1",),
            8: ("M-ALG1",), 9: ("M-I1",), 10: ("M-X1", "M-X2"), 14: ("M-V1",),
        }
        for chapter, figures in expected.items():
            section = re.split(r"(?m)^## ", text.split(f"## {chapter}. ", 1)[1], maxsplit=1)[0]
            with self.subTest(chapter=chapter):
                self.assertEqual(section.count("```mermaid"), len(figures))
                for figure in figures:
                    self.assertIn(f"图 {figure} ·", section)
                    self.assertEqual(text.count(f"图 {figure} ·"), 1)
                self.assertIn("EX-MODULE/v1", section)
                self.assertIn("STD_TEMPLATE_EXAMPLE_BEGIN", section)
        algorithm = text.split("## 8. ", 1)[1].split("## 9. ", 1)[0]
        for term in ("merge_sort(indices):", "before(a, b):", "i += 1", "j += 1",
                     "[b2] 和 [a1]", "O(k log k)", "工作区峰值 O(k)", "R-ORDER"):
            self.assertIn(term, algorithm)
        guide = GUIDE.read_text()
        self.assertIn("仅统计“全文有几张图”不足以", guide)
        self.assertNotIn("M-A1", guide)

    def test_internal_structure_example_maps_components_to_files(self):
        text = TEMPLATE.read_text()
        section = text.split("## 5. 内部结构与实现位置", 1)[1].split("## 6.", 1)[0]
        for term in ("```mermaid", "M-S1", "M101", "src/select/core", "src/select/validate",
                     "src/select/filter", "src/select/order", "interfaces/select/types",
                     "实线表示同步调用", "虚线表示", "不必一一对应", "不自动增加正式设计层级",
                     "结构图不能被文件树或流程图替代", "STD_TEMPLATE_EXAMPLE_BEGIN"):
            self.assertIn(term, section)
        appendix = text.split("## 附录 B.", 1)[1]
        for path in ("core", "validate", "filter", "order"):
            self.assertIn(f"| src/select/{path}（语言后缀待定） |", appendix)

    def test_authoring_residue_is_a_review_blocker_not_a_keyword_ban(self):
        text = TEMPLATE.read_text()
        for term in ("正文与编写过程隔离", "编写/评审记录", "质量评审阻断项",
                     "图注、章节开头和新增段落", "不要关键词禁用“本图”", "不自动迁移"):
            self.assertIn(term, text)
        self.assertIn("编辑指令混入正式正文", GUIDE.read_text())

    def test_unmarked_body_does_not_keep_old_authoring_instructions_or_fiction(self):
        text = TEMPLATE.read_text()
        text = re.sub(r"<!-- STD_TEMPLATE_EXAMPLE_BEGIN -->.*?<!-- STD_TEMPLATE_EXAMPLE_END -->",
                      "", text, flags=re.S)
        text = re.sub(r"<details>.*?</details>", "", text, flags=re.S)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        prose = [line.strip() for line in text.splitlines()
                 if line.strip() and not line.startswith(("#", "|", "> STD 使用入口："))]
        self.assertIn("文档控制信息（与封面和 metadata 保持一致）：", prose)
        self.assertTrue(all(line == "文档控制信息（与封面和 metadata 保持一致）："
                            or re.match(r"^- \*\*[^*]+\*\*：?$", line)
                            for line in prose), prose)

    def test_generation_short_cover_control_and_no_fictional_body(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "README.md").write_text('# Example\n<a id="std-entry"></a>\n')
            command = [str(ROOT / "scripts/new-design"), "--project", "example",
                       "--template", "design.definition", "--name", "module-example",
                       "--project-root", directory, "--repository", "example/repo",
                       "--owner", "Example Owner", "--author", "Example Author"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            meta_path = next(Path(directory).rglob("module-example.metadata.json"))
            meta = json.loads(meta_path.read_text())
            text = meta_path.with_name("module-example.md").read_text()
            self.assertEqual(meta["template_version"], "3.3.0")
            self.assertEqual(meta["template_sha256"], hashlib.sha256(TEMPLATE.read_bytes()).hexdigest())
            self.assertEqual(meta["design_level"], "module")
            self.assertEqual(meta["domain"], ["software"])
            self.assertNotIn("std_version", meta)
            self.assertIn("docs/40_module_design/", meta["source_path"])
            cover = text.split("<!-- STD_DOCUMENT_COVER_END -->")[0]
            self.assertEqual(len(re.findall(r"^\| [A-Z][^|]+ \|", cover, re.M)), 8)
            self.assertNotIn("| Authority |", cover)
            self.assertIn("| Authority |", text.split("<!-- STD_DOCUMENT_CONTROL_BEGIN -->")[1])
            self.assertNotIn("文末 EX-MODULE", text)
            self.assertNotIn("文末类型", text)
            references = re.findall(r"\]\((\.std-template-references/[^)]+)\)", text)
            self.assertTrue(references)
            for reference in references:
                self.assertEqual((meta_path.parent / reference).read_bytes(), TEMPLATE.read_bytes())
            for removed in ("{{", "```mermaid", "图 M-P1", "图 M-S1", "src/select/validate", "附录 B.", "STD_TEMPLATE_EXAMPLE_BEGIN"):
                self.assertNotIn(removed, text)
            self.assertIn("## 附录 A. 机制承接表", text)
            checked = subprocess.run([str(ROOT / "scripts/validate-design"), directory, "--json"],
                                     capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["issues"], [])
            meta["design_level"] = "system"
            meta["domain"] = ["hardware"]
            meta_path.write_text(json.dumps(meta))
            checked = subprocess.run([str(ROOT / "scripts/validate-design"), directory, "--json"],
                                     capture_output=True, text=True)
            self.assertNotEqual(checked.returncode, 0)
            self.assertIn("metadata.module-scope", checked.stdout)

    def test_conditional_state_and_forward_delivery_are_explicit(self):
        text = TEMPLATE.read_text()
        guide = GUIDE.read_text()
        self.assertEqual(re.findall(r"(?m)^## (\d+)\. ", text), [str(n) for n in range(1, 16)])
        for fact in ("常驻服务", "跨步骤状态", "§6.7", "持久提交点", "崩溃恢复"):
            self.assertIn(fact, text)
        state = text.split("### 6.6 运行状态数据结构", 1)[1].split("### 6.7 ", 1)[0]
        for requirement in ("状态图和转换表", "Guard 的权威事实来源", "不变量", "迟到/失败出口"):
            self.assertIn(requirement, state)
        closure = text.split("### 14.1 正向覆盖与交付闭环", 1)[1].split("### 14.2 验证要求与用例", 1)[0]
        for field in ("来源与适用性", "选定方案与正文锚点", "§13 实现文件", "§14 VRC", "父级组合验证"):
            self.assertIn(field, closure)
        self.assertIn("反向核对", closure)
        self.assertIn("M-X2", text)
        self.assertIn("正向覆盖评审清单", guide)
        self.assertIn("自动检查可提示", guide)

    def test_service_surface_fixed_records_and_real_demo_are_available(self):
        text = TEMPLATE.read_text()
        for term in ("服务端点型模块", "HTTP/RPC 端点集", "5.2 内部调用过程",
                     "5.3 文件间接口契约", "5.4 服务提供方式", "5.5 依赖方向",
                     "字段名/类型/必填性/单位/范围", "13.1 文件分解（设计 → 代码文件）",
                     "15.ISD · 实现规格采用方式", "N/A — 父系统机制清单核对结果",
                     "RISK-<MODULE>-<nnn>"):
            self.assertIn(term, text)
        section2 = text.split("## 2. ", 1)[1].split("## 3. ", 1)[0]
        self.assertNotIn("| Function ID | 调用方 |", section2)
        self.assertIn("### 2.N `F-<MODULE>-<NAME>`", section2)
        appendix = text.split("## 附录 A.", 1)[1].split("文档控制信息", 1)[0]
        self.assertNotIn("| 来源机制 Document ID", appendix)
        self.assertIn("#### A.N `<Mechanism Document ID>` / `<Requirement ID>`", appendix)

        demo = ROOT / "demo/llmtier-module-design"
        for name, document_id in (("http-api-design", "http-api"), ("web-ui-design", "web-ui")):
            document = demo / "docs/40_module_design" / f"{name}.md"
            metadata = json.loads((document.with_name(f"{name}.metadata.json")).read_text())
            self.assertEqual(metadata["document_id"], document_id)
            self.assertEqual(metadata["template_version"], "2.3.0")
            self.assertEqual(metadata["status"], "draft")
            for reference in re.findall(r"!?\[[^]]*\]\((\.\./assets/[^)]+)\)", document.read_text()):
                self.assertTrue((document.parent / reference).resolve().is_file(), reference)

    def test_record_format_and_cross_document_id_namespaces_are_consistent(self):
        writing = (ROOT / "docs/design-writing-guide.md").read_text()
        ai_guide = (ROOT / "docs/ai-authoring-guide.md").read_text()
        mechanism = (ROOT / "templates/design/system-mechanism-design.md").read_text()
        mechanism_guide = (ROOT / "docs/ai-guides/system-mechanism.md").read_text()
        for term in ("固定格式段落", "同一文档内同一类记录", "M-<MECH>-DI-<nnn>",
                     "RISK-<scope>-<nnn>", "CON-<scope>-<nnn>"):
            self.assertIn(term, writing)
        self.assertIn("六个以上字段", ai_guide)
        for source in (mechanism, mechanism_guide):
            for term in ("M-<MECH>-DI-<nnn>", "RISK-<MECH>-<nnn>",
                         "CON-<MECH>-<nnn>"):
                self.assertIn(term, source)
        self.assertIn("模板 `3.3.0`", mechanism_guide)
        self.assertIn("版本：0.8.0-draft.6", mechanism_guide)

    def test_module_record_scaffolds_are_consistent_and_demo_version_is_bounded(self):
        text = TEMPLATE.read_text()
        for heading in ("#### 1.1.N `<Constraint ID>`", "#### 3.N `<Surface ID>`",
                        "#### 4.N `<Dependency ID>`", "#### 6.2.N `<真实结构名>`",
                        "#### 8.N `<Rule ID>`", "#### `<真实函数名、完整签名或 HTTP/RPC 路由>`",
                        "#### 10.N `<Failure / Concurrency ID>`",
                        "#### 12.N `<Capacity / Performance ID>`",
                        "#### 14.1.N `<Constraint / Function / Process / Rule / Interface / Error ID>`",
                        "#### 14.2.N `VRC-<MODULE>-<nnn>`",
                        "#### 15.N `RISK-<MODULE>-<nnn>`"):
            self.assertIn(heading, text)
        for old_header in ("| Constraint ID / 上级基线与决定状态 |", "| Surface ID |",
                           "| 依赖/参与方 |", "| 数据/状态 |", "| Rule ID |",
                           "| Interface |", "| 场景 |", "| 指标 |",
                           "| Function/Rule/Constraint |", "| ID | 问题 |"):
            self.assertNotIn(old_header, text)
        for namespace in ("F-<MODULE>-<nnn-or-name>", "IF-<MODULE>-<nnn>",
                          "VRC-<MODULE>-<nnn>", "RISK-<MODULE>-<nnn>",
                          "CON-<MODULE>-<nnn>"):
            self.assertIn(namespace, text)
        self.assertIn("§3 已登记且需要本模块常驻承载的操作面", text)
        demo_readme = (ROOT / "demo/llmtier-module-design/README.md").read_text()
        self.assertIn("仅示范实际模块设计的表达方法", demo_readme)
        self.assertIn("不得照抄本样板的旧字段", demo_readme)


if __name__ == "__main__":
    unittest.main()
