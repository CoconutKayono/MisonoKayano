# Button 类（Scripting API）

**Button**：一种标准按钮，在被点击时发送事件。

## 继承关系（Inheritance）

object → UIBehaviour → Selectable → **Button**

## 实现接口（Implements）

IMoveHandler、IPointerDownHandler、IPointerUpHandler、IPointerEnterHandler、IPointerExitHandler、ISelectHandler、IDeselectHandler、IPointerClickHandler、ISubmitHandler、IEventSystemHandler

## 继承成员（Inherited Members）

Selectable.s_Selectables、Selectable.s_SelectableCount、Selectable.allSelectablesArray、Selectable.allSelectableCount、Selectable.allSelectables

命名空间（Namespace）：UnityEngine.UI

程序集（Assembly）：UnityEngine.UI.dll

## 语法（Syntax）

```csharp
[AddComponentMenu("UI (Canvas)/Button", 30)]
public class Button : Selectable, IMoveHandler, IPointerDownHandler, IPointerUpHandler, IPointerEnterHandler, IPointerExitHandler, ISelectHandler, IDeselectHandler, IPointerClickHandler, ISubmitHandler, IEventSystemHandler
```

## 构造函数（Constructors）

### Button()

```csharp
protected Button()
```

## 属性（Properties）

### onClick

按钮被按下时触发的 UnityEvent。

> 注意：该事件在同一个对象上先发生 MouseDown、随后发生 MouseUp 时触发。

```csharp
public Button.ButtonClickedEvent onClick { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Button.ButtonClickedEvent | 按钮点击事件。 |

示例：

```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class ClickExample : MonoBehaviour
{
    public Button yourButton;

    void Start()
    {
        Button btn = yourButton.GetComponent<Button>();
        btn.onClick.AddListener(TaskOnClick);
    }

    void TaskOnClick()
    {
        Debug.Log("You have clicked the button!");
    }
}
```

## 方法（Methods）

### OnPointerClick(PointerEventData)

调用所有已注册的 IPointerClickHandler。使用 IPointerClickHandler 注册按钮按下事件；也可以用它来判断点击类型（左键、右键等）。请确保场景中有一个 EventSystem。

```csharp
public virtual void OnPointerClick(PointerEventData eventData)
```

参数：

| 类型 | 名称 | 描述 |
| --- | --- | --- |
| PointerEventData | eventData | 与事件关联的指针数据，通常由事件系统提供。 |

示例：

```csharp
// 将此脚本挂载到 Button 游戏对象上
using UnityEngine;
using UnityEngine.EventSystems;

public class Example : MonoBehaviour, IPointerClickHandler
{
    // 检测是否发生了点击
    public void OnPointerClick(PointerEventData pointerEventData)
    {
        // 用于判断用户是否在按钮上点击了鼠标右键
        if (pointerEventData.button == PointerEventData.InputButton.Right)
        {
            // 在控制台输出被点击的游戏对象名称及以下消息。你可以将其替换为点击该游戏对象时要执行的操作。
            Debug.Log(name + " Game Object Right Clicked!");
        }

        // 用于判断用户是否在按钮上点击了鼠标左键
        if (pointerEventData.button == PointerEventData.InputButton.Left)
        {
            Debug.Log(name + " Game Object Left Clicked!");
        }
    }
}
```

### OnSubmit(BaseEventData)

调用所有已注册的 ISubmitHandler。

```csharp
public virtual void OnSubmit(BaseEventData eventData)
```

参数：

| 类型 | 名称 | 描述 |
| --- | --- | --- |
| BaseEventData | eventData | 与事件关联的数据，通常由事件系统提供。 |

备注（Remarks）：

当按钮通过你指定的“提交”（submit）键被选中时，将触发此事件（默认按键为回车键）。

要更改提交键，可以这样做：

- 进入 **Edit → Project Settings → Input**。
- 展开 **Axes** 区域，如果存在 **Submit** 区域则进入其中。
- 如果不存在 Submit，在 **Size** 字段中把数字加 1，这会在底部创建一个新区域。展开该新区域，把 **Name** 字段改为 “Submit”。
- 把 **Positive Button** 字段改为你想要的按键（例如空格键）。

或者：

- 在项目中找到你的 EventSystem。
- 在 Inspector 窗口中，把 **Submit Button** 字段改为 Input Manager 中的某个区域（例如 “Submit”），或者自己创建一个：先按你喜欢的方式命名，然后按照接下来的步骤操作。
- 进入 **Edit → Project Settings → Input** 打开 Input Manager。
- 在 Inspector 窗口中展开 **Axes** 区域，把 **Size** 字段的数字加 1，这会在底部创建一个新区域。
- 展开新区域，命名为与 EventSystem 的 **Submit Button** 字段中填写的名称一致。把 **Positive Button** 字段设置为你想要的按键（例如空格键）。
