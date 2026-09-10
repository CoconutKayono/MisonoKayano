问：想要隐藏官方UI，比如飞行按钮，跳跃按钮，该怎么办？
答：你可通过 DouyinUIService 下的静态函数 GetInteractionButton 来获取到指定类型的按钮类型枚举，并进行SetActive(false)。
> 注：相关按钮类型枚举和方法正在迭代中，暂时不建议使用。

```Go
public static Button GetInteractionButton(HandType handType, UIType uiType)
```

隐藏飞行按钮：
```Go
function Start()
    DouyinUIService.GetInteractionButton(HandType.Right, UIType.Fly).gameObject:SetActive(false)
end    
```

隐藏聊天输入面板
```Go
    local ui = UnityEngine.GameObject.Find("UISystem")
    if ui ~= nil then
        local chat = ui.transform:Find("Canvas/UIRoot/Bottom/MainInputPanel(Clone)/ObserverNotHideLayer") -- 聊天界面
        if chat ~= nil then
            chat.gameObject:SetActive(active)
        end
    end
```


