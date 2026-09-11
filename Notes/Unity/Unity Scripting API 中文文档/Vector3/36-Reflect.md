> 原文：[Vector3.Reflect](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Reflect.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Reflect

## 声明

~~~csharp
public static Vector3 Reflect(Vector3 inDirection, Vector3 inNormal);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| inDirection | 要在平面中反射的向量。 |
| inNormal | 定义反射平面的法向量。 |

## 返回

Vector3 The reflected vector. It has the same magnitude as inDirection .

## 描述

使向量从由法向量定义的平面反射。

## 示例

~~~csharp
// This example moves a  GameObject  to the reflected position 
// of a second object
//
// To run this example, create two GameObjects at different 
// positions. In the  Editor , assign these GameObjects as the 
// Original and Relflect Object variables. The reflected object
// moves to the reflected position of the original object. 

using UnityEngine;

public class ReflectExample :  MonoBehaviour 
{
    public  Transform  originalObject;
    public  Transform  reflectedObject;

    void  Update ()
    {
        // Makes the reflected object appear opposite of the original object,
        // mirrored in the y-z plane of the world
        reflectedObject.position =  Vector3.Reflect (originalObject.position,  Vector3.right );
    }
}
~~~

---

## 文档导航

- 上一页：[[35-ProjectOnPlane]]
- 目录：[[00-Vector3]]
- 下一页：[[37-RotateTowards]]


