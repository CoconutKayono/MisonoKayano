> 原文：[GameObject.activeSelf](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeSelf.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).activeSelf

## 声明

~~~csharp
public bool activeSelf;
~~~

## 描述

GameObject 的本地激活状态。激活时为 true，未激活时为 false。（只读）

此 GameObject 的本地激活状态由 [GameObject.SetActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetActive.html) 设置。本地处于激活状态的 GameObject 仍可能因为父对象未激活而在场景层级中处于未激活状态。如果要检查 GameObject 在场景中是否实际被视为激活，请使用 [GameObject.activeInHierarchy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeInHierarchy.html)。

相关资源：[GameObject.SetActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetActive.html)、[GameObject.activeInHierarchy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeInHierarchy.html)。

## 相关资源

- [GameObject.SetActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetActive.html)
- [GameObject.activeInHierarchy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeInHierarchy.html)

