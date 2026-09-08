在 Unity 中，无论是 C# 还是 Lua（通过 XLua），设置 `Graphic.color` 的 RGB 值都非常直接。`Color` 结构体提供了多种构造方式，而不仅仅是预定义颜色（如 `Color.red`）。

---

### 🎨 方式一：使用 `Color(r, g, b)` 或 `Color(r, g, b, a)`

直接创建新的 `Color` 对象，传入 0~1 范围的浮点数。

#### Lua 示例（XLua）

lua

-- 设置 RGB 值（范围 0~1），Alpha 默认为 1
local img = self:GetComponent(typeof(CS.UnityEngine.UI.Image))
img.color = CS.UnityEngine.Color(1, 0, 0)  -- 红色
-- 指定 Alpha 通道
img.color = CS.UnityEngine.Color(0, 0.5, 0.2, 0.8)  -- 半透明绿色

#### C# 示例


```csharp
Image img = GetComponent<Image>();
img.color = new Color(1f, 0f, 0f);        // 红色
img.color = new Color(0.2f, 0.5f, 1f, 0.5f); // 自定义半透明白色
```


### 🔢 从 0~255 转换

如果你习惯于 0~255 的数值，需要除以 255 转换为 0~1。


```lua
local r = 128 / 255
local g = 64 / 255
local b = 32 / 255
img.color = CS.UnityEngine.Color(r, g, b)
```

---

### 🎯 方式二：使用十六进制字符串（HTML 颜色）

使用 `ColorUtility.TryParseHtmlString` 解析常见的颜色格式（如 `#FF0000`、`#FF0000FF`、`red`）。

```lua
local success, col = CS.UnityEngine.ColorUtility.TryParseHtmlString("#FF0000")  -- 红色
if success then
    img.color = col
end
```

---

### 📌 注意事项

- **取值范围**：`Color` 的 R/G/B/A 都是 `float`，范围 `[0, 1]`，超出会被钳制。
    
- **Alpha 通道**：如果只传三个参数，Alpha 默认为 `1`（不透明）。
    
- **性能**：在 Update 中频繁创建 `Color` 对象会有轻微开销，但通常可忽略。若需要频繁修改，可缓存一个 `Color` 变量再修改其值（如 `color.r = 0.5f`），但在 Lua 中修改需要确保不会影响其他引用。
    

---

### 🧪 示例：在按钮点击时随机变色

```lua

function OnComfrimClick()
    local img = self:GetComponent(typeof(CS.UnityEngine.UI.Image))
    local r = math.random()  -- 0~1 随机
    local g = math.random()
    local b = math.random()
    img.color = CS.UnityEngine.Color(r, g, b)
end
```
