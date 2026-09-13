# 02 Model / View / Projection 变换

## 它解决什么问题？

模型顶点最初只知道自己在模型坐标系中的位置。为了得到“它在世界哪里”“相机怎么看到它”“它怎样投影到屏幕”，需要连续进行三种变换：

- Model：模型变换；
- View：视图变换；
- Projection：投影变换。

## 三种变换

Model 矩阵负责把模型坐标变换到世界坐标：

$$
p_{world}=M_{model}p_{model}
$$

View 矩阵把世界坐标变换到相机坐标：

$$
p_{view}=M_{view}p_{world}
$$

Projection 矩阵把相机坐标变换到裁剪空间：

$$
p_{clip}=M_{projection}p_{view}
$$

## 合并写法

通常把三者合并为 MVP 变换：

$$
p_{clip}=M_{projection}M_{view}M_{model}p_{model}
$$

矩阵乘法的顺序不能随意交换。

## 一个容易混淆的点

MVP 通常把顶点送到 Clip Space，而不是直接送到 NDC。之后还要进行透视除法：

$$
(x_{ndc},y_{ndc},z_{ndc})=
\left(\frac{x_{clip}}{w_{clip}},\frac{y_{clip}}{w_{clip}},\frac{z_{clip}}{w_{clip}}\right)
$$

## 下一步

MVP 变换的输出是 [[Games101-渲染管线-03-Clip-Space]]。

## 相关笔记

- [[Games101-渲染管线-01-模型顶点]]
- [[Games101-渲染管线-03-Clip-Space]]
- [[坐标变换]]
