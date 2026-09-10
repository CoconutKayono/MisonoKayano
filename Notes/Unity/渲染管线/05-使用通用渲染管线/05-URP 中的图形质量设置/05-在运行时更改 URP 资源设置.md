# 在运行时更改 URP 资源设置

> 原文：[Change URP asset settings at runtime](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/quality/change-urp-asset-settings.html)

可以通过 C# 脚本在运行时更改 URP 资源的部分属性。如果设备硬件与项目中的任何质量级别都不能完全匹配，这种方式可以帮助进一步微调性能。

> **注意**：要使用 C# 脚本更改 URP 资源的某个属性，该属性必须具有 `set` 方法。有关这些属性的更多信息，请参阅[通用渲染管线资源 API](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@17.2/api/UnityEngine.Rendering.Universal.UniversalRenderPipelineAsset.html#properties)。

以下示例使用 [[04-在运行时更改活动的 URP 资源#更改质量级别]] 中的 **QualityControls** 脚本和 **QualityController** 对象，并扩展其功能，以找到活动的 URP 资源并更改其中的部分属性，使其适应硬件的性能水平。

1. 打开 **QualityControls** 脚本。
2. 在脚本顶部添加 `using UnityEngine.Rendering` 和 `using UnityEngine.Rendering.Universal`。
3. 在 `QualityControls` 类中添加名为 `ChangeAssetProperties`、返回类型为 `void` 的方法，如下所示。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    using UnityEngine.Rendering;
    using UnityEngine.Rendering.Universal;
    
    public class QualityController : MonoBehaviour
    {
        void Start()
        {
            // 首先选择合适的质量级别
            SwitchQualityLevel();
    
        }
    
        private void SwitchQualityLevel()
        {
            // 此处使用前一个示例中的代码
        }
    
        private void ChangeAssetProperties()
        {
            // 将新代码添加到此方法中
        }
    }
    ```

4. 使用 `GraphicsSettings.currentRenderPipeline` 获取活动的渲染管线资源，如下所示。

    > **注意**：必须使用 `as` 关键字将渲染管线资源转换为 `UniversalRenderPipelineAsset` 类型，脚本才能正常工作。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    using UnityEngine.Rendering;
    using UnityEngine.Rendering.Universal;
    
    public class QualityController : MonoBehaviour
    {
        void Start()
        {
            // 首先选择合适的质量级别
            SwitchQualityLevel();
    
        }
    
        private void SwitchQualityLevel()
        {
            // 此处使用前一个示例中的代码
        }
    
        private void ChangeAssetProperties()
        {
            // 查找当前的 URP 资源
            UniversalRenderPipelineAsset data = GraphicsSettings.currentRenderPipeline as UniversalRenderPipelineAsset;
    
            // 如果 Unity 找不到 URP 资源，则不执行任何操作
            if (!data) return;
        }
    }
    ```

5. 在 `ChangeAssetProperties` 方法中添加 `switch` 语句，设置 URP 资源属性的值。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    using UnityEngine.Rendering;
    using UnityEngine.Rendering.Universal;
    
    public class QualityController : MonoBehaviour
    {
        void Start()
        {
            // 首先选择合适的质量级别
            SwitchQualityLevel();
    
        }
    
        private void SwitchQualityLevel()
        {
            // 此处使用前一个示例中的代码
        }
    
        private void ChangeAssetProperties()
        {
            // 查找当前的 URP 资源
            UniversalRenderPipelineAsset data = GraphicsSettings.currentRenderPipeline as UniversalRenderPipelineAsset;
    
            // 如果 Unity 找不到 URP 资源，则不执行任何操作
            if (!data) return;
    
            // 根据设备的显存大小更改 URP 资源设置
            switch (SystemInfo.graphicsMemorySize)
            {
                case <= 1024:
                    data.renderScale = 0.7f;
                    data.shadowDistance = 50.0f;
                    break;
                case <= 3072:
                    data.renderScale = 0.9f;
                    data.shadowDistance = 150.0f;
                    break;
                default:
                    data.renderScale = 0.7f;
                    data.shadowDistance = 25.0f;
                    break;
            }
        }
    }
    ```

6. 在 `Start` 方法中添加对 `ChangeAssetProperties` 方法的调用，确保只在场景首次加载时更改 URP 资源。

    ```csharp
    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;
    using UnityEngine.Rendering;
    using UnityEngine.Rendering.Universal;
    
    public class QualityController : MonoBehaviour
    {
        void Start()
        {
            // 首先选择合适的质量级别
            SwitchQualityLevel();
    
            // 通过具体的 URP 资源属性微调性能
            ChangeAssetProperties();
        }
    
        private void SwitchQualityLevel()
        {
            // 此处使用前一个示例中的代码
        }
    
        private void ChangeAssetProperties()
        {
            // 查找当前的 URP 资源
            UniversalRenderPipelineAsset data = GraphicsSettings.currentRenderPipeline as UniversalRenderPipelineAsset;
    
            // 如果 Unity 找不到 URP 资源，则不执行任何操作
            if (!data) return;
    
            // 根据设备的显存大小更改 URP 资源设置
            switch (SystemInfo.graphicsMemorySize)
            {
                case <= 1024:
                    data.renderScale = 0.7f;
                    data.shadowDistance = 50.0f;
                    break;
                case <= 3072:
                    data.renderScale = 0.9f;
                    data.shadowDistance = 150.0f;
                    break;
                default:
                    data.renderScale = 0.7f;
                    data.shadowDistance = 25.0f;
                    break;
            }
        }
    }
    ```

现在，当这个场景加载时，Unity 会检测系统的显存总量，并据此设置 URP 资源的属性。

可以将这种更改具体 URP 资源属性的方法与切换质量级别结合使用，为不同系统微调项目性能，而无需为每一种目标硬件配置单独创建质量级别。


## 官方代码示例补充（Unity 6000.7）

### 官方代码片段 1

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class QualityController : MonoBehaviour
{
    void Start()
    {
        // Select the appropriate Quality Level first
        SwitchQualityLevel();
    }

    private void SwitchQualityLevel()
    {
        // Code from previous example
    }

    private void ChangeAssetProperties()
    {
        // New code is added to this method
    }
}
```

### 官方代码片段 2

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class QualityController : MonoBehaviour
{
    void Start()
    {
        // Select the appropriate Quality Level first
        SwitchQualityLevel();
    }

    private void SwitchQualityLevel()
    {
        // Code from previous example
    }

    private void ChangeAssetProperties()
    {
        // Locate the current URP asset
        UniversalRenderPipelineAsset data = GraphicsSettings.currentRenderPipeline as UniversalRenderPipelineAsset;

        // Do nothing if Unity can't locate the URP asset
        if (!data) return;
    }
}
```

### 官方代码片段 3

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class QualityController : MonoBehaviour
{
    void Start()
    {
        // Select the appropriate Quality Level first
        SwitchQualityLevel();
    }

    private void SwitchQualityLevel()
    {
        // Code from previous example
    }

    private void ChangeAssetProperties()
    {
        // Locate the current URP asset
        UniversalRenderPipelineAsset data = GraphicsSettings.currentRenderPipeline as UniversalRenderPipelineAsset;

        // Do nothing if Unity can't locate the URP asset
        if (!data) return;

        // Change URP asset settings based on the size of the device's graphics memory
        switch (SystemInfo.graphicsMemorySize)
        {
            case <= 1024:
                data.renderScale = 0.7f;
                data.shadowDistance = 50.0f;
                break;
            case <= 3072:
                data.renderScale = 0.9f;
                data.shadowDistance = 150.0f;
                break;
            default:
                data.renderScale = 0.7f;
                data.shadowDistance = 25.0f;
                break;
        }
    }
}
```

### 官方代码片段 4

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class QualityController : MonoBehaviour
{
    void Start()
    {
        // Select the appropriate Quality Level first
        SwitchQualityLevel();

        // Fine tune performance with specific URP asset properties
        ChangeAssetProperties();
    }

    private void SwitchQualityLevel()
    {
        // Code from previous example
    }

    private void ChangeAssetProperties()
    {
        // Locate the current URP asset
        UniversalRenderPipelineAsset data = GraphicsSettings.currentRenderPipeline as UniversalRenderPipelineAsset;

        // Do nothing if Unity can't locate the URP asset
        if (!data) return;

        // Change URP asset settings based on the size of the device's graphics memory
        switch (SystemInfo.graphicsMemorySize)
        {
            case <= 1024:
                data.renderScale = 0.7f;
                data.shadowDistance = 50.0f;
                break;
            case <= 3072:
                data.renderScale = 0.9f;
                data.shadowDistance = 150.0f;
                break;
            default:
                data.renderScale = 0.7f;
                data.shadowDistance = 25.0f;
                break;
        }
    }
}
```

---

## 文档导航

- 上一页：[[04-在运行时更改活动的 URP 资源]]
- 目录：[[00-URP 中的图形质量设置]]
- 下一页：[[06-使用 URP 配置包配置设置]]