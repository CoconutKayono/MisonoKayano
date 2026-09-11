> 原文：[HideFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/HideFlags.html)

# HideFlags

`HideFlags` 是控制对象销毁、保存以及在 Inspector 中可见性的位掩码。

如果将 `HideFlags` 设置为 `DontSaveInEditor`、`DontSaveInBuild` 或 `HideInHierarchy`，对象会从场景及其当前物理场景中被 Unity 内部移除，包括 2D 和 3D 物理场景。对象也会触发 `OnDisable` 和 `OnEnable` 调用。

可以使用这些标志控制尚未通过 `AssetDatabase` 保存到项目中的实例化资源（例如 `ScriptableObject` 和 `Material`）是否序列化到场景中。

## 枚举值

| 本地链接                         | API 名                   | 中文说明                                                                         |
| ---------------------------- | ----------------------- | ---------------------------------------------------------------------------- |
| [[01-None]]                  | `None`                  | 普通且可见的对象。这是默认值。                                                              |
| [[02-HideInHierarchy]]       | `HideInHierarchy`       | 对象不会出现在 Hierarchy 中。                                                         |
| [[03-HideInInspector]]       | `HideInInspector`       | 无法在 Inspector 中查看对象。                                                         |
| [[04-DontSaveInEditor]]      | `DontSaveInEditor`      | 对象不会在编辑器中保存到场景。                                                              |
| [[05-NotEditable]]           | `NotEditable`           | 对象无法在 Inspector 中编辑。                                                         |
| [[06-DontSaveInBuild]]       | `DontSaveInBuild`       | 构建 Player 时不会保存对象。                                                           |
| [[07-DontUnloadUnusedAsset]] | `DontUnloadUnusedAsset` | `Resources.UnloadUnusedAssets` 不会卸载对象。                                       |
| [[08-DontSave]]              | `DontSave`              | 对象不会保存到场景，也不会在加载新场景时销毁。                                                      |
| [[09-HideAndDontSave]]       | `HideAndDontSave`       | `GameObject` 不显示在 Hierarchy 中、不保存到场景，也不会被 `Resources.UnloadUnusedAssets` 卸载。 |

```csharp
using UnityEngine;

public class ExampleClass : MonoBehaviour
{
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

另请参阅：[[../Object/01-hideFlags]]。

---

## 文档导航

- 上一页：无
- 目录：[[00-HideFlags]]
- 下一页：[[01-None]]
