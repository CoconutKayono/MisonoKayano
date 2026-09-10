# 在 Camera Stack 中添加、移除和排序相机

> 原文：[Add and remove cameras in a camera stack in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/cameras/add-and-remove-cameras-in-a-stack.html)

Camera Stack 包含一台 Base Camera，以及叠加在其上的一台或多台 Overlay Camera。在 Editor 中，可以按需添加、移除和重新排列这些 Camera，以实现所需效果。

## 将 Camera 添加到 Camera Stack

### 使用 Inspector 添加

1. 在 Scene 中选择一台 **Render Type** 设置为 **Base** 的 Camera，使它成为 Base Camera。如果 Scene 中没有 Base Camera，请创建一台。
2. 在 Scene 中创建另一台 Camera，并选择它。
3. 在 Camera Inspector 窗口中，将 **Render Type** 设置为 **Overlay**。
4. 再次选择 Base Camera。在 Camera Inspector 窗口中进入 **Stack** 区域，选择 **Add**（**+**），然后选择 Overlay Camera 的名称。

Overlay Camera 现在属于 Base Camera 的 Camera Stack。Unity 会将 Overlay Camera 的输出绘制在 Base Camera 的输出之上。

> [!NOTE]
> 创建多台 Camera 组成 Camera Stack 时，应考虑每台 Camera 是否都必要。添加的每台 Camera 都会使渲染变慢，因为 active Camera 即使没有渲染任何内容，也会执行完整的 Render Loop。

### 使用 C# 脚本添加 Camera

使用 Base Camera 的 [Universal Additional Camera Data](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.UniversalAdditionalCameraData.html) Component 的 `cameraStack` 属性：

```csharp
var cameraData = camera.GetUniversalAdditionalCameraData();
cameraData.cameraStack.Add(myOverlayCamera);
```

## 从 Camera Stack 移除 Camera

### 使用 Inspector 移除

1. 创建一个至少包含一台 Overlay Camera 的 Camera Stack。
2. 选择该 Camera Stack 的 Base Camera。
3. 在 Camera Inspector 窗口中进入 **Stack** 区域，选择要移除的 Overlay Camera 名称，然后选择 **Remove**（**-**）。

Overlay Camera 仍保留在 Scene 中，但不再属于该 Camera Stack。

### 使用 C# 脚本移除 Camera

使用 Base Camera 的 Universal Additional Camera Data Component 的 `cameraStack` 属性：

```csharp
var cameraData = camera.GetUniversalAdditionalCameraData();
cameraData.cameraStack.Remove(myOverlayCamera);
```

## 重新排列 Camera Stack 中的 Camera

### 使用 Inspector 排序

1. 创建一个包含多台 Overlay Camera 的 Camera Stack。
2. 选择 Camera Stack 中的 Base Camera。
3. 在 Camera Inspector 中进入 **Stack** 区域。
4. 使用 Overlay Camera 名称旁边的拖动手柄重新排列 Overlay Camera 列表。

Base Camera 负责渲染 Camera Stack 的基础层，Stack 中的 Overlay Camera 会按照列表从上到下的顺序依次绘制在基础层之上。

### 使用 C# 脚本排序

使用 Base Camera 的 Universal Additional Camera Data Component 的 `cameraStack` 属性。`cameraStack` 是一个 `List`，可以像重新排列其他 `List` 一样重新排列它。

---

## 文档导航

- 上一页：[[02-设置Camera Stack]]
- 目录：[[00-多台相机]]
- 下一页：[[04-设置分屏渲染]]
