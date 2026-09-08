# Toggle 类

一个带有开/关状态的标准开关（Toggle）。

## 继承关系

`object` → `UIBehaviour` → `Selectable` → `Toggle`

## 实现的接口

`IMoveHandler`、`IPointerDownHandler`、`IPointerUpHandler`、`IPointerEnterHandler`、`IPointerExitHandler`、`ISelectHandler`、`IDeselectHandler`、`IPointerClickHandler`、`ISubmitHandler`、`IEventSystemHandler`、`ICanvasElement`

## 继承的成员

- `Selectable.s_Selectables`
- `Selectable.s_SelectableCount`
- `Selectable.allSelectablesArray`
- `Selectable.allSelectableCount`
- `Selectable.allSelectables`

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
[AddComponentMenu("UI (Canvas)/Toggle", 30)]
[RequireComponent(typeof(RectTransform))]
public class Toggle : Selectable, IMoveHandler, IPointerDownHandler, IPointerUpHandler, IPointerEnterHandler, IPointerExitHandler, ISelectHandler, IDeselectHandler, IPointerClickHandler, ISubmitHandler, IEventSystemHandler, ICanvasElement
```

备注：

Toggle 组件是一个 `Selectable`，负责控制一个显示开/关状态的子级 Graphic。当开关状态变化时，会向所有已注册的 `onValueChanged` 监听器发送回调。

## 构造函数

### Toggle()

声明：

```csharp
protected Toggle()
```

## 字段

### graphic

Toggle 应配合使用的 Graphic。

声明：

```csharp
public Graphic graphic
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Graphic` | |

### onValueChanged

支持基于委托的订阅，事件触发比 `eventReceiver` 更快，且可挂载多个接收者。

声明：

```csharp
public Toggle.ToggleEvent onValueChanged
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Toggle.ToggleEvent` | |

示例：

```csharp
//Attach this script to a Toggle GameObject. To do this, go to Create>UI>Toggle.
//Set your own Text in the Inspector window

