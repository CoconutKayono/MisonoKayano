# 在 URP 中创建可编程渲染器功能

> 原文：[Inject a render pass with a Scriptable Renderer Feature in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/scriptable-renderer-features/inject-a-pass-using-a-scriptable-renderer-feature.html)


使用 `ScriptableRenderFeature` API 可将[[../01-URP 中的可编程渲染通道简介]]插入到通用渲染管线 (URP) 的帧渲染循环中。

请遵循以下步骤：

1. 创建一个新的 C# 脚本。
2. 将代码替换为继承自 `ScriptableRendererFeature` 类的类。 `using UnityEngine; using UnityEngine.Rendering.Universal; public class MyRendererFeature : ScriptableRendererFeature { }`
3. 在该类中，重写 `Create` 方法。例如： `public override void Create() { }` URP 会在以下事件中调用 `Create` 方法：
  - 首次加载可编程渲染器功能时。
  - 启用或禁用可编程渲染器功能时。
  - 在渲染器功能的**检视面板 (Inspector)** 窗口中更改属性时。

4. 在 `Create` 方法中，创建可编程渲染通道的实例，并将其注入渲染器。 例如，如果您有一个名为 `RedTintRenderPass` 的可编程渲染通道： `// Define an instance of the Scriptable Render Pass private RedTintRenderPass redTintRenderPass; public override void Create() { // Create an instance of the Scriptable Render Pass redTintRenderPass = new RedTintRenderPass(); // Inject the render pass after rendering the skybox redTintRenderPass.renderPassEvent = RenderPassEvent.AfterRenderingSkybox; }`
5. 需要重写 `AddRenderPasses` 方法。 `public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData) { }` URP 每帧调用 `AddRenderPasses` 方法，每个摄像机调用一次。
6. 使用 `EnqueuePass` API 将可编程渲染通道注入帧渲染循环。 `public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData) { renderer.EnqueuePass(redTintRenderPass); }`

现在，您可以将可编程渲染器功能添加到当前激活的 URP 资源中。更多信息,请参阅[[../02-通过 URP 中的渲染器功能添加预构建效果/01-向 URP 渲染器添加渲染器功能]]。

## 示例

以下是使用名为 `RedTintRenderPass` 的可编程渲染通道的可编程渲染器功能的完整示例代码。

```
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class MyRendererFeature : ScriptableRendererFeature
{
    private RedTintRenderPass redTintRenderPass;

    public override void Create()
    {
        redTintRenderPass = new RedTintRenderPass();
        redTintRenderPass.renderPassEvent = RenderPassEvent.AfterRenderingSkybox;
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        renderer.EnqueuePass(redTintRenderPass);
    }
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
if (renderingData.cameraData.cameraType == CameraType.Game)
{
    renderer.EnqueuePass(redTintRenderPass);
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using UnityEngine;
using UnityEngine.Rendering.Universal;

public class MyRendererFeature : ScriptableRendererFeature
{
}
```

### 官方代码片段 2

```csharp
public override void Create()
{
}
```

### 官方代码片段 3

```csharp
// Define an instance of the Scriptable Render Pass
private RedTintRenderPass redTintRenderPass;

public override void Create()
{
    // Create an instance of the Scriptable Render Pass
    redTintRenderPass = new RedTintRenderPass();

    // Inject the render pass after rendering the skybox
    redTintRenderPass.renderPassEvent = RenderPassEvent.AfterRenderingSkybox;
}
```

### 官方代码片段 4

```csharp
public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
{
}
```

---

## 文档导航

- 上一页：[[00-在 URP 中将可编程渲染通道添加到帧渲染循环]]
- 目录：[[00-在 URP 中将可编程渲染通道添加到帧渲染循环]]
- 下一页：[[02-在 URP 中通过脚本注入渲染通道]]
