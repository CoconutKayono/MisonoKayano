# 在 URP Render Loop 外渲染到 Render Texture

> 原文：[Render to a render texture outside the URP rendering loop](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/User-Render-Requests.html)

要在 Universal Render Pipeline（URP）Render Loop 外触发 Camera 渲染到 Render Texture，请在 C# 脚本中使用 `SingleCameraRequest` 和 `SubmitRenderRequest` API。

## 创建 Render Request

1. 创建 `UniversalRenderPipeline.SingleCameraRequest` 类型的 Render Request：

   ```csharp
   UniversalRenderPipeline.SingleCameraRequest request = new UniversalRenderPipeline.SingleCameraRequest();
   ```

2. 使用 [`RenderPipeline.SupportsRenderRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.RenderPipeline.SupportsRenderRequest.html) API 检查 Camera 是否支持该 Render Request 类型。例如检查主 Camera：

   ```csharp
   Camera mainCamera = Camera.main;

   if (RenderPipeline.SupportsRenderRequest(mainCamera, request))
   {
       // Camera 支持该 Render Request。
   }
   ```

3. 使用 Render Request 的 `destination` 参数，将 Camera 的 target 设置为 `RenderTexture` 对象：

   ```csharp
   request.destination = myRenderTexture;
   ```

4. 使用 [`SubmitRenderRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.RenderPipeline.SubmitRenderRequest.html) API 渲染到 Render Texture：

   ```csharp
   RenderPipeline.SubmitRenderRequest(mainCamera, request);
   ```

要确保所有 Camera 在渲染到 Render Texture 前完成渲染，可以使用以下任一方式：

- 使用等待帧结束的 coroutine。参阅 [`WaitForEndOfFrame`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WaitForEndOfFrame.html) API。
- 使用 callback。参阅 [`RenderPipelineManager.endContextRendering`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Rendering.RenderPipelineManager-endContextRendering.html) API。

## 示例

以下示例将多台 Camera 渲染到多个 Render Texture。使用示例的步骤如下：

1. 在 Unity 项目中创建名为 `SingleCameraRenderRequest.cs` 的 C# 脚本，并添加以下代码。
2. 将脚本添加到 Scene 中的 GameObject。
3. 在该 GameObject 的 Inspector 窗口中，分配 Camera 和 Render Texture。确保 Camera 数量与 Render Texture 数量相同。
4. 进入 Play mode。

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class SingleCameraRenderRequest : MonoBehaviour
{
    public Camera[] cameras;
    public RenderTexture[] renderTextures;

    void Start()
    {
        // 在启动 Component 前确保所有数据有效。
        if (cameras == null || cameras.Length == 0 || renderTextures == null || cameras.Length != renderTextures.Length)
        {
            Debug.LogError("Invalid setup");
            return;
        }

        // 启动异步 coroutine。
        StartCoroutine(RenderSingleRequestNextFrame());

        // Camera 完成渲染时调用 OnEndContextRendering 方法。
        RenderPipelineManager.endContextRendering += OnEndContextRendering;
    }

    void OnEndContextRendering(ScriptableRenderContext context, List<Camera> cameras)
    {
        // 输出日志，表示所有 Camera 已完成渲染。
        Debug.Log("All cameras have finished rendering.");
    }

    void OnDestroy()
    {
        // 取消 callback 订阅。
        RenderPipelineManager.endContextRendering -= OnEndContextRendering;
    }

    IEnumerator RenderSingleRequestNextFrame()
    {
        // 等待主 Camera 完成渲染。
        yield return new WaitForEndOfFrame();

        // 为每台 Camera 加入一个 Render Request。
        SendSingleRenderRequests();

        // 等待帧结束。
        yield return new WaitForEndOfFrame();

        // 重启 coroutine。
        StartCoroutine(RenderSingleRequestNextFrame());
    }

    void SendSingleRenderRequests()
    {
        // 遍历 cameras 数组。
        for (int i = 0; i < cameras.Length; i++)
        {
            UniversalRenderPipeline.SingleCameraRequest request =
                new UniversalRenderPipeline.SingleCameraRequest();

            // 检查当前 Render Pipeline 是否支持该 Render Request。
            if (RenderPipeline.SupportsRenderRequest(cameras[i], request))
            {
                // 将 Camera 输出的目标设置为对应的 RenderTexture。
                request.destination = renderTextures[i];

                // 同步将 Camera 输出渲染到 RenderTexture。
                RenderPipeline.SubmitRenderRequest(cameras[i], request);

                // 此时，renderTextures[i] 包含从 cameras[i] 中对应 Camera 视角渲染的 Scene。
            }
        }
    }
}
```

## 其他资源

- [[../00-URP中的相机|URP 中的相机]]
- [渲染到 Texture](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-texture-landing.html)

---

## 文档导航

- 上一页：[[06-将相机输出渲染到Render Texture]]
- 目录：[[00-多台相机]]
- 下一页：[[../04-相机渲染顺序]]
