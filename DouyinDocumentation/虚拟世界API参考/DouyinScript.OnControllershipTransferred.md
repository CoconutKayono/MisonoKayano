function OnControllershipTransferred(DouyinPlayer prevDouyinPlayer, DouyinPlayer currentDouyinPlayer)
# 描述
当控制权转移时，会触发此函数。
# 代码示例
```Lua
function OnControllershipTransferred(player1, player2)
    if not player1 or not player2 then return end
    print(string.format("--DouyinNetSample:OnControllershipTransferred:%s的控制权转移到%s上", player1.playerOpenID,
        player2.playerOpenID))
end
```


