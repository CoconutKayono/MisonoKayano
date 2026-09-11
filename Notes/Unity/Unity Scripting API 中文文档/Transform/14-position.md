> 原文：[Transform.position](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-position.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).position

public Vector3 position;

#### 描述

Transform 的世界空间位置。

GameObject 的 Transform 的 position 属性可以在 Unity Editor 中访问，也可以通过脚本访问。修改此值可以移动 GameObject，读取此值可以获取 GameObject 在三维世界空间中的位置。

有关位置和轴的更多信息，请参阅 [class-Transform](https://docs.unity3d.com/6000.7/Documentation/Manual/class-Transform.html)。

必须将对象实例化到场景中，位置变化才会使其移动。Prefab 资源仍然是 GameObject，但它们尚未实例化。因此，Unity 不会使用 Prefab 层级根资源的 Transform position 数据。

```csharp
using UnityEngine;

public class ExampleClass : MonoBehaviour
{
    //movement speed in units per second
    private float movementSpeed = 5f;

    void Update()
    {
        //get the Input from Horizontal axis
        float horizontalInput = Input.GetAxis("Horizontal");
        //get the Input from Vertical axis
        float verticalInput = Input.GetAxis("Vertical");

        //update the position
        transform.position = transform.position + new Vector3(horizontalInput * movementSpeed * Time.deltaTime, verticalInput * movementSpeed * Time.deltaTime, 0);

        //output to log the position change
        Debug.Log(transform.position);
    }
}
```

此示例通过读取 Horizontal 和 Vertical 轴的输入，改变位置来上下或左右移动 GameObject。

另一个示例：

```csharp
using UnityEngine;

public class ExampleClass2 : MonoBehaviour
{
    //movement speed in units per second
    private float distance = 5f;
    public GameObject prefabToInstantiate;

    void Start()
    {
        if (prefabToInstantiate != null)
            InstantiateAbove(prefabToInstantiate);
    }

    void InstantiateAbove(GameObject prefab)
    {
        //instantiate above at the given distance
        Vector3 offset = new Vector3(0, distance, 0);
        GameObject.Instantiate(prefab, transform.position + offset, Quaternion.identity);
    }
}
```

此示例使用此脚本在 GameObject 位置上方 5 个单位处实例化给定的 prefab。


