> 原文：[Object.ToString](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.ToString.html)

# Object.ToString

```csharp
public string ToString();
```

## 返回值

`string`：`ToString` 返回的名称。

## 描述

返回对象的名称。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    public Text m_Text;

    private void Start()
    {
        // 确认 Inspector 中已分配 Text。
        if (m_Text != null)
            m_Text.text = "GameObject Name : " + gameObject.ToString();
    }
}
```

---

## 文档导航

- 上一页：[[04-GetHashCode]]
- 目录：[[00-Object]]
- 下一页：[[06-Destroy]]
