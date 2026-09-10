public void SetSpeed(float speed = 4.0f, float baseRate = 1f)
# 描述
设置精灵移动速度，并自动联动行走动画的播放速度；速度高于默认基础速度时动画相应加快，避免"脚步打滑"，否则保持原速。
# 参数
| 参数 | 描述 |
| --- | --- |
| speed | 精灵移动的速度 |
| baseRate | 动画加速微调系数，仅当 speed 高于默认基础速度时生效。建议取 (0, 1] :越小越接近原速(易滑步)，越接近 1 越跟随速度加速。 |
# 代码示例
```Lua
function OnActorSpawned(actor)
    if actor ~= nil and actor.isLocal then
        actor:SetSpeed(8, 0.5)
    end
end
```


