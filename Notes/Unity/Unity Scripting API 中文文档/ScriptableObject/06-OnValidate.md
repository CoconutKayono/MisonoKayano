> 原文：[ScriptableObject.OnValidate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.OnValidate.html)

# [ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html).OnValidate

## 描述

这是一个仅限编辑器的函数。当脚本加载或 Inspector 中的值发生变化时，Unity 会调用它。

`OnValidate` 通常用于 Inspector 中的值发生变化后执行操作，例如确保数据保持在某个范围内。

在 `OnValidate` 中执行以下操作不受支持，并且可能导致应用程序出错：

- 修改另一个脚本中的值。
- 调用 `ScriptableSingleton.Save`。
- 执行摄像机渲染操作。安全的替代方式是向 `EditorApplication.update` 添加监听器，并在下一次 Editor Update 调用期间执行渲染。

---

## 文档导航

- 上一页：[[05-OnEnable]]
- 目录：[[00-ScriptableObject]]
- 下一页：[[07-Reset]]
