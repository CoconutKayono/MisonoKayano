# 将 URP 渲染通道限制在场景区域内

> 原文：[Restrict a render pass to a scene area in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/customize/restrict-render-pass-scene-area.html)


要将渲染通道限制在场景的特定区域，请向场景添加一个[体积](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/volumes-landing-page.html)，然后在渲染通道和着色器中添加代码，检查摄像机是否位于该体积内。

请按以下步骤操作：

1. 更新着色器代码，使其根据布尔值启用或禁用自定义渲染效果。例如，在着色器中添加以下代码：`Pass { ... // 添加变量以启用或禁用自定义渲染效果 float _Enabled; ... float4 Frag(Varyings input) : SV_Target0 { ... // 变量为 1 时返回带效果的颜色，为 0 时返回原始颜色 if (_Enabled == 1){ return colorWithEffect; } else { return originalColor; } } }`
2. 创建实现 `VolumeComponent` 类的脚本。该脚本会创建一个可添加到体积的 Volume 覆盖组件：`using UnityEngine; using UnityEngine.Rendering; public class MyVolumeOverride : VolumeComponent { }`
3. 在 **Hierarchy** 窗口中选择 **Add**（**+**）按钮，然后选择 **GameObject** > **Volume** > **Box Volume**。
4. 在新建 Box Volume 的 **Inspector** 窗口中，在 **Volume** 下选择 **New**，创建新的 Volume Profile。
5. 选择 **Add override**，然后选择 Volume 覆盖组件，例如 **My Volume Override**。
6. 向 Volume 覆盖脚本添加属性。Unity 会在 Volume 覆盖组件的 **Inspector** 窗口中添加该属性。例如：`public class MyVolumeOverride : VolumeComponent { // 向 Volume Override 添加默认值为 true 的 Effect Enabled 复选框 public BoolParameter effectEnabled = new BoolParameter(true); }`
7. 在自定义通道中使用 `GetComponent` API 获取 Volume 覆盖组件，并检查属性值。例如：`class myCustomPass : ScriptableRenderPass { ... public void Setup(Material material) { // 获取 Volume 覆盖组件 MyVolumeOverride myOverride = VolumeManager.instance.stack.GetComponent<MyVolumeOverride>(); // 获取 Effect Enabled 属性的值 bool effectStatus = myOverride.effectEnabled.overrideState ? myOverride.effectEnabled.value : false; } }`
8. 将属性值传递给着色器代码中添加的变量。例如：`class myCustomPass : ScriptableRenderPass { ... public void Setup(Material material) { MyVolumeOverride myOverride = VolumeManager.instance.stack.GetComponent<MyVolumeOverride>(); bool effectStatus = myOverride.effectEnabled.overrideState ? myOverride.effectEnabled.value : false; // 将值传递给着色器 material.SetFloat("_Enabled", effectStatus ? 1 : 0); } }`

现在，当摄像机位于体积内时会启用自定义渲染效果；当摄像机位于体积外时会禁用该效果。

## 其他资源

- [编写可编程渲染通道](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/write-a-scriptable-render-pass.html)
- [URP 中的体积](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/volumes-landing-page.html)
- [在 URP 中编写自定义着色器](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/writing-custom-shaders-urp.html)
- [在 URP 中创建支持 Volume 的自定义后期处理效果](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/post-processing/custom-post-processing-with-volume.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
Pass
{
    ...

    // Add a variable to enable or disable your custom rendering effect
    float _Enabled;

    ...

    float4 Frag(Varyings input) : SV_Target0
    {
        ...

        // Return the color with the effect if the variable is 1, or the original color if the variable is 0
        if (_Enabled == 1){
            return colorWithEffect;
        } else {
            return originalColor;
        }
    }
}
```

### 官方代码片段 2

```csharp
public class MyVolumeOverride : VolumeComponent
{
    // Add an 'Effect Enabled' checkbox to the Volume Override, with a default value of true.
    public BoolParameter effectEnabled = new BoolParameter(true);
}
```

### 官方代码片段 3

```csharp
class myCustomPass : ScriptableRenderPass
{

    ...

    public void Setup(Material material)
    {
        // Get the volume override component
        MyVolumeOverride myOverride = VolumeManager.instance.stack.GetComponent<MyVolumeOverride>();

        // Get the value of the 'Effect Enabled' property
        bool effectStatus = myOverride.effectEnabled.overrideState ? myOverride.effectEnabled.value : false;
    }
}
```

### 官方代码片段 4

```csharp
class myCustomPass : ScriptableRenderPass
{

    ...

    public void Setup(Material material)
    {
        MyVolumeOverride myOverride = VolumeManager.instance.stack.GetComponent<MyVolumeOverride>();
        bool effectStatus = myOverride.effectEnabled.overrideState ? myOverride.effectEnabled.value : false;

        // Pass the value to the shader
        material.SetFloat("_Enabled", effectStatus ? 1 : 0);
    }
}
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using UnityEngine;
using UnityEngine.Rendering;

public class MyVolumeOverride : VolumeComponent
{
}
```

---

## 文档导航

- 上一页：[[02-在 URP 中通过脚本注入渲染通道]]
- 目录：[[00-在 URP 中将可编程渲染通道添加到帧渲染循环]]
- 下一页：[[04-URP 的注入点参考]]
