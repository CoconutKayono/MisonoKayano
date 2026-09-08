# 核对工作资料

这里保存官方源码快照和文档结构检查工具，不是正式学习卡片。

- `sources/`：卡片引用的源码文件；具体提交以对应卡片为准。
- `check_cards.py`：当前 A01—A08、B01—B04 文档的本地链接、围栏、进度与实验副本检查。默认只读；`--export` 从 Markdown 正文重新导出配套 C#/Shader 文件，不改学习计划与进度。
- `organize_and_check.py`：第一批 A01—A04 的历史整理脚本，内含当时的进度文本。后续检查请使用 `check_cards.py`，不要重跑历史脚本覆盖新进度。

从百科全书根目录执行：

```powershell
python work/check_cards.py
```

数值测试另见 `实验/README.md`；上述结构检查不编译 Unity 代码，也不验证屏幕效果。
