> 原文：[Vector3.operator !=](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3-operator_ne.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).operator !=

## 声明

~~~csharp
public static bool operator !=(Vector3 lhs, Vector3 rhs);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| lhs | 要比较的第一个向量。 |
| rhs | 要比较的第二个向量。 |

## 描述

如果向量不同，则返回 true。

## 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  Transform  other;

    void Example()
    {
        if (other && transform.position != other.position)
        {
            print("I'm at the different place than the other transform!");
        }
    }
}
~~~

---

## 文档导航

- 上一页：[[44-operator_subtract]]
- 目录：[[00-Vector3]]
- 下一页：[[46-operator_multiply]]



