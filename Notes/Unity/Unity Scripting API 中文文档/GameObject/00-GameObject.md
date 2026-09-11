> 原文：[GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html)

# GameObject

- 命名空间：UnityEngine
- 继承自：[Object](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.html)

## 描述

所有可以存在于场景中的对象的基类。向 GameObject 添加组件可以控制其外观和行为。

GameObject 是 Unity 中最基本的对象类型。使用 GameObject 表示项目中的所有内容，包括角色、道具和场景。GameObject 充当功能组件的容器，这些组件决定 GameObject 的外观和行为。

任何继承自 [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html) 的脚本都可以作为组件添加到 GameObject。可以在 MonoBehaviour 代码中使用 [Component.gameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component-gameObject.html) 属性访问该组件所附加到的 GameObject。

MonoBehaviour 的事件函数（例如每帧调用的 MonoBehaviour.Update）可以使对象响应事件。要接收这些回调，GameObject 必须在场景中处于激活状态，也就是 activeSelf 和 activeInHierarchy 属性都必须为 true。

可以通过调用构造函数创建空 GameObject，但更常见的方式是实例化带有预配置组件、属性值和子对象的 Prefab。详情参阅[运行时实例化预制件](https://docs.unity3d.com/6000.7/Documentation/Manual/instantiating-prefabs.html)。

可以在 Editor 的 Inspector 窗口中修改此类的许多属性。有关 GameObject 类的完整使用指南，请参阅 [GameObject 手册页面](https://docs.unity3d.com/6000.7/Documentation/Manual/class-GameObject.html)。

下面的示例创建名为 myExampleGO 的 GameObject，并添加 AudioSource 组件：

~~~csharp
using UnityEngine;

public class Example_GameObject : MonoBehaviour
{
    private void Start()
    {
        GameObject myExampleGO = new GameObject("myExampleGO", typeof(AudioSource));
    }
}
~~~

相关资源：[Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)。

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-activeInHierarchy]] | activeInHierarchy | GameObject 在场景层级中的激活状态。激活时为 true，未激活时为 false。（只读） |
| [[02-activeSelf]] | activeSelf | GameObject 的本地激活状态。激活时为 true，未激活时为 false。（只读） |
| [[03-isStatic]] | isStatic | GameObject 是否设置了任意 Static Editor Flags。 |
| [[04-layer]] | layer | 标识 GameObject 所分配到的层的整数。 |
| [[05-scene]] | scene | 包含该 GameObject 的场景。 |
| [[06-sceneCullingMask]] | sceneCullingMask | 为 GameObject 定义的场景剔除掩码。（只读） |
| [[07-tag]] | tag | 分配给 GameObject 的标签。 |
| [[08-transform]] | transform | 附加到 GameObject 的 Transform。（只读） |
| [[09-transformHandle]] | transformHandle | GameObject 的 TransformHandle。（只读） |

## 构造函数

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[10-ctor]] | GameObject | 创建新的 GameObject；可以选择指定名称以及要附加的组件集合。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[11-AddComponent]] | AddComponent | 向 GameObject 添加指定类型的组件。 |
| [[12-BroadcastMessage]] | BroadcastMessage | 在 GameObject 或其任意子对象上附加的每个 MonoBehaviour 中调用指定方法。 |
| [[13-CompareTag]] | CompareTag | 检查 GameObject 是否附加了指定标签。 |
| [[14-GetComponent]] | GetComponent | 通过向泛型方法提供组件类型参数，获取指定类型组件的引用。 |
| [[15-GetComponentAtIndex]] | GetComponentAtIndex | 获取 GameObject 组件数组中指定索引处的组件引用。 |
| [[16-GetComponentCount]] | GetComponentCount | 获取当前附加到 GameObject 的组件总数。 |
| [[17-GetComponentInChildren]] | GetComponentInChildren | 获取 GameObject 或其任意子对象上 T 类型组件的引用。 |
| [[18-GetComponentIndex]] | GetComponentIndex | 获取指定组件在附加到 GameObject 的组件数组中的索引。 |
| [[19-GetComponentInParent]] | GetComponentInParent | 获取 GameObject 或其任意父对象上 T 类型组件的引用。 |
| [[20-GetComponents]] | GetComponents | 获取 GameObject 上所有 T 类型组件的引用。 |
| [[21-GetComponentsInChildren]] | GetComponentsInChildren | 获取 GameObject 及其任意子对象上所有 T 类型组件的引用。 |
| [[22-GetComponentsInParent]] | GetComponentsInParent | 获取 GameObject 及其任意父对象上所有 T 类型组件的引用。 |
| [[23-IsDestroying]] | IsDestroying | 检查 GameObject 及其后代对象是否正在销毁过程中。 |
| [[24-SendMessage]] | SendMessage | 在附加到 GameObject 的每个 MonoBehaviour 上调用指定方法。 |
| [[25-SendMessageUpwards]] | SendMessageUpwards | 在附加到 GameObject 的每个 MonoBehaviour 以及该行为的每个祖先对象上调用指定方法。 |
| [[26-SetActive]] | SetActive | 根据提供的参数在本地激活或停用 GameObject。 |
| [[27-TryGetComponent]] | TryGetComponent | 如果指定类型的组件存在，则获取该组件。 |

