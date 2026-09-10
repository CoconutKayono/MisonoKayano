SDK内支持的Lua脚本符合 Unity MonoBehaviour 生命周期，并兼容一部分 MonoBehavior 的事件接口。这意味着我们可以像是使用 Unity C#脚本那样按照 UnityMonoBehaviour 生命周期来编写代码逻辑。
# print方法
打开 MyScript 脚本，可以看到脚本内已经有了一个 Start 方法。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/7d4fa7ee76c640608aa02bbb977a7e11~tplv-goo7wpa0wc-image.image" width="264px" /></div>

这个 Start 方法与Unity C#脚本中的 Start方法的作用是一样的，都是在运行时执行一次。
我们在这个方法内使用 print 方法来输出一段日志。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/57f317c2cf9f4d349e8a9f312958a387~tplv-goo7wpa0wc-image.image" width="264px" /></div>

# 查看运行效果
启动调试器，点击调试器右上方的控制台按钮，打开web端的控制台。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d7f854ffce4d44baaed805484bce5817~tplv-goo7wpa0wc-image.image" width="264px" /></div>

> 注：启动调试时，如果改动了场景则需要勾选打包资源；否则，不必勾选打包资源


打开控制台后，在控制台左侧选择 Logs，并检查输出的日志。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f17f4b2de3d44c75a4e8f7712a1667eb~tplv-goo7wpa0wc-image.image)

