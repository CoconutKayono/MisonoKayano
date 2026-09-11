> 原文：[GameObject.isStatic](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-isStatic.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).isStatic

## 声明

~~~csharp
public bool isStatic;
~~~

## 描述

如果设置了任意 [StaticEditorFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/StaticEditorFlags.html)，则返回 true；如果没有设置 Static Editor Flags，则返回 false。

设置为 true 可启用所有 Static Editor Flags。设置为 false 可停用所有 Static Editor Flags。

Static Editor Flags 决定 Unity 的哪些系统将 GameObject 视为静态对象，并在 Unity Editor 中将 GameObject 纳入这些系统的预计算。运行时设置 StaticEditorFlags 不会影响这些系统。

更多信息请参阅 [Static Editor Flags](https://docs.unity3d.com/6000.7/Documentation/Manual/StaticObjects.html)。相关资源：[StaticEditorFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/StaticEditorFlags.html)、[GameObjectUtility.SetStaticEditorFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObjectUtility.SetStaticEditorFlags.html)。

## 相关资源

- [StaticEditorFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/StaticEditorFlags.html)
- [GameObjectUtility.SetStaticEditorFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObjectUtility.SetStaticEditorFlags.html)

