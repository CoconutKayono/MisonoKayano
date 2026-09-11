# Unity 官方文档迁移进度

> 最后更新：2026-09-10

这张表追踪 `Notes/Unity/脚本`、`Notes/Unity/游戏对象`、`Notes/Unity/Camera` 三棵文档树的逐页迁移进度。

> [!IMPORTANT]
> “已完成”只表示该 Markdown 已按当前流程逐页执行：直接抓取官方网络原文、迁移实际正文与图片、完成单文件校验。“已处理待复核”表示曾经按网络内容处理过，但尚未纳入当前严格逐页审计；“待执行”不代表正文正确。

## 汇总

| 文档树                       |  总数 | 已完成（逐页审计） | 已处理待复核 | 源站异常 | 待执行 |
| ------------------------- | --: | --------: | -----: | ---: | --: |
| [脚本](00-脚本.md)         | 279 |       279 |      0 |    0 |   0 |
| [游戏对象](00-游戏对象.md)   |  58 |        58 |      0 |    0 |   0 |
| [Camera](00-相机.md) |  85 |        85 |      0 |    0 |   0 |
| [渲染管线](00-渲染管线.md)   | 136 |       125 |      0 |    0 |  11 |
|                           |     |           |        |      |     |

## 明细

| # | 本地 Markdown | 原文链接 | 状态 | 审计备注 |
| ---: | --- | --- | --- | --- |
| 1 | [[00-脚本]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 2 | [[00-开始使用Unity编程]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-get-started.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 3 | [[01-Unity编程简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/intro-to-scripting.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 4 | [[02-创建脚本]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/creating-scripts.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 5 | [[03-命名脚本]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/naming-scripts.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 6 | [[04-检查脚本]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/inspecting-scripts.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 7 | [[00-环境与工具]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/environment-and-tools.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 8 | [[01-集成开发环境支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-ide-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 9 | [[00-Unity的.NET功能]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/overview-of-dot-net-in-unity.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 10 | [[01-.NET API兼容级别]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/dotnet-profile-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 11 | [[02-不兼容的.NET API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/dotnet-incompatible-api.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 12 | [[03-添加.NET Framework类库引用]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/dotnet-profile-assemblies.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 13 | [[04-CSharp编译器和语言版本参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/csharp-compiler.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 14 | [[00-Unity基础类型]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/fundamental-unity-types.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 15 | [[01-Object类]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Object.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 16 | [[02-MonoBehaviour类]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-MonoBehaviour.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 17 | [[03-ScriptableObject类]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-ScriptableObject.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 18 | [[04-Unity属性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-attributes.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 19 | [[05-从InstanceID迁移到EntityId]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/instanceid-to-entityid-migration.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 20 | [[00-管理更新和执行顺序]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managing-update-order.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 21 | [[01-脚本执行顺序]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-execution-order.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 22 | [[02-事件函数]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/event-functions.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 23 | [[03-事件函数执行顺序]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/execution-order.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 24 | [[04-自定义Player Loop]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/player-loop-customizing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文结构和 5 个代码块已核对、无图片 |
| 25 | [[05-使用自定义更新管理器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/events-per-frame-optimization.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、标题结构、4 个代码块和无图片已核对 |
| 26 | [[06-Inspector可配置的自定义事件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-events.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、标题结构、1 个代码块、2 张图片已核对 |
| 27 | [[00-管理时间和帧率]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managing-time-and-frame-rate.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文说明、主题表格和资源链接已核对 |
| 28 | [[01-每帧更新]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/time-per-frame-updates.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、2 个代码块、关键 API 链接已核对且无图片 |
| 29 | [[02-固定更新]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/fixed-updates.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、2 张官方图片、固定更新场景与注意事项已核对 |
| 30 | [[03-游戏时间和实时]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/time-scale.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、时间缩放 API 链接、1 个代码块已核对且无图片 |
| 31 | [[04-处理时间变化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/time-handling-variations.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、4 张官方图片与时间逻辑说明已核对 |
| 32 | [[05-捕获帧率]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/time-capture-frame-rate.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、1 个代码块和截图序列说明已核对且无图片 |
| 33 | [[06-模拟卡顿]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/time-simulate-hitches.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、1 个代码块和 2 个官方资源链接已核对且无图片 |
| 34 | [[00-使用协程跨帧分配任务]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/coroutines-section.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、主题表格与 PlayerLoop 资源已核对且无图片 |
| 35 | [[01-编写和运行Coroutine]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Coroutines.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文约 7.2 KB、4 个代码块、关键链接已核对且无图片 |
| 36 | [[02-分析Coroutine]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/coroutines-analyzing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、标题 3/3、图片 1/1，关键性能分析内容已核对 |
| 37 | [[03-Yield指令参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/coroutines-yield-instructions.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、标题 6/6、表格 3/3，运行时、UnityTest、Editor 和批处理模式内容已核对 |
| 38 | [[00-与Web服务器交互]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、目录表与资源说明已核对 |
| 39 | [[01-Unity Web Request API简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-intro.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、架构与事务流程已核对、官方图片 1/1 |
| 40 | [[02-Web Request高级API参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-hlapi.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、方法表 5/5、Handler 说明已核对 |
| 41 | [[03-Web Request低级API参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-llapi.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、5 个正文分节、Download/Upload Handler 表格与 Dispose 行为已核对 |
| 42 | [[00-使用Unity Properties处理类型数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/properties.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、6 个子页面目录项与 2 个相关资源已核对 |
| 43 | [[01-Unity Properties简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/properties-intro.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、场景列表、基础功能与相关资源已核对 |
| 44 | [[02-Property Bag]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/property-bags.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、5 个正文分节、示例代码块 1/1、成员与性能说明已核对 |
| 45 | [[03-Property Visitor]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/property-visitors.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、访问流程、High-Level/Low-Level 两种实现和代码块 2/2 已核对 |
| 46 | [[04-Property Path]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/property-paths.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、两张分配行为表与性能优化建议已核对 |
| 47 | [[05-使用PropertyVisitor类创建Property Visitor]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/property-visitors-PropertyVisitor.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、11 个正文分节、代码块 18/18 已核对 |
| 48 | [[06-使用低级API创建Property Visitor]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/property-visitors-low-level-api.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、6 个正文分节、代码块 7/7、低级 Visitor 与自定义 Adapter 已核对 |
| 49 | [[00-使用数学编程]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/programming-math.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、3 个子页面目录项与 2 个相关资源已核对 |
| 50 | [[01-Unity数学编程简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/programming-math-intro.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、兼容性/转换说明与等效类型表 18 行已核对 |
| 51 | [[02-Unity Engine数学API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-engine-math.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、4 个子页面目录项与 Mono/Burst 适用性说明已核对 |
| 52 | [[00-Unity Engine数学API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-engine-math.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、4 个子页面目录项与适用性说明已核对 |
| 53 | [[01-使用Mathf进行常见数学运算]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Mathf.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、7 个正文分节、Mathf 主要函数列表已核对 |
| 54 | [[02-使用Vector类移动对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-vectors.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、标题 8/8、三级标题 2/2、代码块 10/10、图片 7/7 |
| 55 | [[03-使用Random类生成随机数]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Random.html) | 已完成 | 官方网络正文已迁移并完成单文件审计；原链接大小写错误，已改为官方 canonical URL |
| 56 | [[04-使用Quaternion控制旋转]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Quaternion.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、7 个正文分节、代码块 1/1、图片 1/1 |
| 57 | [[03-Unity Mathematics API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-mathematics.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、7 个正文分节、三级分节 2 个、代码块 6/6 已核对 |
| 58 | [[00-智能字符串]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/smart-strings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、8 个本地分节、代码块 6/6、表格 2/2、图片 2/2 |
| 59 | [[01-生成动态文本]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/smart-strings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、7 个正文分节、三级分节 2 个、代码块 6/6、表格 2/2、图片 2/2 |
| 60 | [[02-配置Smart Strings]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/configure-smart-strings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、5 个正文分节、1 个三级分节、代码块 4/4、两张 API 表已核对 |
| 61 | [[03-Smart Strings设置参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/smart-strings-settings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、设置/Parser/Formatter 3 张表、章节层级已核对 |
| 62 | [[04-处理格式化错误]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/handle-formatting-errors.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、错误操作表、代码块、资源与导航已核对 |
| 63 | [[05-Default Source]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/default-source.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、代码块、资源与导航已核对 |
| 64 | [[06-Properties Source]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/properties-source.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、代码块、资源与导航已核对 |
| 65 | [[07-Dictionary Source]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/dictionary-source.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、代码块、资源与导航已核对 |
| 66 | [[08-String Source]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/string-source.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、代码块、资源与导航已核对 |
| 67 | [[09-Choose Formatter]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/choose-formatter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、表格、资源与导航已核对 |
| 68 | [[10-Conditional Formatter]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/conditional-formatter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、章节、表格、资源与导航已核对 |
| 69 | [[11-Plural Formatter]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/plural-formatter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、代码块、表格、资源与导航已核对 |
| 70 | [[12-List Formatter]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/list-formatter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、表格、资源与导航已核对 |
| 71 | [[13-Sub String Formatter]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/substring-formatter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、代码块、表格、资源与导航已核对 |
| 72 | [[14-创建自定义Formatter]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/smart-strings/create-a-custom-formatter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码块、表格、资源与导航已核对 |
| 73 | [[00-编译和代码重载]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/compilation-and-code-reload.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 74 | [[00-脚本编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-compilation.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 75 | [[00-脚本后端]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 76 | [[01-脚本后端简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-intro.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片、表格与导航已核对 |
| 77 | [[02-Mono脚本后端]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-mono.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、章节、资源与导航已核对 |
| 78 | [[00-IL2CPP脚本后端]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-il2cpp.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 79 | [[01-IL2CPP简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、章节、资源与导航已核对 |
| 80 | [[02-IL2CPP托管Stack Trace]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-managed-stack-traces.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 81 | [[03-IL2CPP运行时代码检查]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/il2cpp-runtime-checks.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、表格、代码与导航已核对 |
| 82 | [[04-额外IL2CPP编译器参数]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/handling-IL2CPP-additional-args.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、表格、代码与导航已核对 |
| 83 | [[05-Linux IL2CPP交叉编译器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/linux-il2cpp-crosscompiler.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、表格、代码与导航已核对 |
| 84 | [[06-IL2CPP限制]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-restrictions.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、列表、代码与导航已核对 |
| 85 | [[00-Burst编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 86 | [[01-Burst简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/introduction-to-burst.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 87 | [[02-Burst入门]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/getting-started.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 88 | [[00-配置Burst编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 89 | [[01-标记代码进行Burst编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-burstcompile.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 90 | [[02-为程序集定义Burst选项]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-burstcompile-assembly.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 91 | [[03-排除代码不进行Burst编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-burstdiscard.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 92 | [[04-泛型Job支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-generic-jobs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 93 | [[05-Play Mode中的Burst编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-synchronous.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 94 | [[06-编译警告参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/compilation-warnings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 95 | [[04-Burst编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/script-compilation-burst.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 96 | [[00-Burst优化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-overview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 97 | [[00-Burst内存别名]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/memory-aliasing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 98 | [[01-内存别名简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/aliasing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 99 | [[02-别名与Job System]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/aliasing-job-system.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 100 | [[03-声明无别名指针和结构体]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/aliasing-noalias.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 101 | [[02-限制整数范围]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-assumerange.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 102 | [[03-检查编译时约束]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-constant.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 103 | [[04-添加优化提示]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-hint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 104 | [[05-循环向量化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-loop-vectorization.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 105 | [[06-避免不必要的零初始化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/optimization-skiplocalsinit.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 106 | [[00-CSharp语言支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-language-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 107 | [[01-高性能CSharp简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-hpc-overview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 108 | [[02-调用Burst编译代码]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-calling-burst-code.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 109 | [[03-函数指针]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-function-pointers.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 110 | [[04-共享CSharp与Burst的静态数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-shared-static.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 111 | [[05-静态只读字段和静态构造函数支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-static-read-only-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 112 | [[06-字符串支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-string-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 113 | [[07-System命名空间支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-system-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 114 | [[08-CSharp和.NET类型支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-type-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 115 | [[09-Native Plug-in和内部调用支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-dllimport.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、结构与导航已核对 |
| 116 | [[00-Burst Intrinsics]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、资源与导航已核对 |
| 117 | [[01-跨平台Burst Intrinsics]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-common.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 118 | [[02-Burst Arm Neon Intrinsics参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-neon.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、操作记录与导航已核对 |
| 119 | [[03-处理器特定SIMD扩展]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-processors.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 120 | [[08-Burst AOT设置参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/building-aot-settings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、设置、图片与导航已核对 |
| 121 | [[09-平台构建支持参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/building-projects.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 122 | [[10-调试和性能分析工具]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/debugging-profiling-tools.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 123 | [[11-Burst Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/editor-burst-inspector.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 124 | [[12-Burst菜单参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/editor-burst-menu.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 125 | [[13-Burst Editor窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/editor-reference-overview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 126 | [[14-浮点精度和确定性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/float-precision-determinism.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 127 | [[15-Burst Modding支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/modding-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 128 | [[00-条件编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/conditional-compilation.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 129 | [[01-Unity中的条件编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/platform-dependent-compilation.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 130 | [[02-自定义脚本符号]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/custom-scripting-symbols.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、表格、列表与导航已核对 |
| 131 | [[03-Unity脚本符号参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-symbol-reference.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、表格、符号列表与导航已核对 |
| 132 | [[04-测试条件编译]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-conditional-compilation.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 133 | [[00-程序集定义]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-files.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、目录与导航已核对 |
| 134 | [[01-程序集简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definitions-intro.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 135 | [[02-创建程序集定义]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definitions-creating.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 136 | [[03-引用程序集]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definitions-referencing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 137 | [[04-程序集包含规则]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-includes.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 138 | [[05-程序集元数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-metadata.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 139 | [[06-程序集定义文件格式]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-file-format.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 140 | [[07-程序集定义Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AssemblyDefinitionImporter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 141 | [[08-程序集定义引用Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AssemblyDefinitionReferenceImporter.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 142 | [[09-预定义程序集参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-compile-order-folders.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 143 | [[00-托管代码剥离]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、目录与导航已核对 |
| 144 | [[01-托管代码剥离和Unity Linker]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-linker.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 145 | [[02-配置托管代码剥离]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-configure.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 146 | [[03-代码剥离对内容的影响]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-content.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 147 | [[04-使用注释保留代码]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-preserving.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 148 | [[05-Link XML格式参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-xml-formatting.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 149 | [[06-Unity Linker标记规则参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-marking-rules.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 150 | [[02-代码重载和代码生命周期]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/code-reloading-editor.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 151 | [[00-集成第三方代码库]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 152 | [[01-导入和配置Plug-in]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-in-inspector.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、设置说明、资源与导航已核对 |
| 153 | [[02-Managed Plug-in]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-managed.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 154 | [[04-为桌面平台构建Plug-in]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-for-desktop.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 155 | [[00-Native Plug-in]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 156 | [[01-Unity中的Native Plug-in简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-overview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 157 | [[00-调用函数]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-invoke.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 158 | [[01-从托管代码调用非托管函数]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-invoke-unmanaged.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 159 | [[02-从非托管代码调用托管函数]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-invoke-managed.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 160 | [[00-传递数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-pass-data.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 161 | [[01-基础类型]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-pass-primitives.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 162 | [[02-字符串]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-pass-strings.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 163 | [[03-结构体类和联合体]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-pass-types.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 164 | [[04-NativeArrays]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-pass-nativearrays.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 165 | [[04-DllImport属性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-dllimport.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 166 | [[00-脚本序列化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 167 | [[01-序列化规则]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-rules.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 168 | [[02-Unity如何使用序列化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-how-unity-uses.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 169 | [[03-序列化最佳实践]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-best-practices.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 170 | [[04-Dictionary序列化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-dictionaries.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 171 | [[05-自定义序列化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-custom-serialization.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 172 | [[06-JSON序列化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/json-serialization.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 173 | [[07-序列化规则分析器参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization-analyzer.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 174 | [[00-Native Plug-in API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 175 | [[01-Native Plug-in API简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 176 | [[02-日志API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-logging.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码与导航已核对 |
| 177 | [[03-内存管理API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-memory-manager-api.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 178 | [[04-IUnityMemoryManager API参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-memory-manager-api-reference.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码与导航已核对 |
| 179 | [[05-图形和渲染API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-rendering-extensions.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码与导航已核对 |
| 180 | [[06-Shader Compiler API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/low-level-native-plugin-shader-compiler-access.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码与导航已核对 |
| 181 | [[07-性能分析API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/LowLevelNativePluginProfiler.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、图片与导航已核对 |
| 182 | [[00-代码和场景重载]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/programming-code-lifecycle.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、目录与导航已核对 |
| 183 | [[01-配置Unity进入Play Mode]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 184 | [[02-Domain和Scene重载执行顺序参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/configurable-enter-play-mode-details.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 185 | [[03-不进行Domain Reload进入Play Mode]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/domain-reloading.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 186 | [[04-不进行Scene Reload进入Play Mode]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scene-reloading.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 187 | [[00-代码优化]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-optimization.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 188 | [[01-Unity编程最佳实践]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/programming-best-practices.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 189 | [[00-异步编程]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/async-await-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 190 | [[01-Awaitable异步编程简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 191 | [[02-Awaitable完成和Continuation]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-continuations.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 192 | [[03-Awaitable代码示例参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/async-awaitable-examples.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 193 | [[00-Job System]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文、资源与导航已核对 |
| 194 | [[01-Job System概览]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-overview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 195 | [[02-Jobs概览]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-jobs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 196 | [[03-创建和运行Job]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-creating-jobs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 197 | [[04-并行Jobs]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-parallel-for-jobs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 198 | [[00-线程安全类型]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-thread-safe-types.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 199 | [[01-NativeContainer简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-native-container.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 200 | [[02-复制NativeContainer结构]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-copy-nativecontainer.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 201 | [[03-实现自定义NativeContainer]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-custom-nativecontainer.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 202 | [[04-自定义NativeContainer示例]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-custom-nativecontainer-example.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 203 | [[05-Job依赖]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/job-system-job-dependencies.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 204 | [[00-优化托管内存代码]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-optimizing-code-managed-memory.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 205 | [[01-优化数组]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-optimizing-arrays.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 206 | [[02-引用类型管理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-reference-types.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 207 | [[03-对象池和复用对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/performance-reusable-code.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 208 | [[05-使用非托管API执行Transform操作]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 209 | [[00-使用非托管API执行Transform操作]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 210 | [[01-TransformHandle API简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 211 | [[02-TransformHandle API代码示例]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-examples.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 212 | [[03-在Burst中使用TransformHandle]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-burst.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 213 | [[04-TransformHandle类参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-TransformHandle.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 214 | [[00-测试代码]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/test-framework-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文、资源与导航已核对 |
| 215 | [[00-开始使用Unity Test Framework]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/getting-started.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 216 | [[01-Edit Mode和Play Mode测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/edit-mode-vs-play-mode-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 217 | [[02-创建测试程序集]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/workflow-create-test-assembly.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 218 | [[03-创建测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/workflow-create-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 219 | [[02-命令行参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-command-line.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、正文与导航已核对 |
| 220 | [[00-编写测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/writing-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 221 | [[00-测试前后的操作]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/before-and-after-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、正文与导航已核对 |
| 222 | [[01-测试操作执行顺序]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-actions-outside-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 223 | [[02-构建时设置和清理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-setup-and-cleanup.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 224 | [[03-UnitySetUp和UnityTearDown]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-unitysetup-and-unityteardown.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 225 | [[04-测试前后执行操作]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-outerunitytestaction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 226 | [[02-断言和比较]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/asserting-and-comparing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 227 | [[03-用于Editor的Yield指令]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-custom-yield-instructions.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 228 | [[04-编写参数化测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-tests-parameterized.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 229 | [[05-编写异步测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-async-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 230 | [[00-运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/running-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 231 | [[01-从Test Runner窗口运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/workflow-run-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 232 | [[02-从命令行运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/run-tests-from-command-line.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 233 | [[00-从代码运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/running-tests-from-code.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 234 | [[01-指定要运行的测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/extension-run-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 235 | [[02-获取测试列表]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/extension-retrieve-test-list.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 236 | [[03-获取测试结果]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/extension-get-test-results.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 237 | [[00-在Player中运行Play Mode测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/workflow-run-playmode-test-standalone.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 238 | [[01-修改Player构建参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/reference-attribute-testplayerbuildmodifier.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 239 | [[00-Unity Test Framework学习材料]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/overview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 240 | [[00-Unity Test Framework通用简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/test-framework-general-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 241 | [[01-在Unity项目中运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/running-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 242 | [[02-Arrange Act Assert]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/arrange-act-assert.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 243 | [[03-自定义比较]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/custom-comparison.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 244 | [[04-断言和预期日志]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/asserting-logs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 245 | [[05-SetUp和TearDown]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/setup-teardown.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 246 | [[06-PlayMode测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/play-mode-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 247 | [[07-Player中的PlayMode测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/play-mode-tests-in-player.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 248 | [[08-使用UnityTest属性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/unitytest-attribute.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 249 | [[09-长时间运行的测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/long-running-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 250 | [[10-基于Scene的测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/scene-based-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 251 | [[11-构建时设置和清理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/build-setup-cleanup.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 252 | [[12-Domain Reload]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/domain-reload.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 253 | [[13-保留测试状态]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/preserve-test-state.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 254 | [[14-测试用例]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/test-cases.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 255 | [[15-自定义属性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/custom-attributes.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 256 | [[16-以代码方式运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/running-tests-programmatically.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 257 | [[17-语义测试断言]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/semantic-test-assertion.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 258 | [[00-测试Lost Crypt]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/lost-crypt-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 259 | [[01-设置LostCrypt]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/setting-up.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 260 | [[02-在LostCrypt中运行测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/first-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 261 | [[03-移动角色]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/moving-character.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 262 | [[04-Reach Wand测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/reach-wand-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 263 | [[05-碰撞测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/collision-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 264 | [[06-Asset变更测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/asset-change-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 265 | [[07-Scene验证测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/scene-validation-test.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 266 | [[08-性能测试]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/performance-tests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 267 | [[00-调试和诊断]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/debugging-and-diagnostics.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 268 | [[01-在Unity中调试CSharp代码]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-debugging.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 269 | [[02-调试故障排查]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-debugging-troubleshooting.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 270 | [[03-Debug类]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Debug.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 271 | [[04-日志文件参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/log-files.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 272 | [[05-Stack Trace日志]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/stack-trace.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 273 | [[00-Roslyn分析器和源生成器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 274 | [[01-安装现有分析器或源生成器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/install-existing-analyzer.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 275 | [[02-创建和使用Roslyn分析器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/create-roslyn-analyzer.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 276 | [[03-创建和使用Source Generator]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/create-source-generator.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 277 | [[04-Analyzer范围和规则集文件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/analyzer-scope-and-diagnostics.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 278 | [[05-Roslyn Analyzer和Source Generator的Additional Files]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers-additional-files.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 279 | [[07-Safe Mode]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/SafeMode.html) | 已完成 | 官方网络正文已迁移并完成单文件审计 |
| 280 | [[00-游戏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/working-with-gameobjects.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、子页面索引和资源已核对 |
| 281 | [[01-游戏对象简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/GameObjects.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、3 张官方图片和关键链接已核对 |
| 282 | [[00-游戏对象基础]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/gameobject-fundamentals.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、子页面和资源已核对 |
| 283 | [[01-GameObject类]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-GameObject.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、12 个代码块和 5 张官方图片已核对 |
| 284 | [[02-Transform组件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Transform.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、5 张官方图片及正文已核对 |
| 285 | [[03-静态游戏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/StaticObjects.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、Static Editor Flags 内容和官方图片已核对 |
| 286 | [[04-停用游戏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/DeactivatingGameObjects.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 1/1 |
| 287 | [[05-原始体和占位对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PrimitiveObjects.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 6/6 |
| 288 | [[06-2D原始游戏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/2DPrimitiveObjects.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 8/8 |
| 289 | [[00-向游戏对象添加组件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/unity-components.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、目录与导航已核对 |
| 290 | [[01-组件简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Components.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 1/1 |
| 291 | [[02-使用组件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/UsingComponents.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 3/3 |
| 292 | [[03-使用脚本创建组件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CreatingComponents.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、脚本组件创建内容已核对 |
| 293 | [[04-管理组件及其值]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorManageComponents.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、组件管理目录已核对 |
| 294 | [[00-管理组件及其值]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorManageComponents.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、组件值管理内容已核对 |
| 295 | [[01-使用数组]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorArray.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 1/1 |
| 296 | [[02-使用数值字段表达式]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorNumericFields.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 3/3 |
| 297 | [[03-使用条形滑块]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorBarSliders.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 1/1 |
| 298 | [[04-选择颜色和颜色渐变]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorColorPicker.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 5/5 |
| 299 | [[05-使用曲线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorCurves.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、曲线、Preset 与资源内容已核对 |
| 300 | [[06-管理引用]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/InspectorReferences.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Reference 管理与额外资源已核对 |
| 301 | [[07-使用高级对象选择器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/search-advanced-object-picker.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 302 | [[05-约束组件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/constraint-components.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 303 | [[00-约束组件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/constraint-components.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 304 | [[01-约束组件简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Constraints.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 305 | [[02-Aim Constraint]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AimConstraint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 306 | [[03-Look At Constraint]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-LookAtConstraint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 307 | [[04-Parent Constraint]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-ParentConstraint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 308 | [[05-Position Constraint]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-PositionConstraint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 309 | [[06-Rotation Constraint]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-RotationConstraint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 310 | [[07-Scale Constraint]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-ScaleConstraint.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 311 | [[00-将游戏对象分配到层]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Layers.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、资源与导航已核对 |
| 312 | [[01-层的用途]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/use-layers.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 313 | [[02-创建功能层]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/create-layers.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、资源与导航已核对 |
| 314 | [[03-层与LayerMask]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/layers-and-layermasks.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 315 | [[00-层与LayerMask]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/layers-and-layermasks.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 316 | [[01-LayerMask简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 317 | [[02-向LayerMask添加Layer]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-add.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 318 | [[03-设置LayerMask]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-set.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 319 | [[04-从LayerMask移除Layer]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-remove.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 320 | [[05-将标签分配给游戏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Tags.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 321 | [[00-预制件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Prefabs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 322 | [[01-预制件简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/prefabs-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 323 | [[02-创建预制件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CreatingPrefabs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、正文与导航已核对 |
| 324 | [[03-编辑预制件资源]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/EditingInPrefabMode.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、正文与导航已核对 |
| 325 | [[04-嵌套预制件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/NestedPrefabs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、正文与导航已核对 |
| 326 | [[05-创建预制件变体]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabVariants.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、正文与导航已核对 |
| 327 | [[06-覆盖预制件实例数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/prefabs-override.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、子页面索引与导航已核对 |
| 328 | [[00-覆盖预制件实例数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/prefabs-override.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 329 | [[01-覆盖预制件实例]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PrefabInstanceOverrides.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、正文与导航已核对 |
| 330 | [[02-移除未使用的覆盖数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/UnusedOverrides.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、图片、正文与导航已核对 |
| 331 | [[07-将预制件实例还原为游戏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/UnpackingPrefabInstances.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 332 | [[08-在运行时实例化预制件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 333 | [[00-在运行时实例化预制件]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 334 | [[01-实例化预制件简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs-intro.html) | 已完成 | 官方网络正文已重新迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 335 | [[02-使用预制件构建结构]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs-structure.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码、图片与导航已核对 |
| 336 | [[03-实例化投射物和爆炸]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs-projectiles.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码、图片与导航已核对 |
| 337 | [[09-预制件实例 Inspector 参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/prefab-instance-inspector-reference.html) | 已完成 | 官方网络正文已重新迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 338 | [[00-相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/Cameras.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 339 | [[01-相机简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CamerasOverview.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 340 | [[02-以第一人称控制相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/control-camera.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 341 | [[00-相机视图]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraView.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 342 | [[01-相机视图简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/UnderstandingFrustum.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 343 | [[02-使相机透视变为斜视]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/ObliqueFrustum.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、1 个代码块和 2 张官方图片已核对 |
| 344 | [[03-计算指定距离处的视锥体大小]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/FrustumSizeAtDistance.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 345 | [[00-相机射线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraRays.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、正文与导航已核对 |
| 346 | [[01-从相机发射射线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraRays-cast.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 347 | [[02-沿射线移动相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraRays-move.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 348 | [[00-使用多个相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/MultipleCameras-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录与导航已核对 |
| 349 | [[01-配置多台相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/MultipleCameras.html) | 已完成 | 官方当前 canonical 页面已同步；正文、图片、本地链接与导航审计通过 |
| 350 | [[02-设置多台相机的顺序]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/multiple-cameras-birp.html) | 已完成 | 官方当前 canonical 页面已同步；正文、本地链接与导航审计通过 |
| 351 | [[03-在多台显示器上显示相机视图]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/MultiDisplay.html) | 已完成 | 官方当前 canonical 页面已同步；正文、图片、本地链接与导航审计通过 |
| 352 | [[00-更改分辨率缩放]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/resolution-scale.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录与导航已核对 |
| 353 | [[01-分辨率缩放简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/resolution-scale-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 354 | [[00-动态分辨率]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/DynamicResolution-landing.html) | 已完成 | 官方当前 canonical 页面已同步；目录、正文、本地链接与导航审计通过 |
| 355 | [[01-动态分辨率简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/DynamicResolution-introduction.html) | 已完成 | 官方当前 canonical 页面已同步；正文、本地链接与导航审计通过 |
| 356 | [[02-控制动态分辨率缩放]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/DynamicResolution-control.html) | 已完成 | 官方当前 canonical 页面已同步；正文、代码、本地链接与导航审计通过 |
| 357 | [[03-控制动态分辨率触发时机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/DynamicResolution-control-when-occurs.html) | 已完成 | 官方当前 canonical 页面已同步；正文、代码、本地链接与导航审计通过 |
| 358 | [[04-为渲染目标启用或禁用动态分辨率]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/DynamicResolution-enable-disable.html) | 已完成 | 官方当前 canonical 页面已同步；正文、代码、本地链接与导航审计通过 |
| 359 | [[03-使用STP放大URP分辨率]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/change-resolution-scale-urp.html) | 已完成 | 官方当前 canonical 页面已同步；目录、正文、本地链接与导航审计通过 |
| 360 | [[04-XR项目中的分辨率控制]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/xr-graphics-resolution-scaling.html) | 已完成 | 官方当前 canonical 页面已同步；正文、代码、本地链接与导航审计通过 |
| 361 | [[00-使用遮挡剔除排除隐藏对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/OcclusionCulling-landing.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、目录与导航已核对 |
| 362 | [[01-遮挡剔除]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/OcclusionCulling.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 2/2 |
| 363 | [[02-设置遮挡剔除场景]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-getting-started.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、烘焙与可视化步骤已核对 |
| 364 | [[03-设置多个场景进行遮挡剔除]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-scene-loading.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、多场景流程已核对 |
| 365 | [[04-剔除移动GameObject]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-dynamic-gameobjects.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Dynamic Occlusion 内容已核对 |
| 366 | [[05-创建高精度遮挡区域]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-OcclusionArea.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、遮挡区域设置与运行时行为已核对 |
| 367 | [[06-使用Occlusion Portal控制区域遮挡]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-OcclusionPortal.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Portal 设置、脚本与组件参考已核对 |
| 368 | [[07-Occlusion Culling窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-window.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 2/2、窗口选项与表格已核对 |
| 369 | [[00-CullingGroup API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CullingGroupAPI-landing.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、目录与导航已核对 |
| 370 | [[01-CullingGroup API简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CullingGroupAPI.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、CullingGroup API 内容已核对 |
| 371 | [[02-创建Culling Group]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CullingGroupAPI-getstarted.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、创建 Culling Group 流程已核对 |
| 372 | [[03-获取剔除结果]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CullingGroupAPI-get-culling-results.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、回调与查询 API 已核对 |
| 373 | [[09-遮挡剔除故障排查]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/occlusion-culling-troubleshooting.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、症状、原因与解决方法已核对 |
| 374 | [[10-URP中的GPU遮挡剔除]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/gpu-culling.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、URP GPU Occlusion 内容已核对 |
| 375 | [[07-渲染队列与排序行为]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/built-in-rendering-order.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Render Queue 与排序规则已核对 |
| 376 | [[00-使用物理相机模拟真实相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PhysicalCameras.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、物理相机目录已核对 |
| 377 | [[01-物理相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PhysicalCameras-introduction.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 1/1 |
| 378 | [[02-使用Lens Shift扩大视野]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PhysicalCameras-LensShift.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 5/5 |
| 379 | [[00-使用 Gate Fit 裁剪或拉伸视图]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PhysicalCameras-GateFit-Landing.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Gate Fit 目录已核对 |
| 380 | [[01-Gate Fit 简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PhysicalCameras-GateFit.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 2/2 |
| 381 | [[02-配置 Gate Fit]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/PhysicalCameras-GateFit-Configure.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、图片 5/5 |
| 382 | [[00-相机输出]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraOutput.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Camera Output 目录已核对 |
| 383 | [[01-相机输出简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraOutput-introduction.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、输出类型与平台支持已核对 |
| 384 | [[02-从相机输出深度纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-CameraDepthTexture.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Depth/DepthNormals 内容已核对 |
| 385 | [[03-从相机输出运动矢量纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-CameraDepthTexture-motionvectors.html) | 已完成 | 官方网络正文已迁移并审计：HTTP 200、canonical 匹配、Motion Vectors 内容已核对 |
| 386 | [[04-在Shader中采样输出纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraOutput-shader.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 387 | [[05-排查相机输出问题]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraOutput-troubleshoot.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 388 | [[00-URP中的相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-cameras-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 389 | [[01-URP中的相机简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/camera-differences-in-urp.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 390 | [[00-相机渲染类型]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-types-and-render-type.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 391 | [[01-相机渲染类型简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-types-and-render-type-introduction.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 392 | [[02-更改相机渲染类型]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-types-and-render-type-change.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 393 | [[00-多台相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras-multiple.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 394 | [[01-Camera Stack原理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/camera-stacking-concepts.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 395 | [[02-设置Camera Stack]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-stacking.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 396 | [[03-在Camera Stack中添加移除和排序相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/add-and-remove-cameras-in-a-stack.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、图片与导航已核对 |
| 397 | [[04-设置分屏渲染]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-to-the-same-render-target.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 398 | [[05-为不同相机应用不同后处理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/apply-different-post-proc-to-cameras.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 399 | [[06-将相机输出渲染到Render Texture]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-to-a-render-texture.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 400 | [[07-创建Render Request]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/User-Render-Requests.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、资源与导航已核对 |
| 401 | [[04-相机渲染顺序]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras-advanced.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、资源与导航已核对 |
| 402 | [[00-运动矢量]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录与导航已核对 |
| 403 | [[01-运动矢量简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 404 | [[02-Shader中的内置运动矢量支持]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-shader-support.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 405 | [[03-运动矢量Render Pass]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-render-pass.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 406 | [[04-在自定义Shader中输出运动矢量纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-custom-shader.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、导航与图片检查已核对 |
| 407 | [[05-在Shader中采样运动矢量]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-sample.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、代码、导航与图片检查已核对 |
| 408 | [[06-运动矢量故障排查]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-troubleshooting.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、导航与图片检查已核对 |
| 409 | [[07-MeshRenderer运动矢量设置参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/motion-vectors-reference.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、设置表格、导航与图片检查已核对 |
| 410 | [[08-从Camera输出运动矢量纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-CameraDepthTexture-motionvectors.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、导航与图片检查已核对 |
| 411 | [[00-使用STP放大分辨率]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/change-resolution-scale-urp.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 412 | [[01-STP Upscaler简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/stp/stp-upscaler.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 413 | [[02-启用STP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/stp/stp-enable.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文与导航已核对 |
| 414 | [[03-STP Rendering Debugger参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/stp/stp-debug-views.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、表格与导航已核对 |
| 415 | [[07-Universal Additional Camera Data]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universal-additional-camera-data.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、代码与导航已核对 |
| 416 | [[00-Camera Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-components-reference-landing.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、目录、表格、图片与导航已核对 |
| 417 | [[01-Camera Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/camera-component-reference.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、正文、图片与导航已核对 |
| 418 | [[02-Physical Camera Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/physical-camera-reference.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、表格、正文、图片与导航已核对 |
| 419 | [[00-Built-In Render Pipeline中的相机]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/cameras-birp.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、警告与导航已核对 |
| 420 | [[01-使用Clear Flags设置相机背景]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/camera-background-birp.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |
| 421 | [[02-Camera Inspector窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Camera.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、属性表、正文与导航已核对 |
| 422 | [[12-相机故障排查]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/CameraTroubleshooting.html) | 已完成 | 官方网络正文已迁移并完成单文件审计：HTTP 200、canonical 匹配、正文、图片与导航已核对 |

## 渲染管线

| # | 本地 Markdown | 原文链接 | 状态 | 审计备注 |
| ---: | --- | --- | --- | --- |
| 423 | [[00-渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 424 | [[01-渲染管线简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-overview.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 425 | [[02-可编程渲染管线基础知识]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/scriptable-render-pipeline-introduction.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 426 | [[00-选择渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/choose-a-render-pipeline-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 427 | [[01-选择渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/choose-a-render-pipeline.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 428 | [[02-渲染管线功能比较参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-feature-comparison.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 429 | [[03-设置渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/render-pipelines-set-up.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 430 | [[04-更改或检测激活的渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/srp-setting-render-pipeline-asset.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 431 | [[04-Unity 中的渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/rendering-paths-introduction.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 432 | [[00-使用通用渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/universal-render-pipeline.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 433 | [[01-通用渲染管线简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-introduction.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 434 | [[02-URP 的要求和兼容性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/requirements.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 435 | [[03-URP 17 (Unity 6) 中的新功能]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/whats-new/urp-whats-new.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 436 | [[00-开始使用 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/introduction-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 437 | [[00-通用渲染管线基础知识]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-concepts.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 438 | [[01-通用渲染管线中的渲染]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-in-universalrp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 439 | [[00-URP 中的渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-paths-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 440 | [[01-URP 中渲染路径简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-paths-introduction-urp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 441 | [[02-在 URP 中选择渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-paths-comparison.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 442 | [[03-在 URP 中设置渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering-paths-set.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 443 | [[04-URP 中的前向渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/forward-rendering-paths.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 444 | [[00-URP 中的延迟渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/deferred-rendering-path-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 445 | [[01-URP 中延迟渲染路径中的渲染通道]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/render-passes-deferred.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 446 | [[02-URP 中延迟渲染路径中的 G 缓冲区布局]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/g-buffer-layout.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 447 | [[03-在 URP 的延迟渲染路径中启用 Accurate G-buffer normals]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/accurate-g-buffer-normals.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 448 | [[04-延迟渲染路径简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/deferred-rendering-path-introduction.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 449 | [[05-在 URP 中使着色器与延迟渲染路径兼容]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/make-shader-compatible-with-deferred.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 450 | [[06-URP 中的 Forward+ 渲染路径的故障排除]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/forward-plus-rendering-path-limitations.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 451 | [[00-安装和升级 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/InstallingAndConfiguringURP.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 452 | [[00-创建 URP 项目]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/creating-a-urp-project.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 453 | [[01-使用 URP 创建新项目]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/creating-a-new-project-with-urp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 454 | [[02-URP 中的场景模板]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/scene-templates.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 455 | [[03-在 URP 中导入包示例]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/package-samples.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 456 | [[04-URP 的包示例参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/package-sample-urp-package-samples.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 457 | [[00-从内置渲染管线升级到 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-from-birp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 458 | [[01-从内置渲染管线迁移到 URP 的工作流]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/migrating-from-birp-workflow.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 459 | [[02-将 URP 安装到现有项目中]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/InstallURPIntoAProject.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 460 | [[03-将内置渲染管线的资源和质量级别转换为 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-assets-to-urp.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 461 | [[04-升级自定义着色器以实现 URP 兼容性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/birp-urp-custom-shader-upgrade-guide.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 462 | [[05-将质量设置从内置渲染管线转换到 URP。]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/birp-onboarding/quality-presets.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 463 | [[06-使用渲染管线转换器转换资源]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/features/rp-converter.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 464 | [[07-URP 中的内置渲染管线材质引用]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-material-refs.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 465 | [[08-使用渲染管线转换器将着色器转换为 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrading-your-shaders.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 466 | [[09-查找 URP 中内置渲染管线质量设置]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/birp-onboarding/quality-settings-location.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 467 | [[00-从 HDRP 迁移到 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/migrating-from-hdrp.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 468 | [[01-从 HDRP 迁移到 URP 的工作流]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/migrating-from-hdrp-workflow.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 469 | [[02-设置 HDRP 项目以使用 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/hdrp-project-setup.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 470 | [[03-将 HDRP Shader 转换为 URP 兼容版本]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-hdrp-shaders-to-urp.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 471 | [[04-将 HDRP 的 Visual Effect Graph 转换为 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-hdrp-vfx-graph-to-urp.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 472 | [[05-将 HDRP 光照转换为 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-hdrp-lighting-to-urp.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 473 | [[06-URP 中的 HDRP 质量设置参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/hdrp-quality-settings-urp-reference.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 474 | [[00-升级 URP]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guides.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 475 | [[01-升级到 URP 17.1（Unity 6.1）]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-unity-6-1.html) | 待执行 | 官方网络页面已抓取；官方中文页面暂缺，已保留英文网络正文，需人工翻译复核 |
| 476 | [[02-升级到 URP 17 (Unity 6)]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-unity-6.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 477 | [[03-升级到 URP 16 (Unity 2023.2)]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-2023-2.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 478 | [[04-升级到 URP 15 (Unity 2023.1)]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-2023-1.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 479 | [[05-升级到 URP 14 (Unity 2022.2)]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-2022-2.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 480 | [[06-升级到 URP 13 (Unity 2022.1)]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-2022-1.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 481 | [[07-升级到 URP 12 (Unity 2021.2)]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-2021-2.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 482 | [[08-升级到通用渲染管线版本 11.0.x]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-11-0-x.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 483 | [[09-升级到通用渲染管线版本 10.1.x]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-10-1-x.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 484 | [[10-升级到通用渲染管线版本 10.0.x]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-10-0-x.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 485 | [[11-升级到通用渲染管线版本 9.0.x]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-9-0-x.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 486 | [[12-升级到通用渲染管线版本 8.2.x]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-8-2-0.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 487 | [[13-升级到通用渲染管线版本 8.1.x]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-8-1-0.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 488 | [[14-升级到通用渲染管线版本 8.0.0]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-8-0-0.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 489 | [[15-升级到通用渲染管线版本 7.4.0]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-7-4-0.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 490 | [[16-升级到通用渲染管线版本 7.3.0]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-7-3-0.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 491 | [[17-升级到通用渲染管线版本 7.2.0]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-guide-7-2-0.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 492 | [[18-从轻量级渲染管线升级到通用渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/upgrade-lwrp-to-urp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 493 | [[05-URP 中的已知问题：]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/known-issues.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 494 | [[03-配置 URP 以获得更好的性能]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/configure-for-better-performance.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 495 | [[00-URP 中的图形质量设置]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-quality-settings-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 496 | [[01-通用渲染管线资源]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-asset-and-renderer.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 497 | [[渲染管线/05-使用通用渲染管线/05-URP 中的图形质量设置/02-Create a Universal Render Pipeline asset.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-asset-create.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 498 | [[03-在 URP 资源中显示高级属性]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-asset-additional-settings.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 499 | [[04-在运行时更改活动的 URP 资源]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/quality/quality-settings-through-code.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 500 | [[05-在运行时更改 URP 资源设置]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/quality/change-urp-asset-settings.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 501 | [[06-使用 URP 配置包配置设置]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/URP-Config-Package.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 502 | [[06-在通用渲染管线中添加抗锯齿]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/anti-aliasing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 503 | [[00-在 URP 中自定义渲染和后期处理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customizing-urp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 504 | [[01-URP 中的可编程渲染通道简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/intro-to-scriptable-render-passes.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 505 | [[00-通过 URP 中的渲染器功能添加预构建效果]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-renderer-feature-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 506 | [[01-向 URP 渲染器添加渲染器功能]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-renderer-feature.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 507 | [[02-通过 URP 中的渲染对象渲染器功能 (Render Objects Renderer Feature) 创建自定义渲染效果的示例]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/how-to-custom-effect-render-objects.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 508 | [[03-URP 的渲染对象渲染器功能 (Render Objects Renderer Feature) 参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/renderer-feature-render-objects.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 509 | [[03-URP 中的自定义渲染通道工作流程]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/custom-rendering-pass-workflow-in-urp.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 510 | [[04-在 URP 中执行 Blit 的最佳实践]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/blit-overview.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 511 | [[00-URP 中的渲染图系统]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 512 | [[01-URP 中的渲染图系统简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-introduction.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 513 | [[02-在 URP 中使用渲染图系统编写渲染通道]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-write-render-pass.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 514 | [[渲染管线/05-使用通用渲染管线/07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/03-Blit using the render graph system in URP.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-blit.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 515 | [[00-URP 中的 Render Graph 系统中的纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/working-with-textures.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 516 | [[01-在 URP 中的渲染通道中使用纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-read-write-texture.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 517 | [[02-在 URP 中的渲染图形系统中创建纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-create-a-texture.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 518 | [[00-在 URP 中的渲染通道之间传输纹理]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-pass-textures-between-passes.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 519 | [[渲染管线/05-使用通用渲染管线/07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/04-URP 中的 Render Graph 系统中的纹理/03-在 URP 中的渲染通道之间传输纹理/01-Add a texture to the frame data in URP.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-add-texture-to-frame-data.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 520 | [[渲染管线/05-使用通用渲染管线/07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/04-URP 中的 Render Graph 系统中的纹理/03-在 URP 中的渲染通道之间传输纹理/02-Create a texture as a global texture in URP.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-create-global-texture.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 521 | [[03-将纹理导入 URP 中的渲染图系统]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-import-a-texture.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 522 | [[00-URP 中的渲染图系统中的帧数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-frame-data.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 523 | [[01-从 URP 中的当前帧获取数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/accessing-frame-data.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 524 | [[02-在 URP 中获取先前帧的数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-get-previous-frames.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 525 | [[03-将纹理添加到摄像机历史记录]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-add-textures-to-camera-history.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 526 | [[04-URP 的帧数据纹理参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-frame-data-reference.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 527 | [[06-在 URP 中的渲染图形系统中绘制对象]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-draw-objects-in-a-pass.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 528 | [[00-在 URP 的渲染图系统中的计算着色器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-compute-shader.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 529 | [[01-在 URP 中的渲染通道中运行计算着色器]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-compute-shader-run.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 530 | [[02-在 URP 中为计算着色器创建输入数据]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-compute-shader-input.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 531 | [[08-在 URP 中分析渲染图]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-view.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 532 | [[渲染管线/05-使用通用渲染管线/07-在 URP 中自定义渲染和后期处理/05-URP 中的渲染图系统/09-Optimize a render graph.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-optimize.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 533 | [[10-在渲染图渲染通道中使用兼容性模式 API]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-unsafe-pass.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 534 | [[11-URP 的渲染图查看器 (Render Graph Viewer) 窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-viewer-reference.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 535 | [[00-在 URP 中将可编程渲染通道添加到帧渲染循环]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/inject-a-render-pass.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 536 | [[01-在 URP 中创建可编程渲染器功能]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/scriptable-renderer-features/inject-a-pass-using-a-scriptable-renderer-feature.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 537 | [[02-在 URP 中通过脚本注入渲染通道]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/inject-render-pass-via-script.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 538 | [[渲染管线/05-使用通用渲染管线/07-在 URP 中自定义渲染和后期处理/06-在 URP 中将可编程渲染通道添加到帧渲染循环/03-Restrict a render pass to a scene area in URP.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/restrict-render-pass-scene-area.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 539 | [[04-URP 的注入点参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/custom-pass-injection-points.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 540 | [[渲染管线/05-使用通用渲染管线/07-在 URP 中自定义渲染和后期处理/07-Modify URP source code.md]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/modify-urp-source-code.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 541 | [[00-通用渲染管线参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-reference-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 542 | [[01-URP 通用渲染管线资源参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universalrp-asset.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 543 | [[02-URP 的通用渲染器资源参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-universal-renderer.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 544 | [[03-URP 的图形设置窗口参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-global-settings.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 545 | [[06-使用高清渲染管线资源]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/high-definition-render-pipeline.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 546 | [[00-使用内置渲染管线]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/built-in-render-pipeline.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 547 | [[01-内置渲染管线的硬件要求]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderTech-HardwareRequirements.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 548 | [[00-内置渲染管线中的图形质量设置]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/built-in-graphics-quality-settings.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 549 | [[01-内置渲染管线中的图形层]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/graphics-tiers.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 550 | [[02-在内置渲染管线中配置图形层]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/graphics-tiers-customize.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 551 | [[00-内置渲染管线中的渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/built-in-rendering-paths.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 552 | [[01-内置渲染管线中的渲染路径简介]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderingPaths.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 553 | [[02-内置渲染管线中的前向渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderTech-ForwardRendering.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 554 | [[03-内置渲染管线中的延迟渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderTech-DeferredShading.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 555 | [[04-内置渲染管线中的旧版顶点光照渲染路径]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/RenderTech-VertexLit.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 556 | [[00-在内置渲染管线中自定义渲染]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/GraphicsCommandBuffers-landing.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 557 | [[01-内置渲染管线中 CommandBuffer 的基础知识]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/GraphicsCommandBuffers.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |
| 558 | [[02-针对内置渲染管线的 CameraEvent 和 LightEvent 事件顺序参考]] | [原文](https://docs.unity3d.com/6000.7/Documentation/Manual/GraphicsCommandBuffers-order.html) | 已完成 | 官方网络页面已抓取；正文、图片、本地链接与导航已生成，待全量校验 |

## 状态说明

- **已完成**：已逐页抓取官方网络页面，并核对正文结构、代码块、图片和导航；后续只需在整体结束前再跑一次根目录链接校验。
- **已处理待复核**：已有实质性搬运记录，但需要重新按当前审计口径逐页确认，暂不计入严格完成数。
- **待执行**：不能依据现有摘要、目录或本地缓存直接判定完成；必须重新读取原文链接对应的官方网络页面。
- **源站异常**：官方 6000.7 原文链接当前无法取得正常页面，单独记录，不伪装成已完成。
