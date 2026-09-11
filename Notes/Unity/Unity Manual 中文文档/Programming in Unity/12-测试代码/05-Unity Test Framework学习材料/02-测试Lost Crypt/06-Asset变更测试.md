# 6. Asset 变更测试

> 原文：[6. Asset Change Test](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/asset-change-test.html)

## 学习目标

学习一种常见的 Game Tests 模式，用于验证 Asset 是否随时间发生变化。

## 练习

如你在 LostCrypt 中看到的那样，拾取 Wand 后，角色会装备护甲。

编写一个测试，检查 Sara 拾取 Wand 后是否装备了护甲。

- 创建 `WandTests.cs` 类，并实现 `MainScene_CharacterReachesWandAndEquipsArmor` 测试。
- 尝试观察 `Sara Variant`，或者更具体地说，观察 `puppet_sara` GameObject 在拾取 Wand 的瞬间发生了什么变化。

## 提示

- 可以复用 [[04-Reach Wand测试]] 中的代码，实现角色拾取 Wand 的逻辑；也可以尝试通过代码触发这个动作。
- 记住，如果测试无法访问某些 Unity 内部 API，可能需要在 `PlayModeTests` assembly definition 中添加新的引用。

## 解决方案

`PlayModeTests.asmdef`

```json
{
    "name": "PlayModeTests",
    "rootNamespace": "",
    "references": [
        "Unity.InputSystem",
        "Unity.InputSystem.TestFramework",
        "TestInputControl",
        "UnityEngine.TestRunner",
        "Unity.2D.Animation.Runtime"
    ],
    "includePlatforms": [],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "autoReferenced": false,
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ],
    "versionDefines": [],
    "noEngineReferences": false
}
```

`WandTests.cs`

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.SceneManagement;
using UnityEngine.Experimental.U2D.Animation;

public class WandTests
{
    private Transform _characterTransform;
    private float _testTimeout = 25.0f;
    private float _wandLocation = 21.080f;

    [UnityTest]
    public IEnumerator MainScene_CharacterReachesWandAndEquipsArmor()
    {
        SceneManager.LoadScene("Assets/Scenes/Main.unity", LoadSceneMode.Single);
        // Skip first frame so Sara have a chance to appear on the screen
        yield return null;
        var puppet = GameObject.Find("puppet_sara");
        var spriteLibrary = puppet.GetComponent<SpriteLibrary>();
        Assert.AreEqual(spriteLibrary.spriteLibraryAsset.name, "Sara");

        var elapsedTime = 0.0f;
        yield return GoRight();
        while (GetCurrentCharacterPosition() <= _wandLocation)
        {
            yield return null;
            elapsedTime += Time.deltaTime;
            if (elapsedTime > _testTimeout)
            {
                Assert.Fail($"Character did not reach location position in {_testTimeout} seconds.");
            }
        }

        // Wait for Wand pickup animation to be over.
        yield return new WaitForSeconds(12);

        Assert.AreEqual(spriteLibrary.spriteLibraryAsset.name, "Sara_var01");
    }

    private float GetCurrentCharacterPosition()
    {
        // Get Main character's Transform which is used to manipulate position.
        if (_characterTransform == null)
        {
            _characterTransform = GameObject.Find("Sara Variant").transform;
        }

        return _characterTransform.position.x;
    }

    private IEnumerator GoRight()
    {
        TestInputControl.MoveLeft = false;
        yield return null;
        TestInputControl.MoveRight = true;
    }
}
```

---

## 文档导航

- 上一页：[[05-碰撞测试]]
- 目录：[[00-测试Lost Crypt]]
- 下一页：[[07-Scene验证测试]]
