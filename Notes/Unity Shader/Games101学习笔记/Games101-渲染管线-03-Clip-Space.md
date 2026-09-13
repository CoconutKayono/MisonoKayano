# 03 Clip Space：裁剪空间

## 它是什么？

经过 Projection 矩阵后，顶点进入 Clip Space。它仍然是齐次坐标：

$$
p_{clip}=(x_{clip},y_{clip},z_{clip},w_{clip})
$$

其中 $w_{clip}$ 会在透视除法中使用。

## 为什么需要 Clip Space？

Clip Space 适合进行视锥体裁剪。在常见约定下，可见范围可以写成：

$$
-w_{clip}\le x_{clip}\le w_{clip}
$$

$$
-w_{clip}\le y_{clip}\le w_{clip}
$$

$$
-w_{clip}\le z_{clip}\le w_{clip}
$$

具体的 $z$ 范围会随图形 API 的约定变化。

如果三角形完全在视锥体外，就可以丢弃；如果只有部分在视锥体内，就需要把它切割成位于可见范围内的新三角形。

## Clip Space 和 NDC 的区别

| 空间 | 坐标形式 | 主要用途 |
|---|---|---|
| Clip Space | $(x_{clip},y_{clip},z_{clip},w_{clip})$ | 裁剪 |
| NDC Space | $(x_{ndc},y_{ndc},z_{ndc})$ | 归一化和屏幕映射 |

Clip Space 经过 [[Games101-渲染管线-04-透视除法]] 后，才变成 [[Games101-渲染管线-05-NDC-Space]]。

## 相关笔记

- [[Games101-渲染管线-02-MVP变换]]
- [[Games101-渲染管线-04-透视除法]]
- [[Games101-渲染管线-05-NDC-Space]]
