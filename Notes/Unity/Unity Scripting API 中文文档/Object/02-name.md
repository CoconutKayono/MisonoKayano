> 原文：[Object.name](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-name.html)

# Object.name

```csharp
public string name;
```

## 描述

对象的名称。

组件与 `GameObject` 以及所有附加组件共享同一个名称。如果某个类继承自 `MonoBehaviour`，它会从 `MonoBehaviour` 继承 `name` 字段；如果该类还附加到 `GameObject`，这个字段就是该 `GameObject` 的名称。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    public GameObject exampleOne;
    public GameObject exampleTwo;
    public GameObject exampleThree;

    void Start()
    {
        // 设置三个 GameObject 的名称。
        exampleOne.name = "Ben";
        exampleTwo.name = "Ryan";
        exampleThree.name = "Oscar";

        Debug.Log("The names of these three objects are " +
            exampleOne.name + exampleTwo.name + exampleThree.name);
    }
}
```

---

## 文档导航

- 上一页：[[01-hideFlags]]
- 目录：[[00-Object]]
- 下一页：[[03-GetEntityId]]
