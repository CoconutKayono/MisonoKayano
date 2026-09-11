> 原文：[MonoBehaviour.OnValidate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnValidate.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnValidate

## 声明

~~~csharp
public void OnValidate(...);
~~~

## 描述

脚本加载或 Inspector 中的值发生变化时调用，用于验证数据。

## 示例

~~~csharp
using UnityEngine;

public class Health :  MonoBehaviour 
{
    [ SerializeField ]
    private int maxHealth = 100;

    [ SerializeField ]
    private int currentHealth = 100;

    // Called in editor when values are changed in Inspector
    private void OnValidate()
    {
        // Ensure maxHealth is at least 1
        if (maxHealth < 1)
            maxHealth = 1;

        // Clamp currentHealth between 0 and maxHealth
        currentHealth =  Mathf.Clamp (currentHealth, 0, maxHealth);
    }
}
~~~

## 相关资源

- [EditorApplication.update](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/EditorApplication-update.html)
- [EditorApplication.delayCall](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/EditorApplication-delayCall.html)

---

## 文档导航

- 上一页：[[61-OnTriggerStay2D]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[63-OnWillRenderObject]]






