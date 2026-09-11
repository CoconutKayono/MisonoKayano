# 08｜URP 空间可视化实验

## 准备一个能直接观察的材质

配套文件：[SpaceAwareness.shader](示例/SpaceAwareness.shader)。

适用范围：Unity 6 的 URP 项目，普通静态网格、不透明 Unlit 教学材质。此示例不提供完整光照、阴影、蒙皮特性覆盖或 XR 支持。已核对 API 用法与公式，但本工作区未完成 Unity 编辑器编译和实际渲染验证。

1. 将文件复制到 URP 项目的 Assets 中。
2. 新建材质，在 Shader 下拉菜单选择 **FAQ/SpaceAwareness**。
3. 创建 Cube 和 Sphere，把材质赋给它们。
4. 保持初始缩放 $(1,1,1)$，给相机安排能同时看到两者的位置。
5. 在材质 Mode 下拉中切换观察模式。

该文件只是普通文本附件，在当前笔记目录不会自动参与 Unity 导入。

## 六种模式

| Mode | 输入 | 画面含义 |
| --- | --- | --- |
| ObjectStripes | positionOS.y | 贴着模型的周期条纹 |
| WorldStripes | positionWS.y | 固定世界高度的周期条纹 |
| WorldNormal | 正确世界法线 | RGB 分别显示法线 x、y、z |
| WrongNormal | 普通矩阵变换法线 | 展示非均匀缩放时的方向错误 |
| ScreenStripes | screenUV.y | 固定在画面中的条纹 |
| NormalError | 两种单位法线的差 | 黑色近似一致，红色越亮差异越大 |

法线颜色映射为 $0.5n+0.5$，把 $[-1,1]$ 映射到 $[0,1]$。朝 +X 偏红、朝 +Y 偏绿、朝 +Z 偏蓝，其他通道在 0.5 附近；这不是实际照明颜色。

Frequency 在 OS/WS 模式代表每坐标单位的周期数，在 Screen 模式代表视口高度方向的周期数。建议空间条纹设 3，屏幕条纹设 12。

## 实验一：先平移，再旋转，再缩放

使用 Cube：

| 操作 | ObjectStripes 预期 | WorldStripes 预期 |
| --- | --- | --- |
| 沿世界 y 平移 0.17 | 图案留在模型同一处 | 模型穿过固定条纹，表面图案变化 |
| 绕 z 旋转 45° | 条纹跟着模型倾斜 | 条纹继续按世界水平面切模型 |
| y 缩放改成 2 | 世界里的条纹间距被拉大 | 世界里的条纹间距保持不变 |

不要恰好按条纹周期的整数倍平移，否则周期图案可能看似没变。也不要只沿世界 x 平移来测试 y 条纹，它的输入 y 本来就没变。

ScreenStripes 模式下移动相机或物体，条纹相位相对画面保持固定；但条纹只出现在有这个材质的物体覆盖的像素里，并不是全屏后处理。

## 实验二：为什么要用 Sphere 测法线

使用 Sphere，把缩放设为 $(2,1,0.5)$，轮流看 WorldNormal、WrongNormal、NormalError。

预期：斜向表面的两种法线明显不同，Error 显示红色。恢复统一缩放 $(2,2,2)$，差异应接近黑色。

默认 Cube 的法线主要沿坐标轴，非均匀缩放后归一化常会掩盖问题；Sphere 含有大量斜向法线，能更有效暴露错误。

## 核心数据路线

~~~hlsl
OUT.positionCS = TransformObjectToHClip(IN.positionOS.xyz);
OUT.positionOS = IN.positionOS.xyz;
OUT.positionWS = TransformObjectToWorld(IN.positionOS.xyz);
OUT.normalWS = TransformObjectToWorldNormal(IN.normalOS);
OUT.wrongNormalWS = mul((float3x3)GetObjectToWorldMatrix(), IN.normalOS);
~~~

positionCS 负责把顶点送入光栅化流程；其他数据通过 TEXCOORD 通道插值到片元着色器，供着色计算使用。把 TEXCOORD 命名成 normalWS 不会自动执行空间变换，真正转换发生在赋值表达式里。

WrongNormal 模式是有意的错误对照，不要复制到实际光照 Shader。

## 用纸笔核对模型矩阵

在 Unity 中找一个无父物体的对象，设置位置 $(3,1,0)$，绕 z 旋转 90°，缩放 $(2,1,1)$。可检查其 localToWorldMatrix 的前三列与最后一列：

- 原点：$(3,1,0)$；
- 局部 x 一步：约 $(0,2,0)$；
- 局部 y 一步：约 $(-1,0,0)$；
- 局部 z 一步：$(0,0,1)$。

这是第 01 篇的例子扩展到三维。注意读取的是列，不是行；微小的非零小数是浮点误差。

## 如果没有出现预期

材质粉色：先看 Console 的编译错误，并确认项目确实启用了 URP。画面没有阴影：本例是 Unlit。条纹太密：降低 Frequency。法线误差不明显：使用非均匀缩放的 Sphere，别只看轴向面。

空间变换函数来自 [URP 坐标转换方法](https://docs.unity3d.com/6000.0/Documentation/Manual/urp/use-built-in-shader-methods-transformations.html)；屏幕 UV 的阶段语义还可查看 [Unity ShaderVariablesFunctions.hlsl](https://github.com/Unity-Technologies/Graphics/blob/master/Packages/com.unity.render-pipelines.universal/ShaderLibrary/ShaderVariablesFunctions.hlsl)。

导航：[[00-学习路线|目录]] · 上一篇：[[07-把空间选择变成视觉效果]] · 下一篇：[[09-排错速查与参考资料]]
