问：云处理失败后，让更新 Douyin UIHV Adapterin One Prefab，应该怎么做？
答：在云处理失败时，若出现因 Douyin UIHV Adapterin One Prefab 导致云处理失败，需要替换一下项目中**所有使用到 Douyin UIHV Adapterin One Prefab 的地方**。
具体操作如下：

1. 找到项目中使用到的 UI（下面以共享组件排行榜为例子）

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6d56dc8dd9b0482ba675e755c310e7d4~tplv-goo7wpa0wc-image.image" width="300px" /></div>


2. 找到所有UI中挂载 **Douyin UIHV Adapterin One Prefab** 的物体（或者预制体）

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/816bf13ea99e4e83bf0f58b69b8319dc~tplv-goo7wpa0wc-image.image" width="2938px" /></div>


3. 将物体挂载的 **Douyin UIHV Adapterin One Prefab** 移除

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9648ee1dbc044a4fb62980d547c4e17d~tplv-goo7wpa0wc-image.image" width="2940px" /></div>


4. 添加新的 **Douyin UIHVAdapterinOnePrefab 即可**

<video src=https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/19e5b230527645c6ad2621ca07dac6c7~tplv-goo7wpa0wc-image.image></video>
> 注意：你可以直接打开UI预制体，对预制体进行修改
