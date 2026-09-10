# 使用 Shader Graph 创建自定义 UI 效果（Create Custom UI Effects With Shader Graph）

> 来源：[Unity UGUI 2.6 — Create Custom UI Effects With Shader Graph](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/HOWTO-ShaderGraph.html)  
> 官方源文件：[uGUI/Documentation~/HOWTO-ShaderGraph.md](https://github.com/Unity-Technologies/uGUI/blob/main/com.unity.ugui/Documentation~/HOWTO-ShaderGraph.md)  
> 整理日期：2026-09-05

Shader Graph 可以帮助你创建自定义的 UI 效果，包括动画背景和独特的 UI 元素。使用 Shader Graph，你可以把 Image 元素从静态变为动态，轻松定义自己的按钮状态外观。Shader Graph 还可以让你更好地控制 UI 的外观，并帮助你优化性能和纹理内存。

以下是一些可以通过 Shader Graph 在 uGUI（Unity UI）中实现的效果示例：

- 为你的用户界面创建微妙地旋转、流动或漂移的自定义背景。
- 仅凭一张灰度图像，即可定义按钮的视觉状态，如鼠标悬停、鼠标按下或未聚焦。
- 设计指示时间流逝的动画 HUD 元素。

## 基础（The Basics）

要为 Canvas UI 元素创建 Shader Graph 着色器，可以使用以下方法之一：

**修改现有的 Shader Graph：**

- 在 Shader Editor 中打开 Shader Graph。
- 在 Graph Settings 中，选择 HDRP Target。如果没有，请转到 Active Targets > Plus，然后选择 HDRP。
- 在 Material 下拉菜单中，选择 Canvas。

**创建新的 Shader Graph：**

- 转到 Assets > Create > Shader Graph > HDRP，然后选择 Canvas Shader Graph。

## 创建动画背景（Create Animated Backgrounds）

按照以下步骤为界面创建一个简单的动画背景。

1. 向图中添加两个 Sample Texture 2D 节点，并将它们设置为使用平铺的云朵纹理。我们将让它们以不同的方向和速度滚动。

![Background1.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background1.png)

2. 为每个 Sample Texture 2D 节点添加一个 Tiling and Offset 节点，并将其连接到 Sample Texture 2D 节点的 UV 输入端口。我们将使用 Offset 输入端口来添加滚动。

![Background2.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background2.png)

3. 为每个 Tiling and Offset 节点创建一个 Multiply 节点，并将其连接到 Offset 输入端口。

![Background3.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background3.png)

4. 对于第一个 Multiply 节点，创建一个连接到 A 输入端口的 Vector 2 节点，并将其设置为 0.2 和 0.13。对于第二个 Multiply 节点，创建一个连接到 B 输入端口的 Vector 2 节点，并将其设置为 -0.1 和 0.23。这些值控制滚动方向。

![Background4.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background4.png)

5. 创建一个 Time 节点，并将 Time 输出值乘以 0.3。该值用于调整效果的速度。

![Background5.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background5.png)

6. 将 Time 乘法节点的输出端口连接到另外两个 Multiply 节点。现在我们的纹理开始滚动了。

![Background6.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background6.png)

7. 创建一个新的 Blend 节点，用它混合两个 Sample Texture 2D 节点的输出。这将把两个纹理的贡献结合起来。

![Background7.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background7.png)

8. 添加一个 Lerp 节点，把 Blend 节点的输出接到 Lerp 的 T 输入。这将使用纹理贡献作为混合的遮罩。

![Background8.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background8.png)

9. 要使用动画遮罩混合这两种颜色，创建两个 Color 节点并连接到 Lerp 的 A 和 B 输入。按你的偏好设置颜色。

![Background9.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Background9.png)

10. 最后，将 Lerp 的输出连接到 Fragment Context Block 上的 Base Color 输入。

现在你就拥有一个动画背景着色器了。你可以通过更改颜色、更换所使用的纹理或控制速度来自定义它。

## 将着色器应用到 Canvas 元素（Apply the Shader to a Canvas Element）

按照以下步骤，将你创建的着色器应用到 Canvas UI 元素上。

1. 在 Project 窗口中右键单击你的 Shader Graph 资源，选择 Create > Material。给材质命名。

![CreateMaterial.png](Unity/UI/UGUI/Unity%20User%20Manual/images/CreateMaterial.png)

2. 确保场景中有 Canvas 元素。如果没有，在 Hierarchy 面板中右键单击，选择 UI (Canvas) > Canvas。

![CreateCanvas.png](Unity/UI/UGUI/Unity%20User%20Manual/images/CreateCanvas.png)

3. 向 Canvas 添加新的 Image 元素。右键单击 Canvas 元素，选择 UI > Image。

![CreateImage.png](Unity/UI/UGUI/Unity%20User%20Manual/images/CreateImage.png)

4. 在 Hierarchy 面板中选择 Image 元素。在 Inspector 窗口中，在 Material 槽位上选择 Browse。

![SelectMaterial.png](Unity/UI/UGUI/Unity%20User%20Manual/images/SelectMaterial.png)

5. 选择你在步骤 1 中创建的材质资源。

现在你的 Canvas 元素就使用了你创建的着色器。

## 向着色器传递自定义数据（Pass Custom Data into the Shader）

可以在 Shader Graph 着色器中获取自定义数据，例如 Canvas Image 元素的宽度和高度尺寸。你可以使用脚本轻松实现这一点，步骤如下：

1. 按照“将着色器应用到 Canvas 元素”中的步骤，创建材质并将其应用到 Canvas Image 元素。

2. 打开 Shader Graph 资源，然后选择右上角的 Blackboard，以访问 Blackboard 窗口。

![Blackboard.png](Unity/UI/UGUI/Unity%20User%20Manual/images/Blackboard.png)

3. 在 Blackboard 窗口中，点击右上角的 +，添加一个新的 Blackboard 参数。

4. 选择与你要传入的数据类型相匹配的数据类型。在本例中，添加一个 Vector 2 参数。

5. 将新参数命名为 “Size”。然后你可以把 Size 参数拖入图中，并根据需要加以使用。

![BlackboardToGraph.png](Unity/UI/UGUI/Unity%20User%20Manual/images/BlackboardToGraph.png)

6. 创建以下脚本，将 Canvas Image 的 Width 和 Height 值连接到着色器的 Size 参数：

```csharp
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Graphic))]
[ExecuteAlways]
public class ImageSize : MonoBehaviour
{
    private Image m_myCanvasImage;
    private void Start() 
    {
        m_myCanvasImage = GetComponent<Image>();
    }

#if UNITY_EDITOR
    void OnValidate() { UpdateMaterial(); }
#endif 

    private void FixedUpdate()
    {
        UpdateMaterial();
    }

    void UpdateMaterial()
    {
        if (m_myCanvasImage != null && m_myCanvasImage.material != null)
        {
            var imageRect = m_myCanvasImage.rectTransform.rect;
            var widthHeight = new Vector2(x: imageRect.width, y: imageRect.height);
            m_myCanvasImage.material.SetVector(name: "_Size", widthHeight);
        }
    }
}
```

7. 将脚本保存为 ImageSize.cs 并添加到项目中。

8. 在场景的 Hierarchy 面板中选择 Image 元素。

9. 在 Inspector 窗口中，选择 Add Component，然后选择 Scripts > Image Size。

![AddComponent.png](Unity/UI/UGUI/Unity%20User%20Manual/images/AddComponent.png)

Image 元素的 Rect Transform 中的 Width 和 Height 值会被传入材质的 Size 参数。现在你可以在着色器中使用它们了。
