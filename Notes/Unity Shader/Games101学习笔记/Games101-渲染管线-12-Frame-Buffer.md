# 12 Frame Buffer：保存最终显示的颜色

## 它是什么？

Frame Buffer，也叫颜色缓冲区，可以理解为一张和屏幕采样网格对应的颜色图：

```text
frameBuffer[x,y] = 屏幕位置 (x,y) 当前最终要显示的颜色
```

它通常包含每个像素的 RGB 颜色，有时还包含 Alpha 等信息。

## 它是如何得到的？

对每个 Fragment，渲染过程大致是：

```text
Fragment 到达
  ↓
深度测试
  ↓ 通过
着色得到颜色
  ↓
写入 Frame Buffer
```

如果深度测试失败，这个 Fragment 就不会覆盖该位置原来的颜色。

## Frame Buffer 和 Depth Buffer 的区别

| 缓冲区 | 保存什么 | 是否直接作为画面显示 |
|---|---|---|
| Frame Buffer | 最终颜色 | 是 |
| Depth Buffer | 每个位置的深度 | 通常不是，主要用于遮挡判断 |

例如，一个位置经过深度测试后可能保存：

```text
frameBuffer[100,200] = RGB(255, 0, 0)
depthBuffer[100,200] = 4
```

表示位置 $(100,200)$ 最终显示红色，并且当前留下的表面深度是 $4$。

## 一张图是怎样产生的？

屏幕上的每个位置都重复进行类似过程：

$$
frameBuffer(x,y)=color\left(\operatorname*{arg\,min}_i z_i\right)
$$

含义是：在所有覆盖该位置的候选 Fragment 中，找到深度最小的那个，把它的颜色放进 Frame Buffer。

当所有三角形都处理完后，Frame Buffer 中的颜色集合就构成了最终图像。

## 整条流程到这里闭环

```text
模型顶点
  → MVP 变换
  → Clip Space
  → 透视除法
  → NDC
  → 视口变换
  → 屏幕坐标
  → 光栅化
  → Fragment
  → 深度测试与着色
  → Frame Buffer
```

## 相关笔记

- [[Games101-渲染管线-10-深度测试]]
- [[Games101-渲染管线-11-着色]]
- [[Games101 第七节：深度缓冲（Z-Buffer）注释]]
