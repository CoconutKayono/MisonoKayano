from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
cards = root / "01-数学与数据"
navigation = root / "00-学习导航"
experiments = root / "实验"

# 从正文提取，避免另存的实验副本与独立卡片不一致。
exports = [
    ("A01-向量点积叉积与归一化.md", "hlsl", "A01VectorLab.shader", 0),
    ("A02-坐标基矩阵与空间变换.md", "csharp", "A02SpaceLab.cs", 0),
    ("A03-齐次坐标投影与裁剪空间.md", "csharp", "A03ProjectionLab.cs", 0),
    ("A04-法线逆转置切线与TBN.md", "csharp", "A04NormalLab.cs", 0),
]
for filename, language, output, index in exports:
    content = (cards / filename).read_text(encoding="utf-8")
    blocks = re.findall(r"```" + language + r"\n(.*?)\n```", content, re.S)
    assert blocks, filename
    (experiments / output).write_text(blocks[index] + "\n", encoding="utf-8")

plan_path = navigation / "学习计划.md"
plan = plan_path.read_text(encoding="utf-8")
start = plan.index("## 13.")
end = plan.index("## 14.", start)
plan = plan[:start] + """## 13. 当前实施位置与下一组

本计划与卡片统一存放在 `E:\\Claude Skills\\学习仓库\\图形学百科全书`。

已收录完整 [K00 总览卡](K00-Draw-Call完整执行链路.md)，并生成第一组 A01—A04：向量、空间变换、投影与法线/TBN。四张均为自包含 Markdown，必要术语、公式、数值例子、示例和答案均保留在正文；可复制实验另放在 `实验/`。

已运行 12 项 Python 数学校验并通过。Unity 示例尚未在 Editor 编译或实机验证，读者学习状态不由文件生成自动推定。完整状态见 [学习进度](学习进度.md)。

推荐先完成 **A01 → A02 → A03 → A04 → 基础实验**。下一组按 **A05 线性颜色/sRGB/HDR → A06 Mesh 与索引 → A07 GPU 资源 → A08 纹理格式** 推进，再完成 A 阶段的数据可视化材质检查点。

新卡片使用稳定编号，如 `A01-向量点积叉积与归一化.md`。尚未生成的主题只登记在计划与进度表，不创建只有标题的占位卡片。根目录已有 Draw Call 稿件原样保留，导航使用 `00-学习导航/K00-Draw-Call完整执行链路.md`。

""" + plan[end:]
plan_path.write_text(plan, encoding="utf-8")

entries = re.findall(r"^\| ([A-F]\d{2}) \| ([^|]+) \|", plan, re.M)
assert len(entries) == 48 and len(set(x[0] for x in entries)) == 48
links = {filename[:3]: filename for filename, *_ in exports}
progress = """# 学习进度与验证记录

记录日期：2026-09-06。主线计划 48 张，已生成 4 张；完整 K00 导览已收录。下一个生成主题为 A05。选修 8 个方向均尚未生成。

## 状态解释

- **已生成**：独立 Markdown 已完成，含必要概念、例子、实验与来源。
- **数值已校验**：配套脚本对卡片中的数学关系进行了验证。
- **Unity 未实测**：没有把静态核对误写成 Editor 编译、GPU 运行或性能测量通过。
- **学习未确认**：没有用户实验或理解反馈，不能推定读者已掌握。

## 卡片状态

| 编号 | 主题 | 文档状态 | 数值/实验状态 | 个人学习状态 |
| --- | --- | --- | --- | --- |
| [K00](K00-Draw-Call完整执行链路.md) | Draw Call 完整执行链路 | 已收录完整版 | 源码核对；Unity 未实测 | 未确认 |
"""
for code, title in entries:
    if code in links:
        progress += f"| [{code}](../01-数学与数据/{links[code]}) | {title.strip()} | 已生成 | 数值已校验；Unity 未实测 | 未确认 |\n"
    else:
        progress += f"| {code} | {title.strip()} | 待生成 | 未开展 | 未开始 |\n"
progress += """
## 本轮验证结果

已执行 `python 实验/验证基础数学.py`：**12 项测试全部通过**。其中一般剪切/反射法线约束测试包含固定随机种子的 50 组输入。

覆盖：向量长度和零输入、点积阈值、叉积与顺序、TRS 和点/位移区别、矩阵逆变换、非均匀缩放后的方向、透视近远端点、正交对照、像素偏移、法线逆转置、TBN 与行列式手性。

数值验证运行在 Python 的浮点模型上，不能替代 GPU 精度验证。Unity 示例已经对照 API/源码并核对文本结构，没有在 Editor 编译、播放或抓帧。

数学测试：[验证基础数学.py](../实验/验证基础数学.py)。操作说明：[实验 README](../实验/README.md)。

## 后续更新方式

生成新卡后更新文档状态；运行对应实验后记录具体输入和证据；用户能独立预测并解释反例后，才能将个人学习状态更新为“已验证”或“已迁移”。进度不依赖后台定时生成，本文件是当前实施记录。
"""
(navigation / "学习进度.md").write_text(progress, encoding="utf-8")

# 检查新整理的文档：代码围栏闭合，所有相对文件链接存在。
targets = [root / "README.md", *navigation.glob("*.md"), *cards.glob("*.md"), experiments / "README.md"]
checked_links = 0
for path in targets:
    text = path.read_text(encoding="utf-8")
    assert len(re.findall(r"^```", text, re.M)) % 2 == 0, f"Unclosed fence: {path}"
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in link or link.startswith("#"):
            continue
        target = link.split("#")[0]
        assert (path.parent / target).exists(), f"Missing link: {path}: {link}"
        checked_links += 1

for _, _, output, _ in exports:
    content = (experiments / output).read_text(encoding="utf-8")
    assert content.count("{") == content.count("}"), output

print(f"Mainline entries: {len(entries)}; generated foundations: {len(exports)}")
print(f"Markdown files checked: {len(targets)}; local links checked: {checked_links}")
print("Experiment copies extracted from cards; code fences and brace counts valid.")
