# 将 3D 角色渲染到 2D UI 上（Unity 中文文档）

## 1. 方案总览

Unity 的 UI（Canvas）基于 RectTransform 体系，**不能**直接把 3D 模型作为子物体放进 UI 层级。要把 3D 角色显示在 2D UI 上（角色立绘、捏脸预览、商店展示、头像等），主要有三种做法：

| 方案 | 原理 | 适用场景 | 推荐度 |
| --- | --- | --- | --- |
| **RenderTexture + RawImage** | 专用摄像机只渲染角色，输出到 RenderTexture，再由 UI 上的 RawImage 显示 | 需要实时动画、可交互、精确控制遮挡 | ★★★★★（推荐） |
| **World Space Canvas** | Canvas 放在 3D 世界中，角色作为场景物体站在面板前 | UI 与场景一体、需要透视和阴影 | ★★★ |
| **Screen Space - Camera 前摆放角色** | 角色放在主相机视野中，视觉上"靠近" UI | 临时展示、非正式功能 | ★ |

---

## 2. 方案一：RenderTexture + RawImage（推荐）

### 2.1 原理

角色与 UI 完全解耦：主摄像机照常渲染游戏画面，另有一个**角色专用摄像机**只渲染角色，把画面写入 RenderTexture；UI 上的 RawImage 每帧显示这张纹理。角色动画、换装、换材质都会实时反映在 UI 上。

因为最终显示的是一个 UI 元素（RawImage），所以它天然参与 UI 的层级排序和射线检测：可以放在任意 UI 兄弟节点之间，可以被其他 UI 遮挡，也可以响应点击。

### 2.2 操作步骤（编辑器）

1. **创建 RenderTexture**

   Project 窗口右键 → Create → Render Texture：

   - **Size**：按 UI 中实际显示尺寸设置（如 512×512 或 1024×1024）。移动端不要盲目开大。
   - **Color Format**：`ARGB32`（必须有 Alpha 通道，否则透明背景失效）。
   - **Depth Buffer**：16 或 24 位（角色需要深度缓冲）。

2. **给角色建专属 Layer**

   Project Settings → Tags and Layers 新建一个 Layer（如 `Character`），把角色根物体及其所有子物体设到这个 Layer。

3. **创建角色专用摄像机**

   - **Culling Mask**：只勾选 `Character` 层（只渲染角色）。
   - **Clear Flags**：`Solid Color`，背景色 **Alpha 设为 0**（内置管线下透明背景的关键）。
   - **Target Texture**：赋为第 1 步创建的 RenderTexture。
   - 调整摄像机位置、旋转、FOV（或正交 Size）完成取景。

4. **主摄像机排除角色层**

   在主摄像机的 Culling Mask 里取消勾选 `Character` 层，否则角色会同时出现在游戏场景中。

5. **UI 中放置 RawImage**

   在 Canvas 下创建 UI → Raw Image，把 RenderTexture 拖到 Texture 属性上。显示尺寸由 RectTransform 决定；如需保持画面比例，可以挂 `Aspect Ratio Fitter`（Aspect Mode 设为 Fit In Parent 等）。

### 2.3 代码示例

**C#**

```csharp
using UnityEngine;
using UnityEngine.UI;

public class CharacterPreviewUI : MonoBehaviour
{
    public Camera previewCamera;   // 角色专用摄像机（背景 Alpha=0，只渲染角色层）
    public RawImage rawImage;      // UI 上的 RawImage

    private RenderTexture rt;

    void Start()
    {
        // ARGB32：保证透明背景
        rt = new RenderTexture(512, 512, 24, RenderTextureFormat.ARGB32);
        rt.Create();

        previewCamera.targetTexture = rt;
        rawImage.texture = rt;
    }

    void OnDestroy()
    {
        if (rt != null)
        {
            previewCamera.targetTexture = null;
            rt.Release();
            Destroy(rt);
        }
    }
}
```

**Lua（XLua 环境）**

