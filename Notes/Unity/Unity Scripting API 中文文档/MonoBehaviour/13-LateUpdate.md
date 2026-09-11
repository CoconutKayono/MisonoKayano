> 原文：[MonoBehaviour.LateUpdate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.LateUpdate.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).LateUpdate

## 声明

~~~csharp
public void LateUpdate(...);
~~~

## 描述

如果 Behaviour 已启用，则每帧调用一次。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    void LateUpdate()
    {
        transform.Translate(0,  Time.deltaTime , 0);
    }
}
~~~

---

## 文档导航

- 上一页：[[12-IsInvoking]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[14-OnAnimatorIK]]



