> 原文：[MonoBehaviour.OnBecameVisible](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnBecameVisible.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnBecameVisible

## 声明

~~~csharp
public void OnBecameVisible(...);
~~~

## 描述

当 Renderer 被摄像机看到时调用。

## 示例

~~~csharp
// Enables the behaviour when it is visible

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void OnBecameVisible()
    {
        enabled = true;
    }
}
~~~

---

## 文档导航

- 上一页：[[20-OnBecameInvisible]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[22-OnChildRectTransformDimensionsChange]]





