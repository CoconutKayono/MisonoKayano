# 抖音虚拟世界：对 C# 的支持

> 一句话结论：平台**只接受 Lua 逻辑**，不能编写或携带自定义 C# 脚本 / 第三方 C# 插件；但 Lua 可以直接调用 **Unity 官方引擎的 C# API** 和 **SDK 提供的 C# 接口**（限定白名单命名空间）。

## 1. 官方规定（原话）

- **配置脚本环境**：「所有功能逻辑必须使用 Lua 脚本来编写，而非 C# 脚本。」
- **组件介绍**：「由于 SDK 在处理创作者所提交的世界时会**剔除非 SDK 内的 C# 脚本**，所以创作者目前**无法新建自己的 C# 组件或者使用第三方的 C# 插件**。」
- **云处理报错解决文档**：「SDK 暂不支持使用自定义 C# 组件，请尝试替换为官方提供组件。」

## 2. 支持 / 不支持一览

| 能力 | 是否支持 | 说明 |
| --- | --- | --- |
| 自己写 C# 脚本 / 自定义 C# 组件 | ❌ | 上传世界时会被剔除，不生效 |
| 使用第三方 C# 插件 | ❌ | 同样会被剔除 |
| Lua 调用 Unity 内置 C# API | ✅ | 限定白名单命名空间 |
| Lua 调用 SDK 官方组件（Douyin Script、Douyin Object Sync 等） | ✅ | 平台封装好的 C# 接口 |
| 美术资源（模型 / 材质 / Shader / 贴图） | ✅ | 不涉及脚本限制 |

所以「想用 C# 只能用 Lua 调用」准确的说法是：**没有你自己的 C# 代码可调，Lua 调的是平台允许的 Unity 官方 API 和 SDK 接口。**

## 3. Lua 如何调用 C#（Unity API）

调用规则（详见 [[03-Lua与C#比较]]）：

- 使用 API 时必须书写**完整命名空间**
- **静态方法用点 `.`**，**成员方法用冒号 `:`**
- `GetComponent` / `AddComponent` 需要在参数中加 `typeof`

```lua
-- 静态方法：用点
local obj = UnityEngine.GameObject.Find("ObjectName")

-- 成员方法：用冒号
local collider = obj:AddComponent(typeof(UnityEngine.BoxCollider))
local rigidbody = obj:GetComponent(typeof(UnityEngine.Rigidbody))

-- 通过 ---@var 声明 Unity 对象引用（仅支持继承自 UnityEngine.Object 的 class）
---@var tipPanel:UnityEngine.GameObject
---@end
```

## 4. 白名单与黑名单（Lua 能碰到的边界）

### 可用的 Unity 官方命名空间（白名单）

- `UnityEngine`
- `UnityEngine.UI`
- `UnityEngine.Events`
- `UnityEngine.AI`
- `UnityEngine.Audio`
- `UnityEngine.Video`
- `UnityEngine.Playables`
- `UnityEngine.Animations`
- `UnityEngine.Networking`

> ⚠️ 白名单之外的自定义命名空间、自定义组件、第三方模块，Lua 侧均不可访问。

### 被禁用的能力（黑名单节选）

- `System.IO`
- 反射：`GetType / GetMethod / GetField / Invoke` 等
- `System.Activator`、`System.AppDomain`、`System.GC`、`System.Console`
- `UnityEngine.Networking.UnityWebRequest`（命名空间在白名单，但该 API 禁用）
- Android / JNI：`AndroidJavaObject`、`AndroidJNI` 等
- Lua 标准库：`io`、`os.execute`、`os.exit`、`os.getenv`、`package.loadlib` 等

## 5. 常见误区

1. **“用 Lua 调用我写的 C#”**：不可能。没有你自己的 C# 代码存在于运行时，只有 Unity 官方 API 和 SDK 接口可调。
2. **“场景里能放 TextMeshPro，Lua 就能改”**：编辑器可以放 TMP 文本，但 `TMPro` 命名空间不在白名单，Lua 无法 `GetComponent(typeof(TMPro.TextMeshProUGUI))`；动态改文字请用 `UnityEngine.UI.Text`。
3. **“把 C# 脚本挂到物体上”**：不允许。Lua 脚本也要通过 **Douyin Script** 组件（C# 容器）挂载。
4. **“Lua 写不了复杂逻辑”**：Lua 脚本兼容 Unity MonoBehaviour 生命周期（Awake/Start/Update/OnTriggerEnter…），写法和 C# 脚本很像，只是语言不同。

## 6. 相关笔记

- [[03-Lua与C#比较]]（静态函数/成员函数、点与冒号）
- [[02-调用函数]]（static 用点，成员用冒号）
- [[01-a如何判断变量是否为空]]（判空规则）
- [[抖音虚拟世界-如何加载并实例化对象]]（Instantiate 与 NetSpawn 的边界）