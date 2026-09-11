> 原文：[GameObject.InstantiateGameObjects](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.InstantiateGameObjects.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).InstantiateGameObjects

## 声明

~~~csharp
public static void InstantiateGameObjects(
    EntityId sourceEntityId,
    int count,
    NativeArray<EntityId> newInstanceIDs,
    NativeArray<EntityId> newTransformInstanceIDs,
    Scene destinationScene = default);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| sourceEntityId | 要创建其他实例的 GameObject 的 EntityId。 |
| count | 要创建的 GameObject 实例数量。 |
| newInstanceIDs | 用于填充新 GameObject EntityId 的预分配 NativeArray；大小必须与 count 相同。 |
| newTransformInstanceIDs | 用于填充新 GameObject 的 Transform EntityId 的预分配 NativeArray；大小必须与 count 相同。 |
| destinationScene | 放置实例化 GameObject 的 Scene。如果为 default，则将 GameObject 添加到当前活动 Scene。 |

## 描述

创建指定数量的 GameObject 实例，并将新 GameObject 及其 Transform 组件的 EntityId 填充到 NativeArray 中。

使用 InstantiateGameObjects 可以批量实例化多个 GameObject。可以使用 [Resources.EntityIdToObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Resources.EntityIdToObject.html) 将 EntityId 解析为对象。

## 示例

~~~csharp
using  System ;
using Unity.Collections;
using UnityEngine;

public class InstantiateEntityId :  MonoBehaviour 
{
public  GameObject  prefab;
public int count = 100;

     EntityId  m_EntityId;
    NativeArray< EntityId > m_EntityIds;
    NativeArray< EntityId > m_TransformIds;
    
    void Start()
    {
        m_EntityId = prefab.GetEntityId();
        m_EntityIds = new NativeArray< EntityId >(count,  Allocator.Persistent );
        m_TransformIds = new NativeArray< EntityId >(count,  Allocator.Persistent );

         GameObject.InstantiateGameObjects (m_EntityId, count, m_EntityIds,m_TransformIds );
    }

    void OnDestroy()
    {
        m_EntityIds.Dispose();
        m_TransformIds.Dispose();
    }
}
~~~

## 相关资源

- [GameObject.SetGameObjectsActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetGameObjectsActive.html)
- [Resources.InstanceIDToObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Resources.InstanceIDToObject.html)


