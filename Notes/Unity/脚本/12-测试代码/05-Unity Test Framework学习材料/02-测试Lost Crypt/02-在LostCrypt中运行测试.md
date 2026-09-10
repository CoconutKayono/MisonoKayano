# 2. 在 LostCrypt 中运行测试

> 原文：[2. Running a test in a LostCrypt](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/first-test.html)

## 学习目标

为 LostCrypt 设置一个简单的 Play Mode 测试。

## 练习

- 前往 `Assets/Scripts` 目录，花一些时间查看 LostCrypt 正常运行所需的脚本。
- 创建一个新目录 `Assets/Tests`。
- 在 Test Runner 窗口中，点击 **Create PlayModeTest Assembly Folder**，并将新文件夹命名为 `PlayModeTests`。最终应得到 `Assets/Tests/PlayModeTests`。
- 打开刚创建的文件夹，在 Test Runner 窗口中点击 **Create Test Script in current folder**。
- 将文件命名为 `SceneSetupTests.cs`。
- 编写你的第一个测试：加载 `Main` 场景后，断言当前时间处于白天。

## 提示

- 如需加载场景，请参考 [UnityEngine.SceneManagement](https://docs.unity3d.com/ScriptReference/SceneManagement.SceneManager.html) 文档。
- 在 `Scenes/Main.unity` 中[查找 GameObject](https://docs.unity3d.com/ScriptReference/GameObject.Find.html) **FX - Day**。

## 解决方案

`SceneSetupTests.cs`

```csharp
using System.Collections;
using System.Collections.Generic;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.SceneManagement;

public class SceneSetupTests
{
    [UnityTest]
    public IEnumerator MainScene_LoadsCorrectlyAndItsDaytime()
    {
        SceneManager.LoadScene("Assets/Scenes/Main.unity", LoadSceneMode.Single);
        yield return null;

        var fxDay = GameObject.Find("FX - Day");

        Assert.IsTrue(fxDay != null, "should find the 'FX - Day' object in the scene");
    }
}
```

---

## 文档导航

- 上一页：[[01-设置LostCrypt]]
- 目录：[[00-测试Lost Crypt]]
- 下一页：[[03-移动角色]]
