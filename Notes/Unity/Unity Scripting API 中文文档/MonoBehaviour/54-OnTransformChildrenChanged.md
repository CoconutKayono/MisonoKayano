> 原文：[MonoBehaviour.OnTransformChildrenChanged](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTransformChildrenChanged.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnTransformChildrenChanged

## 声明

~~~csharp
public void OnTransformChildrenChanged(...);
~~~

## 描述

此 Transform 的子项发生变化时调用。

## 示例

~~~csharp
// Attach this script to any  GameObject  (for example, an empty "Parent" object).
// Assign a UI Text component to the countText field in the Inspector.
// Add or remove children from the  GameObject  at runtime or in the  Editor .

using UnityEngine;
using UnityEngine.UI;

public class ChildrenCounter :  MonoBehaviour 
{
    public Text countText;

    private void Start()
    {
        UpdateChildrenCount();
    }

    // Called by Unity when a child is added or removed
    private void OnTransformChildrenChanged()
    {
        UpdateChildrenCount();
    }

    private void UpdateChildrenCount()
    {
        int childrenCount = transform.childCount;
        if (countText != null)
        {
            countText.text = $"Children: {childrenCount}";
        }
    }
}
~~~

## 相关资源

- [MonoBehaviour.OnTransformParentChanged](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnTransformParentChanged.html)

---

## 文档导航

- 上一页：[[53-OnRenderObject]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[55-OnTransformParentChanged]]






