public void SitDown(GameObject go, bool switchSeat ＝ false)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| go | 要坐下的座位的游戏对象 |
| switchSeat | 用于控制是否允许切换座位，默认为不允许 |
# 描述
坐在指定的座位上，该方法只对本地玩家有效。
# 代码示例
执行SitDown方法，并不会真正执行坐下操作，需要开发者实现坐下逻辑。当调用DouyinActor.SitDown坐在A物体上时，会找到A物体上的DouyinScript脚本，然后执行A物体上的OnSeatEntered方法，开发者需要在OnSeatEntered方法中，实现玩家坐在物体上的逻辑。以下是相关功能的实现Demo，您也可以参考官方的DouyinSeat.lua脚本，去实现自己想要的功能。
```Lua
---@var sitDownSprite:UnityEngine.Sprite
---@var standUpSprite:UnityEngine.Sprite
---@var seatDownTrans:UnityEngine.Transform
---@var standUpTrans:UnityEngine.Transform
---@end
local localActor
local interationButton_1

-- Start is called before the first frame update
function Start()
end

function OnActorTriggerEnter(actor)
    if not actor or not actor.isLocal then
        return
    end
    if not localActor then
        localActor = actor
    end
    self:EnableInteraction()
end

function OnActorTriggerExit(actor)
    if not actor or not actor.isLocal then
        return
    end
    self:DisableInteraction()
end

function OnInteractorButtonClick(index)
    print("--DouyinInteractionSample:OnInteractorButtonClick:index=" .. index)
    if localActor:IsSitting() then
        localActor:StandUp(self.gameObject)
    else
        localActor:SitDown(self.gameObject)
    end
end

function OnSeatEntered(actor, handType)
    if actor == nil or not actor.isLocal then
        return
    end
    print("玩家坐下")
    local trans = actor.gameObject.transform
    trans:SetParent(seatDownTrans)
    trans.localPosition = CS.UnityEngine.Vector3.zero
    trans.localRotation = CS.UnityEngine.Quaternion.identity
    local animator = actor.gameObject:GetComponentInChildren(typeof(CS.UnityEngine.Animator))
    if animator ~= nil then
        local currentPlayerBone = animator:GetBoneTransform(CS.UnityEngine.HumanBodyBones.Hips)
        local offset = currentPlayerBone.position - trans.position
        trans.position = trans.position - offset
    end
end

function OnSeatExited(actor)
    if actor == nil or not actor.isLocal then
        return
    end
    print("玩家站起")
    local trans = actor.gameObject.transform
    trans:SetParent(nil)
    actor.position = standUpTrans.position
    actor.rotation = standUpTrans.rotation
end

function OnFocus(handType)
    print("--DouyinInteractionSample2:OnFocus")
    local iconSprite
    local inreractStr
    if localActor:IsSitting() then
        iconSprite = sitDownSprite
        inreractStr = "站起"
    else
        iconSprite = standUpSprite
        inreractStr = "坐下"
    end
    interationButton_1 = self:AddInteractorButton()
    local interactText_1 = interationButton_1:GetComponentInChildren(typeof(CS.UnityEngine.UI.Text))
    interactText_1.text = inreractStr
    SetBtnSprite(iconSprite)
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
    print("--DouyinInteractionSample2:On LostFocus")
    self:RemoveInteractorButton(interationButton_1)
    -- self:RemoveAllInteractorButtons()
    -- self:RemoveInteractorButtonAt(1)
end
```


