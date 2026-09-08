# Catlike Coding — Basics 系列中文翻译

这是对 [Catlike Coding](https://catlikecoding.com/) 的 Unity **Basics** 系列教程的简体中文翻译，作者 [Jasper Flick](https://catlikecoding.com/)。

Basics 系列是入门 Unity 底层概念的第一站，从最基础的游戏对象与脚本讲起，一路深入到计算着色器与 Job 系统。原文以"从零搭建、逐步重构、一路测量性能"的方式推进，是理解 Unity 渲染与 CPU 并行化思想的绝佳起点。

## 教程目录

| # | 中文标题 | 原文标题 | 主题 |
|---|---|---|---|
| 1 | [游戏对象与脚本](01_游戏对象与脚本.md) | Game Objects and Scripts | 游戏对象、组件、脚本生命周期 |
| 2 | [构建图表](02_构建图表.md) | Building a Graph | 立方体、数学函数、URP/BRP 着色器 |
| 3 | [数学曲面](03_数学曲面.md) | Mathematical Surfaces | 曲面参数化、网格构造 |
| 4 | [测量性能](04_测量性能.md) | Measuring Performance | Profiler、帧率、内存 |
| 5 | [计算着色器](05_计算着色器.md) | Compute Shaders | GPU 程序化绘制、计算缓冲区 |
| 6 | [Job 系统](06_Job系统.md) | Jobs | 原生数组、Burst 编译、多核并行 |
| 7 | [有机多样性](07_有机多样性.md) | Organic Variety | 分形着色、下垂模拟、随机多样性 |

## 阅读建议

- 教程基于 **Unity 2020.3.6f1**，代码为**内置渲染管线（BRP）+ URP 着色器图**双版本并存。建议跟随原项目仓库实操，边改边看效果。
- 每篇代码块保留**原文（diff 格式）**，仅翻译讲解文字，方便对照原文核对。
- 图片为**热链接**（直接引用 Catlike Coding 官网），阅读时需要联网。如需离线保存，请运行本目录下的图片下载脚本。

## 关于图片

教程中的图片没有打包进仓库，而是通过外链引用。你可以用下面的脚本把全部图片下载到本地（需要 Python）：

```bash
python 下载图片.py
```

脚本会抓取各篇 markdown 里引用的图片 URL，并按教程分目录保存到 `images/` 下。

## 许可

本系列翻译仅供学习使用。原教程版权归 Jasper Flick 所有，遵循 Catlike Coding 的[教程许可协议](https://catlikecoding.com/unity/tutorials/license/)。各篇文末附有原文链接、项目仓库与 PDF 版本地址。
