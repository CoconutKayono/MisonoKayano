# 在 URP 中的渲染通道中运行计算着色器

> 原文：[Write to and read output data from a compute shader in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-compute-shader-run.html)


要创建运行计算着色器的渲染通道，请执行以下操作：

1. 将渲染通道设置为使用计算着色器。
2. 添加输出缓冲区。
3. 传入并执行计算着色器。
4. 从输出缓冲区获取输出数据。

要检查平台是否支持计算着色器，请使用 [SystemInfo.supportsComputeShaders](https://docs.unity3d.com/ScriptReference/SystemInfo-supportsComputeShaders.html) API

## 将渲染通道设置为使用计算着色器

[[02-在 URP 中使用渲染图系统编写渲染通道]] 时，请执行以下操作：

1. 使用 `AddComputePass` 而不是 `AddRasterRenderPass`。
2. 使用 `ComputeGraphContext` 而不是 `RasterGraphContext`。

例如：

```
class ComputePass : ScriptableRenderPass
{
    ...

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer contextData)
    {
        ...
        // Use AddComputePass instead of AddRasterRenderPass.
        using (var builder = renderGraph.AddComputePass("MyComputePass", out PassData data))
        {
            ...

            // Use ComputeGraphContext instead of RasterGraphContext.
            builder.SetRenderFunc((PassData data, ComputeGraphContext context) => ExecutePass(data, context));

            ...
        }
    }
}
```

## 添加输出缓冲区

要创建计算着色器输出到的缓冲区，请遵循以下步骤：

1. 创建一个图形缓冲区，然后在通道数据中添加一个句柄。 `// Declare an output buffer public GraphicsBuffer outputBuffer; // Add a handle to the output buffer in your pass data class PassData { public BufferHandle output; } // Create the buffer in the render pass constructor public ComputePass(ComputeShader computeShader) { // Create the output buffer as a structured buffer // Create the buffer with a length of 5 integers, so the compute shader can output 5 values. outputBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, 5, sizeof(int)); }`
2. 使用 `ImportBuffer` 渲染图 API 将缓冲区转换为渲染图系统可以使用的句柄，然后在通道数据中设置 `BufferHandle` 字段。例如： `BufferHandle outputHandleRG = renderGraph.ImportBuffer(outputBuffer); passData.output = outputHandleRG;`
3. 使用 `UseBuffer` 方法可将缓冲区设置为渲染图形系统中的可写缓冲区。 `builder.UseBuffer(passData.output, AccessFlags.Write);`

## 传入并执行计算着色器

请遵循以下步骤：

1. 将计算着色器传递到渲染通道。例如，在 `ScriptableRendererFeature` 类中，显示 `ComputeShader` 属性，然后将计算着色器传递给渲染通道类。
2. 将 `ComputeShader` 字段添加到通道数据，并将其设置为计算着色器。例如： `// Add a `ComputeShader` field to your pass data class PassData { ... public ComputeShader computeShader; } // Set the `ComputeShader` field to the compute shader passData.computeShader = yourComputeShader;`
3. 在 `SetRenderFunc` 方法中，使用 [SetComputeBufferParam](https://docs.unity3d.com/ScriptReference/Rendering.CommandBuffer.SetComputeBufferParam.html) API 将缓冲区附加到计算着色器。例如： `// The first parameter is the compute shader // The second parameter is the function that uses the buffer // The third parameter is the StructuredBuffer output variable to attach the buffer to // The fourth parameter is the handle to the output buffer context.cmd.SetComputeBufferParam(passData.computeShader, passData.computeShader.FindKernel("Main"), "outputData", passData.output);`
4. 使用 [DispatchCompute](https://docs.unity3d.com/ScriptReference/Rendering.CommandBuffer.DispatchCompute.html) API 执行计算着色器。 `context.cmd.DispatchCompute(passData.computeShader, passData.computeShader.FindKernel("CSMain"), 1, 1, 1);`

## 从输出缓冲区获取输出数据

要从输出缓冲区获取数据，请使用 [GraphicsBuffer.GetData](https://docs.unity3d.com/ScriptReference/GraphicsBuffer.GetData.html) API。

只有在渲染通道执行和计算着色器运行完毕后，才能获取数据。

例如：

```
// Create an array to store the output data
outputData = new int[5];

// Copy the output data from the output buffer to the array
outputBuffer.GetData(outputData);
```

## 示例

有关完整示例，请参阅[[03-在 URP 中导入包示例]]中名为 **Compute** 的示例。

## 其他资源

- [计算着色器](https://docs.unity3d.com/6000.0/Documentation/Manual/class-ComputeShader.html)
- [编写着色器](https://docs.unity3d.com/6000.0/Documentation/Manual/shader-writing.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
class ComputePass : ScriptableRenderPass
{
    ...

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer contextData)
    {
        ...
        // Use AddComputePass instead of AddRasterRenderPass.
        using (var builder = renderGraph.AddComputePass("MyComputePass", out PassData data))
        {
            ...

            // Use ComputeGraphContext instead of RasterGraphContext.
            builder.SetRenderFunc(static (PassData data, ComputeGraphContext context) => ExecutePass(data, context));

            ...
        }
    }
}
```

### 官方代码片段 2

```csharp
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
{
    // Create the output buffer as a structured buffer of 20 ints
    BufferDesc desc = new BufferDesc
    {
        name   = "OutputBuffer",
        count  = 20,
        stride = sizeof(int),
        target = GraphicsBuffer.Target.Structured
    };

    m_OutputBufferHandle = renderGraph.CreateBuffer(desc);

        
    // Add the compute pass
    using (var builder = renderGraph.AddComputePass("ComputePass", out PassData passData))
    {
        // Set the pass data
        passData.output = m_OutputBufferHandle;
    }
}
```

### 官方代码片段 3

```csharp
// The first parameter is the compute shader
// The second parameter is the function that uses the buffer
// The third parameter is the StructuredBuffer output variable to attach the buffer to
// The fourth parameter is the handle to the output buffer
context.commandBuffer.SetComputeBufferParam(passData.computeShader, passData.computeShader.FindKernel("Main"), "outputData", passData.output);
```

### 官方代码片段 4

```csharp
context.commandBuffer.DispatchCompute(passData.computeShader, passData.computeShader.FindKernel("Main"), 1, 1, 1);
```

### 官方代码片段 5

```csharp
// Data container for the pass that reads back from the GPU
class ReadbackPassData
{
    // The buffer to read back from
    public BufferHandle processedDataBuffer;
}
```

### 官方代码片段 6

```csharp
passData.processedDataBuffer = m_OutputBufferHandle;
```

### 官方代码片段 7

```csharp
// Declare read access to the buffer
builder.UseBuffer(passData.processedDataBuffer, AccessFlags.Read);
```

### 官方代码片段 8

```csharp
context.commandBuffer.RequestAsyncReadback(passData.processedDataBuffer, (AsyncGPUReadbackRequest request) =>
{  
    // Get the data
    int result = request.GetData<int>();
})
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
builder.UseBuffer(passData.output, AccessFlags.Write);
```

### 官方代码片段 2

```csharp
// Add a `ComputeShader` field to your pass data
class PassData
{
    ...
    public ComputeShader computeShader;
}

// Set the `ComputeShader` field to the compute shader
passData.computeShader = yourComputeShader;
```

---

## 文档导航

- 上一页：[[00-在 URP 的渲染图系统中的计算着色器]]
- 目录：[[00-在 URP 的渲染图系统中的计算着色器]]
- 下一页：[[02-在 URP 中为计算着色器创建输入数据]]
