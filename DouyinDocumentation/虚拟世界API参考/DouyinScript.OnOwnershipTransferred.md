function OnOwnershipTransferred()
# 描述
当主权转移时，会触发此函数。
# 代码示例
```Lua
function OnOwnershipTransferred()
    print(string.format("--DouyinNetSample:OnOwnershipTransferred:%s的主权被转移了", self.gameObject.name))
end
```


