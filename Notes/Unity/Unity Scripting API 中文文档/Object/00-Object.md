> 原文：[Object](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.html)

# Object

`UnityEngine.Object` 是 Unity 中所有可引用对象的基类。不要直接继承或实例化此类，应使用适当的子类，例如 `GameObject`、`MonoBehaviour` 或 `ScriptableObject`。

任何派生自 `UnityEngine.Object` 的公共变量，都会在 Inspector 中显示为可拖放的引用字段。许多 API 也使用 `Object` 表示“任意 Unity 对象”，例如 `Resources.LoadAll`、`EditorJsonUtility.ToJson` 和 `SerializedObject`。

每个 `UnityEngine.Object` 实例都与一个原生对象对应。如果原生对象先于托管对象被销毁，或者实例引用了缺失的资源或类型，托管实例可能进入“分离”状态。分离对象仍保留 `InstanceID`，但不能再调用方法或访问属性。Unity 重载的 `==`、`!=` 和 `bool` 会把这类对象与 `null` 比较为 `true`；但 `Object.ReferenceEquals(myObject, null)` 仍返回 `false`。

Unity Object 不支持空条件运算符 `?.` 和空合并运算符 `??`，因为它们不能被重载来识别分离对象。只有在能够保证对象不会处于分离状态时，才可以使用这些运算符。

## 属性

| 本地链接             | API 名       | 中文说明                        |
| ---------------- | ----------- | --------------------------- |
| [[01-hideFlags]] | `hideFlags` | 控制对象是否隐藏、是否随场景保存以及是否可由用户编辑。 |
| [[02-name]]      | `name`      | 对象的名称。                      |

## 公共方法

| 本地链接               | API 名         | 中文说明              |
| ------------------ | ------------- | ----------------- |
| [[03-GetEntityId]] | `GetEntityId` | 获取对象的 `EntityId`。 |
| [[04-GetHashCode]] | `GetHashCode` | 返回对象的哈希码。         |
| [[05-ToString]]    | `ToString`    | 返回对象的名称。          |

## 静态方法

| 本地链接                       | API 名                 | 中文说明                    |
| -------------------------- | --------------------- | ----------------------- |
| [[06-Destroy]]             | `Destroy`             | 移除 `GameObject`、组件或资源。  |
| [[07-DestroyImmediate]]    | `DestroyImmediate`    | 立即销毁指定对象；仅应谨慎地在编辑模式中使用。 |
| [[08-DontDestroyOnLoad]]   | `DontDestroyOnLoad`   | 加载新场景时不销毁目标对象。          |
| [[09-FindAnyObjectByType]] | `FindAnyObjectByType` | 获取任意已加载的活动 `T` 类型对象。    |
| [[10-FindObjectsByType]]   | `FindObjectsByType`   | 获取指定类型的所有已加载对象。         |
| [[11-Instantiate]]         | `Instantiate`         | 克隆 `original` 并返回克隆对象。  |
| [[12-InstantiateAsync]]    | `InstantiateAsync`    | 创建异步实例化操作，获得相关对象的副本。    |

## 运算符

| 本地链接               | API 名         | 中文说明              |
| ------------------ | ------------- | ----------------- |
| [[13-bool]]        | `bool`        | 判断对象是否存在。         |
| [[14-operator-ne]] | `operator !=` | 比较两个对象是否引用不同对象。   |
| [[15-operator-eq]] | `operator ==` | 比较两个对象引用是否指向同一对象。 |

---

## 文档导航

- 上一页：无
- 目录：[[00-Object]]
- 下一页：无
