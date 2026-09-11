> 原文：[MonoBehaviour.OnTransformParentChanged](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTransformParentChanged.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTransformParentChanged

## 声明

~~~csharp
public void OnTransformParentChanged(...);
~~~

## 描述

此 Transform 的父项发生变化时调用。

## 示例

~~~csharp
// Attach this script to any  GameObject  (for example, an empty "Parent" object).
// Assign a Text UI element to the infoText field in the Inspector (optional, for UI feedback).
// At runtime, change the object's parent in the hierarchy (via script or by dragging in the  Editor ).
// You'll see a log message, and the UI text will update whenever the parent changes.

using UnityEngine;
using UnityEngine.UI; // For UI Text

public class ParentChangeWatcher :  MonoBehaviour 
{
    public Text infoText; // Assign in inspector

    void Start()
    {
        UpdateInfoText();
    }

    // Called automatically by Unity when the parent changes
    void OnTransformParentChanged()
    {
         Debug.Log ($"{gameObject.name} parent changed to: {transform.parent?.name ?? "None"}");
        UpdateInfoText();
    }

    void UpdateInfoText()
    {
        if (infoText != null)
        {
            string parentName = transform.parent ? transform.parent.name : "None";
            infoText.text = $"{gameObject.name} is now child of: {parentName}";
        }
    }
}
~~~

## 相关资源

- [MonoBehaviour.OnTransformChildrenChanged](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTransformChildrenChanged.html)

---

## 文档导航

- 上一页：[[54-OnTransformChildrenChanged]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[56-OnTriggerEnter]]






