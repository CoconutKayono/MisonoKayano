# ToggleGroup 类

## 继承关系

`object` → `MonoBehaviour` → `UIBehaviour` → `ToggleGroup`

## 继承的成员

- `UIBehaviour.Awake()`
- `UIBehaviour.OnDisable()`
- `UIBehaviour.OnDestroy()`
- `UIBehaviour.IsActive()`
- `UIBehaviour.OnValidate()`

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
[AddComponentMenu("UI (Canvas)/Toggle Group", 31)]
[DisallowMultipleComponent]
public class ToggleGroup : UIBehaviour
```

## 构造函数

### ToggleGroup()

声明：

```csharp
protected ToggleGroup()
```

## 字段

### m_Toggles

声明：

```csharp
protected List<Toggle> m_Toggles
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `List<Toggle>` | |

## 属性

### allowSwitchOff

是否允许所有 Toggle 都处于关闭状态？

声明：

```csharp
public bool allowSwitchOff { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

备注：

如果启用此设置，按下当前已开启的 Toggle 会将其关闭，从而使所有 Toggle 都处于关闭状态。如果禁用此设置，按下当前已开启的 Toggle 不会改变其状态。请注意，即使 `allowSwitchOff` 为 false，如果场景加载或组实例化时组内一个开启的 Toggle 都没有，Toggle Group 也不会立刻强制纠偏；它只会阻止用户手动把 Toggle 关掉。

## 方法

### ActiveToggles()

返回此组中处于开启状态的 Toggle。

声明：

```csharp
public IEnumerable<Toggle> ActiveToggles()
```

返回值：

| 类型 | 说明 |
| --- | --- |
| `IEnumerable<Toggle>` | 组中处于开启状态的 Toggle。 |

备注：

此方法仅检查开/关状态，不检查 GameObject 的激活状态。

### AnyTogglesOn()

是否有任何 Toggle 处于开启状态？

声明：

```csharp
public bool AnyTogglesOn()
```

返回值：

| 类型 | 说明 |
| --- | --- |
| `bool` | 是否有任何 Toggle 处于开启状态。 |

### EnsureValidState()

确保 ToggleGroup 仍具有有效状态。仅当 ToggleGroup 启动时或组中有 Toggle 被删除时，此方法才相关。

声明：

```csharp
public void EnsureValidState()
```

### GetFirstActiveToggle()

返回第一个处于开启状态的 Toggle。

声明：

```csharp
public Toggle GetFirstActiveToggle()
```

返回值：

| 类型 | 说明 |
| --- | --- |
| `Toggle` | 第一个处于开启状态的 Toggle；如果没有处于开启状态的 Toggle，则返回 null。 |

备注：

此方法仅检查开/关状态，不检查 GameObject 的激活状态。

### NotifyToggleOn(Toggle, bool)

通知组：指定的 Toggle 已开启。

声明：

```csharp
public void NotifyToggleOn(Toggle toggle, bool sendCallback = true)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Toggle` | `toggle` | 被触发开启的 Toggle。 |
| `bool` | `sendCallback` | 其他 Toggle 是否应发送 `onValueChanged`。 |

### OnEnable()

声明：

```csharp
protected override void OnEnable()
```

重写：

`UIBehaviour.OnEnable()`

### RegisterToggle(Toggle)

将 Toggle 注册到 ToggleGroup，使组能监听它的变化，并在组内其他 Toggle 变化时通知它。

声明：

```csharp
public void RegisterToggle(Toggle toggle)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Toggle` | `toggle` | 要向组注册的 Toggle。 |

### SetAllTogglesOff(bool)

关闭所有 Toggle。

声明：

```csharp
public void SetAllTogglesOff(bool sendCallback = true)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `bool` | `sendCallback` | |

备注：

无论 `allowSwitchOff` 属性是否启用，都可以使用此方法关闭所有 Toggle。

### Start()

由于所有 Toggle 都在 OnEnable 中完成注册，Start 应检查未启用 AllowSwitchOff 的组是否至少有一个 Toggle 处于开启状态。

声明：

```csharp
protected override void Start()
```

重写：

`UIBehaviour.Start()`

### UnregisterToggle(Toggle)

从组中注销一个 Toggle。

声明：

```csharp
public void UnregisterToggle(Toggle toggle)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `Toggle` | `toggle` | 要移除的 Toggle。 |

---

相关文档：[[UnityEngine-UI-Toggle-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
