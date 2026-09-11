> 原文：[GameObject.SetGameObjectsActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetGameObjectsActive.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).SetGameObjectsActive

## 声明

~~~csharp
public static void SetGameObjectsActive(NativeArray<int> instanceIDs, bool active);
~~~

## 声明

~~~csharp
public static void SetGameObjectsActive(ReadOnlySpan<int> instanceIDs, bool active);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| instanceIDs | 要激活或停用的 GameObject 实例 ID。 |
| active | 要设置的激活状态；true 将 GameObject 设为激活，false 将其设为未激活。 |

## 描述

激活或停用由实例 ID 标识的多个 GameObject。

## 示例

~~~csharp
using  System ;
using Unity.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

//Add this script to a  GameObject . This example requires the  Input   System  package.

public class DeactivateGOComponent :  MonoBehaviour 
{
public  GameObject  prefab;
public int count = 100;

    NativeArray<int> m_SpawnedInstanceIDsNative;
    int[] m_SpawnedInstanceIDs;
    
    bool m_SetActive = false;
    bool m_UseSlowMethod = false;
    
    void Start()
    {
        m_SpawnedInstanceIDs = new int[count];
        
        //Spawn some prefabs 
        for (int i = 0; i < count; i++)
        {
            //Save their instanceID
            m_SpawnedInstanceIDs[i] = Instantiate(prefab).GetInstanceID();
        }
        
        //Create native array with instanceIDs
        m_SpawnedInstanceIDsNative = new NativeArray<int>(m_SpawnedInstanceIDs,  Allocator.Persistent );
        
    }

    void  Update ()
    {
        if (Keyboard.current[Key.A].wasPressedThisFrame)
        {
            if (m_UseSlowMethod)
            {
                SetActiveSlow(m_SetActive);
            }
            else
            {
                SetActiveFast(m_SpawnedInstanceIDsNative, m_SetActive);
                
            }
            m_SetActive = !m_SetActive; 
        }
    }
    
    void SetActiveSlow(bool setActive)
    {
        foreach(int id in m_SpawnedInstanceIDs)
        {
            (( GameObject ) Resources.InstanceIDToObject (id)).SetActive(setActive);
        }
    }
    
    static void SetActiveFast(NativeArray<int> ids, bool setActive)
    {
         GameObject.SetGameObjectsActive (ids, setActive);
    }

    void OnDestroy()
    {
        m_SpawnedInstanceIDsNative.Dispose();
    }
}
~~~

## 相关资源

- [GameObject.SetActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetActive.html)
- [GameObject.InstantiateGameObjects](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.InstantiateGameObjects.html)

