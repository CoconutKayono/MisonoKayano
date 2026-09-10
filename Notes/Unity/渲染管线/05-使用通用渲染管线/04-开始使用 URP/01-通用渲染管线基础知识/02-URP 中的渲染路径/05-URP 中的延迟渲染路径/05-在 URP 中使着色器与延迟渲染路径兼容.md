# 在 URP 中使着色器与延迟渲染路径兼容

> 原文：[Make a shader compatible with the Deferred or Deferred+ rendering paths in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/rendering/make-shader-compatible-with-deferred.html)


## 在延迟渲染路径中使用着色器

要在延迟渲染路径中使用着色器，请将 `UniversalGBuffer` 标签添加到 ShaderLab（Unity 用于定义着色器对象结构的语言）代码中的通道。Unity 会在 G 缓冲区渲染通道期间执行该着色器。

例如：

```
Shader "Examples/ExamplePassFlag"
{
    SubShader
    {
        Pass
        {    
              Tags
              { 
                "RenderPipeline" = "UniversalPipeline"
                "LightMode" = "UniversalGBuffer"
              }
            
              // The rest of the code that defines the Pass goes here.
        }
    }
}
```

## 在延迟渲染路径的前向通道中使用着色器

要在延迟渲染路径的前向通道中使用着色器，请将 `UniversalForwardOnly` 和 `DepthNormalsOnly` 标签添加到 ShaderLab 代码中的通道。Unity 会在延迟渲染路径的前向通道期间执行该着色器。

例如：

```
Shader "Examples/ExamplePassFlag"
{
    SubShader
    {
        Pass
        {    
              Tags { 
                "RenderPipeline" = "UniversalPipeline"
                "LightMode" = "UniversalForwardOnly"
              }
            
              // The rest of the code that defines the Pass goes here.
        }
    }
}
```

## 指定着色器光照模型

要将着色器光照模型指定为光照 (Lit) 或简单光照 (Simple Lit)，需使用 `UniversalMaterialType` 标签。例如：

```
Shader "Examples/ExamplePassFlag"
{
    SubShader
    {
        Pass
        {    
              Tags
              { 
                "RenderPipeline" = "UniversalPipeline"
                "LightMode" = "UniversalGBuffer"
                "UniversalMaterialType" = "Lit" 
              }
            
              // The rest of the code that defines the Pass goes here.
        }
    }
}
```

## 其他资源

- [URP 中 ShaderLab 通道标签](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html)
- [ShaderLab 中通道标签的参考](https://docs.unity3d.com/6000.7/Documentation/Manual/SL-PassTags.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
Shader "Examples/ExamplePassFlag"
{
    SubShader
    {
        Pass
        {    
              Tags { 
                "RenderPipeline" = "UniversalPipeline"
                "LightMode" = "UniversalForwardOnly"
                "LightMode" = "DepthNormalsOnly"
              }
            
              // The rest of the code that defines the Pass goes here.
        }
    }
}
```

---

## 文档导航

- 上一页：[[04-延迟渲染路径简介]]
- 目录：[[00-URP 中的延迟渲染路径]]
- 下一页：[[../06-URP 中的 Forward+ 渲染路径的故障排除]]
