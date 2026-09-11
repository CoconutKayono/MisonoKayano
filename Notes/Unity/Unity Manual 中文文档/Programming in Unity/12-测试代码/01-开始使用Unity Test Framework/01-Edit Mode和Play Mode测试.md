# Edit Mode 和 Play Mode 测试

> 原文：[Edit mode and Play mode tests](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/edit-mode-vs-play-mode-tests.html)

Unity Test Framework 会根据父程序集的引用，将测试识别为 Edit Mode 测试或 Play Mode 测试。

## Edit Mode 测试

Edit Mode 测试（也称为 Editor 测试）只能在 Unity Editor 中运行，并且可以访问 Editor 代码和运行时应用程序代码。因此，Edit Mode 测试程序集可以引用 `UnityEditor` 和 `UnityEngine` 命名空间中的代码。

使用 Edit Mode 测试时，可以通过 [`[UnityTest]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityTestAttribute.html) Attribute 测试任意[编辑器扩展](https://docs.unity3d.com/6000.7/Documentation/Manual/ExtendingTheEditor.html)。Edit Mode 测试在 [`EditorApplication.update`](https://docs.unity3d.com/ScriptReference/EditorApplication-update.html) 回调循环中运行。

不能在 Edit Mode 测试中运行[协程](https://docs.unity3d.com/ScriptReference/Coroutine.html)。

你还可以在 Edit Mode 测试中控制进入和退出 Play Mode，使测试能够在进入 Play Mode 之前进行更改。

Edit Mode 测试必须具有一个引用 `nunit.framework.dll` 的[[02-创建测试程序集|程序集定义]]，并且只能将 Editor 作为目标平台：

```json
assembly
    "includePlatforms": [
        "Editor"
    ],
```

## Play Mode 测试

你可以[[../../04-运行测试/04-在Player中运行Play Mode测试/00-在Player中运行Play Mode测试|在 Player 中]]或在 Editor 内运行 Play Mode 测试。Play Mode 测试用于测试运行时应用程序代码；如果使用 `[UnityTest]` Attribute 标记，测试会作为[协程](https://docs.unity3d.com/ScriptReference/Coroutine.html)运行。

Play Mode 测试必须满足以下条件：

- 测试必须拥有自己的[[02-创建测试程序集|程序集定义]]，并引用 `nunit.framework.dll`。
- 测试脚本必须位于与 `.asmdef` 文件同级的文件夹中。
- 测试程序集必须引用包含要测试代码的任何其他程序集。

```json
assembly
    "references": [
        "NewAssembly"
    ],
    "optionalUnityReferences": [
        "TestAssemblies"
   ],
    "includePlatforms": [],
```

> **注意**：测试程序集不能引用预定义的 `Assembly-Csharp.dll` 程序集。你必须将要测试的代码移入自定义程序集，然后由测试程序集引用该自定义程序集。更多信息请参阅[创建程序集资源](02-创建程序集定义.md)。

## 建议

除非满足以下条件，否则请使用 NUnit 的 [`[Test]`](https://docs.nunit.org/articles/nunit/writing-tests/attributes/test.html) Attribute，而不是 [`[UnityTest]`](https://docs.unity3d.com/Packages/com.unity.test-framework@latest/index.html?subfolder=/api/UnityEngine.TestTools.UnityTestAttribute.html)：

- 需要在 Edit Mode 测试中[[../../03-编写测试/03-用于Editor的Yield指令|为 Editor 生成 Yield 指令]]。
- 需要在 Play Mode 测试中跳过一帧，或等待一段特定的时间。

## 其他资源

- [[02-创建测试程序集]]
- [[03-创建测试]]


---

## 文档导航

- 上一页：[[00-开始使用Unity Test Framework]]
- 目录：[[00-开始使用Unity Test Framework]]
- 下一页：[[02-创建测试程序集]]
