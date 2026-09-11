# 在运行时更改活动的 URP 资源

> 原文：[Change the active URP asset at runtime](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/quality/quality-settings-through-code.html)

Unity 提供了多个预设的[质量设置级别](https://docs.unity3d.com/6000.7/Documentation/Manual/class-QualitySettings.html)，也可以为项目添加更多级别。为了适应不同的硬件规格，可以通过 C# 脚本切换这些级别及其关联的 URP 资源。以下示例展示如何使用 API 更改质量设置级别和活动的 URP 资源，以及如何在运行时更改 URP 资源中的具体设置。

> **注意**：应当只在性能并不关键的时机更改质量设置和 URP 资源设置，例如加载画面或静态菜单期间。这些更改会带来短暂但显著的性能影响。

## 更改活动的 URP 资源

每个质量级别都使用一个 URP 资源来控制许多具体的图形设置。可以为各个质量级别分配不同的 URP 资源，并在运行时切换。

### 配置项目质量设置

要使用质量设置切换 URP 资源，需要确保项目的不同质量级别配置为使用不同的 URP 资源。URP 3D 示例场景默认采用这种配置。

1. 为每个质量级别创建一个 URP 资源。在 **Project** 窗口中右键单击，选择 **Create** > **Rendering** > **URP Asset (with Universal Renderer)**。

    > **注意**：这些说明同样适用于使用 2D Renderer 的 URP 资源。

2. 根据需要配置新建的 URP 资源并为其命名。
3. 打开项目设置的质量部分：**Edit** > **Project Settings** > **Quality**。
4. 为每个质量级别分配 URP 资源。在 **Levels** 列表中选择一个质量级别，然后转到 **Rendering** > **Render Pipeline Asset**，选择为该质量级别创建的 URP 资源。对每个质量级别重复此操作。

现在，项目的质量级别已配置完成，可以用于在运行时切换 URP 资源。

### 更改质量级别

可以通过 [QualitySettings API](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/QualitySettings.html) 在运行时更改 Unity 使用的质量级别。按前述方式设置质量级别后，就可以同时切换 URP 资源和质量设置预设。

下面的简单示例使用 C# 脚本，根据系统的显存总量确定合适的质量级别。用户打开构建后的项目时，无需进行任何输入。

1. 创建名为 **QualityControls** 的 C# 脚本。
2. 打开 **QualityControls** 脚本，在 `QualityControls` 类中添加 `SwitchQualityLevel` 方法。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    
    public class QualityControls : MonoBehaviour
    {
        void Start()
        {
    
        }
    
        private void SwitchQualityLevel()
        {
    
        }
    }
    ```

3. 在 `SwitchQualityLevel` 方法中添加 `switch` 语句，使用 `QualitySettings.SetQualityLevel()` 方法选择质量级别，如下所示。

    > **注意**：每个质量级别都有一个索引，对应它在 **Project Settings** 窗口的 **Quality** 部分中所处的列表位置。列表顶部的质量级别索引为 0。此索引只计入为项目构建版本的目标平台启用的质量级别。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    
    public class QualityControls : MonoBehaviour
    {
        void Start()
        {
    
        }
    
        private void SwitchQualityLevel()
        {
            // 根据设备的显存大小选择质量设置级别（URP 资源）
            switch (SystemInfo.graphicsMemorySize)
            {
                case <= 2048:
                    QualitySettings.SetQualityLevel(1);
                    break;
                case <= 4096:
                    QualitySettings.SetQualityLevel(2);
                    break;
                default:
                    QualitySettings.SetQualityLevel(0);
                    break;
            }
        }
    }
    ```

4. 在 `Start` 方法中添加对 `SwitchQualityLevel` 方法的调用，确保只在场景首次加载时更改质量级别。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    
    public class QualityControls : MonoBehaviour
    {
        void Start()
        {
            SwitchQualityLevel();
        }
    
        private void SwitchQualityLevel()
        {
            // 根据设备的显存大小选择质量设置级别（URP 资源）
            switch (SystemInfo.graphicsMemorySize)
            {
                case <= 2048:
                    QualitySettings.SetQualityLevel(1);
                    break;
                case <= 4096:
                    QualitySettings.SetQualityLevel(2);
                    break;
                default:
                    QualitySettings.SetQualityLevel(0);
                    break;
            }
        }
    }
    ```

5. 打开构建后的项目启动时加载的第一个场景。
6. 创建一个空游戏对象，将其命名为 **QualityController**。在 **Hierarchy** 窗口中右键单击，选择 **Create Empty** 即可创建。
7. 在 **Inspector** 中打开 **QualityController** 对象。
8. 将 **QualityControls** 脚本作为组件添加到 **QualityController**。

现在，当这个场景加载时，Unity 会运行 **QualityControls** 脚本中的 `SwitchQualityLevel` 方法，检测系统显存总量并设置质量级别。该质量级别会将对应的 URP 资源设为活动的渲染管线资源。

可以创建更复杂的系统和一系列检查来确定使用哪个质量级别，但基本流程相同：项目启动时运行脚本，使用 [`QualitySettings.SetQualityLevel`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/QualitySettings.SetQualityLevel.html) 选择质量级别，进而选择项目在运行时使用的 URP 资源。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QualityControls : MonoBehaviour
{
    void Start()
    {
            
    }
        
    private void SwitchQualityLevel()
    {
        // Select Quality settings level (URP asset) based on the size of the device's graphics memory
        switch (SystemInfo.graphicsMemorySize)
        {
            case <= 2048:
                QualitySettings.SetQualityLevel(1);
                break;
            case <= 4096:
                QualitySettings.SetQualityLevel(2);
                break;
            default:
                QualitySettings.SetQualityLevel(0);
                break;
        }
    }
}
```

### 官方代码片段 2

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class QualityControls : MonoBehaviour
{
    void Start()
    {
        SwitchQualityLevel();
    }
        
    private void SwitchQualityLevel()
    {
        // Select Quality settings level (URP asset) based on the size of the device's graphics memory
        switch (SystemInfo.graphicsMemorySize)
        {
            case <= 2048:
                QualitySettings.SetQualityLevel(1);
                break;
            case <= 4096:
                QualitySettings.SetQualityLevel(2);
                break;
            default:
                QualitySettings.SetQualityLevel(0);
                break;
        }
    }
}
```

---

## 文档导航

- 上一页：[[03-在 URP 资源中显示高级属性]]
- 目录：[[00-URP 中的图形质量设置]]
- 下一页：[[05-在运行时更改 URP 资源设置]]