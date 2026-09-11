> 原文：[CharacterController](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/CharacterController.html)

# CharacterController

`CharacterController` 让你可以方便地执行受碰撞约束的移动，而不必处理 `Rigidbody`。

`CharacterController` 不受力影响，只有在调用 `Move` 时才会移动。它会执行请求的移动，同时受到碰撞约束。

相关资源：[Character Controller component](https://docs.unity3d.com/6000.7/Documentation/Manual/class-CharacterController.html)、[Character animation examples](http://unity3d.com/learn/tutorials/modules/beginner/animation)。

## 属性

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-center]] | center | 角色胶囊体相对于 Transform 位置的中心。 |
| [[02-collisionFlags]] | collisionFlags | 上次调用 CharacterController.Move 时胶囊体与环境发生碰撞的部分。 |
| [[03-detectCollisions]] | detectCollisions | 是否检测其他刚体或角色控制器与此角色控制器的碰撞，默认始终启用。 |
| [[04-enableOverlapRecovery]] | enableOverlapRecovery | 启用或禁用重叠恢复，用于检测到重叠时将角色控制器从静态对象中推出。 |
| [[05-height]] | height | 角色胶囊体的高度。 |
| [[06-isGrounded]] | isGrounded | 角色控制器在上次移动期间是否接触地面。 |
| [[07-minMoveDistance]] | minMoveDistance | 获取或设置角色控制器的最小移动距离。 |
| [[08-radius]] | radius | 角色胶囊体的半径。 |
| [[09-skinWidth]] | skinWidth | 角色的碰撞皮肤宽度。 |
| [[10-slopeLimit]] | slopeLimit | 角色控制器允许的坡度限制（度）。 |
| [[11-stepOffset]] | stepOffset | 角色控制器允许的台阶高度（米）。 |
| [[12-velocity]] | velocity | 角色当前的相对速度。 |

## 公共方法

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[13-Move]] | Move | 提供带有 CharacterController 组件的 GameObject 的移动。 |
| [[14-SimpleMove]] | SimpleMove | 以指定速度移动角色。 |

## 继承成员

### 属性

| 链接 | API名 | 中文说明 |
| --- | --- | --- |
| [attachedArticulationBody](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-attachedArticulationBody.html) | attachedArticulationBody | 此碰撞体所附加到的 Articulation Body。 |
| [attachedRigidbody](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-attachedRigidbody.html) | attachedRigidbody | 此碰撞体所附加到的 Rigidbody。 |
| [bounds](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-bounds.html) | bounds | 碰撞体在世界空间中的包围体（只读）。 |
| [contactOffset](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-contactOffset.html) | contactOffset | 此碰撞体的接触偏移值。 |
| [enabled](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-enabled.html) | enabled | 启用的 Collider 会与其他 Collider 碰撞，禁用的 Collider 不会碰撞。 |
| [excludeLayers](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-excludeLayers.html) | excludeLayers | 此 Collider 在判断是否可以与另一个 Collider 接触时应排除的其他层。 |
| [GeometryHolder](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider.GeometryHolder.html) | GeometryHolder | 保存碰撞体几何形状及其类型的结构（只读）。 |
| [hasModifiableContacts](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-hasModifiableContacts.html) | hasModifiableContacts | 指定此 Collider 的接触点是否可以修改。 |
| [includeLayers](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-includeLayers.html) | includeLayers | 此 Collider 在判断是否可以与另一个 Collider 接触时应包含的其他层。 |
| [isTrigger](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-isTrigger.html) | isTrigger | 指定此碰撞体是否配置为触发器。 |
| [layerOverridePriority](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-layerOverridePriority.html) | layerOverridePriority | 当两个 Collider 是否可以相互接触的判断发生冲突时，分配给此 Collider 的决策优先级。 |
| [material](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-material.html) | material | 碰撞体使用的材质。 |
| [providesContacts](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-providesContacts.html) | providesContacts | 此 Collider 是否为 Physics.ContactEvent 生成接触点。 |
| [sharedMaterial](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider-sharedMaterial.html) | sharedMaterial | 此碰撞体共享的物理材质。 |
| [gameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component-gameObject.html) | gameObject | 此组件附加到的游戏对象。组件始终附加到游戏对象。 |
| [tag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component-tag.html) | tag | 此游戏对象的标签。 |
| [transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component-transform.html) | transform | 附加到此 GameObject 的 Transform。 |
| [transformHandle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component-transformHandle.html) | transformHandle | 此 GameObject 的 TransformHandle。 |
| [hideFlags](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-hideFlags.html) | hideFlags | 控制对象是否隐藏、是否随场景保存以及用户是否可以编辑对象。 |
| [name](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-name.html) | name | 对象的名称。 |

