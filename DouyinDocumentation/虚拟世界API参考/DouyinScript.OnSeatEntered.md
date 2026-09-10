function OnSeatEntered(DouyinActor actor)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| actor | 与物体进行交互的 [Actor](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219) |
# 描述
当被 [Actor](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219) 坐下时，调用 Api 时触发。
# 代码示例
当调用DouyinActor.SitDown(go)时，会找到go的DouyinScript，执行DouyinScript中的OnSeatEntered方法。
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


