public float gravityScale
# 描述
获取或设置当前 Actor 的重力缩放系数。<span style="color: #D83931">注意：</span><span style="color: #D83931"><code>gravityScale</code></span><span style="color: #D83931"> 属性的修改仅在本地客户端生效，不会自动同步到其他客户端。</span>
# 代码示例
```Lua
local localActor

function Update()
    if localActor == nil then
        return
    end
    if Input.GetKeyDown("1") then
        ActorGravityScaleSample(localActor)
    end
end

function OnActorSpawned(actor)
    if not actor or not actor.isLocal then
        return
    end
    localActor = actor
end

function ActorGravityScaleSample(actor)
    if not actor or not actor.isLocal then
        return
    end
    print("--DouyinActor3CSample:gravityScale=" .. actor.gravityScale)
    actor.gravityScale = 10
end
```


