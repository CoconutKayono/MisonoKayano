> 原文：[Object.bool](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_Object.html)

# Object.bool

## 描述

判断对象是否存在。下面三个示例结果相同：

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        if (GetComponent<Rigidbody>() == true)
            Debug.Log("Rigidbody attached to this transform");
    }
}
```

```csharp
if (GetComponent<Rigidbody>())
    Debug.Log("Rigidbody attached to this transform");
```

```csharp
if (GetComponent<Rigidbody>() != null)
    Debug.Log("Rigidbody attached to this transform");
```

Unity 的 `Object` 具有自定义的存在性判断，会识别底层原生对象是否已经被销毁。相关的空值比较行为请参阅 [[15-operator-eq]]。

---

## 文档导航

- 上一页：[[12-InstantiateAsync]]
- 目录：[[00-Object]]
- 下一页：[[14-operator-ne]]
