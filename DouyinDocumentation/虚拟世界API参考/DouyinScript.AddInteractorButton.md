public Button AddInteractorButton()
# 返回
Button
Unity按钮组件
# 描述
新增C区按钮
# 代码示例
```Lua
---@var interactSprite:UnityEngine.Sprite
---@end
local localActor
local interationButton_1
local interationButton_2

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
    end
end

--执行self:EnableInteraction()后，会触发OnFocus方法
function OnFocus(handType)
    --执行self:AddInteractorButton可以创建一个交互按钮，返回Button对象
    --返回的Button对象的图片和文字，都是默认的，你可以按需修改
    interationButton_1 = self:AddInteractorButton()
    local interactText_1 = interationButton_1:GetComponentInChildren(typeof(CS.UnityEngine.UI.Text))
    interactText_1.text = "拾取"
    local iconTrans = interationButton_1.transform:Find("Icon")
    if iconTrans then
        local interactImg = iconTrans:GetComponent(typeof(CS.UnityEngine.UI.Image))
        if interactImg then
            --处理图片的显示
            SetBtnSprite(interactSprite)
        end
    end
    
    interationButton_2 = self:AddInteractorButton()
    local interactText_2 = interationButton_2:GetComponentInChildren(typeof(CS.UnityEngine.UI.Text))
    interactText_2.text = "对话"
end

function SetBtnSprite(iconSprite)
    local iconTrans = interationButton_1.transform:Find("Icon")
    if iconTrans then
        local interactImg = iconTrans:GetComponent(typeof(CS.UnityEngine.UI.Image))
        interationButton_1.transition = CS.UnityEngine.UI.Selectable.Transition.SpriteSwap
        if interactImg then
            interactImg.sprite = iconSprite
            local spriteState = interationButton_1.spriteState
            spriteState.highlightedSprite = iconSprite
            spriteState.pressedSprite = iconSprite
            spriteState.selectedSprite = iconSprite
            interationButton_1.spriteState = spriteState
        end
    end
end

function OnLostFocus(handType)
    self:RemoveInteractorButton(interationButton_1)
    -- self:RemoveAllInteractorButtons()
    -- self:RemoveInteractorButtonAt(1)
end
```


