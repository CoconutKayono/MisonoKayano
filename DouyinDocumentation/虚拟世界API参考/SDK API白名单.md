本文档统一规范**Lua 脚本内允许访问、调用的 Unity 官方引擎命名空间**，以及项目内置 抖音虚拟世界 专属组件白名单。
不在本表内的命名空间、自定义组件、第三方模块，Lua 侧均避免直接调用与反射获取，用于运行环境安全管控、脚本沙箱权限约束。

## Unity 官方引擎命名空间白名单

以下为 Lua 脚本**允许直接使用**的 Unity 原生官方命名空间，其余未收录引擎命名空间不建议使用。


1. `UnityEngine`
2. `UnityEngine.UI`
3. `UnityEngine.Events`
4. `UnityEngine.AI`
5. `UnityEngine.Audio`
6. `UnityEngine.Video`
7. `UnityEngine.Playables`
8. `UnityEngine.Animations`
9. `UnityEngine.Networking`


## Douyin 项目组件白名单

Lua 脚本仅可调用下方登记在册的 Douyin 专属组件，未录入组件禁止 Lua 实例化、获取组件、调用接口。

### 2.1 核心脚本组件


* `DouyinScript`：Lua 脚本挂载组件
* `DouyinScriptLoader`：Lua 脚本加载管理组件
* `DouyinWorldRoot`：世界根节点定义组件


### 2.2 专用服务器（Dedicated Server / DS）组件（待上线）


* `DouyinServerRoot`：DS 服务端根节点定义组件
* `DouyinServerScriptLoader`：DS 专用脚本加载器


### 2.3 网络同步相关组件


* `DouyinObjectSync`：物体网络状态同步组件
* `DouyinNetworkGuid`：网络唯一标识 GUID 组件


### 2.4 通用功能业务组件


* `DouyinWaterArea`：水域功能组件
* `DouyinVideoPlayer`：视频播放组件
* `DouyinWorldPortal`：场景传送门组件
* `DouyinSceneEnvironment`：场景环境管理组件
* `DouyinPlayerArea`：玩法区域定义组件


## 3 权限约束规则

1. **白名单严格生效**：仅本文档列出的命名空间、组件可在 Lua 环境安全访问。
2. 禁止通过反射、GetComponent 非常规方式绕过白名单调用未授权类型。
3. 后续新增 Unity 命名空间、Douyin 业务组件，**必须更新本文档白名单**后方可开放 Lua 调用权限。
4. 本清单为运行时沙箱校验依据，用于脚本安全审计、打包校验规范。
