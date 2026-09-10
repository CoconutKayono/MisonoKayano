# 导入和配置 Plug-in

> 原文：[Import and configure plug-ins](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html)

如果有 Managed Plug-in 或 Native Plug-in，可以将其导入 Unity，再进行配置。Unity Editor 将 Plug-in 作为类似 Script 的 Asset 处理，并可以在 Inspector 窗口中配置它。

通过 Plug-in 配置，可以指定 Plug-in 运行的位置、支持的平台和平台配置，以及加载 Plug-in 的条件。

## 导入 Plug-in

导入 Plug-in 最简单的方式是将它拖入项目的 **Assets** 文件夹或其子文件夹。Unity 会识别特定的文件和文件夹类型，并可以根据 Plug-in 的目标平台应用默认设置。

> [!NOTE]
> Native Plug-in 被加载到内存后，会在整个 Unity Editor 会话中保持加载状态。要修改已加载的 Native Plug-in Code，必须重启 Unity；否则仍会使用 Plug-in 的旧版本。此问题只影响在 Editor 中运行的 Native Plug-in，包括在 Native Plug-in 架构与当前 Editor 匹配时的 Play mode。

Unity 将以下扩展名的文件视为 Plug-in：

`.a`、`.aar`、`.bc`、`.c`、`.cc`、`.cpp`、`.dll`、`.def`、`.dylib`、`.h`、`.jar`、`.jslib`、`.jspre`、`.m`、`.mm`、`.prx`、`.rpl`、`.so`、`.sprx`、`.suprx`、`.swift`、`.winmd`、`.xcframework`、`.xex` 和 `.xib`。

以下扩展名的文件夹会被视为 bundled Plug-in：`.androidlib`、`.bundle`、`.framework` 和 `.plugin`。Unity 不会在这些文件夹中继续查找其他 Plug-in 文件，文件夹中的全部内容会被视为一个 Plug-in。

## Plug-in 默认设置

如果 Plug-in 在 Assets 文件夹中的路径符合平台专用模式，Unity 会自动应用平台专用默认设置；如果不符合任何模式，则应用 Editor 平台默认设置。

## 更改 Plug-in 设置

Plug-in 分为 Managed 和 Native 两类，不同类型对应的设置不同。要在 Inspector 中查看或更改设置，请在 Project 窗口中选择 Plug-in 文件。

如果 Plug-in 是 Roslyn Source Code Generator 或 Analyzer，必须在 Plug-in 设置中将 `RoslynAnalyzer` 分配为 Asset Label。

### 通用 Plug-in 设置

**Select platform for plugin** 和 **Platform settings** 指定 Unity 在哪些构建中包含 Plug-in。对每个选定平台，还可以配置 CPU 架构和依赖项等平台专用设置。Unity 只显示适用于目标平台以及对应 Plug-in 类型的设置。

**Define Constraints** 指定 Unity 加载 Plug-in 并建立引用的条件。这些条件是必须满足的符号，可以要求符号已定义或未定义。它们的行为类似 C# 中的 `#if` Preprocessor Directive，但作用级别是 Plug-in 或 Assembly，而不是 Script。可以使用 Unity 内置的 Scripting Symbol，也可以定义自定义 Symbol。

例如，以下两个约束可以限制 Unity 仅在非 IL2CPP Runtime 且 Unity 6000.6 或更高版本中加载和引用 Plug-in：

- `ENABLE_IL2CPP` 未定义。
- `UNITY_6000_6_OR_NEWER` 已定义。

### Managed Plug-in 设置

**Auto Reference** 控制项目中的 Assembly Definition 是否引用 Plug-in 文件。启用后，所有预定义 Assembly 和 Assembly Definition 都会自动引用该 Plug-in，默认启用。

禁用 Auto Reference 可以限制 Plug-in 的引用范围。此时必须显式声明所有引用；例如，可以避免 Script 错误使用 Plug-in、在迭代 Plug-in 时只重新编译依赖的 Assembly，或避免 Asset Store Package 中的 Plug-in 与项目代码冲突。禁用后，引用 Plug-in 的代码必须位于使用 Assembly Definition 创建的 Assembly 中，并在定义文件中显式添加 Plug-in 引用。Auto Reference 不影响文件是否包含在构建中；构建包含关系由 Platform settings 控制。

**Validate References** 可以检查 Plug-in 的引用是否存在，以及 Strong Named Reference 是否能够加载。启用后，如果 Plug-in 引用的程序集（例如 `Newtonsoft.Json.dll`）缺失，Unity 会显示错误。如果不想验证 Strong Named Reference，但仍想验证引用存在，可以在 Plug-in Inspector 中启用 Validate References，并在 **Project Settings > Player > Other Settings** 中禁用 **Assembly Version Validation**。

### Plug-in load settings - Load on startup

启用 **Load on startup** 后，可以在图形初始化、Script、Asset 和 Scene 等执行之前开始执行与图形无关的 Unmanaged Code。要启用它，需要在 Plug-in 中实现 `UnityPluginLoad`，再在 Editor 的 Plug-in 设置中选择 **Plugin load settings > Load on startup**。

## 其他资源

- [[02-Managed Plug-in]]
- [[04-Native Plug-in/00-Native Plug-in]]
- [[04-为桌面平台构建Plug-in]]
- [[04-Native Plug-in/00-Native Plug-in]]

---

## 文档导航

- 上一页：[[00-集成第三方代码库]]
- 目录：[[00-集成第三方代码库]]
- 下一页：[[02-Managed Plug-in]]
