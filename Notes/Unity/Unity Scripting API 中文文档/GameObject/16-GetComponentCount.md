> 原文：[GameObject.GetComponentCount](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentCount.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponentCount

## 声明

~~~csharp
public int GetComponentCount();
~~~

## 返回值

GameObject 上组件的数量，以 Integer 值表示。

## 描述

获取当前附加到 GameObject 的组件总数。

## 示例

~~~csharp
using UnityEngine;

public class IterateComponents :  MonoBehaviour 
{
int m_SavedComponentIndex = -1;

    void Start()
    {
        //Iterate through components  on the  GameObject 
        for (int i = 0; i < gameObject.GetComponentCount(); i++)
        {
            var currComponent = gameObject.GetComponentAtIndex(i);
            
            //Check if it is a  Rigidbody  component
            if (currComponent.GetType() == typeof( Rigidbody ) )
            {
                m_SavedComponentIndex = i;
            }
        }

         Debug.Log (m_SavedComponentIndex != -1 ? $"Found component at index: {m_SavedComponentIndex}" : "Could not find component");
    }
}
~~~

## 相关资源

- [GameObject.GetComponentAtIndex](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentAtIndex.html)


