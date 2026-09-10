public void Interact(GameObject go)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| go | 代表要与之交互的游戏对象 |
# 描述
触发当前 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)与指定游戏对象的交互逻辑，该方法只对本地玩家有效。
# 代码示例
调用DouyinActor.Interact和物体交互时，会找到A物体上的DouyinScript脚本，然后执行A物体上的OnInteract方法，开发者需要在OnInteract方法中，实现物体的交互逻辑。以下是相关功能的实现Demo：
```Lua
---@var interactSprite:UnityEngine.Sprite
---@end
local localActor
local interationButton_1
local interationButton_2
local btn2Click = false

function OnActorTriggerEnter(actor)
    if not actor or not actor.isLocal then
        return
    end
    if not localActor then
        localActor = actor
    end
    --启用交互，启用之后会触发OnFocus方法，在OnFocus中创建交互按钮
    self:EnableInteraction()
end

function OnActorTriggerExit(actor)
    if not actor or not actor.isLocal then
        return
    end
    --禁用交互，禁用之后会触发OnLostFocus方法，在OnLostFocus中移除交互按钮
    self:DisableInteraction()
end

--玩家点击弹出的交互按钮时，会执行该函数
--index表示点击的是第几个按钮
function OnInteractorButtonClick(index)
    if index == 1 then
        --判断手中是否有物体，有物体丢弃，没有物体捡起
        if localActor:IsPickup() then
            localActor:Drop(self.gameObject)
        else
            --Actor捡起物体，目前只支持右手
            localActor:Pickup(self.gameObject, CS.HandType.Right)
        end
    elseif index == 2 then
        btn2Click = true
        localActor:Interact(self.gameObject)
    end
end

function OnInteract(actor)
    if actor == nil or not actor.isLocal then
        return
    end
    --目前OnInteract方法没有区分具体是哪个按钮点击的逻辑，但是会根据点击的顺序，依次调用OnInteract
    --可以使用标记，来判断当前是哪个按钮的点击逻辑，分别进行处理
    if btn2Click then
        print("--OnInteractorButtonClick:处理对话逻辑")
        btn2Click = false
    end
end

--执行self:EnableInteraction()后，会触发OnFocus方法
function OnFocus(handType)
    --执行self:AddInteractorButton可以创建一个交互按钮，返回Button对象
    --返回的Button对象的图片和文字，都是默认的，你可以按需修改
    interationButton_2 = self:AddInteractorButton()
    local interactText_2 = interationButton_2:GetComponentInChildren(typeof(CS.UnityEngine.UI.Text))
    interactText_2.text = "对话"
end

function OnLostFocus(handType)
    self:RemoveInteractorButton(interationButton_1)
    -- self:RemoveAllInteractorButtons()
    -- self:RemoveInteractorButtonAt(1)
end
```


