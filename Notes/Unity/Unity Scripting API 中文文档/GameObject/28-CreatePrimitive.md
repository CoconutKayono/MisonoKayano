> 原文：[GameObject.CreatePrimitive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.CreatePrimitive.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).CreatePrimitive

## 声明

~~~csharp
public static GameObject CreatePrimitive(PrimitiveType type);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| type | 要创建的原始体类型。 |

## 返回值

使用指定 PrimitiveType 创建的 GameObject。

## 描述

使用指定的 PrimitiveType 创建带有 Mesh Renderer 和适当 Collider 的 GameObject。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    // Create a plane, sphere and cube in the  Scene .

    void Start()
    {
         GameObject  plane  =  GameObject.CreatePrimitive ( PrimitiveType.Plane );

         GameObject  cube =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        cube.transform.position = new  Vector3 (0, 0.5f, 0);

         GameObject  sphere =  GameObject.CreatePrimitive ( PrimitiveType.Sphere );
        sphere.transform.position = new  Vector3 (0, 1.5f, 0);

         GameObject  capsule =  GameObject.CreatePrimitive ( PrimitiveType.Capsule );
        capsule.transform.position = new  Vector3 (2, 1, 0);

         GameObject  cylinder =  GameObject.CreatePrimitive ( PrimitiveType.Cylinder );
        cylinder.transform.position = new  Vector3 (-2, 1, 0);
    }
}
~~~

## 相关资源

- [PrimitiveType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PrimitiveType.html)


