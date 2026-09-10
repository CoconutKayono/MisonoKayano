# Unity Linker 标记规则参考

> 原文：[Unity linker marking rules reference](https://docs.unity3d.com/6000.7/Documentation/Manual/managed-code-stripping-marking-rules.html)

Unity Linker 执行静态分析时，会遵循多组规则，以确定要将 CIL 字节码的哪些部分标记为构建所必需：

- <a id="root-marking-rules"></a>[[#root-marking-rules|根标记规则]]决定 Unity Linker 如何识别并保留构建中的顶层程序集。
- <a id="dependency-marking-rules"></a>[[#dependency-marking-rules|依赖标记规则]]决定 Unity Linker 如何识别并保留根程序集所依赖的代码。

[[02-配置托管代码剥离|已配置的 Managed Stripping Level]] 会改变 Unity Linker 使用的规则集合。以下章节描述每个 Managed Stripping Level 下的标记规则。

## 根标记规则

下表描述 Unity Linker 针对不同程序集类型和 Managed Stripping Level，如何识别程序集中的顶层类型：

| 程序集类型 | 不同 Managed Stripping Level 下的根标记规则 |
| --- | --- |
| **.NET Class & Platform SDK and UnityEngine Assemblies** | **Minimal** 和 **Low**：<ul><li>Precautionary preservations。</li></ul>**Minimal**、**Low**、**Medium** 和 **High**：<ul><li>`link.xml` 文件中定义的保留内容。</li></ul> |
| **Assemblies with types referenced in a scene** | **Minimal** 和 **Low**：<ul><li>程序集中的所有类型和成员。</li></ul>**Medium** 和 **High**：<ul><li>所有带有 `[RuntimeInitializeOnLoadMethod]` 或 `[Preserve]` Attribute 的方法。</li><li>`link.xml` 文件中定义的保留内容。</li><li>precompiled、package、Unity Script 或 assembly definition 程序集中所有派生自 `MonoBehaviour` 和 `ScriptableObject` 的类型。</li></ul> |
| **All other** | **Minimal**：<ul><li>程序集中的所有类型和成员。</li></ul>**Low** 和 **Medium**：<ul><li>所有 public 类型及这些类型的 public 成员。</li></ul>**Medium** 和 **High**：<ul><li>所有带有 `[RuntimeInitializeOnLoadMethod]` 或 `[Preserve]` Attribute 的方法。</li><li>`link.xml` 文件中定义的保留内容。</li><li>precompiled、package、Unity Script 或 assembly definition 程序集中所有派生自 `MonoBehaviour` 和 `ScriptableObject` 的类型。</li></ul> |
| **Test** | **Minimal**、**Low**、**Medium** 和 **High**：<ul><li>任何带有 `[UnityTest]` Attribute 的方法，以及任何使用 NUnit.Framework 中定义的 Attribute 注释的方法。</li></ul> |

## 依赖标记规则

Unity Linker 识别出程序集中的根后，还需要识别这些根所依赖的代码。下表描述 Unity Linker 在不同 Managed Stripping Level 下如何识别程序集根类型的依赖项：

| 规则目标 | 不同 Managed Stripping Level 下的依赖标记规则 |
| --- | --- |
| **MonoBehaviour** | **Minimal**、**Low**、**Medium** 和 **High**：<ul><li>Unity Linker 标记 MonoBehavior 类型时，会标记该类型的所有成员。</li></ul> |
| **ScriptableObject** | **Minimal**、**Low**、**Medium** 和 **High**：<ul><li>Unity Linker 标记 ScriptableObject 类型时，会标记该类型的所有成员。</li></ul> |
| **Attributes** | **Minimal** 和 **Low**：<ul><li>Unity Linker 标记程序集、类型或其他代码结构时，也会标记这些结构的所有 Attribute。</li></ul>**Medium** 和 **High**：<ul><li>Unity Linker 标记程序集、类型或其他代码结构时，只有在 Attribute 类型也被标记的情况下，才会标记这些结构的 Attribute。</li></ul> |
| **Debugging Attributes** | **Minimal** 和 **Low**：<ul><li>启用 script debugging 时，Unity Linker 会标记所有带有 `[DebuggerDisplay]` Attribute 的成员，即使没有代码路径使用这些成员。</li></ul>**Medium** 和 **High**：<ul><li>Unity Linker 始终移除 `DebuggerDisplayAttribute` 和 `DebuggerTypeProxyAttribute` 等 debugging Attribute。</li></ul> |
| **.NET Facade Class Library** | **Minimal**、**Low**、**Medium** 和 **High**：<ul><li>移除 facade assemblies，因为它们在运行时不是必需的。</li></ul> |

## 其他资源

- [[01-托管代码剥离和Unity Linker]]
- [[04-使用注释保留代码]]
- [[05-Link XML格式参考]]

---

## 文档导航

- 上一页：[[05-Link XML格式参考]]
- 目录：[[00-托管代码剥离]]
- 下一页：[[../../02-代码重载和代码生命周期]]
