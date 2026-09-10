使用 Actor Tag 可以方便地在对象身上存储一些信息，这些信息会自动在房间内所有客户端上保持信息同步。 
Tag 是一个键值对，key 和 value 均为 string 类型。 
比如可以给某个对象设置 Tag 为： 

* group：red 
* role：scientist 

以下是关于Actor Tag的常用 API： 
| **DouyinActor**.SetPlayerTag(tagName, tagValue) | 给 Actor 增加 Tag。  |
| --- | --- |
| **DouyinActor**.GetPlayerTag(tagName) | 获得 Actor 的 Tag。  |
| **DouyinActor**.ClearPlayerTags(tagName) | 清除 Actor 的指定 Tag，参数为空则清除所有 Tag。  |
| **DouyinActorService**.GetActorsWithTag(tagName, tagValue) | 获得拥有某个 Tag 的所有对象；  <br> 可以只指定 tagName，也可以指定 tagName 和 tagValue。  |
| **DouyinActorService**.ClearAllActorsTag(tagName) | 清除所有对象的某个 Tag，参数为空则清除所有对象的所有 Tag。  |
由于同一个脚本会在所有进入此房间的客户端上运行，Tag 相关的 API 是不需要额外权限的，也就是说所有人都会执行这段代码；**请在使用时注意此类操作的权限管理！**
常用的方式有： 

1. 每个人设置自己的 Tag，其他人只读取（使用 DouyinActor.isLocal 判断是不是“自己”）。 
2. 由房主或某个特定客户端负责设置所有人的 Tag，其他人都只读取。 


