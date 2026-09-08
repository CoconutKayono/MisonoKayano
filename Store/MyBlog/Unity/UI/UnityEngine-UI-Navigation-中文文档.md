# Navigation 结构体（Scripting API）

**Navigation**：实现 IEquatable\<Navigation\> 的导航结构体。

## 继承成员（Inherited Members）

ValueType.Equals(object)、ValueType.GetHashCode()、ValueType.ToString()、object.Equals(object, object)、object.GetType()

命名空间（Namespace）：UnityEngine.UI

程序集（Assembly）：UnityEngine.UI.dll

## 语法（Syntax）

```csharp
[Serializable]
public struct Navigation : IEquatable<Navigation>
```

## 属性（Properties）

### defaultNavigation

返回一个带有合理默认值的 Navigation。

```csharp
public static Navigation defaultNavigation { get; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Navigation | 默认导航配置。 |

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI; // 使用 UI 元素时需要引入。

public class ExampleClass : MonoBehaviour
{
    public Button button;

    void Start()
    {
        // 将导航设置为默认值（"Automatic" 是默认值）。
        button.navigation = Navigation.defaultNavigation;
    }
}
```

### mode

导航模式（Navigation mode）。

```csharp
public Navigation.Mode mode { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Navigation.Mode | 导航模式。 |

### selectOnDown

指定按下下方向键时要高亮显示的 Selectable UI GameObject。

```csharp
public Selectable selectOnDown { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Selectable | 按下下方向键时高亮的目标。 |

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI;  // 使用 UI 元素时需要引入。

public class HighlightOnKey : MonoBehaviour
{
    public Button btnSave;
    public Button btnLoad;

    public void Start()
    {
        // 获取 Navigation 数据
        Navigation navigation = btnLoad.navigation;

        // 将模式切换为 Explicit，以允许自定义指定行为
        navigation.mode = Navigation.Mode.Explicit;

        // 按下下方向键时高亮显示 Save 按钮
        navigation.selectOnDown = btnSave;

        // 将结构体数据重新赋给按钮
        btnLoad.navigation = navigation;
    }
}
```

### selectOnLeft

指定按下左方向键时要高亮显示的 Selectable UI GameObject。

```csharp
public Selectable selectOnLeft { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Selectable | 按下左方向键时高亮的目标。 |

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI;  // 使用 UI 元素时需要引入。

public class HighlightOnKey : MonoBehaviour
{
    public Button btnSave;
    public Button btnLoad;

    public void Start()
    {
        // 获取 Navigation 数据
        Navigation navigation = btnLoad.navigation;

        // 将模式切换为 Explicit，以允许自定义指定行为
        navigation.mode = Navigation.Mode.Explicit;

        // 按下左方向键时高亮显示 Save 按钮
        navigation.selectOnLeft = btnSave;

        // 将结构体数据重新赋给按钮
        btnLoad.navigation = navigation;
    }
}
```

### selectOnRight

指定按下右方向键时要高亮显示的 Selectable UI GameObject。

```csharp
public Selectable selectOnRight { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Selectable | 按下右方向键时高亮的目标。 |

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI;  // 使用 UI 元素时需要引入。

public class HighlightOnKey : MonoBehaviour
{
    public Button btnSave;
    public Button btnLoad;

    public void Start()
    {
        // 获取 Navigation 数据
        Navigation navigation = btnLoad.navigation;

        // 将模式切换为 Explicit，以允许自定义指定行为
        navigation.mode = Navigation.Mode.Explicit;

        // 按下右方向键时高亮显示 Save 按钮
        navigation.selectOnRight = btnSave;

        // 将结构体数据重新赋给按钮
        btnLoad.navigation = navigation;
    }
}
```

### selectOnUp

指定按下上方向键时要高亮显示的 Selectable UI GameObject。

```csharp
public Selectable selectOnUp { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| Selectable | 按下上方向键时高亮的目标。 |

示例：

```csharp
using UnityEngine;
using System.Collections;
using UnityEngine.UI;  // 使用 UI 元素时需要引入。

public class HighlightOnKey : MonoBehaviour
{
    public Button btnSave;
    public Button btnLoad;

    public void Start()
    {
        // 获取 Navigation 数据
        Navigation navigation = btnLoad.navigation;

        // 将模式切换为 Explicit，以允许自定义指定行为
        navigation.mode = Navigation.Mode.Explicit;

        // 按下上方向键时高亮显示 Save 按钮
        navigation.selectOnUp = btnSave;

        // 将结构体数据重新赋给按钮
        btnLoad.navigation = navigation;
    }
}
```

### wrapAround

启用导航环绕功能：可以从最后一个元素循环到第一个元素，或从第一个元素循环到最后一个元素。在移动的相反方向上，会找到距离当前元素最远的元素。

```csharp
public bool wrapAround { get; set; }
```

属性值：

| 类型 | 描述 |
| --- | --- |
| bool | 是否启用导航环绕。 |

示例：

> 注意：如果有一个元素网格，而当前位于某一行最后一个元素上，导航不会环绕到下一行，而是会选中相反方向上距离最远的元素。

## 方法（Methods）

### Equals(Navigation)

```csharp
public bool Equals(Navigation other)
```

参数：

| 类型 | 名称 | 描述 |
| --- | --- | --- |
| Navigation | other | 要与之比较的 Navigation。 |

返回值：

| 类型 | 描述 |
| --- | --- |
| bool | 两者是否相等。 |

实现接口（Implements）：IEquatable\<T\>
