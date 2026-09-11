> 原文：[MonoBehaviour.OnRenderImage](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnRenderImage.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnRenderImage

## 声明

~~~csharp
public void OnRenderImage(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| source | 包含源图像的 RenderTexture。 |
| destination | 要使用修改后图像进行更新的 RenderTexture。 |

## 描述

对最终图像进行后处理时调用。

## 示例

~~~csharp
using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    // A  Material  with the Unity shader you want to process the image with
    public  Material  mat;

    void OnRenderImage( RenderTexture  src,  RenderTexture  dest)
    {
        // Read pixels from the source  RenderTexture , apply the material, copy the updated results to the destination  RenderTexture 
         Graphics.Blit (src, dest, mat);
    }
}
~~~

---

## 文档导航

- 上一页：[[51-OnPreRender]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[53-OnRenderObject]]








