> 原文：[ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html)

# ScriptableObject

- 命名空间：`UnityEngine`
- 继承自：[`Object`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.html)

## 描述

可以继承此类来创建独立于 `GameObject` 存在的对象。

使用 `ScriptableObject` 可以集中管理数据，使场景和项目中的资源能够方便地访问这些数据。

使用 [`CreateInstance`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.CreateInstance.html) 实例化 `ScriptableObject`。可以通过 Editor UI 中的 [`CreateAssetMenuAttribute`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CreateAssetMenuAttribute.html) 创建资源文件，也可以在脚本中调用 [`AssetDatabase.CreateAsset`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetDatabase.CreateAsset.html) 保存资源。还可以通过 [`ScriptedImporter`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetImporters.ScriptedImporter.html) 生成 `ScriptableObject`，参阅 [`AssetImportContext.AddObjectToAsset`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetImporters.AssetImportContext.AddObjectToAsset.html)。

如果 `ScriptableObject` 尚未保存为资源，但场景中的对象引用了它，Unity 会直接将它序列化到场景文件中。对于项目中只有一个持久实例且仅在编辑模式使用的 `ScriptableObject`，可以使用 [`ScriptableSingleton<T0>`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableSingleton_1.html) 基类。运行时单例 `ScriptableObject` 则必须自行实现单例模式，并手动管理资源的创建和加载。

之前保存的对象可以通过 [`AssetDatabase`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetDatabase.html) 访问，例如 [`AssetDatabase.LoadAssetAtPath`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetDatabase.LoadAssetAtPath.html)。当 `MonoBehaviour` 的字段引用 `ScriptableObject` 时，Unity 会自动加载该对象，因此脚本可以直接使用字段值访问它。

`ScriptableObject` 的 C# 字段与 `MonoBehaviour` 字段采用相同的序列化方式，详情参阅 [脚本序列化](https://docs.unity3d.com/6000.7/Documentation/Manual/script-serialization.html)。包含大型数组或其他大型数据的类应使用 [`PreferBinarySerialization`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PreferBinarySerialization.html)，因为 YAML 并不是这类数据的高效表示方式。

对 `ScriptableObject` 调用 `Destroy` 会释放与其关联的原生资源，但对象会一直留在内存中，直到被垃圾回收。处于这种分离状态的对象看起来像 `null`，但实际上并不是真正的 `null`。此类不支持空条件运算符 `?.` 或空合并运算符 `??`。

下面的示例展示一种典型用法：从 `ScriptableObject` 派生 `VehicleTypeInfo`，在字段中保存不同车辆类型的参数。每种车辆类型都有自己的资源文件，并设置相应参数；游戏中的每辆车只引用对应类型的资源，而不保存重复的参数副本。这样可以在一个集中位置调整车辆行为，也有利于性能，尤其是在共享数据量较大时。

第一个脚本实现派生自 `ScriptableObject` 的类：

```csharp
using UnityEngine;

[CreateAssetMenu]
public class VehicleTypeInfo : ScriptableObject
{
    // 表示特定车辆类型的类
    [Range(0.1f, 100f)]
    public float m_MaxSpeed = 0.1f;

    [Range(0.1f, 10f)]
    public float m_MaxAcceration = 0.1f;

    // 还可以包含其他车辆参数，例如转弯半径、范围、伤害等
}
```

第二个脚本实现使用该 `ScriptableObject` 的 `MonoBehaviour`：

```csharp
using UnityEngine;
using UnityEditor;

public class VehicleInstance : MonoBehaviour
{
    [Range(0f, 200f)]
    public float m_CurrentSpeed;

    [Range(0f, 50f)]
    public float m_Acceleration;

    // 对 ScriptableObject 资源的引用
    public VehicleTypeInfo m_VehicleType;

    public void Initialize(VehicleTypeInfo vehicleType)
    {
        m_VehicleType = vehicleType;
        m_CurrentSpeed = 0f;
        m_Acceleration = Random.Range(0.05f, m_VehicleType.m_MaxAcceration);
    }

    void Update()
    {
        m_CurrentSpeed += m_Acceleration * Time.deltaTime;

        // 使用 ScriptableObject 中的参数控制车辆行为
        if (m_VehicleType && m_VehicleType.m_MaxSpeed < m_CurrentSpeed)
            m_CurrentSpeed = m_VehicleType.m_MaxSpeed;

        gameObject.transform.position += gameObject.transform.forward * Time.deltaTime * m_CurrentSpeed;
    }
}
```

下面的编辑器脚本以编程方式创建资源并在当前场景中创建示例车辆：

