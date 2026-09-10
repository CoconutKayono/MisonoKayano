# 4. Reach Wand 测试

> 原文：[4. Reach Wand Test](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/reach-wand-test.html)

## 学习目标

对角色的位置和行为执行断言。

## 练习

- 返回之前的 `MovementTest.cs` 文件。
- 编写 `MainScene_CharacterReachesWand` 测试，让角色向右移动，并检查角色是否到达 Wand 所在的位置。

## 提示

- 在场景中查找 `Altar` 和 `Sara Variant` GameObject。你需要测量它们的 Transform 的 X 位置。
- Wand 位置的 X 坐标等于浮点数 `21.080`。主角的 X 坐标是动态的，会随着移动而改变。
- 可以设置超时时间，让测试在未到达 Wand 时失败。

## 解决方案

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using UnityEngine.SceneManagement;

public class MovementTest
{
    private Transform _characterTransform;
    private float _testTimeout = 25.0f;
    private float _wandLocation = 21.080f;

    [UnityTest]
    public IEnumerator MainScene_CharacterReachesWand()
    {
      SceneManager.LoadScene("Assets/Scenes/Main.unity", LoadSceneMode.Single);
      yield return waitForSceneLoad();

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

    private IEnumerator waitForSceneLoad()
    {
        while (SceneManager.GetActiveScene().buildIndex > 0)
        {
            yield return null;
        }
    }
}
```

---

## 文档导航

- 上一页：[[03-移动角色]]
- 目录：[[00-测试Lost Crypt]]
- 下一页：[[05-碰撞测试]]
