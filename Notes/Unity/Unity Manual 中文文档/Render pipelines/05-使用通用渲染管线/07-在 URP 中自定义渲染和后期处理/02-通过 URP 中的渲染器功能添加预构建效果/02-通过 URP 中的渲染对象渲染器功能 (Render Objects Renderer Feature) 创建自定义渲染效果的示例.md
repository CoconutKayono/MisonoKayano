# 通过 URP 中的渲染对象渲染器功能 (Render Objects Renderer Feature) 创建自定义渲染效果的示例

> 原文：[Example of creating a custom rendering effect using a Render Objects Renderer Feature in URP](https://docs.unity3d.com/6000.7/Documentation/Manual/urp/renderer-features/how-to-custom-effect-render-objects.html)


URP 在 **DrawOpaqueObjects** 和 **DrawTransparentObjects** 通道中绘制对象。您可能需要在帧渲染中的不同点绘制对象，或者以其他方式解释和写入渲染数据（如深度和模板）。[[03-URP 的渲染对象渲染器功能 (Render Objects Renderer Feature) 参考]]允许您通过特定的覆盖在特定的图层上、特定的时间绘制对象来进行此类自定义。

本页上的示例说明如何使用渲染对象渲染器功能创建自定义渲染效果。

## 概述示例

本页的示例将演示如何实现以下效果：

- 场景中有一个角色。  ![Character](character.png) Character
- 当角色位于游戏对象后面时，Unity 会使用不同的材质绘制角色的轮廓。  ![角色位于游戏对象后面](character-goes-behind-object.gif) 角色位于游戏对象后面

## 先决条件

此示例需要满足以下条件：

- 安装了 URP 包的 Unity 项目。
- **Scriptable Render Pipeline Settings** 属性是指 URP 资源（**项目设置** (Project Settings) > **图形** (Graphics) > **可编程渲染管线设置** (Scriptable Render Pipeline Settings)）。

## 创建示例场景和游戏对象

要按照此示例中的步骤操作，请创建一个包含以下游戏对象的新场景：

1. 创建一个立方体。设置其 **Scale** 值，使其看起来像一堵墙。  ![代表墙壁的立方体](rendobj-cube-wall.png) 代表墙壁的立方体
2. 创建一个新材质并将其分配给 `Universal Render Pipeline/Lit` 着色器。选择基色（例如红色）。调用材质 `Character`。
3. 创建一个基本角色并为其分配 Character 材质。在此示例中，角色由三个胶囊体组成：中间的大胶囊体代表身体，两个较小的胶囊体代表双手。  ![角色由三个胶囊体组成](character-views-side-top-persp.png) 角色由三个胶囊体组成  为了更容易在场景中操作角色，请添加三个胶囊体作为 Character 游戏对象下的子游戏对象。  ![层级视图中的角色对象](character-in-hierarchy.png) 层级视图中的角色对象
4. 创建一个新材质并将其分配给 `Universal Render Pipeline/Unlit` 着色器。选择您希望角色位于游戏对象后面时具有的基色（例如蓝色）。调用材质 `CharacterBehindObjects`。

现在已经完成了执行此示例中的步骤所需的设置。

## 实现示例

此部分假设已创建一个场景，如部分所述。

此实现示例使用了两个渲染对象渲染器功能：一个用于绘制位于其他游戏对象后面的角色部分，另一个用于绘制位于其他游戏对象前面的角色部分。

### 创建一个渲染器功能来绘制游戏对象后面的角色

按照以下步骤创建一个渲染器功能来绘制游戏对象后面的角色。

1. 选择一个 URP 渲染器。  ![选择一个 URP 渲染器](rendobj-select-urp-renderer.png) 选择一个 URP 渲染器
2. 在检视器中，单击**添加渲染器功能 (Add Renderer Feature)** 然后选择**渲染器对象 (Render Objects)**。  ![添加渲染对象渲染器功能](rendobj-add-rend-obj.png) 添加渲染对象渲染器功能  选择 **Name** 字段，然后输入新渲染器功能的名称，例如 **DrawCharacterBehind**。
3. 此示例使用层来过滤要渲染的游戏对象。创建一个新层并将其命名为 **Character**。  ![创建一个名为 Character 的新层](rendobj-new-layer-character.png) 创建一个名为 Character 的新层
4. 选择 **Character** 游戏对象并将其分配到 `Character` 层。为此，请打开层下拉选单并选择 `Character`。![将 Character 游戏对象分配给 Character 层](rendobj-assign-character-gameobject-layer.png)
5. 在 `DrawCharacterBehind` 渲染器功能的 **Filters** > **Layer Mask** 中，选择 `Character`。使用此设置后，此渲染器功能仅在 `Character` 层中渲染游戏对象。
6. 在 **Overrides** > **Material** 中，选择 `CharacterBehindObjects` 材质。 渲染器功能使用选定的材质覆盖游戏对象的材质。  ![Layer Mask, Material Override](rendobj-change-layer-override-material.png) Layer Mask, Material Override
7. 预期的行为是，渲染器功能仅当字符位于其他游戏对象后面时才使用 `CharacterBehindObjects` 材质渲染字符。 为此，请选中 **Depth** 复选框，并将 **Depth Test** 属性设置为 **Greater**。  ![将 Depth Test 设置为 Greater](rendobj-depth-greater.png) 将 Depth Test 设置为 Greater

完成这些设置后，Unity 仅在角色位于另一个游戏对象后面时才使用 `CharacterBehindObjects` 材质渲染角色。但是，Unity 也使用 `CharacterBehindObjects` 材质渲染角色的某些部分，因为角色的一些部分会遮挡角色本身。

![Unity 使用 CharacterBehindObjects 材质渲染角色的某些部分](character-depth-test-greater.gif)

Unity 使用 CharacterBehindObjects 材质渲染角色的某些部分

### 创建额外渲染器功能以避免自我透视效果

由于以下原因，上一节中的设置会导致自透视效果：

- 在执行 URP 渲染器的不透明渲染通道时，Unity 使用 `Character` 材质来渲染属于角色的所有游戏对象，并将深度值写入深度缓冲区。这发生在 Unity 开始执行 `DrawCharacterBehind` 渲染器功能之前，因为默认情况下，新的渲染对象渲染器功能在 **Event** 属性中具有 **AfterRenderingOpaques** 值。  **Event** 属性定义了 Unity 从渲染对象渲染器功能注入渲染通道的注入点。URP 渲染器在 **Opaque Layer Mask** 中绘制游戏对象时的事件是 **BeforeRenderingOpaques** 事件。
- 在执行 `DrawCharacterBehind` 渲染器功能时，Unity 使用 **Depth Test** 属性中指定的条件执行深度测试。在下面的屏幕截图中，较大胶囊体遮挡了较小胶囊体的一部分，并且对于较小胶囊体的这个部分，通过了深度测试。渲染器功能会覆盖这个部分的材质。  ![自我透视效果](rendobj-depth-greater-see-through.png) 自我透视效果

以下步骤描述了如何避免此类行为并确保 Unity 使用正确的材质绘制角色的所有部分。

1. ![清除 Character 层旁边的复选标记](rendobj-in-urp-asset-clear-character.png) 清除 `Character` 层旁边的复选标记  现在，除非角色位于游戏对象后面，否则 Unity 不会渲染角色。  ![除非角色位于某个对象后面，否则 Unity 不会渲染角色](rendobj-character-only-behind.png) 除非角色位于某个对象后面，否则 Unity 不会渲染角色
  1. 在 URP 资源的 **Filtering** > **Opaque Layer Mask** 中，清除 `Character` 层旁边的复选标记。

2. 添加一个新的渲染对象渲染器功能，并将其命名为 `Character`。
3. 在 `Character` 渲染器功能的 **Filters** > **Layer Mask** 中，选择 `Character` 层。  ![将 Layer Mask Filter 设置为 Character 层](rendobj-render-objects-character.png) 将 Layer Mask Filter 设置为 Character 层  现在，即使角色位于游戏对象后面，Unity 也会使用 `Character` 材质渲染角色。 发生这种情况是因为 `DrawCharacterBehind` 渲染器功能将值写入深度缓冲区。当 Unity 执行 `Character` 渲染器功能时，角色上的像素看起来位于 Unity 先前绘制的像素之前，并且 Unity 在这些像素之上进行绘制。
4. 在 `DrawCharacterBehind` Renderer 功能的 **Overrides** > **Depth** 中，清除 **Write Depth** 复选框。使用此设置后，`DrawCharacterBehind` 渲染器功能不会对深度缓冲区进行更改，并且 `Character` 渲染器功能不会在角色位于游戏对象后面时绘制角色。  ![清除 Write Depth](rendobj-render-objects-no-write-depth.png) 清除 Write Depth

此示例已完成。当角色位于游戏对象后面时，Unity 会使用 `CharacterBehindObjects` 材质绘制角色的轮廓。

![角色位于对象后面](character-goes-behind-object.gif)

角色位于对象后面

使用额外的 `Character` 渲染器功能，Unity 按以下方式渲染游戏对象：

1. URP 渲染器不会在 **BeforeRenderingOpaques** 事件中渲染 `Character` 游戏对象，因为 `Character` 层不包括在 **Opaque Layer Mask** 列表中。
2. `DrawCharacterBehind` 渲染器功能可绘制角色位于其他游戏对象后面的部分。这发生在 **AfterRenderingOpaques** 事件中。
3. `Character` 渲染器功能可绘制角色位于其他游戏对象前面的部分。这发生在 **AfterRenderingOpaques** 事件中以及执行 `DrawCharacterBehind` 渲染器功能之后。

---

## 文档导航

- 上一页：[[01-向 URP 渲染器添加渲染器功能]]
- 目录：[[00-通过 URP 中的渲染器功能添加预构建效果]]
- 下一页：[[03-URP 的渲染对象渲染器功能 (Render Objects Renderer Feature) 参考]]
