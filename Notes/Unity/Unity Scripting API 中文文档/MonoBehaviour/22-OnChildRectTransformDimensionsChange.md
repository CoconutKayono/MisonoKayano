> 原文：[MonoBehaviour.OnChildRectTransformDimensionsChange](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnChildRectTransformDimensionsChange.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnChildRectTransformDimensionsChange

## 声明

~~~csharp
public void OnChildRectTransformDimensionsChange(...);
~~~

## 描述

子 RectTransform 的尺寸发生变化时调用。

## 示例

~~~csharp
using UnityEngine;

[ RequireComponent (typeof( RectTransform ))]
public class OnChildRectTransformDimensionsChangeExample :  MonoBehaviour 
{
     RectTransform  rt;

    void OnEnable()
    {
        if (rt == null)
            rt = GetComponent< RectTransform >();

        rt.sendChildDimensionsChange = true;
    }

    void OnDisable()
    {
        rt.sendChildDimensionsChange = false;
    }

    void OnChildRectTransformDimensionsChange()
    {
         Debug.Log ("A child  RectTransform  has changed dimensions.");
    }
}
~~~

---

## 文档导航

- 上一页：[[21-OnBecameVisible]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[23-OnCollisionEnter]]





