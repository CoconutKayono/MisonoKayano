# 使用 Universal Additional Camera Data 访问相机数据

> 原文：[Access camera data with the Universal Additional Camera Data component in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/universal-additional-camera-data.html)

Universal Additional Camera Data Component 是 Universal Render Pipeline（URP）用于存储内部数据的 Component。它允许 URP 扩展和覆盖 Unity 标准 Camera Component 的功能和外观。

在 URP 中，带有 Camera Component 的 GameObject 也必须带有 Universal Additional Camera Data Component。若项目使用 URP，Unity 会在创建 Camera GameObject 时自动添加 Universal Additional Camera Data Component。不能从 Camera GameObject 中移除 Universal Additional Camera Data Component。

如果不使用脚本控制和自定义 URP，则不需要对 Universal Additional Camera Data Component 执行任何操作。

如果使用脚本控制和自定义 URP，可以在脚本中这样访问 Camera 的 Universal Additional Camera Data Component：

```csharp
UniversalAdditionalCameraData cameraData = camera.GetUniversalAdditionalCameraData();
```

> [!NOTE]
> 要使用 `GetUniversalAdditionalCameraData()` 方法，必须使用 `UnityEngine.Rendering.Universal` namespace。在脚本顶部添加以下 statement：
>
> ```csharp
> using UnityEngine.Rendering.Universal;
> ```

有关更多信息，请参阅 [UniversalAdditionalCameraData API](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEngine.Rendering.Universal.UniversalAdditionalCameraData.html)。

如果在脚本中频繁访问 Universal Additional Camera Data Component，应缓存对它的 reference，以避免不必要的 CPU 工作。

> [!NOTE]
> 当 Camera 使用 Preset 时，只支持部分属性，不支持的属性会被隐藏。

---

## 文档导航

- 上一页：[[06-使用STP放大分辨率/03-STP Rendering Debugger参考]]
- 目录：[[00-URP中的相机]]
- 下一页：[[08-Camera Inspector窗口参考/00-Camera Inspector窗口参考]]
