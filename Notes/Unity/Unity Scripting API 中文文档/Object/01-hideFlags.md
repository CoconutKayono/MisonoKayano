> 原文：[Object.hideFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-hideFlags.html)

# Object.hideFlags

```csharp
public HideFlags hideFlags;
```

## 描述

控制对象是否隐藏、是否随场景保存以及是否可由用户编辑。

另请参阅：[[../HideFlags/00-HideFlags]]。

```csharp
using UnityEngine;
using System.Collections;

public class ExampleClass : MonoBehaviour
{
    // 创建一个由此组件显式创建和销毁的材质。
    // Resources.UnloadUnusedAssets 不会卸载它，Inspector 也无法编辑它。
    private Material ownedMaterial;

    void OnEnable()
    {
        ownedMaterial = new Material(Shader.Find("Diffuse"));
        ownedMaterial.hideFlags = HideFlags.HideAndDontSave;
        GetComponent<Renderer>().sharedMaterial = ownedMaterial;
    }

    // 以 hide and don't save 方式创建的对象必须由所有者显式销毁。
    void OnDisable()
    {
        DestroyImmediate(ownedMaterial);
    }
}
```

---

## 文档导航

- 上一页：[[00-Object]]
- 目录：[[00-Object]]
- 下一页：[[02-name]]
