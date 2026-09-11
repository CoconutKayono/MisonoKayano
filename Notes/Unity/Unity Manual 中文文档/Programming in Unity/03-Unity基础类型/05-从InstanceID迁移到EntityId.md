# 从 InstanceID 迁移到 EntityId

> 原文：[Migrate from InstanceID to EntityId](https://docs.unity3d.com/6000.7/Documentation/Manual/instanceid-to-entityid-migration.html)

从 Unity 6.4 开始，Unity 使用 64 位的 `EntityId` 结构体替代 32 位整数 `InstanceID`。`EntityId` 统一了 GameObject 和 Entity 标识 Unity 对象的方式，并移除了旧标识符行为中的一些隐含假设。

此迁移会影响直接使用对象标识符的代码，例如 Editor Extension、对象查找和选择代码、自定义 TreeView、自定义序列化、缓存、对象池，以及将 Unity 对象标识符存储在 `int` 字段中的 Package。

本指南只适用于 Unity 对象身份相关的 API，不适用于 Shader 和 GPU Instancing 标识符，例如 `unity_InstanceID` 或 `SV_InstanceID`。

## 升级前准备

从 Unity 6.5 开始，已废弃的 InstanceID API 会导致编译错误。应在升级前使用对应的 EntityId API 替换这些 API。

`EntityId` 是 64 位值，32 位整数无法表示它。通过抑制编译错误，或从预编译程序集调用基于 `int` 的 API 来绕过错误，可能导致标识符在 Runtime 中被静默截断。

在使用目标 Unity 版本打开项目之前：

1. 更新 Unity Package、嵌入式 Package 和 Asset Store Package。
2. 在项目和嵌入式 Package 中搜索以下标识符和模式：
   - `GetInstanceID`、`InstanceID`、`instanceID`、`instanceIDs`。
   - `FindObjectsSortMode`、`FindObjectsSortMode.InstanceID`。
   - `FindFirstObjectByType`、`FindObjectOfType`。
   - 对 `UnityEngine.Object` 或 `EntityId` 调用 `GetHashCode`。
   - `objectInstanceId`、`objectReferenceInstanceIDValue` 以及其他包含 InstanceID 的字段或属性名称。
   - 标识符字符串附近的 `int.Parse` 或 `int.TryParse`。
   - 将 EntityId 或 Object 转换为 `ToString`，再保存、解析或比较的代码。
3. 修复编译错误。
4. 如果第三方 Package 的供应商还没有发布 EntityId 兼容版本，检查该 Package 的代码。

可以考虑先迁移到中间 Unity 版本，以便在弃用警告变成错误前修复它们。Unity 的自动脚本更新器不会替换主要的 InstanceID API（例如 `GetInstanceID`）。应结合编译器错误、IDE 警告和手动代码搜索，检查受影响的代码，并手动更新周围的数据类型。

## 替换 InstanceID API

当值表示 Unity 对象身份时，应使用 EntityId API。下面列出了常见替代方案：

| 旧 API 或模式 | 替代方案 | 迁移时的检查事项 |
| --- | --- | --- |
| `Object.GetInstanceID()` | `Object.GetEntityId()` | 将接收值的类型从 `int` 改为 `EntityId`。 |
| `Resources.InstanceIDToObject(int)` | `Resources.EntityIdToObject(EntityId)` | 传递 EntityId，而不是被截断的整数。 |
| `Resources.InstanceIDIsValid(int)` | `Resources.EntityIdIsValid(EntityId)` | 将有效性检查保持为 EntityId 类型。 |
| `Resources.InstanceIDToObjectList(NativeArray<int>, List<Object>)` | `Resources.EntityIdsToObjectList(NativeArray<EntityId>, List<Object>)` | 将完整的数组或 List 数据流改为 EntityId。 |
| `Resources.InstanceIDsToValidArray(...)` | `Resources.EntityIdsToValidArray(...)` | 将 NativeArray 和 Span 的调用点都改为 EntityId。 |
| `Selection.instanceIDs`、`Selection.activeInstanceID`、`Selection.Contains(int)` | `Selection.entityIds`、`Selection.activeEntityId`、`Selection.Contains(EntityId)` | 将选择数据从 `int[]` 改为 `EntityId[]`。 |
| `EditorUtility.InstanceIDToObject(int)` | `EditorUtility.EntityIdToObject(EntityId)` | 这是 Editor API；Runtime 代码应使用 Runtime API。 |
| `SerializedProperty.objectReferenceInstanceIDValue` | `SerializedProperty.objectReferenceEntityIdValue` | 同时更新读取和写入。 |
| `EditorApplication.hierarchyWindowItemOnGUI` | `EditorApplication.hierarchyWindowItemByEntityIdOnGUI` | 将回调参数从 `int` 改为 `EntityId`。 |
| `ProjectWindowCallback.EndNameEditAction` | `ProjectWindowCallback.AssetCreationEndAction` | 将重写方法的签名从 `int` 更新为 `EntityId`。 |
| 带 `int` 参数的 `[OnOpenAsset]` 回调 | 带 `EntityId` 参数的 `[OnOpenAsset]` 回调 | 必须显式搜索；IDE 更新器不会迁移此签名。 |
| `LazyLoadReference<T>.instanceID` | `LazyLoadReference<T>.entityId` | 检查保存旧整数值的序列化数据。 |
| `Object.FindObjectsByType(..., FindObjectsSortMode)` | `Object.FindObjectsByType(Type)` 或 `Object.FindObjectsByType(Type, FindObjectsInactive)` | 使用无排序重载；需要顺序时按实际属性排序。 |
| `Object.FindFirstObjectByType` | `Object.FindAnyObjectByType` | `FindFirstObjectByType` 依赖 InstanceID 排序，已被废弃。 |
| `Object.FindObjectOfType` | `Object.FindAnyObjectByType` | 同上。 |
| `EntityId.GetRawData()` | `EntityId.ToULong(target)` | `GetRawData` 已废弃，使用 `ToULong` 和 `FromULong`。 |
| 保存对象 ID 时使用 `SessionState.GetULong`、`SetULong`、`EraseULong` | `SessionState.GetEntityId`、`SetEntityId`、`EraseEntityId` 及对应数组 API | 基于 `ulong` 的 API 已移除，改用 EntityId 系列。 |
| `Physics.BakeMesh(int, bool)` | `Physics.BakeMesh(EntityId, bool)` | 将传入调用的 Mesh ID 数组或对象池改为 EntityId。 |
| 使用隐式 `int` ID 的 `TreeView`、`TreeViewItem`、`TreeViewState` | `TreeView<TIdentifier>`、`TreeViewItem<TIdentifier>`、`TreeViewState<TIdentifier>` | 只有当树项目代表 Unity 对象身份时才使用 EntityId。 |
| `HierarchyProperty` | `HierarchyIterator` | 迁移层级遍历代码。 |

这张表不是完整列表。`AssetDatabase`、`GlobalObjectId`、`ObjectChangeEvents` 事件参数、`EditorUtility`、`InternalEditorUtility`、`EventMarker`、`Terrain` 和各种 Render Pipeline API，也会同时提供 EntityId 重载以及已废弃的 `int` 成员。任何接收、返回、存储或比较对象 InstanceID 的 API 都需要同样检查。

迁移时要区分“表示对象身份的 `int`”和普通的临时 `int`。只要 `int` 保存的是 UnityEngine.Object 引用的标识，就必须改为 EntityId；与 Unity 对象身份无关的临时局部值仍然可以使用 `int`。

## 将身份数据结构改为 EntityId

不要用 `int` 哈希值替代 Unity 对象标识。如果值用于标识 Unity 对象，就保存完整的 `EntityId`。

迁移前：

```csharp
Dictionary<int, ObjectState> states = new();
int id = target.GetInstanceID();
states[id] = state;
```

迁移后：

```csharp
Dictionary<EntityId, ObjectState> states = new();
EntityId id = target.GetEntityId();
states[id] = state;
```

身份映射和集合应使用 `HashSet<EntityId>` 及 `Dictionary<EntityId, TValue>`。这些集合可以在内部使用 `EntityId.GetHashCode`，同时仍然使用完整的 EntityId 值进行相等性比较。

不要把 `EntityId.GetHashCode` 或 `Object.GetHashCode` 作为保存的标识符。哈希码只由 EntityId 值的一部分计算得到，不同对象可能共享同一个哈希码；它既不唯一，也不是稳定的序列化格式，更不能替代旧的 `int` InstanceID。

## 不要将 EntityId 转换为 int

不存在通用、唯一且无损的 EntityId 到 `int` 的转换。将标识符存储在 `int` 字段中的代码，通常必须将字段、参数、属性或集合键的类型改为 EntityId。

不要这样做：

```csharp
int id = (int)target.GetEntityId();
int id = target.GetEntityId().GetHashCode();
int id = (int)EntityId.ToULong(target.GetEntityId());
```

直接使用 EntityId：

```csharp
EntityId id = target.GetEntityId();
```

某些无关的 Unity API 仍然使用 `int` ID，例如 IMGUI control ID。它不是 Unity 对象标识符；除非 API 只需要临时且非持久化的 control ID，并且代码不依赖唯一对象身份，否则不要将 EntityId 哈希值传给这些 API。

要检查 EntityId 是否为非默认值，请使用 `EntityId.IsValid` 实例方法。要检查它标识的对象当前是否已加载，请使用 `Resources.EntityIdIsValid`。

如果旧代码使用 `EntityId.GetRawData`，请将它替换为 `EntityId.ToULong`。如果需要将值转换并再转换回来，使用 `EntityId.ToULong` 和 `EntityId.FromULong`，并将原始值作为 `ulong` 保存。

## 不要从数值推断含义

旧的 InstanceID 值本来就是实现细节，但一些项目会使用它的数值推断对象状态。EntityId 不再保证这些假设。不要使用 EntityId 推断：

- 创建顺序。
- Scene 层级顺序。
- 加载顺序。
- 对象是在 Runtime 创建还是从 Asset 加载。
- Prefab 实例状态。
- 持久性。

尤其不要检查 ID 是否为负数。旧代码有时使用 `instanceID < 0` 猜测对象是否在 Runtime 创建，但这从来不是保证行为，也不适用于 EntityId。所有 EntityId 值都是正数。

Unity 销毁对象后，可能会将该对象的 EntityId 重新用于另一个对象。因此，先后创建的两个对象，其 EntityId 值可能是任意顺序。

Editor 代码如果需要判断对象是否持久化，应使用仅限 Editor 的 `EditorUtility.IsPersistent` API。Runtime 代码应使用项目自己的数据模型完成类似判断，而不要解释标识符数值。

## 按实际需要的属性排序

不要按 InstanceID 或 EntityId 排序来恢复创建顺序。EntityId 的排序没有意义。比较运算符和 `CompareTo` 只适用于数据结构需要稳定顺序的场景，例如排序集合或二分查找。

迁移前：

```csharp
var objectsInCreationOrder = objects.OrderBy(obj => obj.GetInstanceID());
```

迁移后：

```csharp
var objectsByName = objects.OrderBy(obj => obj.name);
```

如果代码需要创建顺序，应显式记录它：

```csharp
readonly List<GameObject> m_CreationOrder = new();

public void Register(GameObject instance)
{
    m_CreationOrder.Add(instance);
}
```

如果代码需要层级顺序，应根据 sibling index、Transform path 或其他领域专用键排序。

### FindObjects API

不要依赖 Unity 在迁移过程中保留 InstanceID 顺序。以下 API 因依赖 InstanceID 排序而被废弃：

- `Object.FindObjectsByType(..., FindObjectsSortMode)` 及其泛型版本。
- `Object.FindFirstObjectByType` 及其泛型版本。
- `FindObjectsSortMode` 枚举本身。

InstanceID 排序也很慢。Unity Engine 团队测量发现，根据项目不同，InstanceID 排序可能占 `FindObjectsOfType` 总耗时的约 93%。

如果不需要顺序，使用不接收 `FindObjectsSortMode` 的重载：

```csharp
var renderers = Object.FindObjectsByType<MeshRenderer>();
```

如果顺序很重要，按代码真正需要的属性排序：

```csharp
var renderers = Object.FindObjectsByType<MeshRenderer>()
    .OrderBy(renderer => renderer.transform.GetSiblingIndex())
    .ToArray();
```

`FindAnyObjectByType` 是唯一不依赖标识符顺序的单结果 API。如果任意匹配对象都可以接受，应使用它。如果需要特定对象，应先批量查找，再显式排序，而不要依赖 `FindFirstObjectByType` 返回旧 InstanceID 顺序中的第一个对象。

## 更新序列化和保存数据

检查所有在序列化字段、保存文件、Editor Preferences、缓存或自定义 Asset 格式中保存 InstanceID 的代码，例如：

- `[SerializeField] int m_InstanceId`。
- 通过自定义格式序列化的 `Dictionary<int, TValue>`。
- 由 `instanceID.ToString()` 生成的字符串数据。
- 将对象 ID 作为数字保存的缓存文件。
- 以 `int` 暴露对象 ID 的公共 Package API。

将 `int` 字段改为 EntityId 会改变序列化数据结构。Unity 无法知道任意序列化 `int` 字段过去保存的是 InstanceID；如果数据必须在升级后继续使用，应规划数据迁移。

不要使用 `ToString` 序列化 EntityId，再在以后解析结果。EntityId 的字符串格式已经在 Unity 版本之间发生过变化，未来也可能继续变化。`ToString` 只适合显示和调试。

如果必须在 `ulong` 与 EntityId 之间转换原始值，请同时使用 `EntityId.ToULong` 和 `EntityId.FromULong`，并把 `ulong` 当作不能读取和解释的原始值：

```csharp
EntityId id = target.GetEntityId();
ulong raw = EntityId.ToULong(id);
EntityId restored = EntityId.FromULong(raw);
```

应将原始值保存为 `ulong`，而不是 `int`。通过 `int` 转换 EntityId 会静默截断高 32 位，而 `EntityId.FromULong` 会构造出损坏的值，且无法检测这个错误。

不要检查原始值的位、按原始值排序、在原始值中保存状态、将其转换为 `int`，也不要围绕当前位布局构建长期外部格式。原始布局是实现细节，可能在 Unity 版本之间改变。

对于存档、网络协议、分析数据或其他持久化外部数据，应使用项目自己的稳定标识符，而不是原始 EntityId。

## 更新 Editor 回调

Editor 回调 API 是迁移工作的常见来源，因为变化的不只是 API 名称，回调签名也会变化。

对于 Hierarchy GUI 回调，将 `hierarchyWindowItemOnGUI` 替换为 `hierarchyWindowItemByEntityIdOnGUI`：

```csharp
using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
public static class CustomHierarchyStyling
{
    static CustomHierarchyStyling()
    {
        EditorApplication.hierarchyWindowItemByEntityIdOnGUI += OnHierarchyGUI;
        EditorApplication.hierarchyChanged += EditorApplication.RepaintHierarchyWindow;
    }

    static void OnHierarchyGUI(EntityId entityId, Rect selectionRect)
    {
        GameObject obj = EditorUtility.EntityIdToObject(entityId) as GameObject;
        if (obj == null || !obj.CompareTag("Special"))
            return;

        Rect iconRect = new Rect(selectionRect.x - 20, selectionRect.y, 18, 18);
        GUI.Label(iconRect, EditorGUIUtility.IconContent("d_Favorite"));
    }
}
```

对于 Project 窗口 Asset 创建回调，将 `EndNameEditAction` 替换为 `AssetCreationEndAction`，并更新重写方法签名：

```csharp
using UnityEditor.ProjectWindowCallback;
using UnityEngine;

public class CreateAssetAction : AssetCreationEndAction
{
    public override void Action(EntityId entityId, string pathName, string resourceFile)
    {
        Object asset = UnityEditor.EditorUtility.EntityIdToObject(entityId);
        Debug.Log($"Created asset: {asset}");
    }
}
```

对于 Asset 打开回调，将 `[OnOpenAsset]` 回调参数从 `int` 改为 `EntityId`：

```csharp
using UnityEditor;
using UnityEditor.Callbacks;
using UnityEngine;

public static class OpenAssetHandler
{
    [OnOpenAsset]
    public static bool OnOpenAsset(EntityId entityId, int line)
    {
        Object asset = EditorUtility.EntityIdToObject(entityId);
        // 自定义打开行为。
        return false;
    }
}
```

在后续 Unity 版本中，带 `int` 参数的 `[OnOpenAsset]` 重载会被完全移除。由于 IDE 侧更新器不会迁移 `[OnOpenAsset]` 签名，应显式搜索代码库。某些用户定义的回调方法无法在声明位置标记为 obsolete，因此还要搜索旧回调签名，并修复 IDE 或 Unity 工具报告的分析器警告。

## 更新 TreeView 代码

如果 Editor Extension 使用 IMGUI TreeView API，应有意识地迁移标识符类型。泛型 TreeView API 允许选择标识符类型：

```csharp
using UnityEditor.IMGUI.Controls;
using UnityEngine;

class ObjectTreeView : TreeView<EntityId>
{
    public ObjectTreeView(TreeViewState<EntityId> state) : base(state) { }

    protected override TreeViewItem<EntityId> BuildRoot()
    {
        return new TreeViewItem<EntityId>
        {
            id = EntityId.None,
            depth = -1,
            displayName = "Root"
        };
    }
}
```

只有当树项目代表 Unity 对象时，才将 `EntityId` 作为 `TIdentifier`；如果树项目代表其他概念，应使用属于该概念的稳定标识符。

Unity 的自动脚本更新器会为非泛型 TreeView 类型应用 `using` 别名升级。因此，使用 `TreeView`、`TreeViewItem` 和 `TreeViewState` 的旧代码可以暂时继续使用固定为 `<int>` 的泛型版本。可以将此作为临时措施，同时迁移底层标识符类型。大型文件可以使用 using 别名减少修改数量，但要注意类型名称冲突，确认 TreeView 当前仍使用 `int` 还是已经改为 EntityId。

## 迁移层级遍历

如果 Editor 代码使用 `HierarchyProperty` 遍历层级，应迁移到 `HierarchyIterator`。类本身、所有接收或返回标识符的方法，以及 expanded-set 数组，都要从 `int` 改为 EntityId：

```csharp
// Before
var prop = new HierarchyProperty(HierarchyType.GameObjects);
int[] expanded = Array.Empty<int>();
while (prop.Next(expanded))
{
    int id = prop.instanceID;
    Debug.Log($"Object: {prop.name}, id={id}");
}

// After
var iter = new HierarchyIterator(HierarchyType.GameObjects);
EntityId[] expanded = Array.Empty<EntityId>();
while (iter.Next(expanded))
{
    EntityId id = iter.entityId;
    Debug.Log($"Object: {iter.name}, id={id}");
}
```

如果 expanded-state 数组保存为 `int[]`，也要改为 `EntityId[]`。

对于自定义 Scene 搜索引擎，将 `ISceneSearchEngine` 替换为 `ISceneSearchEngineV2`，将 `Filter` 方法签名从 `HierarchyProperty` 更新为 `HierarchyIterator`，并调用匹配的 `SceneSearch.RegisterEngine` 和 `SceneSearch.UnregisterEngine` 重载。如果代码读取 `SceneSearchContext.rootProperty`，改为 `SceneSearchContext.rootIterator`。相关的拖放辅助方法 `InternalEditorUtility.HierarchyWindowDrag` 和 `InternalEditorUtility.ProjectWindowDrag` 也已废弃；使用接收 HierarchyIterator 的 V2 版本。

## 处理第三方 Package

仍使用已废弃 InstanceID API 的 Package 可能导致整个项目无法编译。如果 Package 仍使用这些 API：

1. 通过 Package Manager 或 Asset Store 更新 Package。
2. 检查 Package 是否嵌入 `Packages` 文件夹，或缓存于 `Library/PackageCache`。
3. 如果项目不使用该 Package，则将其移除。
4. 联系供应商，索取 EntityId 兼容版本。
5. 如果必须在供应商发布更新前继续使用，可以修补嵌入式副本。

如果维护需要支持多个 Unity 版本的代码，请围绕新旧 API 路径使用版本保护。版本符号应选择为包含所调用替代 API 的第一个 Unity 版本，不要假设一个符号适用于所有 EntityId 替换。

## 更新自动化测试

如果项目或 Package 包含自动化测试，应更新依赖 InstanceID 顺序、符号或整数大小行为的测试。

迁移后失败的测试通常依赖旧的偶然排序。不要通过按 EntityId 排序来恢复旧行为，而应让测试表达真正的需求。

当顺序不是契约的一部分时，使用与顺序无关的断言：

```csharp
CollectionAssert.AreEquivalent(expectedObjects, actualObjects);
```

当顺序是契约的一部分时，显式排序：

```csharp
var actualObjects = Object.FindObjectsByType<MyComponent>()
    .OrderBy(component => component.name)
    .ToArray();
```

项目编译通过后，还要测试 Editor Extension 和 Package 代码。回调迁移、序列化数据迁移和 Package 修补可能在最初的编译错误列表之外失败。

## EntityId 大小和二进制布局

确保代码不依赖 EntityId 的二进制表示。EntityId 占 8 字节，结构体不公开其内部字段，位布局属于实现细节，可能在 Unity 版本之间改变。

| 特性 | 旧 `InstanceID`（`int`） | 新 `EntityId`（结构体） |
| --- | --- | --- |
| 大小 | 4 字节 | 8 字节 |
| 符号位含义 | 负数表示 Runtime 创建，正数表示持久化对象。 | 没有此含义；所有值都是正数。 |
| 是否适合指针大小字段 | 所有平台都适合。 | 只有 64 位平台适合。 |
| 排序顺序 | 在某些情况下碰巧反映创建顺序。 | 没有有意义的顺序；Unity 会为不同对象复用值。 |
| 位布局 | 实现细节。 | 实现细节，可能在 Unity 版本之间改变。 |

### 不要将标识符存储在指针大小字段中

EntityId 占 8 字节，因此在包含 Unity Editor 的 64 位平台上适合指针大小字段，但不适合 WebGL 或 32 位 Android 等 32 位 Runtime 平台。使用指针大小字段保存旧的 4 字节 InstanceID，在 64 位平台上只是偶然可用，在 32 位平台上会静默失败或损坏数据。

应将 EntityId 保存在 EntityId 类型字段中，而不是 `IntPtr`、`void*`、`nint` 或 `int` 字段中。

### 不要对 EntityId 执行算术运算

不要对 EntityId 执行算术、位运算或符号检查。仅通过检查 64 位原始值，无法区分有效值和无效值，而且位布局是实现细节。比较时使用 EntityId API；检查非默认值时使用 `EntityId.IsValid`。

### Runtime 会检测被截断的 EntityId

如果代码将被截断的 EntityId 值传递给 `Resources.EntityIdToObject` 等 API，例如高位因 `int` 转换而丢失的值，Unity 会在 Runtime 检测到截断并报告错误，而不是静默返回错误对象。这可以保护最常见的 int 截断错误，但不能替代底层类型迁移。

### 不要比较包含 EntityId 的结构体原始字节

避免以下行为：

- 将状态存储在 EntityId 的位中。
- 比较包含 EntityId 字段的结构体原始字节。
- 依赖 EntityId 字段周围的填充。
- 假设 `sizeof(EntityId) == 4`。

EntityId 从 4 字节变为 8 字节后，包含它的结构体可能具有不同的填充或成员偏移。应显式比较结构体字段，并通过 EntityId API 比较 EntityId 值。

## 迁移检查清单

- 将 InstanceID API 调用替换为对应的 EntityId API 调用。
- 将表示对象身份的 `int` 字段、参数、属性、数组和集合键改为 EntityId。
- 将传递 `int` ID 的 Editor 回调替换为 EntityId 回调，包括 `[OnOpenAsset]`。
- 更新 TreeView 代码，使用正确的泛型标识符类型。
- 将 `HierarchyProperty` 迁移到 `HierarchyIterator`，包括 expanded-set 数组。
- 移除 `id < 0` 等符号检查。
- 不对 EntityId 执行算术或位运算。
- 不按 InstanceID 或 EntityId 排序来恢复创建顺序。
- 将已废弃的 `FindObjectsByType(..., FindObjectsSortMode)`、`FindFirstObjectByType` 和 `FindObjectOfType` 替换为无排序重载或 `FindAnyObjectByType`，并在顺序重要时显式排序。
- 不再使用 `GetHashCode` 作为对象标识符。
- 不再使用 `ToString` 加整数解析进行序列化。
- 将 `EntityId.GetRawData` 替换为 `EntityId.ToULong` 或 `EntityId.FromULong`，并将原始值作为 `ulong` 保存，不对它进行解释。
- 审查使用 InstanceID 的序列化数据和保存格式。
- 审查将标识符存储在指针大小字段（`IntPtr`、`void*`、`nint`、`int`）中的代码。
- 更新或修补仍使用 InstanceID API 的第三方 Package。
- 更新依赖旧排序、符号或整数大小行为的自动化测试。

---

## 其他资源

- `EntityId`
- `Object.GetEntityId`

---

## 文档导航

- 上一页：[[04-Unity属性]]
- 目录：[[00-Unity基础类型]]
- 下一页：[[00-管理更新和执行顺序]]
