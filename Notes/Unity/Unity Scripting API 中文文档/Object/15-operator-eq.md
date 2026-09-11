> 原文：[Object.operator ==](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_eq.html)

# Object.operator ==

```csharp
public static bool operator ==(Object x, Object y);
```

## 参数

| 参数 | 说明 |
| --- | --- |
| `x` | 第一个对象。 |
| `y` | 要与第一个对象比较的对象。 |

## 描述

比较两个对象引用是否指向同一对象。与 `Object.ReferenceEquals` 或标准 C# 的 `==` 不同，Unity 的实现还会检查底层原生对象指针；只要托管引用或原生指针为空，`object == null` 就会得到 `true`。这也是对象处于分离状态时的行为来源。

```csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    public Collider target;

    void OnTriggerEnter(Collider trigger)
    {
        if (trigger == target)
            print("We hit the target trigger");
    }

    void Update()
    {
        // 目标被销毁时提前返回。
        if (target == null)
            return;
    }
}
```

---

## 文档导航

- 上一页：[[14-operator-ne]]
- 目录：[[00-Object]]
- 下一页：无
