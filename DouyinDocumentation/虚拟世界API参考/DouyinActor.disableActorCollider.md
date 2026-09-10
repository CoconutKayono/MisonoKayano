public bool disableActorCollider
# 描述
该API用于禁用精灵（Actor）之间的碰撞，实现精灵之间互相穿透的效果，且只会影响玩家之间的碰撞，不会影响玩家与环境的碰撞。
# 代码示例
```Lua
function OnActorSpawned(actor)
    if actor ~= nil and actor.isLocal then
        actor.disableActorCollider = true
    end
end
```


