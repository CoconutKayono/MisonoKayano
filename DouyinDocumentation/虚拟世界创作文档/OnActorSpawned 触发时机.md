问：OnActorSpawned 什么时候会触发？
答：OnActorSpawned 会在如下几个情况下触发：

1. 初次进入房间时
2. 在房间内切换合养精灵形象时
3. 触发了断线重连时

断线重连时会触发 OnActorSpawned 接口，而且是仅有本地断线重连的玩家会触发该接口，但不会触发 OnActorDespawned 接口，这点需要各位开发者注意，在使用OnActorSpawned 和 OnActorDespawned 做对象管理时，要注意触发时机和初始化。


