public void EnableInteraction(InteractiveButtonType type)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| type | 交互类型 |
# 描述
设置为可交互，
包括3D交互和2D交互。
public enum InteractiveButtonType 
{
        Hand, // 手部交互按鈕
        Additive, // 辅助交互按鈕
        None, // 无按钮
}
# 代码示例
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


