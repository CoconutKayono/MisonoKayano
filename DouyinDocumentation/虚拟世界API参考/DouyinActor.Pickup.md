
public void Pickup(GameObject go, HamletHandType handType ＝ HandType.Right, Matrix4x4 matrix ＝ Matrix4x4.identity)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| go | 要拾取的游戏对象 |
| handType | 指定使用哪只手进行拾取，可取值为 HandType 枚举中的不同值，用于区分左手或右手等 |
| matrix | 用于指定拾取物体后的位置和旋转信息，通过该矩阵可以获取物体的位置和欧拉角 |
# 描述
拾取指定物品。
注意：当前只支持右手拾取，传入左手无法拾取物体。
# 代码示例
执行Pickup方法，并不会真正执行拾取操作，需要开发者实现拾取逻辑。当调用DouyinActor.Pickup拾取A物体时，会找到A物体上的DouyinScript脚本，然后执行A物体上的OnPickup方法，开发者需要在OnPickup方法中，实现物体的挂载等逻辑。以下是相关功能的实现Demo，您也可以参考官方的DouyinPickup.lua脚本，去实现自己想要的功能。
```Lua
---@var interactSprite:UnityEngine.Sprite
---@end
local localActor
local interationButton_1

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

--开发者处理拾取逻辑的地方
function OnPickup(actor, handType)
    if actor == nil or not actor.isLocal then
        return
    end
    if handType ~= CS.HandType.Right then
        return
    end
    local animator = actor.gameObject:GetComponentInChildren(typeof(CS.UnityEngine.Animator))
    if animator ~= nil then
        local bone = animator:GetBoneTransform(CS.UnityEngine.HumanBodyBones.RightHand)
        if bone ~= nil then
            self.transform:SetParent(bone)
        end
        local position, rotation = ActorCalculatePalmTransform(actor, false)
        self.transform.position = position
        self.transform.rotation = rotation
    end
    local interactText = interationButton_1:GetComponentInChildren(typeof(CS.UnityEngine.UI.Text))
    interactText.text = "丢弃"
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