using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    Toggle m_Toggle;
    public Text m_Text;

    void Start()
    {
        //Fetch the Toggle GameObject
        m_Toggle = GetComponent<Toggle>();
        //Add listener for when the state of the Toggle changes, to take action
        m_Toggle.onValueChanged.AddListener(delegate {
                ToggleValueChanged(m_Toggle);
            });

        //Initialise the Text to say the first state of the Toggle
        m_Text.text = "First Value : " + m_Toggle.isOn;
    }

    //Output the new state of the Toggle into Text
    void ToggleValueChanged(Toggle change)
    {
        m_Text.text =  "New Value : " + m_Toggle.isOn;
    }
}
```

### toggleTransition

Toggle 的过渡模式。

声明：

```csharp
public Toggle.ToggleTransition toggleTransition
```

字段值：

| 类型 | 说明 |
| --- | --- |
| `Toggle.ToggleTransition` | |

## 属性

### group

Toggle 所属的组。

声明：

```csharp
public ToggleGroup group { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `ToggleGroup` | |

### isOn

Toggle 当前是否处于开启状态。

声明：

```csharp
public bool isOn { get; set; }
```

属性值：

| 类型 | 说明 |
| --- | --- |
| `bool` | |

示例：

```csharp
//Attach this script to a Toggle GameObject. To do this, go to Create>UI>Toggle.
//Set your own Text in the Inspector window

using UnityEngine;
using UnityEngine.UI;

public class Example : MonoBehaviour
{
    Toggle m_Toggle;
    public Text m_Text;

    void Start()
    {
        //Fetch the Toggle GameObject
        m_Toggle = GetComponent<Toggle>();
        //Add listener for when the state of the Toggle changes, and output the state
        m_Toggle.onValueChanged.AddListener(delegate {
                ToggleValueChanged(m_Toggle);
            });

        //Initialize the Text to say whether the Toggle is in a positive or negative state
        m_Text.text = "Toggle is : " + m_Toggle.isOn;
    }

    //Output the new state of the Toggle into Text when the user uses the Toggle
    void ToggleValueChanged(Toggle change)
    {
        m_Text.text =  "Toggle is : " + m_Toggle.isOn;
    }
}
```

## 方法

### GraphicUpdateComplete()

当此 `ICanvasElement` 完成 Graphic 重建时发送的回调。

声明：

```csharp
public virtual void GraphicUpdateComplete()
```

### LayoutComplete()

当此 `ICanvasElement` 完成布局时发送的回调。

声明：

```csharp
public virtual void LayoutComplete()
```

### OnDestroy()

声明：

```csharp
protected override void OnDestroy()
```

重写：

`UIBehaviour.OnDestroy()`

### OnDidApplyAnimationProperties()

声明：

```csharp
protected override void OnDidApplyAnimationProperties()
```

重写：

`Selectable.OnDidApplyAnimationProperties()`

### OnDisable()

声明：

```csharp
protected override void OnDisable()
```

重写：

`Selectable.OnDisable()`

### OnEnable()

声明：

```csharp
protected override void OnEnable()
```

重写：

`Selectable.OnEnable()`

### OnPointerClick(PointerEventData)

响应点击。

声明：

```csharp
public virtual void OnPointerClick(PointerEventData eventData)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `PointerEventData` | `eventData` | |

### OnSubmit(BaseEventData)

声明：

```csharp
public virtual void OnSubmit(BaseEventData eventData)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `BaseEventData` | `eventData` | |

### OnValidate()

声明：

```csharp
protected override void OnValidate()
```

重写：

`Selectable.OnValidate()`

### Rebuild(CanvasUpdate)

为指定的 CanvasUpdate 阶段重建元素。

声明：

```csharp
public virtual void Rebuild(CanvasUpdate executing)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `CanvasUpdate` | `executing` | 当前正在重建的 CanvasUpdate 阶段。 |

### SetIsOnWithoutNotify(bool)

设置 `isOn` 而不调用 `onValueChanged` 回调。

声明：

```csharp
public void SetIsOnWithoutNotify(bool value)
```

参数：

| 类型 | 名称 | 说明 |
| --- | --- | --- |
| `bool` | `value` | `isOn` 的新值。 |

### Start()

确保呈现正确的视觉状态。

声明：

```csharp
protected override void Start()
```

重写：

`UIBehaviour.Start()`

## 实现的接口

- `IMoveHandler`
- `IPointerDownHandler`
- `IPointerUpHandler`
- `IPointerEnterHandler`
- `IPointerExitHandler`
- `ISelectHandler`
- `IDeselectHandler`
- `IPointerClickHandler`
- `ISubmitHandler`
- `IEventSystemHandler`
- `ICanvasElement`

---

# Toggle.ToggleEvent 类

## 继承关系

`object` → `UnityEventBase` → `UnityEvent<bool>` → `Toggle.ToggleEvent`

## 实现的接口

`ISerializationCallbackReceiver`

## 继承的成员

- `UnityEvent<bool>.AddListener(UnityAction<bool>)`
- `UnityEvent<bool>.RemoveListener(UnityAction<bool>)`
- `UnityEvent<bool>.FindMethod_Impl(string, Type)`
- `UnityEvent<bool>.Invoke(bool)`
- `UnityEventBase.FindMethod_Impl(string, object)`

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
[Serializable]
public class Toggle.ToggleEvent : UnityEvent<bool>, ISerializationCallbackReceiver
```

## 实现的接口

`ISerializationCallbackReceiver`

---

# Toggle.ToggleTransition 枚举

Toggle 被激活或停用时的显示设置。

命名空间：`UnityEngine.UI`

程序集：`UnityEngine.UI.dll`

## 语法

```csharp
public enum Toggle.ToggleTransition
```

## 字段

| 名称 | 说明 |
| --- | --- |
| `Fade` | 平滑地淡入/淡出 Toggle。 |
| `None` | 立即显示/隐藏 Toggle。 |

---

相关文档：[[UnityEngine-UI-ToggleGroup-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
