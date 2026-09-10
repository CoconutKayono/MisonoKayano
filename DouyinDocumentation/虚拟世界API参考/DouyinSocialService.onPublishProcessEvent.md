public static DouyinPublishProcessEvent onPublishProcessEvent = new()
# 描述
平台向API，用于监听玩家的抖音视频的投稿发布状态
# 参数
| 参数 | 参数描述 |
| --- | --- |
| string | 当前发布id hamlet_world_{时间戳} |
| int | 视频的发布进度 （0-100） |
# 代码示例
```Lua
function Start()
    DouyinSocialService.onPublishProcessEvent:AddListener(OnPublishProcessEventCallBack)
end

function OnPublishProcessEventCallBack(publishId, process)
    print(string.format("---DouyinSocialService:发布ID={%s}_发布进度{%d}", publishId, process))
end

function OnDestroy()
    DouyinSocialService.onPublishProcessEvent:RemoveListener(OnPublishProcessEventCallBack)
end
```


