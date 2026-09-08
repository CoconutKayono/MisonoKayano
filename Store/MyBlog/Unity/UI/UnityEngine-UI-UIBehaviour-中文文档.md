# UIBehaviour 类（Scripting API）

**UIBehaviour**：对 Unity 生命周期函数提供受保护实现的基类行为（Base behaviour）。

## 继承关系（Inheritance）

object → Behaviour → MonoBehaviour → **UIBehaviour**

## 派生类（Derived）

以下类直接或间接继承自 UIBehaviour：

- [TextContainer](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/TMPro.TextContainer.html)
- [BaseInput](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.BaseInput.html)
- [BaseInputModule](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.BaseInputModule.html)
- [BaseRaycaster](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.BaseRaycaster.html)
- [EventSystem](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.EventSystem.html)
- [AspectRatioFitter](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.AspectRatioFitter.html)
- [BaseMeshEffect](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.BaseMeshEffect.html)
- [CanvasScaler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.CanvasScaler.html)
- [ContentSizeFitter](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.ContentSizeFitter.html)
- [Graphic](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.Graphic.html)
- [LayoutElement](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.LayoutElement.html)
- [LayoutGroup](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.LayoutGroup.html)
- [Mask](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.Mask.html)
- [RectMask2D](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.RectMask2D.html)
- [SafeArea](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.SafeArea.html)
- [ScrollRect](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.ScrollRect.html)
- [Selectable](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.Selectable.html)
- [ToggleGroup](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UI.ToggleGroup.html)
- [PanelEventHandler](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.UIElements.PanelEventHandler.html)

## 继承成员（Inherited Members）

MonoBehaviour.IsInvoking()、MonoBehaviour.CancelInvoke()、MonoBehaviour.Invoke(string, float)、MonoBehaviour.InvokeRepeating(string, float, float)、MonoBehaviour.CancelInvoke(string)

命名空间（Namespace）：[UnityEngine.EventSystems](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/api/UnityEngine.EventSystems.html)

程序集（Assembly）：UnityEngine.UI.dll

## 语法（Syntax）

```csharp
public abstract class UIBehaviour : MonoBehaviour
```

## 方法（Methods）

### Awake()

```csharp
protected virtual void Awake()
```

### IsActive()

如果 GameObject 和 Component 都处于激活状态，则返回 true。

```csharp
public virtual bool IsActive()
```

返回值：

| 类型 | 描述 |
| --- | --- |
| [bool](https://learn.microsoft.com/dotnet/api/system.boolean) | 对象与组件是否均处于激活状态。 |

### IsDestroyed()

如果该 behaviour 的原生表示（native representation）已被销毁，则返回 true。

```csharp
public bool IsDestroyed()
```

返回值：

| 类型 | 描述 |
| --- | --- |
| [bool](https://learn.microsoft.com/dotnet/api/system.boolean) | 行为是否已被销毁。 |

### OnBeforeTransformParentChanged()

```csharp
protected virtual void OnBeforeTransformParentChanged()
```

### OnCanvasGroupChanged()

```csharp
protected virtual void OnCanvasGroupChanged()
```

### OnCanvasHierarchyChanged()

当父级 Canvas 的状态发生变化时调用。

```csharp
protected virtual void OnCanvasHierarchyChanged()
```

备注（Remarks）：

当父级 Canvas 被启用或禁用，或嵌套 Canvas 的 OverrideSorting 属性发生变化时，会调用此函数。例如，你可以用它来修改某个 Canvas 下依赖于该父级 Canvas 的对象——比如当 Canvas 被禁用时，你可能希望暂停某个 UI 元素的处理。

### OnDestroy()

```csharp
protected virtual void OnDestroy()
```

### OnDidApplyAnimationProperties()

```csharp
protected virtual void OnDidApplyAnimationProperties()
```

### OnDisable()

```csharp
protected virtual void OnDisable()
```

### OnEnable()

```csharp
protected virtual void OnEnable()
```

### OnRectTransformDimensionsChange()

当关联的 RectTransform 的尺寸发生变化时，会调用此回调。它总是在 Awake、OnEnable 或 Start 之前被调用。该调用也会发送给所有子级 RectTransform，无论它们的尺寸是否发生变化（这取决于它们的锚定方式）。

```csharp
protected virtual void OnRectTransformDimensionsChange()
```

### OnTransformParentChanged()

```csharp
protected virtual void OnTransformParentChanged()
```

### OnValidate()

```csharp
protected virtual void OnValidate()
```

### Reset()

```csharp
protected virtual void Reset()
```

### Start()

```csharp
protected virtual void Start()
```
