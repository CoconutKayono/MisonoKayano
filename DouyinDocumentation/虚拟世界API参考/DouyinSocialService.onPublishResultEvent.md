public static DouyinPublishResultEvent onPublishResultEvent = new()
# 描述
平台向API，用于监听玩家的抖音视频的投稿结果
# 参数
| 参数 | 参数描述 |
| --- | --- |
| 参数1 | 当前发布id hamlet_world_{时间戳} |
| 参数2 | 1 - 发布成功 0 - 发布失败 |
| 参数3 | 作品id，发布失败没有该参数 |
# 代码示例
```Lua
function Start()
    DouyinSocialService.onPublishResultEvent:AddListener(OnPublishResultEventCallBack)
end

function OnPublishResultEventCallBack(publishId, success, contentId)
    --发布成功
    if success == 1 then
        print(string.format("---DouyinSocialService:发布成功，发布ID={%s}_作品ID={%s}", publishId, contentId))
    else
        print(string.format("---DouyinSocialService:发布失败，发布ID={%s}", publishId))
    end
end

function OnDestroy()
    DouyinSocialService.onPublishResultEvent:RemoveListener(OnPublishResultEventCallBack)
end
```


