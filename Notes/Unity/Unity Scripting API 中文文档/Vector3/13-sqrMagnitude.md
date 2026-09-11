> 原文：[Vector3.sqrMagnitude](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-sqrMagnitude.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).sqrMagnitude

## 声明

~~~csharp
public float sqrMagnitude;
~~~

## 描述

返回此向量长度的平方。（只读）

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    // detects when the other transform is closer than closeDistance
    // this is faster than using  Vector3.magnitude 
    public  Transform  other;
    public float closeDistance = 5.0f;

    void  Update ()
    {
        if (other)
        {
             Vector3  offset = other.position - transform.position;
            float sqrLen = offset.sqrMagnitude;

            // square the distance we compare with
            if (sqrLen < closeDistance * closeDistance)
            {
                print("The other transform is close to me!");
            }
        }
    }
}
~~~

## 相关资源

- [magnitude](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-magnitude.html)

---

## 文档导航

- 上一页：[[12-normalized]]
- 目录：[[00-Vector3]]
- 下一页：[[14-Index_operator]]



