> 原文：[HideFlags.DontSave](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/HideFlags.DontSave.html)

# HideFlags.DontSave

## 描述

对象不会保存到场景，也不会在加载新场景时销毁。它是以下标志的快捷组合：

```csharp
HideFlags.DontSaveInBuild |
HideFlags.DontSaveInEditor |
HideFlags.DontUnloadUnusedAsset
```

必须使用 `DestroyImmediate` 手动从内存中清除对象，以避免内存泄漏。

对于场景中的 Prefab 实例，可以在 Prefab 实例句柄对象上设置此 hide flag，从而为 Prefab 实例中的所有对象设置相同的 hide flag。另请参阅 `PrefabUtility.GetPrefabInstanceHandle`。

---

## 文档导航

- 上一页：[[07-DontUnloadUnusedAsset]]
- 目录：[[00-HideFlags]]
- 下一页：[[09-HideAndDontSave]]
