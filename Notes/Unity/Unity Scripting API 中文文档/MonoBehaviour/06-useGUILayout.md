> 原文：[MonoBehaviour.useGUILayout](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour-useGUILayout.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).useGUILayout

## 声明

~~~csharp
public bool useGUILayout;
~~~

## 描述

指定是否为此 MonoBehaviour 添加额外的 GUI 布局阶段。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public void Start()
    {
        //Disabling this lets you skip the  GUI  layout phase.
        useGUILayout = false;
    }
}
~~~

---

## 文档导航

- 上一页：[[05-runInEditMode]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[07-Awake]]



