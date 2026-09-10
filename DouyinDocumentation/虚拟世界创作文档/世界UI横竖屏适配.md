想要开启横竖屏切换功能，需要先在 Douyin World Root 组件上进行配置选择。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d57a7118baf14112a426e13f0db34e9f~tplv-goo7wpa0wc-image.image" width="264px" /></div>

目前SDK支持2种模式的横竖屏切换：

* 单套UI适配：使用一套UI prefab来适应横竖屏切换。
* 双套UI适配：使用两套UI prefab来适应横竖屏切换。

# 单套UI适配
想要使用一套UI来适应横竖屏切换，可以按照下述步骤来操作。

1. 创建canvas，在canvas下创建空物体<span style="color: #D83931"><strong>（必须要新建一个空物体，在空物体下处理正式的UI内容）</strong></span>，命名为aaa（命名随意，此处仅为方便后文指代）

> 注：一定要选中canvas后右键直接创建子物体，另行创建后拖进来的子物体不可以

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/85c3ea01214b4980ac5b0775369ac983~tplv-goo7wpa0wc-image.image" width="1915px" /></div>


2. 保证aaa下有UI物件作为子物体。可以将已经构建好的一个UIprefab拖入aaa作为子物体，或者右键创建任意一个UI物体作为aaa的子物体。完成后，将aaa拖入assets，转化为prefab
3. assets中双击打开aaa的prefab，进入prefab编辑界面，确认inspector中aaa上一级的canvas后缀有**Environment**，再添加 **Douyin UIHVAdapterinOnePrefab** 组件，即可在prefab中开始构建UI物件。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d99b84e2b24348c48c69ae06646169a8~tplv-goo7wpa0wc-image.image" width="1448px" /></div>


4. 打开gameplay 模式，在画面预设中添加手机横屏大小和竖屏大小。

> 参考尺寸：横屏2532×1170，竖屏1170×2532。

在横屏大小和竖屏大小状态下分别返回scene界面中aaa的prefab编辑页面，即可拖动UI物件到横屏或者竖屏指定位置，两种状态下分别编辑UI物体位置，不相互影响。

5. 在父物件canvas下添加 **Douyin Canvas Adapter（该组件只能挂到空物体上）**。


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/5bd955ebbe1c42bfbbe5766166a07caa~tplv-goo7wpa0wc-image.image" width="1399px" /></div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/485ea1f58b954b78b17b2b310666afe1~tplv-goo7wpa0wc-image.image" width="1920px" /></div>




</div>
</div>


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b23e9e69e66a4c48bbac20686dc8a1e0~tplv-goo7wpa0wc-image.image" width="1252px" /></div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/117f3f843998480ca98e6d2a462fe980~tplv-goo7wpa0wc-image.image" width="1911px" /></div>



</div>
</div>

## 视频演示
<video src=https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f21fdf971913479bab06f6ddd7687971~tplv-goo7wpa0wc-image.image></video>

# 双套UI适配
想要使用两套UI来适应横竖屏切换，可以按照下述步骤来操作。

1. 创建canvas，在canvas下创建空物体<span style="color: #D83931"><strong>（必须要新建一个空物体，在空物体下处理正式的UI内容）</strong></span>，命名为aaa（命名随意，此处仅为方便后文指代）

> 注：一定要选中canvas后右键直接创建子物体，另行创建后拖进来的子物体不可以


2. 保证aaa下有UI物件作为子物体，可以将已经构建好的一个UIprefab拖入aaa作为子物体，或者右键创建任意一个UI物体作为aaa的子物体。完成后，将aaa拖入assets，转化为prefab
3. assets中双击打开aaa的prefab，进入prefab编辑界面，确认inspector中aaa上一级的canvas后缀有 **Environment**，再添加 **Douyin UIHVAdapterinTwoPrefab** 组件，即可在prefab中开始构建
4. 中分别设置横屏/竖屏想要的UI效果，再将做好的横屏/竖屏UIprefab拖入成为aaa的prefab的子物体，再拖入上一步添加的组件对应的槽之中，如果有用脚本实现的UI则拖入脚本槽，没有则不用。
5. 在父物件canvas下添加 **Douyin Canvas Adapter（该组件只能挂到空物体上）**。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6b1f84f49de447eebcefffb81595f28c~tplv-goo7wpa0wc-image.image" width="652px" /></div>


