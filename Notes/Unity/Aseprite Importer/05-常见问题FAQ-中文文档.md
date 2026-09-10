# 常见问题（Frequently asked questions）

> 来源：[Unity Package 官方文档 · Frequently asked questions](https://docs.unity3d.com/Packages/com.unity.2d.aseprite@6.0/manual/ImporterFAQ.html)
> 插图：来自 `MyBlog/Unity/UI/图片/Asprite/`

## Unity 中的图层是如何排序的？

当使用导入模式 **Individual**（独立图层）导入 Aseprite 文件时，源文件中的每个图层都会成为生成的模型预制件内的一个 GameObject。如果该图层是普通图层（而非组图层），则会为其添加 SpriteRenderer 组件。为确保每个 SpriteRenderer 的渲染顺序与 Aseprite 中一致，Unity 会自动为 SpriteRenderer 组件上的 **Order in Layer**（图层顺序）字段赋值。该值由两个变量组合而成：一是图层在 Aseprite 中的顺序，其中底部图层为 0，顶部图层为图层总数——例如源文件包含五个图层时，顶部图层的值为 5；二是 z-index，可以在 Aseprite 中按单元（cell）设置。Order in Layer 的最终计算公式为：从底部数起的图层数 + 当前单元的 Z-Index。

除了 Order in Layer 值之外，Unity 还会在模型预制件的根 GameObject 上添加 Sorting Group 组件，确保预制件内的每个 SpriteRenderer 一起排序。

关于 Unity 中 2D 排序的常规信息，请参阅 Unity 手册中的 2D Sorting 页面。

## 哪些操作会导致 Sprite 数据被覆盖？

在以下操作发生时，Aseprite Importer 会覆盖在 Sprite Editor 中自定义的 Sprite 数据：

- 更新以下任意导入器设置：
  - Pivot alignment（枢轴对齐）
  - Pivot space（枢轴空间）
  - Custom pivot point（自定义枢轴点）
  - Sprite padding（Sprite 填充）
- 更改了 Aseprite 中单元（cell）的尺寸。
- 打包纹理的尺寸发生了变化。
- 移除或重命名了图层。
- 导入模式设置为 TileSet。
- 为图层启用 UUID。

## 为图层启用 UUID

默认情况下，Aseprite Importer 通过图层的名称和路径来识别图层（和 Sprite）。Aseprite v1.3.14-beta1 引入了图层的唯一标识符。如果开启此功能，即使更改 Aseprite 中的图层名称，Sprite 数据也会保留。

要开启唯一标识符，请打开 Aseprite，进入 **Sprite > Properties...** 并勾选 **Create UUID for layers** 复选框。注意：这需要对每个 Aseprite 文件执行。

![为图层启用UUID](Faq_uuid_00.png)

## 如何将多个精灵表合并为一个？

你可以使用 Sprite Atlas 将多个精灵表合并为单个纹理。更多信息请参阅 Sprite Atlas 文档。将多个精灵表合并为一个，是减少场景中 Draw Call 的好方法。

## 为什么我的已裁剪 Aseprite 文件在 Unity 中没有被裁剪？

修改画布尺寸时，请确保勾选 **Trim content outside the canvas**（裁剪画布外的内容）复选框。这样存储的纹理就会被裁剪为指定尺寸。

![裁剪画布外的内容](Faq_TrimContent.png)

## 如何向 Animation Clip 添加事件？

通过在 Aseprite 中向单元（Cell）添加用户数据，可以生成动画事件。

按照以下步骤向帧添加动画事件：

1. 在 Aseprite 中，选择要添加事件的帧中的任意 cel（单元）。

   ![选择cel](Faq_AddEvents_00.png)

2. 右键点击该 cel，选择 **Cel Properties**。

   ![Cel属性](Faq_AddEvents_01.png)

3. 点击 Opacity（不透明度）滑块右侧的 **User Data** 按钮，打开 User Data 字段。

   ![用户数据按钮](Faq_AddEvents_02.png)

4. 按以下格式输入事件名称：`event:EventName`。例如 `event:OnIdle`。
5. 保存文件并切换到 Unity。
6. 打开 Animation 窗口并检查 Animation Clip。你可以看到事件已添加到帧中。

   ![Animation窗口中的事件](Faq_AddEvents_03.png)

要接收事件，请将以下脚本放在与 Animator 相同的 GameObject 上：

```csharp
using UnityEngine;

public class MyEventReceiver : MonoBehaviour
{
    // In our example, we created an event called "OnIdle".
    // This should be changed to the event name you specified in Aseprite.
    private void OnIdle()
    {
        Debug.Log("OnIdle was called.");
    }
}
```

### 为事件添加参数

你还可以为事件添加一个参数。我们支持以下数据类型：

- String（字符串）
- Integer（整数）
- Float（浮点数）

要为事件添加参数，请在事件名称后添加逗号（,），然后填写参数。例如：

```
event:MyIntEvent, 123
event:MyFloatEvent, 1.234f
event:MyStringEvent, "Hello"
```

> **注意**：如果在 Generate Assets（生成资源）设置中取消了 **Individual Events** 开关，事件中将不可用参数。通用事件（OnAnimationEvent）使用的唯一参数是一个字符串，其中包含来自 Aseprite User Data 的事件名称。

要接收带参数的事件，请将以下脚本放在与 Animator 相同的 GameObject 上：

```csharp
using UnityEngine;

public class MyEventReceiver : MonoBehaviour
{
    // In our example, we created an event called "MyEventReceiver" with a string parameter.
    // This should be changed to the event name and parameter type you specified in Aseprite.
    private void MyStringEvent(string data)
    {
        Debug.Log($"MyStringEvent was called with the data: {data}");
    }
}
```

### 为所有事件使用单一接收器

有时你希望在一个方法中接收来自 Animator 的所有动画事件。为此，首先在 Aseprite Importer Inspector 中取消勾选 **Individual Events** 开关。

![单一事件接收器](Faq_ComboEvents_00.png)

取消勾选 **Individual Events** 开关并点击 **Apply** 后，Aseprite Importer 会将所有事件的 AnimationClip 更新为使用事件字符串 "OnAnimationEvent"。

要接收事件，请将以下脚本放在与 Animator 相同的 GameObject 上：

```csharp
using UnityEngine;

public class MyEventReceiver : MonoBehaviour
{
    private void OnAnimationEvent(string eventName)
    {
        Debug.Log($"{eventName} was called.");
    }
}
```

> **注意**：如果在 Generate Assets（生成资源）设置中取消了 **Individual Events** 开关，事件中将不可用参数。通用事件（OnAnimationEvent）使用的唯一参数是一个字符串，其中包含来自 Aseprite User Data 的事件名称。

## 如何修改 Animator Controller？

如果 Aseprite 文件包含多个帧，并且导入器中勾选了 **Animation Clip** 复选框，Aseprite Importer 会生成一个 Animator Controller。此 Animator Controller 是只读的，无法更改。

![只读的Animator Controller](Faq_AnimController.png)

如果你希望拥有可以更改的 Animator Controller，请按以下步骤操作：

1. 在 Unity 中选择一个 Aseprite 文件。
2. 点击 **Export Animation Assets** 按钮。
3. 在弹出的窗口中，确保勾选 **Animator Controller** 复选框。如果你不想编辑任何剪辑，请保持 **Animation Clips** 复选框为未勾选。
4. 点击 **Export** 并选择一个文件夹来放置资源。

![导出动画资源弹窗](Faq_ExportPopup.png)

现在所选文件夹中应该有一个 Animator Controller。如果 **Animation Clips** 复选框保持未勾选，Animator Controller 内的所有状态都会链接回 Aseprite 文件，意味着剪辑会随着 Aseprite 中的任何更改保持最新。

请注意，如果你在 Aseprite 中添加了新标签，需要将生成的 Animation Clip 添加到导出的 Animator Controller 中，因为这不会自动发生。

## 如何在导入时注入自定义资源？

Aseprite Importer 带有一个事件 `OnPostAsepriteImport`，它在导入过程结束时触发。此事件可用于在导入 Aseprite 文件时注入或更改生成的资源。

```csharp
using UnityEditor;
using UnityEditor.U2D.Aseprite;
using UnityEngine;

public class GameObjectInjector : AssetPostprocessor
{
    void OnPreprocessAsset()
    {
        if (assetImporter is AsepriteImporter aseImporter)
            aseImporter.OnPostAsepriteImport += OnPostAsepriteImport;
    }

    static void OnPostAsepriteImport(AsepriteImporter.ImportEventArgs args)
    {
        var myGo = new GameObject("MyGameObject");
        args.context.AddObjectToAsset(myGo.name, myGo);
    }
}
```

## 如何禁用 Animation Clip 的循环？

默认情况下，从 Aseprite 标签生成的 Animation Clip 会自动循环。要禁用循环，请打开 Aseprite，打开要设为非循环的标签的 Tag Property 窗口。在 **Repeat** 字段中，将值从 `∞` 改为 `1`（Aseprite Importer 只支持循环和非循环两种结果，任何大于 1 的值仍然只会播放一次）。

![禁用循环设置](Faq_NonLoop_00.png)

在 Aseprite 中保存更改并切换到 Unity。Aseprite 文件会自动重新导入，Animation Clip 也会更新为非循环设置。
