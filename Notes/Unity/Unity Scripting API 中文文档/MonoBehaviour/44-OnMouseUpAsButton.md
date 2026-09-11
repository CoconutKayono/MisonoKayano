> 原文：[MonoBehaviour.OnMouseUpAsButton](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseUpAsButton.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnMouseUpAsButton

## 声明

~~~csharp
public void OnMouseUpAsButton(...);
~~~

## 描述

用户在同一个 Collider 上按下并释放鼠标按钮时调用。

## 示例

~~~csharp
// Loads the level named "SomeLevel" as a response
// to the user clicking on the object

using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    void OnMouseUpAsButton()
    {
         Application.LoadLevel ("SomeLevel");
    }
}
~~~

## 相关资源

- [OnMouseUp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnMouseUp.html)

---

## 文档导航

- 上一页：[[43-OnMouseUp]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[45-OnParticleCollision]]






