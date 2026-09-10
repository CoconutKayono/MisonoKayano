# 官方 UI 关闭与自定义 UI 接入

## 1. 结论

如果希望关闭抖音虚拟世界提供的全部官方 UI，建议同时调用：

```lua
function HideAllOfficialUI()
    -- 隐藏 Native 层官方 UI：操作按钮、平台功能按钮等
    DouyinUIService.SetNativeUIVisible(false)

    -- 隐藏 Unity 层官方 UI：主界面、聊天等 Unity UI
    DouyinUIService.SetUIVisible(false)
end
```

恢复官方 UI：

```lua
function ShowAllOfficialUI()
    DouyinUIService.SetNativeUIVisible(true)
    DouyinUIService.SetUIVisible(true)
end
```

## 2. 两个接口的区别

### 2.1 `SetNativeUIVisible`

```lua
DouyinUIService.SetNativeUIVisible(false)
```

用于显示或隐藏 Native 层界面。根据本地 API 文档，它用于隐藏所有非 Unity 层级的官方 UI。

适合隐藏：

- 飞行、跳跃等操作按钮
- 平台功能按钮
- 相机、分享、横竖屏切换等系统级入口
- 其他 Native 层官方 UI

### 2.2 `SetUIVisible`

```lua
DouyinUIService.SetUIVisible(false)
```

用于显示或隐藏 Unity 层界面。

它的作用范围通常比“官方 UI”更大。调用后，官方 Unity UI 和项目中使用 Unity UGUI 创建的自定义 UI 都可能被隐藏。因此，如果项目已经显示自己的创建舞者 UI，不建议在 UI 打开期间调用它，除非希望整个 Unity UI 层一起消失。

## 3. 推荐的全关闭实现

如果游戏需要完全接管界面，例如进入创建舞者、过场或全屏玩法，可以在游戏入口中调用：

```lua
function EnterFullScreenGameUI()
    DouyinUIService.SetNativeUIVisible(false)
    DouyinUIService.SetUIVisible(false)
end
```

离开全屏界面时恢复：

```lua
function ExitFullScreenGameUI()
    DouyinUIService.SetUIVisible(true)
    DouyinUIService.SetNativeUIVisible(true)
end
```

建议成对调用，避免只恢复其中一层导致部分官方 UI 消失。

## 4. 只关闭部分官方按钮

如果不希望关闭全部官方 UI，可以通过 `GetInteractionButton` 获取指定按钮并隐藏：

```lua
function HideJumpButton()
    local button = DouyinUIService.GetInteractionButton(
        HandType.Right,
        UIType.Jump
    )

    if button ~= nil then
        button.gameObject:SetActive(false)
    end
end
```

本地文档列出的 `UIType` 包括：

- `CustomMain`
- `CustomSub`
- `Throw`
- `Jump`
- `MoveJoyStick`
- `HoldHands`
- `StopHoldHands`
- `Fly`
- `StandUp`

单独隐藏按钮适合只禁用飞行、跳跃、牵手等功能。官方文档同时说明，按钮枚举和方法仍可能迭代；如果目标是整体隐藏，优先使用 `SetNativeUIVisible(false)`。

## 5. 与角色能力联动

部分功能除了 UI，还可以通过 Actor 或玩家设置接口禁用。例如：

```lua
local actor = DouyinActorService.GetLocalActor()
if actor ~= nil then
    -- 第二个参数为 true 时同时隐藏相关 UI
    actor:DisableFly(true)
    actor:DisableHoldHand(true)
end
```

这类接口适合“功能不可用 + UI 隐藏”的场景。仅隐藏按钮并不一定等于禁用了对应能力。

## 6. 自定义 UI 的层级

官方 UI 和自定义 UI 不完全处于同一个 Unity `sortingOrder` 层级。根据本地 UI 层级规范：

| UI 区域 | 建议层级 |
| --- | --- |
| 世界玩法 UI，显示在官方主界面下方 | `< -10` |
| 官方主界面 UI | `0` |
| 世界玩法 UI，显示在官方主界面上方 | `1 - 999` |
| Native 系统级 UI | 不受普通 Unity Sort Order 控制 |

如果关闭官方 UI 后显示创建舞者界面，可以给自定义 Canvas 设置正数 `sortingOrder`，例如 `100` 或更高。

## 7. 注意事项

### 7.1 `SetUIVisible(false)` 可能隐藏自己的 UI

如果创建舞者 UI 是通过 Unity UGUI 创建的，那么它通常属于 Unity UI 层。调用：

```lua
DouyinUIService.SetUIVisible(false)
```

可能连创建舞者 UI 一起隐藏。推荐流程是：

```lua
-- 进入创建流程前只隐藏 Native 官方 UI
DouyinUIService.SetNativeUIVisible(false)

-- 显示自己的创建舞者 UI
GetSys("UISystem"):OpenUI("CreateActorUI")
```

只有在确实需要隐藏所有 Unity UI 时，才同时调用 `SetUIVisible(false)`。

### 7.2 官方 UI 可能在重连或系统状态变化后恢复

如果断线重连、进入相机模式或发生平台 UI 状态切换后官方 UI 被恢复，应在自己的流程状态切换处重新调用隐藏接口，而不要只在 Unity `Start` 中调用一次。

### 7.3 调用时机

建议在以下时机调用：

- 本地玩家进房后
- 创建舞者流程开始时
- 游戏状态机进入全屏玩法状态时
- 自定义 UI 打开前

如果依赖网络初始化，先确保网络状态已经就绪；UI 隐藏本身通常是本地操作，但不要在网络对象尚未完成初始化时执行依赖网络对象的逻辑。

## 8. 本项目建议

对当前创建舞者流程，推荐使用：

```lua
function OpenCreateActorFlow()
    DouyinUIService.SetNativeUIVisible(false)

    local uiSystem = GetSys("UISystem")
    if uiSystem == nil then
        print("[UI] UISystem 未初始化")
        return
    end

    uiSystem:OpenUI("CreateActorUI")
end

function CloseCreateActorFlow()
    local uiSystem = GetSys("UISystem")
    if uiSystem ~= nil then
        uiSystem:CloseUI("CreateActorUI")
    end

    DouyinUIService.SetNativeUIVisible(true)
end
```

这里不调用 `SetUIVisible(false)`，这样可以保留自定义创建舞者 UI。

## 9. 本地参考文档

- [如何关闭与显示官方UI](./如何关闭与显示官方UI.md)
- [自定义UI如何避开官方UI](./自定义UI如何避开官方UI.md)
- [世界UI层级规范](./世界UI层级规范.md)
- [UIType的枚举有哪些](./UIType的枚举有哪些.md)
- [DouyinUIService.SetNativeUIVisible](../虚拟世界API参考/DouyinUIService.SetNativeUIVisible.md)
- [DouyinUIService.SetUIVisible](../虚拟世界API参考/DouyinUIService.SetUIVisible.md)
- [DouyinUIService](../虚拟世界API参考/DouyinUIService.md)
