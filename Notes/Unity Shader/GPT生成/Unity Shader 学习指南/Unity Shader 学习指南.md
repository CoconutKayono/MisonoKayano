# Unity Shader 学习指南

以 **URP 为实践主线**，按「基础 → 编写 → 光照 → 效果 → 优化」组织。

[打开交互式学习思维导图](<Unity Shader 学习思维导图.html>)（用浏览器打开后，点击分支标题可展开或折叠。）

## 如何使用

1. 先学习图形学基础与 Unity 渲染管线，理解顶点如何变成像素。
2. 用 Shader Graph 理解效果，再用 ShaderLab + HLSL 重写相同效果。
3. 逐步加入纹理、光照与阴影，再组合成完整材质效果。
4. 对照阶段验收检查掌握程度，在目标设备上验证性能。

注意区分教程所属管线：**Surface Shader 仅适用于 Built-in，URP/HDRP 不支持。** 教程与代码示例应匹配项目的 Unity 和渲染管线版本。

## 01 · 图形学与数学基础

- 向量与矩阵
  - 点积：夹角、光照强度
  - 叉积：法线、方向与朝向
  - 矩阵：平移、旋转、缩放
- 坐标空间
  - 模型 → 世界 → 观察 → 裁剪
  - 透视除法 → NDC → 屏幕
  - 切线空间：法线贴图的基础
- 渲染流程
  - 顶点处理 → 光栅化 → 片元处理
  - 深度测试、混合与帧缓冲
- 练习：用颜色显示 UV 与法线

## 02 · Unity 与渲染管线

- 对象关系
  - Mesh：顶点、法线、UV、切线
  - Shader：着色程序与渲染状态
  - Material：Shader 与参数
  - Renderer：提交物体进行渲染
- 选择学习环境
  - URP：本图的实践主线
  - HDRP：高保真材质与高级渲染
  - Built-in：旧项目与传统教程
- 版本边界
  - 教程需匹配 Unity 与管线版本
  - Surface Shader 仅用于 Built-in

## 03 · Shader Graph 入门

- 图结构
  - Blackboard：暴露材质属性
  - 节点与连线：数据的计算过程
  - Master Stack：顶点与片元输出
- 常用节点
  - UV、Sample Texture 2D、Time
  - Add、Multiply、Lerp、Smoothstep
  - Normal Vector、View Direction
- 模块复用
  - Sub Graph：封装公共逻辑
  - Custom Function：接入 HLSL
- 练习：UV 流动 → 溶解 → 边缘光

## 04 · ShaderLab 与 HLSL

- ShaderLab：定义结构与状态
  - Properties → SubShader → Pass
  - Tags、Cull、ZTest、ZWrite、Blend
- HLSL：实现计算
  - float / half、向量、矩阵、结构体
  - 语义：POSITION、TEXCOORD、SV_Position、SV_Target
  - 顶点函数、插值数据、片元函数
  - 纹理与采样器、常量缓冲区
- URP 实践
  - Core.hlsl：空间变换与基础工具
  - Lighting.hlsl：光照相关工具
  - 理解 UnityPerMaterial 与 SRP Batcher 兼容要求
- 练习：纯色 → 贴图 → UV 动画

## 05 · 材质、光照与阴影

- 纹理与颜色
  - UV、Tiling / Offset、Wrap / Filter
  - Mipmap、纹理压缩、sRGB 与线性空间
  - 法线贴图与 TBN 变换
- 光照模型
  - Lambert：漫反射
  - Blinn–Phong：理解高光
  - PBR：BRDF、金属度、粗糙度
  - 直接光、环境光与反射探针
- 阴影链路
  - 接收阴影：坐标与衰减
  - 投射阴影：ShadowCaster Pass
  - 深度与法线 Pass 按效果需求实现
- 练习：法线贴图材质与可调高光

## 06 · 常见效果与综合实践

- 风格化
  - 卡通光照：Ramp 与分段明暗
  - 描边：反向外壳或屏幕空间边缘
- 动态材质
  - 溶解：噪声、阈值、clip
  - 水面：UV 扰动、法线、Fresnel
  - 植被：顶点位移、风场、遮罩
- 透明与屏幕空间
  - Alpha Clip 与 Alpha Blend
  - 渲染顺序、深度写入、透明排序
  - 深度纹理、场景颜色、后处理
- 练习：完成一个可调参的效果材质

## 07 · 调试与性能

- 定位问题
  - 编译日志：语法、宏与管线不匹配
  - 输出中间值：UV、法线、深度
  - Frame Debugger：Pass 与绘制顺序
  - RenderDoc：GPU 帧与资源检查
- 分析成本
  - GPU Profiler：先确定瓶颈
  - Overdraw、纹理采样、带宽、计算量
  - Shader 关键字与变体数量
- 针对性优化
  - 减少无效 Pass 与透明叠加
  - 按精度需求使用 half / float
  - SRP Batcher 与 GPU Instancing
  - 在目标设备上验证视觉与耗时

## 08 · 进阶方向与学习验收

- 按项目需求深入
  - Compute Shader：并行计算与缓冲区
  - SDF、Ray Marching：程序化几何
  - Renderer Feature / Render Pass
  - Render Graph 与资源依赖
  - 阅读 URP / HDRP Shader 源码
- 阶段验收
  - 入门：解释顶点如何变成像素
  - 基础：独立写出纹理与 UV 动画
  - 进阶：组合光照、阴影和透明效果
  - 工程：定位问题并验证性能优化
- 作品闭环
  - 参考图 → 原理拆解 → 最小实现
  - 参数设计 → 性能验证 → 效果复盘

## 官方参考

- [Unity 6 渲染管线功能比较](https://docs.unity3d.com/cn/6000.0/Manual/render-pipelines-feature-comparison.html)
- [URP 自定义 Shader 编写](https://docs.unity.cn/6000.1/Documentation/Manual/urp/writing-custom-shaders-urp.html)

整理日期：2026-09-11。
