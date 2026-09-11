# 在 URP 中为计算着色器创建输入数据

> 原文：[Read input data into a compute shader in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/render-graph-compute-shader-input.html)


[[01-在 URP 中的渲染通道中运行计算着色器]]时，可以分配缓冲区来为计算着色器提供输入数据。

请遵循以下步骤：

1. 创建一个图形缓冲区，然后在通道数据中添加一个句柄。例如： `// Declare an input buffer public GraphicsBuffer inputBuffer; // Add a handle to the input buffer in your pass data class PassData { ... public BufferHandle input; } // Create the buffer in the render pass constructor public ComputePass(ComputeShader computeShader) { // Create the input buffer as a structured buffer // Create the buffer with a length of 5 integers, so you can input 5 values. inputBuffer = new GraphicsBuffer(GraphicsBuffer.Target.Structured, 5, sizeof(int)); }`
2. 设置缓冲区中的数据。例如： `var inputValues = new List<int> { 1, 2, 3, 4, 5 }; inputBuffer.SetData(inputValues);`
3. 使用 `ImportBuffer` 渲染图 API 将缓冲区转换为渲染图系统可以使用的句柄，然后在通道数据中设置 `BufferHandle` 字段。例如： `BufferHandle inputHandleRG = renderGraph.ImportBuffer(inputBuffer); passData.input = inputHandleRG;`
4. 使用 `UseBuffer` 方法可将缓冲区设置为渲染图形系统中的可读缓冲区。例如： `builder.UseBuffer(passData.input, AccessFlags.Read);`
5. 在 `SetRenderFunc` 方法中，使用 [SetComputeBufferParam](https://docs.unity3d.com/ScriptReference/Rendering.CommandBuffer.SetComputeBufferParam.html) API 将缓冲区附加到计算着色器。例如： `// The first parameter is the compute shader // The second parameter is the function that uses the buffer // The third parameter is the RWStructuredBuffer input variable to attach the buffer to // The fourth parameter is the handle to the input buffer context.cmd.SetComputeBufferParam(passData.computeShader, passData.computeShader.FindKernel("Main"), "inputData", passData.input);`

## 示例

有关完整示例，请参阅[[03-在 URP 中导入包示例]]中名为 **Compute** 的示例。

## 其他资源

- [计算着色器](https://docs.unity3d.com/6000.0/Documentation/Manual/class-ComputeShader.html)
- [编写着色器](https://docs.unity3d.com/6000.0/Documentation/Manual/shader-writing.html)


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
// Declare a buffer handle
BufferHandle m_InputBufferHandle;

// Add the handle to your pass data
class PassData
{
    public BufferHandle input;
    // ...
}

// Create the buffer in RecordRenderGraph
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
{
    // Create the input buffer as a structured buffer of 20 ints
    BufferDesc desc = new BufferDesc
    {
        name   = "InputBuffer",
        count  = 20,
        stride = sizeof(int),
        target = GraphicsBuffer.Target.Structured
    };

    m_InputBufferHandle = renderGraph.CreateBuffer(desc);
}
```

### 官方代码片段 2

```csharp
// Placeholder input data for the compute shader
private List<int> inputData = new List<int>();

// Initialize in the render pass constructor
public ComputePass()
{
    for (int i = 0; i < 20; i++)
    {
        inputData.Add(i);
    }
}
```

### 官方代码片段 3

```csharp
using (var builder = renderGraph.AddComputePass("ComputePass", out PassData passData))
{
    passData.input = m_InputBufferHandle;
    passData.bufferData = inputData;
}
```

### 官方代码片段 4

```csharp
// Upload input data to the Render Graph buffer
context.commandBuffer.SetBufferData(passData.input, passData.bufferData);

// Attach buffer to the compute shader

// The first parameter is the compute shader
// The second parameter is the function that uses the buffer
// The third parameter is the RWStructuredBuffer input variable to attach the buffer to
// The fourth parameter is the handle to the input buffer
context.commandBuffer.SetComputeBufferParam(passData.computeShader, passData.computeShader.FindKernel("Main"), "inputData", passData.input);
```


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
builder.UseBuffer(passData.input, AccessFlags.Read);
```

---

## 文档导航

- 上一页：[[01-在 URP 中的渲染通道中运行计算着色器]]
- 目录：[[00-在 URP 的渲染图系统中的计算着色器]]
- 下一页：[[08-在 URP 中分析渲染图]]
