# Burst AOT 设置参考

> 原文：[Burst AOT Settings reference](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/building-aot-settings.html)

要控制 Burst 的 AOT 编译，请使用 Project Settings 窗口中的 Burst AOT Settings 部分（**Edit > Project Settings > Burst AOT Settings**）。这些设置只控制 Player 构建中的 Burst 编译。要配置 Unity Editor 中的 Burst 编译，请参阅 [Burst 菜单参考](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/editor-burst-menu.html)。

![Burst AOT Settings](burst_aot_settings.png)

| 设置 | 功能 |
| --- | --- |
| **Target Platform** | 显示当前平台。要更改平台，请转到 **File > Build Profiles**。你可以为每个平台定义不同的 Burst AOT 设置。 |
| **Enable Burst Compilation** | 启用此设置可开启 Burst 编译。禁用此设置可停用所选平台的 Burst 编译。 |
| **Enable Optimizations** | 启用此设置可激活 Burst 优化。 |
| **Force Debug Information** | 启用此设置可让 Burst 生成调试信息。即使项目是发布构建，这也会向项目添加调试符号，使你在调试器中加载项目时能够查看文件和行信息。 |
| **Target 32Bit CPU Architectures**<br>（仅在支持该架构时显示） | 选择要用于 32 位构建的 CPU 架构。默认选择 SSE2 和 SSE4。 |
| **Target 64Bit CPU Architectures**<br>（仅在支持该架构时显示） | 选择要用于 64 位构建的 CPU 架构。默认选择 SSE2 和 SSE4。 |
| **Target Arm 64Bit CPU Architectures**<br>（仅在支持该架构时显示） | 选择要用于 Arm 64 位构建的 CPU 架构。默认选择 ARMV8A。 |
| **Optimize For** | 选择编译 Burst 代码时使用的优化设置：<br>**Performance**：优化 Job，使其尽可能快速运行。<br>**Size**：优化代码生成，使其尽可能小。<br>**Fast Compilation**：以尽可能快的速度编译代码，并进行最少的优化。Burst 不执行向量化、内联或循环优化。<br>**Balanced（默认）**：优化出运行速度快的代码，同时尽量缩短编译时间。<br><br>注意：任何 `OptimizeFor` 设置都是所有 Burst Job 或函数指针的全局默认优化设置。如果程序集级别的 `BurstCompile`，或特定 Burst Job/函数指针设置了 `OptimizeFor`，则该设置会覆盖这些 Job 的全局优化设置。有关更多信息，请参阅 `OptimizeFor`。 |
| **Floating Point Mode** | 选择 Burst 编译代码的默认浮点模式。可以通过 `BurstCompile` 特性的 `FloatMode` 字段或 Job 覆盖此设置。有关更多信息，请参阅 `FloatMode`。 |
| **Disabled Warnings** | 指定以分号分隔的 Burst 警告编号列表，以禁用 Player 构建中的这些警告。Unity 在所有平台之间共享此设置。在测试应用时，如果希望忽略特定编译警告，此设置会很有用。 |
| **Stack Protector**<br>（仅在支持该架构时显示） | 指定栈保护级别。启用栈保护的函数会在栈帧中增加一个额外值；函数返回时会验证该值，以帮助检测潜在的缓冲区溢出并防止被利用。选项如下：<br>**Off**：不生成栈保护器。<br>**Basic**：对应 clang 选项 `--fstack-protector` 的栈保护级别。<br>**Strong**：对应 clang 选项 `--fstack-protector-strong` 的栈保护级别。<br>**All**：对应 clang 选项 `--fstack-protector-all` 的栈保护级别。 |
| **Stack Protector Buffer Size**<br>（仅在支持该架构时显示） | 指定不同 Stack Protector 选项用于判断函数是否易受攻击，并指导栈上数组和结构体布局的阈值。 |
| **CPU Architecture** | 此设置仅支持 Windows、macOS、Linux 和 Android。Unity 会构建支持所选 CPU 架构的 Player。Burst 会在模块中生成特殊分派代码，使生成的代码在运行时检测目标平台所使用的 CPU，并选择相应的 CPU 架构。 |

## 相关资源

- [项目构建](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/building-projects.html)
- [Editor 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/editor-reference-overview.html)
- [Project Settings](https://docs.unity3d.com/6000.7/Documentation/Manual/comp-ManagerGroup.html)

---

## 文档导航

- 上一页：[[09-平台构建支持参考]]
- 目录：[[00-Burst编译]]
- 下一页：[[00-Burst优化]]
