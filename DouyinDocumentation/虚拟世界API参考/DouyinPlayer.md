在阅读此类前，请参阅[玩家与合养精灵](unknown)章节，以了解更多关于玩家和合养精灵的背景信息。
# 描述
玩家类，用来定义一个玩家对象，并获取这些玩家的数据。 每个玩家都与一个 DouyinPlayer 对象关联。

* 包含玩家的一些基础属性，比如ID、昵称、头像、GameObject等。
* 当玩家的角色加入、离开时，将对应触发 OnPlayerJoined、OnPlayerLeft 事件。您可以在与 DouyinScript 关联的 Lua 脚本中监听这些事件，并处理相关业务逻辑。

# 公开属性
| [gameObject](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=douyinplayer_gameobject) | 与玩家关联的 GameObject |
| --- | --- |
| [playerID](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=playerID) | 房间内玩家实例ID，每次进房都会重新生成，客户端可以用该ID来标识玩家。 |
| [playerOpenID](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=b2wp670q) | 房间内玩家的抖音开放ID，玩家ID的唯一标识 |
| [playerName](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=douyingPlayer_playerName) | 玩家名称 |
| [isLocal](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=DouyinPlayer_isLocal) | 是否是MainPlayer，本地玩家 |
| [isServer](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4090vw68) | 是否是Dedicated Server的DouyinPlayer；Dedicated Server 是特殊的DouyinPlayer； |
# 公开方法
| [GetActor](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3hac4un1) | 获取此玩家当前控制的Actor对象实例，返回可能为Null，表示还没有控制的Actor对象实例 |
| --- | --- |
| [GetPlayerPortrait](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=x0sbl336) | 获取玩家头像 |

