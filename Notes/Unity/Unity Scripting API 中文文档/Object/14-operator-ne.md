> 原文：[Object.operator !=](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_ne.html)

# Object.operator !=

```csharp
public static bool operator !=(Object x, Object y);
```

## 参数

| 参数 | 说明 |
| --- | --- |
| `x` | 要比较的第一个对象。 |
| `y` | 要与第一个对象比较的对象。 |

## 描述

比较两个对象是否引用不同对象。Unity 对 `Object` 重载了此运算符，因此它会同时考虑托管引用和底层原生对象是否存在；这与标准 C# 引用比较可能不同。

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    Transform target;

    void Update()
    {
        if (target != transform)
            print("Another object");
    }
}
```

---

## 文档导航

- 上一页：[[13-bool]]
- 目录：[[00-Object]]
- 下一页：[[15-operator-eq]]
