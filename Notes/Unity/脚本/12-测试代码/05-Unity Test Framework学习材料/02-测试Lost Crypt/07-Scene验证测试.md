# 7. Scene 验证测试

> 原文：[7. Scene Validation Test](https://docs.unity3d.com/6000.7/Documentation/Manual/test-framework/course/LostCrypt/scene-validation-test.html)

## 学习目标

测试场景中是否存在 Sara 和 Wand GameObject。使用 Test Framework 的功能，让这个测试将所有场景作为 fixtures。

## 练习

- 创建 `ValidationTest.cs` 文件，其中包含一个 namespace 和两个类：`SceneValidationTests`、`GameplayScenesProvider`。
- 在测试类中创建 `SaraAndWandArePresent` 测试，检查 `Sara Variant` 和 `Wand` GameObject 不为 null。
- 在 fixture 类 `GameplayScenesProvider` 中实现 `IEnumerable<string>`，并在生成器方法中从 `EditorBuildSettings.scenes` 产生所有场景。
- 在 `SceneValidationTests` 类上使用 `TestFixture` 和 `TestFixtureSource` annotations。
- 创建一个新的空场景，并将其添加到 `EditorBuildSettings`，以验证测试是否会动态创建。

## 提示

- `TestFixture` 和 `TestFixtureSource` NUnit annotations 要求测试类必须位于 Namespace 内。相关信息请参阅 [NUnit TestFixtureSource](https://docs.nunit.org/articles/nunit/writing-tests/attributes/testfixturesource.html) 文档。
- `EditorBuildSettings.scenes` 的详细信息请参阅 [EditorBuildSettings.scenes](https://docs.unity3d.com/ScriptReference/EditorBuildSettings-scenes.html) 文档。
- 要将场景添加到 `EditorBuildSettings`，需要创建一个新场景，然后前往 **File > Build Settings** 将其添加进去。

## 解决方案

`ValidationTests.cs`

```csharp
using System.Collections;
using System.Collections.Generic;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace ValidationTests
{
    [TestFixture]
    [TestFixtureSource(typeof(GameplayScenesProvider))]
    public class SceneValidationTests
    {
        private readonly string _scenePath;

        public SceneValidationTests(string scenePath)
        {
            _scenePath = scenePath;
        }

        [OneTimeSetUp]
        public void LoadScene()
        {
            SceneManager.LoadScene(_scenePath);
        }

        [UnityTest]
        public IEnumerator SaraAndWandArePresent()
        {
            yield return waitForSceneLoad();
            var wand = GameObject.Find("Wand");
            var sara = GameObject.Find("Sara Variant");

            Assert.NotNull(wand, "Wand object exists");
            Assert.NotNull(sara, "Sara object exists");
        }

        IEnumerator waitForSceneLoad()
        {
            while (!SceneManager.GetActiveScene().isLoaded)
            {
                yield return null;
            }
        }
    }

    public class GameplayScenesProvider : IEnumerable
    {
        public IEnumerator GetEnumerator()
        {
            foreach (var scene in EditorBuildSettings.scenes)
            {
                if (!scene.enabled || scene.path == null)
                {
                    continue;
                }

                yield return scene.path;
            }
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }
}
```

---

## 文档导航

- 上一页：[[06-Asset变更测试]]
- 目录：[[00-测试Lost Crypt]]
- 下一页：[[08-性能测试]]
