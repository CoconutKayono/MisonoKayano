# SDF 零基础图文教程

先打开 **[sdf-from-zero.md](sdf-from-zero.md)**。正文按直觉、二维绘图、形状组合、三维渲染逐步展开，配有 6 张图片和 5 道练习。

第一遍建议先读第 1～4 节，手算圆的距离；再读第 5～8 节，理解形状怎么画；最后读三维渲染。公式和代码可以分两遍阅读。

## 文件内容

| 文件 | 用途 |
|---|---|
| `sdf-from-zero.md` | 完整中文教程 |
| `sdf-images/` | 1 张 imagegen 概念插画和 5 张数学教学图 |
| `sdf_demo.py` | 完整的 Python 3 示例，只使用标准库 |
| `sdf-render.png` | 示例实际生成的球体渲染结果 |
| `imagegen-prompt.md` | 插画完整提示词及生成方式记录 |

## 运行示例

在 `sdf_demo.py` 所在文件夹打开终端，运行：

```bash
python sdf_demo.py
```

程序会在自身所在文件夹生成或覆盖 `sdf-render.png`。没有安装 Python 也不影响阅读正文和查看已经生成的图片。

## 保持图文完整

请先完整解压学习包，再打开教程。移动文件时，保留 Markdown 与 `sdf-images` 文件夹的相对位置。使用支持 LaTeX 数学公式的 Markdown 阅读器，可以获得更好的公式显示效果。