```lua
-- 场景中已摆好 previewCamera（角色专用摄像机，背景 Alpha=0，只渲染角色层）
-- UI 上已有一个 rawImage（UnityEngine.UI.RawImage）

local rt = CS.UnityEngine.RenderTexture(512, 512, 24, CS.UnityEngine.RenderTextureFormat.ARGB32)
rt:Create()

previewCamera.targetTexture = rt
rawImage.texture = rt

-- 之后切换展示角色：把新的模型放到 Character 层即可，previewCamera 会自动渲染它
```

### 2.4 透明背景的注意事项

- **背景色 Alpha 必须为 0**：Clear Flags 用 Solid Color 时，把颜色 Alpha 调成 0，否则 RawImage 会显示黑底/灰底。
- **URP 下不要给角色摄像机开后处理**：URP 的 Bloom、AO 等后处理会改写 RenderTexture 的 Alpha，导致透明背景失效。主场景相机开后处理不影响角色相机，但角色相机自身开了就会出问题。
- **HDR 建议关闭**：HDR 渲染会把亮度信息写进 Alpha，影响透明判定。
- 角色材质一般用不透明渲染（Opaque）；如果角色本身有半透明部分，要检查渲染顺序，必要时用专用 Shader 修正 Alpha 输出。

### 2.5 交互与遮挡

- RawImage 默认 `raycastTarget = true`，可以直接挂 Button，或监听 `IPointerClickHandler` 等指针事件。
- RawImage 在 UI 树中的位置决定遮挡关系：想让它"在面板后/前"，调整它在 Canvas 下的兄弟顺序即可。
- 若想实现"点角色身体的某一部分才响应"（精确到像素），RawImage 本身没有 alpha 测试；需要把屏幕点击坐标换算到 RenderTexture 的 UV，再采样纹理 Alpha 判断。

### 2.6 性能

- 每帧会额外渲染一个摄像机，移动端注意 RenderTexture 分辨率（512² 通常足够做立绘预览）。
- 不需要实时更新时，可以只在需要时把摄像机 `enabled` 打开一次再关闭，冻结画面。

---

## 3. 方案二：World Space Canvas

1. Canvas 的 Render Mode 设为 **World Space**，把 Canvas 面板摆到 3D 场景中合适的位置和大小。
2. 角色作为普通场景物体，站在面板前方。

优点：角色天然带透视、光照和阴影，和场景融为一体。

缺点：UI 和场景耦合，Camera 移动时面板要跟着布局；如果项目大部分 UI 是屏幕空间，混排比较麻烦。

---

## 4. 方案三：Screen Space - Camera 前摆放角色（不推荐）

把角色直接放在主摄像机视野内，让它"看起来"位于 UI 附近。这个方案无法精确控制遮挡顺序，角色会受主场景相机影响（雾、后处理、裁剪），一般只用于临时演示。

---

## 5. 常见问题

| 问题                  | 原因                                        | 解决                                                |
| ------------------- | ----------------------------------------- | ------------------------------------------------- |
| RawImage 黑底/灰底      | RenderTexture 没有 Alpha 通道，或背景色 Alpha 不是 0 | Color Format 用 `ARGB32`；Clear Flags 背景 Alpha 设为 0 |
| URP 下背景不透明          | 角色摄像机开了后处理                                | 关闭角色摄像机的后处理                                       |
| 角色在游戏场景里出现两份        | 主摄像机也渲染了角色层                               | 主摄像机 Culling Mask 排除角色层                           |
| RawImage 显示被拉伸      | RT 分辨率与 RawImage 宽高比不一致                   | 挂 Aspect Ratio Fitter，或让 RT 分辨率与显示尺寸同比例           |
| 透明边缘有白边/灰边          | HDR 或光照/材质导致 Alpha 异常                     | 关闭 HDR；检查材质是否输出正确 Alpha                           |
| 点击区域是整块矩形           | RawImage 是矩形 Graphic                      | 需要精确像素点击时做"屏幕坐标 → RT UV → Alpha 采样"               |
| Douyin平台下，摄像机运行时被删除 | Douyin SDK 会删除所有没记录的自定义摄像机                | 需要在Douyin World Root中添加自定义摄像机                     |

---

相关文档：[[UnityEngine-UI-Graphic-中文文档]]、[[02-02-UnityEngine-UI-GraphicRaycaster-中文文档]]
