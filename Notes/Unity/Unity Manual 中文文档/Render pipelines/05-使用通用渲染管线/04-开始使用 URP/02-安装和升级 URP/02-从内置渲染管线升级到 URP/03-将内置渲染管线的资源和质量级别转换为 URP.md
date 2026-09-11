# 将内置渲染管线的资源和质量级别转换为 URP

> 原文：[Convert assets and quality levels from the Built-In Render Pipeline to URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/convert-assets-to-urp.html)


在[[02-将 URP 安装到现有项目中]]后，使用[[06-使用渲染管线转换器转换资源]]，将为内置渲染管线项目制作的材质引用、着色器和质量级别转换为与通用渲染管线（URP）兼容的资源。

**注意**：渲染管线转换器不支持转换自定义着色器。有关转换自定义着色器的信息，请参阅[[04-升级自定义着色器以实现 URP 兼容性]]。

**警告**：以下任务会覆盖项目文件夹中的多个文件。Unity 覆盖后无法恢复这些文件。开始前，请备份所有不希望丢失的文件。

## 使用渲染管线转换器转换材质引用、着色器和质量级别

要将内置渲染管线的只读材质引用、预构建着色器和质量级别转换为 URP 资源，请执行以下操作：

1. 选择 **Window** > **Rendering** > **Render Pipeline Converter**。Unity 会打开[[06-使用渲染管线转换器转换资源]]窗口。
2. 将 **Source Pipeline** 设置为 **Built-in**。
3. 将 **Target Pipeline** 设置为 **Universal Render Pipeline (Universal Renderer)**。
4. 选中 **Material Reference Converter**、**Material Shader Converter** 和 **Rendering Settings** 旁的复选框。如果项目中有动画剪辑或 Post-Processing Stack v2 资源，也选中 **Animation Clip** 和 **Post-Processing Stack v2**。有关这些转换器的更多信息，请参阅[[06-使用渲染管线转换器转换资源]]。
5. 选择 **Scan**。Unity 会处理项目资源，并在所选转换器下显示可转换的材质和级别列表。
6. 选中要转换的资源旁的复选框。
7. 选择 **Convert Assets**。转换完成后，窗口会显示每次转换的状态。

URP 中的质量级别可能与内置渲染管线项目提供不同的性能。要手动更新质量级别以匹配之前的性能，请参阅[[05-将质量设置从内置渲染管线转换到 URP。]]。

有关 Unity 转换的材质引用、着色器和质量级别的更多信息，请参阅：

- [[07-URP 中的内置渲染管线材质引用]]
- [[08-使用渲染管线转换器将着色器转换为 URP]]

## 使用命令行转换资源

您可以使用 [Converters](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEditor.Rendering.Universal.Converters.html) 类的 [RunInBatchMode](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEditor.Rendering.Universal.Converters.html#UnityEditor_Rendering_Universal_Converters_RunInBatchMode_UnityEditor_Rendering_Universal_ConverterContainerId_) 方法从命令行运行转换过程。

使用 `RunInBatchModeCmdLine` 命令及以下命令和选项：

| **Command** | **Description** |
| --- | --- |
| `--help` | Shows help and exit. |
| `--list` | Lists all available containers and their converters. |
| **Option** | **Description** |
| --- | --- |
| `-container` | Defines the name of the container to be batched. This is required. Use the `--list` command to find the possible values. |
| `--inclusive` | Includes the list of converters specified with `-typesFilter` when batching. You must also provide values for `-typesFilter`. Using either `--inclusive` or `--exclusive` is required. Do not use both. |
| `--exclusive` | Excludes the list of converters specified with `-typesFilter` when batching. Using either `--inclusive` or `--exclusive` is required. Do not use both. |
| `-typesFilter` | Defines the list of converters to include or exclude from batching. These converters must be part of the container you pass in for them to run. Use the `--list` command to find the possible values. These values must be provided as a space-separated list, for example, `-typesFilter typeA typeB typeC`. Adding values is required when using `--inclusive`, and optional when using `--exclusive`. |

例如，以下命令会从命令行初始化并执行 **Material Reference Converter** 和 **Material Shader Converter**。

```shell
<path to Unity application> -projectPath <project path> -batchmode -executeMethod UnityEditor.Rendering.Universal.Converters.RunInBatchModeCmdLine -container BuiltInToURP -typesFilter Material --inclusive ReadonlyMaterial
```

## 使用 API/CLI 转换材质

**注意**：此方法已弃用。请改用。

You can also convert materials using the [Converters](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEditor.Rendering.Universal.Converters.html) class with [RunInBatchMode](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest/index.html?subfolder=/api/UnityEditor.Rendering.Universal.Converters.html#UnityEditor_Rendering_Universal_Converters_RunInBatchMode_UnityEditor_Rendering_Universal_ConverterContainerId_).

例如，以下脚本会初始化并执行 **Material Reference Converter** 和 **Material Shader Converter**。

```cs
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.Rendering.Universal;
using UnityEngine;

public class MyUpgradeScript : MonoBehaviour
{
    public static void ConvertBuiltinToURPMaterials()
    {
        Converters.RunInBatchMode(
            ConverterContainerId.BuiltInToURP
            , new List<ConverterId> {
                ConverterId.Material,
                ConverterId.ReadonlyMaterial
            }
            , ConverterFilter.Inclusive
        );
        EditorApplication.Exit(0);
    }
}
```

要从[命令行](https://docs.unity3d.com/6000.7/Documentation/Manual/EditorCommandLineArguments.html)运行示例转换，请使用以下命令：

```shell
"<path to Unity application> -projectPath <project path> -batchmode -executeMethod MyUpgradeScript.ConvertBuiltinToURPMaterials
```

## Additional resources

- [[02-将 URP 安装到现有项目中]]
- [[06-使用渲染管线转换器转换资源]]
- [[07-URP 中的内置渲染管线材质引用]]
- [[08-使用渲染管线转换器将着色器转换为 URP]]
- [[05-将质量设置从内置渲染管线转换到 URP。]]

---

## 文档导航

- 上一页：[[02-将 URP 安装到现有项目中]]
- 目录：[[00-从内置渲染管线升级到 URP]]
- 下一页：[[04-升级自定义着色器以实现 URP 兼容性]]
