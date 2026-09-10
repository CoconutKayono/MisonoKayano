# 创建Lua脚本
通过SDK，我们可以在Assets文件夹内按照 **Create->Douyin->Lua script** 创建Lua脚本。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e4927cb59b1642bf8db6ea4fd0d1ec7c~tplv-goo7wpa0wc-image.image" width="264px" /></div>

创建完成后，脚本名称默认为 LuaScript，你可以根据脚本要实现的逻辑功能来修改它的名字，比如：这里将脚本的名字修改为：MyScript。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1374b7bf3a3b4c81961155aa7b307e7e~tplv-goo7wpa0wc-image.image" width="264px" /></div>

此时，如果你想像Unity C#脚本那样，直接将创建好的脚本挂载到场景物体对象上，你会发现这个操作是不行的。
# 使用Lua脚本
SDK提供了一个用于向物体挂载Lua脚本的 C#组件，叫做 **Douyin Script**。
在使用Lua脚本之前，需要先在对应物体上添加 Douyin Script 组件，它相当于运行Lua脚本的容器。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9ca0a39729ec4d22926f8cdf7b54c668~tplv-goo7wpa0wc-image.image" width="264px" /></div>

我们可以直接将刚才创建的Lua脚本直接拖入到 Douyin Script 组件的脚本文件属性上，也可以点击圆形按钮打开搜索框进行选择。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/0eac17b1d7874dba9770148de22dc209~tplv-goo7wpa0wc-image.image" width="264px" /></div>

这样就完成了Lua脚本的挂载，也意味着你编写的Lua脚本将会在世界启动后生效。
不建议对挂载Lua脚本的对象进行SetActive操作，若需要对物体进行显示隐藏操作，可将Lua脚本挂载到空节点上，将对象设置为空节点的子节点。


---


如果你完全不了解Unity编程，可以先看看：[Unity脚本](https://docs.unity3d.com/Manual/scripting.html)**。**
想要了解更多Lua知识，可以阅读：[Lua教程](https://www.tutorialspoint.com/lua/lua_overview.htm)。 