### 公共方法

| 链接 | API名 | 中文说明 |
| --- | --- | --- |
| [ClosestPoint](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider.ClosestPoint.html) | ClosestPoint | 返回给定位置在碰撞体上的最近点。 |
| [ClosestPointOnBounds](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider.ClosestPointOnBounds.html) | ClosestPointOnBounds | 返回附加碰撞体的包围盒上的最近点。 |
| [GetGeometry](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider.GetGeometry.html) | GetGeometry | 返回请求类型的碰撞体几何形状。 |
| [Raycast](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Collider.Raycast.html) | Raycast | 投射一条忽略除当前碰撞体之外所有 Collider 的射线。 |
| [BroadcastMessage](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.BroadcastMessage.html) | BroadcastMessage | 在此游戏对象或其任意子对象上的每个 MonoBehaviour 中调用名为 methodName 的方法。 |
| [CompareTag](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.CompareTag.html) | CompareTag | 将 GameObject 的标签与指定标签进行比较。 |
| [GetComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponent.html) | GetComponent | 获取与指定组件位于同一 GameObject 上的 T 类型组件的引用。 |
| [GetComponentInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponentInChildren.html) | GetComponentInChildren | 获取与指定组件位于同一 GameObject 上或其任意子对象上的 T 类型组件的引用。 |
| [GetComponentIndex](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponentIndex.html) | GetComponentIndex | 获取组件在其父 GameObject 上的索引。 |
| [GetComponentInParent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponentInParent.html) | GetComponentInParent | 获取与指定组件位于同一 GameObject 上或其任意父对象上的 T 类型组件的引用。 |
| [GetComponents](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponents.html) | GetComponents | 获取与指定组件位于同一 GameObject 上的所有 T 类型组件的引用。 |
| [GetComponentsInChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponentsInChildren.html) | GetComponentsInChildren | 获取与指定组件位于同一 GameObject 及其任意子对象上的所有 T 类型组件的引用。 |
| [GetComponentsInParent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.GetComponentsInParent.html) | GetComponentsInParent | 获取与指定组件位于同一 GameObject 及其任意父对象上的所有 T 类型组件的引用。 |
| [SendMessage](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.SendMessage.html) | SendMessage | 在此游戏对象上的每个 MonoBehaviour 中调用名为 methodName 的方法。 |
| [SendMessageUpwards](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.SendMessageUpwards.html) | SendMessageUpwards | 在此游戏对象上的每个 MonoBehaviour 以及该行为的每个祖先对象上调用名为 methodName 的方法。 |
| [TryGetComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Component.TryGetComponent.html) | TryGetComponent | 如果指定类型的组件存在，则获取该组件。 |
| [GetEntityId](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.GetEntityId.html) | GetEntityId | 获取对象的 EntityId。 |
| [GetHashCode](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.GetHashCode.html) | GetHashCode | 返回对象的哈希代码。 |
| [ToString](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.ToString.html) | ToString | 返回对象的名称。 |

### 静态方法

| 链接 | API名 | 中文说明 |
| --- | --- | --- |
| [Destroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html) | Destroy | 移除 GameObject、组件或资源。 |
| [DestroyImmediate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DestroyImmediate.html) | DestroyImmediate | 立即销毁指定对象；仅应谨慎地在编辑模式下使用。 |
| [DontDestroyOnLoad](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DontDestroyOnLoad.html) | DontDestroyOnLoad | 加载新场景时不销毁目标 Object。 |
| [FindAnyObjectByType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.FindAnyObjectByType.html) | FindAnyObjectByType | 获取任意一个处于活动状态的已加载 T 类型对象。 |
| [FindObjectsByType](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.FindObjectsByType.html) | FindObjectsByType | 获取所有已加载指定类型对象的列表。 |
| [Instantiate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Instantiate.html) | Instantiate | 克隆原对象并返回克隆对象。 |
| [InstantiateAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.InstantiateAsync.html) | InstantiateAsync | 捕获与另一个 GameObject 相关的原对象快照，并获取结果对象的 AsyncInstantiateOperation 实例。 |

### 运算符

| 链接 | API名 | 中文说明 |
| --- | --- | --- |
| [bool](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_Object.html) | bool | 判断对象是否存在。 |
| [operator !=](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_ne.html) | operator != | 比较两个对象是否引用不同对象。 |
| [operator ==](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object-operator_eq.html) | operator == | 比较两个对象引用是否指向同一个对象。 |
