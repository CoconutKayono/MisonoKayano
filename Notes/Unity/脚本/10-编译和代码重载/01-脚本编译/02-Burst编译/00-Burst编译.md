# Burst 编译

> 原文：[Burst compilation](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html)

将 C# 代码中兼容 Burst 的部分编译为高度优化的原生 CPU 代码。

| 页面 | 说明 |
| --- | --- |
| [[01-Burst简介]] | 了解 Burst 编译器的基础知识，以及它在 Unity 编译生态中的作用。 |
| [[02-Burst入门]] | 通过创建第一个简单的 Burst 编译示例开始使用 Burst。 |
| [[06-CSharp语言支持/00-CSharp语言支持]] | 了解 Burst 可以编译的高性能 C# 子集中的语言元素。 |
| [[03-配置Burst编译/00-配置Burst编译]] | 定义 Burst 在不同上下文中编译什么以及如何编译，标记代码进行 Burst 编译，并配置编译过程的各个方面。 |
| [[07-Burst Intrinsics/00-Burst Intrinsics]] | 如果正在编写 single instruction, multiple data（SIMD）汇编代码，使用低级 intrinsics 从 Burst 获得额外性能。 |
| [[13-Burst Editor窗口参考]] | 使用 Unity Editor 中的 Burst 菜单和 Burst Inspector 窗口配置 Burst 选项，并检查项目中可由 Burst 编译的 Job。 |
| [[09-平台构建支持参考]] | 使用适当的平台专用 toolchain，在不同平台上构建由 Burst 编译的项目代码。 |
| [[08-Burst AOT设置参考]] | 为目标平台和架构配置 Burst 的 Ahead-of-Time（AOT）编译设置。 |
| [[05-Burst优化/00-Burst优化]] | 调试和分析 Burst 编译的代码以查找错误或瓶颈，并配置一系列选项来优化性能。 |
| [[15-Burst Modding支持]] | 将 Burst 编译的代码作为 mod 中的附加库包含进来。 |

## 其他资源

- 📺 **视频**：[Getting started with Burst - Unite Copenhagen 2019](https://www.youtube.com/watch?v=Tzn-nX9hK1o)
- 📺 **视频**：[Supercharging mobile performance with ARM Neon and Unity Burst Compiler](https://www.youtube.com/watch?v=7iEUvlUyr4k)
- 📺 **视频**：[Using Burst Compiler to optimize for Android - Unite Now 2020](https://www.youtube.com/watch?v=WnJV6J-taIM)
- 📺 **视频**：[Intrinsics: Low-level engine development with Burst - Unite Copenhagen 2019](https://www.youtube.com/watch?v=BpwvXkoFcp8)
- 📺 **视频**：[Behind the Burst compiler: Converting .NET IL to highly optimized native code - DotNext 2018](https://www.youtube.com/watch?v=LKpyaVrby04)
- 📺 **视频**：[Deep dive into the Burst compiler - Unite LA 2018](https://www.youtube.com/watch?v=QkM6zEGFhDY)
- 📺 **视频**：[C# to machine code: GDC 2018](https://www.youtube.com/watch?v=NF6kcNS6U80)
- 📺 **视频**：[Using the native debugger for Burst compiled code](https://www.youtube.com/watch?v=nou6AIHKJz0)
- 📚 **文档**：[Raising your game with Burst 1.7](https://blog.unity.com/technology/raising-your-game-with-burst-17)
- 📚 **文档**：[Enhancing mobile performance with the Burst compiler](https://blog.unity.com/technology/enhancing-mobile-performance-with-the-burst-compiler)
- 📚 **文档**：[Enhanced aliasing with Burst](https://blogs.unity3d.com/2020/09/07/enhanced-aliasing-with-burst/)
- 📚 **文档**：[In parameters in Burst](https://blogs.unity3d.com/2020/11/25/in-parameters-in-burst/)

---

## 文档导航

- 上一页：[[../01-脚本后端/00-脚本后端]]
- 目录：[[00-Burst编译]]
- 下一页：[[01-Burst简介]]
