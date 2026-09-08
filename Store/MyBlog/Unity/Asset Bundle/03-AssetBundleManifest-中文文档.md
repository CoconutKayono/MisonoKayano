# AssetBundleManifest 类

继承关系：`object` → `Object` → `AssetBundleManifest`

命名空间：`UnityEngine`

程序集：`Unity.AssetBundleModule.dll`

## 描述

构建所生成的所有 AssetBundle 的清单（Manifest）。

其他资源：[BuildPipeline.BuildAssetBundles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/BuildPipeline.BuildAssetBundles.html)、[AssetBundle.GetAllAssetNames](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.GetAllAssetNames.html)

## 公共方法

| 方法 | 说明 |
| --- | --- |
| [GetAllAssetBundles](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.GetAllAssetBundles.html) | 获取清单中的所有 AssetBundle。 |
| [GetAllAssetBundlesWithVariant](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.GetAllAssetBundlesWithVariant.html) | 获取清单中所有带变体（variant）的 AssetBundle。 |
| [GetAllDependencies](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.GetAllDependencies.html) | 获取给定 AssetBundle 的所有依赖 AssetBundle（包含间接依赖）。 |
| [GetAssetBundleHash](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.GetAssetBundleHash.html) | 获取给定 AssetBundle 的哈希值。 |
| [GetDirectDependencies](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleManifest.GetDirectDependencies.html) | 获取给定 AssetBundle 的直接依赖 AssetBundle。 |

## 继承的成员（来自 Object）

### 属性

| 属性 | 说明 |
| --- | --- |
| [hideFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-hideFlags.html) | 控制对象是否被隐藏、随场景保存以及是否可由用户编辑。 |
| [name](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-name.html) | 对象的名称。 |

### 公共方法

| 方法 | 说明 |
| --- | --- |
| [GetEntityId](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.GetEntityId.html) | 获取对象的 EntityId。 |
| [GetHashCode](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.GetHashCode.html) | 返回对象的哈希码。 |
| [ToString](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.ToString.html) | 返回对象的名称。 |

### 静态方法

| 方法 | 说明 |
| --- | --- |
| [Destroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html) | 移除一个 GameObject、组件或资源。 |
| [DestroyImmediate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DestroyImmediate.html) | 立即销毁指定对象。请谨慎使用，且仅在编辑器模式下使用。 |
| [DontDestroyOnLoad](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DontDestroyOnLoad.html) | 加载新场景时不要销毁目标对象。 |
| [FindAnyObjectByType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.FindAnyObjectByType.html) | 查找当前已加载的任意活动对象（类型 T）。 |
| [FindObjectsByType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.FindObjectsByType.html) | 查找所有已加载的指定类型（Type）对象列表。 |
| [Instantiate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Instantiate.html) | 克隆对象 original，并返回克隆体。 |
| [InstantiateAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.InstantiateAsync.html) | 捕获与另一个 GameObject 相关的原对象（original）快照，并取得所生成对象的 AsyncInstantiateOperation 实例。 |

### 运算符

| 运算符 | 说明 |
| --- | --- |
| [bool](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_Object.html) | 判断对象是否存在。 |
| [operator !=](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_ne.html) | 判断两个对象引用是否指向不同的对象。 |
| [operator ==](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_eq.html) | 判断两个对象引用是否指向同一个对象。 |

---

相关文档：[[00-AssetBundleModule]]、[[01-AssetBundle-中文文档]]、[[02-AssetBundleCreateRequest-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