```csharp
using UnityEngine;
using UnityEditor;

public class ScriptableObjectVehicleExample
{
    [MenuItem("Example/Setup ScriptableObject Vehicle Example")]
    static void MenuCallback()
    {
        VehicleTypeInfo wagon = AssetDatabase.LoadAssetAtPath<VehicleTypeInfo>("Assets/VehicleTypeWagon.asset");
        if (wagon == null)
        {
            wagon = ScriptableObject.CreateInstance<VehicleTypeInfo>();
            wagon.m_MaxSpeed = 5f;
            wagon.m_MaxAcceration = 0.5f;
            AssetDatabase.CreateAsset(wagon, "Assets/VehicleTypeWagon.asset");
        }

        VehicleTypeInfo cruiser = AssetDatabase.LoadAssetAtPath<VehicleTypeInfo>("Assets/VehicleTypeCruiser.asset");
        if (cruiser == null)
        {
            cruiser = ScriptableObject.CreateInstance<VehicleTypeInfo>();
            cruiser.m_MaxSpeed = 75f;
            cruiser.m_MaxAcceration = 2f;
            AssetDatabase.CreateAsset(cruiser, "Assets/VehicleTypeCruiser.asset");
        }

        {
            var vehicle = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            vehicle.name = "Wagon1";
            var vehicleBehaviour = vehicle.AddComponent<VehicleInstance>();
            vehicleBehaviour.Initialize(wagon);
        }

        {
            var vehicle = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            vehicle.name = "Wagon2";
            var vehicleBehaviour = vehicle.AddComponent<VehicleInstance>();
            vehicleBehaviour.Initialize(wagon);
        }

        {
            var vehicle = GameObject.CreatePrimitive(PrimitiveType.Cube);
            vehicle.name = "Cruiser1";
            var vehicleBehaviour = vehicle.AddComponent<VehicleInstance>();
            vehicleBehaviour.Initialize(cruiser);
        }
    }
}
```

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-CreateInstance]] | `CreateInstance` | 创建脚本化对象的实例。 |

## 消息

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[02-Awake]] | `Awake` | 创建 `ScriptableObject` 实例时调用。 |
| [[03-OnDestroy]] | `OnDestroy` | 脚本化对象即将销毁时调用。 |
| [[04-OnDisable]] | `OnDisable` | 脚本化对象离开作用域时调用。 |
| [[05-OnEnable]] | `OnEnable` | 对象加载时调用。 |
| [[06-OnValidate]] | `OnValidate` | 脚本加载或 Inspector 中的值发生变化时由 Unity 在编辑器中调用。 |
| [[07-Reset]] | `Reset` | 重置为默认值。 |

## 继承成员

### 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/01-hideFlags]] | `hideFlags` | 控制对象是否隐藏、是否随场景保存以及用户是否可以编辑对象。 |
| [[../Object/02-name]] | `name` | 对象的名称。 |

### 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/03-GetEntityId]] | `GetEntityId` | 获取对象的 EntityId。 |
| [[../Object/04-GetHashCode]] | `GetHashCode` | 返回对象的哈希代码。 |
| [[../Object/05-ToString]] | `ToString` | 返回对象的名称。 |

### 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/06-Destroy]] | `Destroy` | 移除 GameObject、组件或资源。 |
| [[../Object/07-DestroyImmediate]] | `DestroyImmediate` | 立即销毁指定对象；仅应谨慎地在编辑模式下使用。 |
| [[../Object/08-DontDestroyOnLoad]] | `DontDestroyOnLoad` | 加载新场景时不销毁目标对象。 |
| [[../Object/09-FindAnyObjectByType]] | `FindAnyObjectByType` | 获取任意一个处于活动状态的已加载 `T` 类型对象。 |
| [[../Object/10-FindObjectsByType]] | `FindObjectsByType` | 获取所有已加载的指定类型对象的列表。 |
| [[../Object/11-Instantiate]] | `Instantiate` | 克隆原对象并返回克隆对象。 |
| [[../Object/12-InstantiateAsync]] | `InstantiateAsync` | 捕获与其他 GameObject 相关的原对象快照，并获取结果对象的 `AsyncInstantiateOperation` 实例。 |

### 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/13-bool]] | `bool` | 判断对象是否存在。 |
| [[../Object/14-operator-ne]] | `operator !=` | 比较两个对象是否引用不同对象。 |
| [[../Object/15-operator-eq]] | `operator ==` | 比较两个对象引用是否指向同一个对象。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-ScriptableObject]]
- 下一页：[[01-CreateInstance]]
