> 原文：[Object.Instantiate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Instantiate.html)

# [Object](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.html).Instantiate

## 声明

~~~csharp
public static Object Instantiate(Object original);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要复制的现有对象。 |

## 返回值

实例化的克隆对象。

## 描述

克隆 original 对象并返回克隆对象。

此方法会复制对象，行为类似于编辑器中的 **Duplicate** 命令。克隆 GameObject 或 Component 时，Unity 还会克隆其所有子对象和组件，并使其属性与原对象一致。克隆 Component 时，Unity 还会克隆该组件所附加到的 GameObject。

此重载不会为克隆对象设置位置、旋转或父级。默认情况下，新对象没有父级，即使 original 有父级也是如此。克隆对象会保留原对象的激活状态；只有在调用时对象在层级中处于激活状态，Unity 才会调用克隆层级中 MonoBehaviour 或 Component 的 Awake 和 OnEnable。

克隆子对象时也会克隆其子对象。若嵌套克隆超过栈大小的一半，Unity 会抛出 InsufficientExecutionStackException。此方法不会创建预制件连接；如需预制件连接，请使用 [PrefabUtility.InstantiatePrefab](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PrefabUtility.InstantiatePrefab.html)。

---

## 声明

~~~csharp
public static Object Instantiate(Object original, Scene scene);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要复制的现有对象。 |
| **scene** | 要将新对象添加到的场景。 |

## 返回值

实例化的克隆对象。

## 描述

克隆 original 对象并将克隆对象添加到指定场景。此重载会将克隆对象添加到指定的已加载场景，而不是活动场景。

---

## 声明

~~~csharp
public static Object Instantiate(Object original, Transform parent);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要复制的现有对象。 |
| **parent** | 要设置为克隆对象父级的 Transform。 |

## 返回值

实例化的克隆对象。

## 描述

克隆 original 对象，并将 parent 设置为克隆对象的父级。此重载设置父级，但不设置位置或旋转；Unity 会将现有对象的位置和旋转作为相对于 parent 的克隆局部位置和旋转。

若要保留原对象的世界位置和旋转，请使用下一个重载，并将 instantiateInWorldSpace 设置为 true。

---

## 声明

~~~csharp
public static Object Instantiate(Object original, Transform parent, bool instantiateInWorldSpace);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要复制的现有对象。 |
| **parent** | 要设置为克隆对象父级的 Transform。 |
| **instantiateInWorldSpace** | 是否让克隆对象保留原对象的世界位置和旋转。 |

## 返回值

实例化的克隆对象。

## 描述

克隆 original 对象，将 parent 设置为克隆对象的父级，并设置克隆对象保留局部位置还是世界位置。

当 instantiateInWorldSpace 为 false 时，Unity 使用现有对象的位置和旋转作为相对于 parent 的局部位置和旋转；为 true 时，Unity 保留现有对象的世界位置和旋转。

---

## 声明

~~~csharp
public static Object Instantiate(Object original, Vector3 position, Quaternion rotation);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要复制的现有对象。 |
| **position** | 新对象在世界空间中的位置。 |
| **rotation** | 新对象的朝向。 |

## 返回值

实例化的克隆对象。

## 描述

克隆 original 对象并设置克隆对象的位置和旋转。Unity 使用指定的 position 和 rotation 作为世界空间中的位置和旋转；新对象没有父级。可以使用此方法在运行时创建发射物或爆炸效果的粒子系统。

---

## 声明

~~~csharp
public static Object Instantiate(Object original, Vector3 position, Quaternion rotation, Transform parent);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要复制的现有对象。 |
| **position** | 新对象在世界空间中的位置。 |
| **rotation** | 新对象的朝向。 |
| **parent** | 要设置为新对象父级的 Transform。 |

## 返回值

实例化的克隆对象。

## 描述

克隆 original 对象，设置克隆对象的位置和旋转，并将 parent 设置为克隆对象的父级。Unity 使用指定的 position 和 rotation 作为世界空间中的位置和旋转，并将 parent 设置为父级。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

克隆 T 类型的对象并返回克隆对象。使用泛型类型可以实例化对象，而不必将结果强制转换为特定类型。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original, InstantiateParameters parameters);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |
| **parameters** | 用于设置克隆对象的 InstantiateParameters。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

使用 parameters 中的设置克隆 T 类型对象，并返回克隆对象。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original, Transform parent);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |
| **parent** | 要设置为克隆对象父级的 Transform。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

克隆 T 类型对象，并将 parent 设置为克隆对象的父级。该重载不设置位置或旋转。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original, Transform parent, bool worldPositionStays);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |
| **parent** | 要设置为克隆对象父级的 Transform。 |
| **worldPositionStays** | 是否让克隆对象保留原对象的世界位置和旋转。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

克隆 T 类型对象，将 parent 设置为克隆对象的父级，并设置克隆对象保留局部位置还是世界位置。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original, Vector3 position, Quaternion rotation);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |
| **position** | 新对象在世界空间中的位置。 |
| **rotation** | 新对象的朝向。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

克隆 T 类型对象并设置克隆对象的位置和旋转。新对象没有父级。

也可以直接克隆脚本实例。Unity 会克隆整个 GameObject 层级并返回克隆后的脚本实例。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original, Vector3 position, Quaternion rotation, InstantiateParameters parameters);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |
| **position** | 新对象在世界空间中的位置。 |
| **rotation** | 新对象的朝向。 |
| **parameters** | 用于设置克隆对象的 InstantiateParameters。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

克隆 T 类型对象，设置克隆对象的位置和旋转，并应用 parameters 中的设置。

---

## 声明

~~~csharp
public static T Instantiate<T>(T original, Vector3 position, Quaternion rotation, Transform parent);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| **original** | 要克隆的 T 类型对象。 |
| **position** | 新对象在世界空间中的位置。 |
| **rotation** | 新对象的朝向。 |
| **parent** | 要设置为克隆对象父级的 Transform。 |

## 返回值

类型为 T 的实例化克隆对象。

## 描述

克隆 T 类型对象，设置克隆对象的位置和旋转，并将 parent 设置为克隆对象的父级。

---

## 示例

### 将预制件实例化为另一个对象的子对象

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    public GameObject prefab;
    public Transform parent;

    void Start()
    {
        Instantiate(prefab, parent);
        Instantiate(prefab, parent, true);
    }
}
~~~

### 实例化 Rigidbody

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    public Rigidbody projectile;

    void Update()
    {
        if (Input.GetButtonDown("Fire1"))
        {
            Rigidbody clone = Instantiate(projectile, transform.position, transform.rotation);
            clone.linearVelocity = transform.TransformDirection(Vector3.forward * 10);
        }
    }
}
~~~

### 实例化多个克隆

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    public GameObject prefab;

    void Start()
    {
        for (var i = 0; i < 10; i++)
            Instantiate(prefab, new Vector3(i * 2.0f, 0, 0), Quaternion.identity);
    }
}
~~~

---

## 相关资源

- [运行时实例化预制件](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs.html)
- [PrefabUtility.InstantiatePrefab](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/PrefabUtility.InstantiatePrefab.html)

---

## 文档导航

- 上一页：[[10-FindObjectsByType]]
- 目录：[[00-Object]]
- 下一页：[[12-InstantiateAsync]]
