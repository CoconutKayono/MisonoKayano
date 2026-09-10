function OnOwnershipRequest(int senderID) end
# 描述
请求主权的事件，owner返回true代表同意主权转移；返回false代表不同意主权转移；当原来的owner同意时，才会发送OnOwnershipTransferred事件给所有其他人，才算正式完成owner的转移。
如果一个物体上有多个脚本都有此事件函数，则所有脚本都返回true才是同意请求，若有一个脚本返回false，则拒绝请求，且后续的脚本中对应事件不再执行。
# 代码示例
```Lua
local isAgree = true

function OnOwnershipRequest(objId)
    if isAgree then
        print(string.format("--DouyinNetSample:OnOwnershipRequest:同意其他玩家成为%d主权方的请求", objId))
    else
        print(string.format("--DouyinNetSample:OnOwnershipRequest:不同意其他玩家成为%d主权方的请求", objId))
    end
    return isAgree
end
```


