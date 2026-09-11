> 原文：[HideFlags.HideAndDontSave](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/HideFlags.HideAndDontSave.html)

# HideFlags.HideAndDontSave

## 描述

`GameObject` 不显示在 Hierarchy 中、不保存到场景，也不会被 `Resources.UnloadUnusedAssets` 卸载。

此标志最常用于由脚本创建、完全由脚本控制的 `GameObject`。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    // 创建一个由此组件显式创建和销毁的 Material。
    // Resources.UnloadUnusedAssets 不会卸载它，Inspector 也无法编辑它。
    private Material ownedMaterial;

    void OnEnable()
    {
        ownedMaterial = new Material(Shader.Find("Diffuse"));
        ownedMaterial.hideFlags = HideFlags.HideAndDontSave;
        GetComponent<Renderer>().sharedMaterial = ownedMaterial;
    }

    // HideAndDontSave 对象必须由所有者显式销毁。
    void OnDisable()
    {
        DestroyImmediate(ownedMaterial);
    }
}
```

---

## 文档导航

- 上一页：[[08-DontSave]]
- 目录：[[00-HideFlags]]
- 下一页：无
