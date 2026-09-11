# NativeArrays

> 原文：[NativeArrays](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-native-pass-nativearrays.html)

NativeArrays 以及 [Unity.Collections](https://docs.unity3d.com/Packages/com.unity.collections@latest) Namespace 中的其他 Type，会将数据存储在不由 Scripting Runtime 管理的内存中。将指向这些数据的 Pointer 传递给 Native Code 时，不需要将 Buffer “pin” 在内存中。不过，仍然需要考虑数据的 Memory Lifetime，它由所使用的 [Allocator](https://docs.unity3d.com/Packages/com.unity.collections@2.5/manual/allocation.html) 决定：

| Allocator | Lifetime | Typical memory pool size |
| --- | --- | --- |
| Allocator.Temp | 内存在每一帧结束时自动清理。 | Main Thread 为 4–16 MB；Worker Thread 为 256 KB |
| Allocator.Persistent | 内存会一直保留，直到拥有该 Allocation 的 Object 被 Dispose。 |  |
| Allocator.Domain | 内存会一直保留，直到 C# Domain 被卸载。 |  |
| Allocator.TempJob | 内存会一直保留，直到拥有该 Allocation 的 Object 被 Dispose。TempJob Allocation 不应保留超过四帧。如果这种类型的内存耗尽，Unity 会回退到较慢的 Memory Allocation Method。 | 16–64 MB |
| Allocator.None | None Allocator 用于该 Instance 不拥有其所引用 Buffer 中内存的情况。 |  |

`Allocator.Temp` 通常是分配内存最快的方式，但只能使用到当前帧结束。如果分配的内存超过 Memory Pool 可用量，Unity 会回退到较慢的 Allocation Type。更多信息请参阅 [Unmanaged C# memory](https://docs.unity3d.com/Manual/performance-unmanaged-memory.html)。

NativeArray Struct 的 Layout 属于内部实现细节，因此无法控制其 Field 如何进行 Marshalling。不过，可以在 `unsafe` Context 中使用 Explicit Pointer，将指向 Array 内 Buffer 的 Pointer 传递出去。

## 使用 unsafe 获取 Array Pointer

使用 `NativeArray.GetUnsafePtr()` Method 或 [NativeArrayUnsafeUtility](https://docs.unity3d.com/ScriptReference/Unity.Collections.LowLevel.Unsafe.NativeArrayUnsafeUtility.html) Class，获取 NativeArray 中 Buffer 的 Pointer。将 Pointer 传递给 Unmanaged Function 时，可以像使用 C Array 一样处理它。

以下是一个将 `Color`（Unsigned 32-bit Integer）Array 作为参数的 Unmanaged Function：

```cpp
typedef int32_t Color;

extern "C" {
    void CheckerFill(Color* texture, int width, int height, int numSquares, const Color colors[], int numColors) {

        const int squareSize = width / numSquares;

        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                // Select a palette entry, staying within the bounds of the colors array
                const int colorIndex = ((y / squareSize) + (x / squareSize)) % numColors;
                texture[y * width + x] = colors[colorIndex];
            }
        }
    }
}
```

**Note**：关于将此类 Function 作为动态加载 Library 的一部分进行编译和调用时所需的 Annotation，请参阅 [[01-从托管代码调用非托管函数]]。

可以将 NativeArray Buffer 的 Pointer 传给该 Function。在 C# 中使用 Pointer 需要 `unsafe` Context。关于在 Unity 中启用 `unsafe` Code 编译的信息，请参阅 [[02-Managed Plug-in#编译 Unsafe C# Code]]。

以下 Code 演示如何调用 Unmanaged `CheckerFill()` Function。示例执行以下步骤：

1. 获取包含 Texture2D Object Pixel Data 的 NativeArray。
2. 使用 `GetUnsafePtr()` 获取 NativeArray Buffer 的 Pointer。
3. 调用 Unmanaged `CheckerFill()` Function，用 Checker Pattern 填充 Texture。
4. 将结果应用到 Texture2D Object。

```csharp
using UnityEngine;
using Unity.Collections;
using System.Runtime.InteropServices;
using Unity.Collections.LowLevel.Unsafe;

public class NativeArrayExamples
{
    // Change DllImport to use library name for
    // precompiled, dynamically linked libraries.
    [DllImport("__Internal")]
    static extern unsafe void CheckerFill(Color32* pixelDataPtr, int width, int height, int squares, [In] Color32[] colors, int numColors);

    public static void FillTextureWithCheckerboard(Texture2D texture, Color32 one, Color32 two, int squaresPerSide)
    {
        unsafe
        {
            // Get the pixel data as a NativeArray
            NativeArray<Color32> pixelData = texture.GetPixelData<Color32>(0);
            // Get a pointer to the NativeArray's buffer
            void* pixelBuffer = pixelData.GetUnsafePtr();
            // The color palette to choose from
            var palette = new Color32[] { one, two };
            // Call the unmanaged function, passing the palette length so it stays within the colors array
            CheckerFill((Color32*)pixelBuffer, texture.width, texture.height, squaresPerSide, palette, palette.Length);
            // Apply the changes to the texture
            texture.Apply(false);
        }
    }
}
```

**Note**：要安全地从 Unmanaged Code 访问 Array，必须传递其中包含的 Element 数量。在本例中，Code 传递 `numColors`（Color Palette 的长度），因此 Function 不会读取 `colors` Array 末尾之外的内容。Texture Array 的长度可以根据 `width` 和 `height` 参数计算，因此本例不显式传递其长度。

## Demonstration

可以使用以下 `MonoBehaviour` Class 调用 `NativeArrayExamples` 的 `FillTextureWithCheckerboard` Method。该示例使用 Unmanaged `CheckerFill` Function 生成 Texture，并将带有这些 Texture 的两个 GameObject Primitive 添加到 Scene 中。

```csharp
using UnityEngine;

public class DemoNativeArray : MonoBehaviour
{
    void Start()
    {
        AddCheckeredObject(PrimitiveType.Sphere, Color.blue,  Color.yellow, Vector3.zero);
        AddCheckeredObject(PrimitiveType.Cube, Color.red,  Color.white, Vector3.one);
    }

    void AddCheckeredObject(PrimitiveType primitive, Color colorOne, Color colorTwo, Vector3 position)
    {
        // Create a new texture
        Texture2D checkerboard = new Texture2D(256, 256, TextureFormat.RGBA32, false);
        // Fill the texture with a checkerboard pattern using the NativeArrayExamples class
        NativeArrayExamples.FillTextureWithCheckerboard(checkerboard, colorOne, colorTwo, 8);

        var go = GameObject.CreatePrimitive(primitive);
        go.transform.position = position;

        var litShader = Shader.Find("Universal Render Pipeline/Lit");
        if (litShader != null)
        {
            // Create a new material using the URP Lit shader
            Material material = new Material(litShader);
            // Assign the texture to the material
            material.SetTexture("_BaseMap", checkerboard);
            go.GetComponent<MeshRenderer>().material = material;
        }
        else
            Debug.LogError("Unable to load the Universal Render Pipeline/Lit shader.");
    }
}
```

**Notes**：

- 使用 `[DllImport("__Internal")]` 时，此示例需要 IL2CPP，且不能在 Editor Play Mode 中运行。要在 Play Mode 中运行示例，可以将 Unmanaged 示例 Code 编译为 Library，并将 `DLLImport` Statement 改为使用 Library Name。更多信息请参阅 [[04-DllImport属性]]。
- 此 Demonstration 在 Runtime 加载 URP Lit Shader。Build Process 会剥离未使用的 Shader 和 Variant，无法检测这种 Runtime Usage。运行此示例最简单的解决办法是在 Build 前向 Scene 中添加一个 Primitive Object。
- [`Texture2D.GetPixelData<T>`](https://docs.unity3d.com/ScriptReference/Texture2D.GetPixelData.html) 返回一个指向 Texture 现有内存的 NativeArray。它不分配内存，因此不需要 Dispose NativeArray。（Dispose 它不会产生任何效果。）

---

## 文档导航

- 上一页：[[03-结构体类和联合体]]
- 目录：[[00-传递数据]]
- 下一页：[[04-DllImport属性]]
