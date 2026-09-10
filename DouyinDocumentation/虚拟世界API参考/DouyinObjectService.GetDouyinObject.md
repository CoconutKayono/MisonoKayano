public static DouyinObject GetDouyinObject(int objectID)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| objectID | 对应DouyinObject.UID和DouyinObjectService.NetSpawn函数out出来的id，可以通过该值获取到DouyinObject。 |
# 返回值
返回对应的DouyinObject对象
# 描述
根据网络对象的id获取到对应的DouyinObject对象。
# 代码示例
```Lua
function GetDouyinObjectSample(netObjID)
    local netObj1 = DouyinObjectService.GetDouyinObject(netObjID)
    if netObj1 and netObj1.gameObject then
        print(string.format("--GetDouyinObjectSample:netObj1name=" .. netObj1.gameObject.name))
    end
end
```