## 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[28-CreatePrimitive]] | CreatePrimitive | 使用指定的 PrimitiveType 创建带有网格渲染器和适当碰撞体的 GameObject。 |
| [[29-Find]] | Find | 按指定名称或层级路径查找并返回 GameObject。 |
| [[30-FindGameObjectsWithTag]] | FindGameObjectsWithTag | 获取所有带有指定标签的活动 GameObject 数组。如果没有 GameObject 带有该标签，则返回空数组。 |
| [[31-FindWithTag]] | FindWithTag | 获取第一个带有指定标签的活动 GameObject。如果没有找到，则返回 null。 |
| [[32-GetScene]] | GetScene | 获取包含指定实例 ID 对应 GameObject 的场景。 |
| [[33-InstantiateGameObjects]] | InstantiateGameObjects | 创建指定数量的实例，并将新 GameObject 及其 Transform 组件的 EntityId 填充到 NativeArray 中。 |
| [[34-SetGameObjectsActive]] | SetGameObjectsActive | 激活或停用由实例 ID 标识的多个 GameObject。 |

## 继承成员

### 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/01-hideFlags]] | hideFlags | 控制对象是否隐藏、是否随场景保存以及用户是否可以编辑对象。 |
| [[../Object/02-name]] | name | 对象的名称。 |

### 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/03-GetEntityId]] | GetEntityId | 获取对象的 EntityId。 |
| [[../Object/04-GetHashCode]] | GetHashCode | 返回对象的哈希代码。 |
| [[../Object/05-ToString]] | ToString | 返回对象的名称。 |

### 静态方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/06-Destroy]] | Destroy | 移除 GameObject、组件或资源。 |
| [[../Object/07-DestroyImmediate]] | DestroyImmediate | 立即销毁指定对象；仅应谨慎地在编辑模式下使用。 |
| [[../Object/08-DontDestroyOnLoad]] | DontDestroyOnLoad | 加载新场景时不销毁目标对象。 |
| [[../Object/09-FindAnyObjectByType]] | FindAnyObjectByType | 获取任意一个处于活动状态的已加载 T 类型对象。 |
| [[../Object/10-FindObjectsByType]] | FindObjectsByType | 获取所有已加载指定类型对象的列表。 |
| [[../Object/11-Instantiate]] | Instantiate | 克隆原对象并返回克隆对象。 |
| [[../Object/12-InstantiateAsync]] | InstantiateAsync | 捕获与另一个 GameObject 相关的原对象快照，并获取结果对象的 AsyncInstantiateOperation 实例。 |

### 运算符

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[../Object/13-bool]] | bool | 判断对象是否存在。 |
| [[../Object/14-operator-ne]] | operator != | 比较两个对象是否引用不同对象。 |
| [[../Object/15-operator-eq]] | operator == | 比较两个对象引用是否指向同一个对象。 |

## 示例

~~~csharp
using UnityEngine;

  public class Example_GameObject :  MonoBehaviour 
  {
      private void Start()
      {
           GameObject  myExampleGO = new  GameObject ("myExampleGO", typeof( AudioSource ));
      }
  }
~~~

## 相关资源

- [Component](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.html)

