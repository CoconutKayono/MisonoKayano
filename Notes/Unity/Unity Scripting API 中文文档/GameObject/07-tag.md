> 原文：[GameObject.tag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-tag.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).tag

## 声明

~~~csharp
public string tag;
~~~

## 描述

分配给 GameObject 的标签。

标签可用于标识 GameObject。使用标签前，必须先在 [Tags and Layers manager](https://docs.unity3d.com/6000.7/Documentation/Manual/class-TagManager.html) 中声明标签。

注意：不要在 [Awake()](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.Awake.html) 或 [OnValidate()](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnValidate.html) 中设置标签。组件之间调用 Awake 的顺序不确定，标签可能在其 Awake 被调用时被覆盖。如果这样做，Unity 会生成警告：SendMessage cannot be called during Awake, CheckConsistency, or OnValidate。

下面的示例将当前 GameObject 的标签设置为 Player，然后实现 MonoBehaviour.OnTriggerEnter，检查与此对象发生碰撞的另一个对象上的 Collider 是否带有 Enemy 标签。

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        gameObject.tag = "Player";
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Enemy")
        {
            Debug.Log("Triggered by Enemy");
        }
    }
}
~~~

相关资源：[GameObject.CompareTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.CompareTag.html)、[MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html)。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
        //Set the tag of this  GameObject  to Player
        gameObject.tag = "Player";
    }

    private void OnTriggerEnter( Collider  other)
    {
        //Check if the collider of the other  GameObject  involved in the collision is tagged "Enemy"
        if (other.tag == "Enemy")
        {
             Debug.Log ("Triggered by Enemy");
        }
    }
}
~~~

## 相关资源

- [GameObject.CompareTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.CompareTag.html)
- [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html)


