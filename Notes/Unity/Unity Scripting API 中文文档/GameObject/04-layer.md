> 原文：[GameObject.layer](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-layer.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).layer

## 声明

~~~csharp
public int layer;
~~~

## 描述

标识 GameObject 所分配到的层的整数。

这是标识层的标准整数值，而不是 [LayerMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LayerMask.html)。可以使用层实现摄像机的选择性渲染，或忽略 Raycast。Unity 会生成 32 个层，以 0 到 31 的标准整数表示，并为其自身系统保留其中一些层。有关预定义层以及如何创建新层的信息，请参阅 [在 Unity 中创建功能层](https://docs.unity3d.com/6000.7/Documentation/Manual/create-layers.html)。

要将此 layer 标识符转换为 LayerMask，请参阅[设置 LayerMask](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-set.html)。要从 layer 标识符获取层的 string 名称，请使用 [LayerMask.LayerToName](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LayerMask.LayerToName.html)。有关使用层的完整指南，请参阅手册中的 [Layers](https://docs.unity3d.com/6000.7/Documentation/Manual/Layers.html)。

~~~csharp
// 将 GameObject 放入忽略 Raycast 层（2）。
using UnityEngine;

[ExecuteInEditMode]
public class ExampleClass : MonoBehaviour
{
    void Awake()
    {
        // gameObject.layer 只使用整数，
        // 但可以使用 LayerMask.NameToLayer 将层名称转换为层整数。
        int LayerIgnoreRaycast = LayerMask.NameToLayer("Ignore Raycast");
        gameObject.layer = LayerIgnoreRaycast;
        Debug.Log("Current layer: " + gameObject.layer);
    }
}
~~~

相关资源：[LayerMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LayerMask.html)。

## 示例

~~~csharp
// Put the  GameObject  in the ignore raycast layer (2)

using UnityEngine;

[ ExecuteInEditMode ]
public class ExampleClass :  MonoBehaviour 
{
    void Awake()
    {
        //gameObject.layer uses only integers, but we can turn a layer name into a layer integer using  LayerMask.NameToLayer ()
        int LayerIgnoreRaycast =  LayerMask.NameToLayer ("Ignore Raycast");
        gameObject.layer = LayerIgnoreRaycast;
         Debug.Log ("Current layer: " + gameObject.layer);
    }
}
~~~

## 相关资源

- [LayerMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/LayerMask.html)


