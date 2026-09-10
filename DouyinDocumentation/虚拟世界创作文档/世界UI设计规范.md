> 该文档主要服务于世界开发者建设使用，使开发者了解世界内官方组件、基础形式以及布局环境。提升各个世界体验的整体性，提升开发者与官方的沟通效率等内容，此文档也会随着功能的增加以及不同世界需求的增加进行持续迭代。


以下正文描述会使用部分简称进行阐述
**三方世界**：UGC开发者的世界场景；
**系统级**：官方开发应用于全量世界的功能or展示等内容；
**跨世界**：在所有世界or多个世界内展示的玩法功能；


## 主页框架
### 界面基础形式
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d5ca90ef7961483781c80827c0e49ee9~tplv-goo7wpa0wc-image.image)
### 界面基础尺寸
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b26654d8dd424e86b7d2bc97230a7e1e~tplv-goo7wpa0wc-image.image" width="4358px" /></div>

### 主界面分区
| ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6dee889a23e245cfaad949a4175ba7c8~tplv-goo7wpa0wc-image.image) <br>  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ee190b45646d4bc89070ccb084320977~tplv-goo7wpa0wc-image.image) | 1.系统功能/入口 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e015f5fa63b44d0b9bc7bfd69812e19d~tplv-goo7wpa0wc-image.image) | 2.三方世界使用区域 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/7137adda48ca4fbfb4bcb74b12ecc6e0~tplv-goo7wpa0wc-image.image) | 3.官方设计占用资源 |
| ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/14990c954da647a9a96305798f8a2400~tplv-goo7wpa0wc-image.image) | 4.小火人显示区域 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1f5d986e85194ce9a3c008ae7245b6df~tplv-goo7wpa0wc-image.image) | 5.官方社交功能区域 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6b46906338f94ad7bb811f6fe55abe52~tplv-goo7wpa0wc-image.image) | 6.HUD功能区域 |
#### 系统功能/入口
| **面积展示** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c0526efc551e4d8b8a305201582c2979~tplv-goo7wpa0wc-image.image) |  |  |  |
| --- | --- | --- | --- | --- |
| **功能定位** | 全量世界系统/入口操作内容，此部分设计为官方世界开发维护 |  |  |  |
| **功能解析** | 包含了更多、在玩朋友等内容 |  |  |  |
| **图标清单** <br>  | **名称** | **图例** | **尺寸** | **描述** |
|  | 返回 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/01ec4a0fa4a5496fb40731885e2c8121~tplv-goo7wpa0wc-image.image) | 28*28 | 用于退出世界使用 |
|  | 在玩朋友 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3ee46c00e84b459686c25c717200c767~tplv-goo7wpa0wc-image.image) | 124*28 | 用于打开在玩朋友的列表入口 |
|  | 更多世界 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/32265aad60e34b04b5d7f414d90f39bc~tplv-goo7wpa0wc-image.image) | 86*28 | 用于打开更多世界入口 |
#### 三方世界使用区域
| **面积展示** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4a17245c4e054444b80fea3d537ccb31~tplv-goo7wpa0wc-image.image) <br>  |  |  |
| --- | --- | --- | --- |
| **功能定位** | 此区域为三方世界使用，内容包含了三方世界主入口显示，主面板显示，如常见的计分板、任务面板、奖励指引面板等信息 |  |  |
| **功能解析** | 该区域是开放给三方世界使用的功能区域，除主入口限制位置和大小之外，给三方世界更多的自由展示空间，可贴合自主的玩法体验等内容设计不同的展示内容 |  |  |
| **三方世界主按钮规则** |  |  |  |
| --- | --- | --- | --- |
| **数量要求** | 0-5个（若超出则可收归最后一个功能按钮位，点击展开弹窗进行选择） |  |  |
| **数量示例** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1f2eca705f434f12bad6f30d71860fc5~tplv-goo7wpa0wc-image.image) <br> ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/953e3462a94d41909e790eef9f051422~tplv-goo7wpa0wc-image.image) <br> ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/246be0a1be5b443aa268c20304d38d06~tplv-goo7wpa0wc-image.image) <br>  |  |  |
| **位置要求** | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e9783eea90e64a6aabe459ee6fa852f2~tplv-goo7wpa0wc-image.image) |  |  |
| 图标要求 <br>  | **图例** | **尺寸** | **描述** |
|  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/bf538899bada443abd61b5cfb164b36b~tplv-goo7wpa0wc-image.image) | 40*40 | 图标最大尺寸规范40*40 <br> 标题长度最大支持4个字符 <br> 标题文本字号10pt <br> 图标需考虑在背景的衬托下是否清晰可见 |
以下列举了一些主功能图标的使用案例~

| 分类 | 图例 | 说明 |
| --- | --- | --- |
| Good case <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/5f9c838c507748b7beb2164d3f15a590~tplv-goo7wpa0wc-image.image) | 1.图标颜色一致； <br> 2.图标形式风格统一； <br> 3.图标文字大小，颜色效果一致； <br> 4.图标整体大小、位置及间距统一； |
| Bad case | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c429b03045c54cb1b3f713c0bb4b8002~tplv-goo7wpa0wc-image.image) | 1.图标视角不统一; <br> 2.文字大小、阴影不统一； <br> 3.图标结构不统一； <br> 4.图标位置关系错位，间距差异明显； |
| Bad case | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/df79ff1114e54f1498355303c954ce8a~tplv-goo7wpa0wc-image.image) | 1.图标间距过大； <br> 2.图标轻微上下错位； <br> 3.图标描边棱角突兀； |
除了主功能按钮之外，该区域可显示一些重点功能的信息呈现和可视化功能

功能的数量和面积有以下要求说明

> * 功能显示保持在1-2个，
> * 显示的面积小于可用面积的70%，适当留白；
> * 每个模块需要有清晰的边界；

以下使用横屏案例进行说明
|  | 概况 | 图例 | 说明 |
| --- | --- | --- | --- |
| **Good case** <br>  | 单独面板展示 <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f5026ebf739741cd808ddb423b96b542~tplv-goo7wpa0wc-image.image) <br>  | 三方世界可根据添加一些地图信息组件以符合玩法； |
|  | 展示等级、状态、金币等信息 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b9af88d8d8ce478990e991918498aa54~tplv-goo7wpa0wc-image.image) | 三方世界可以展示至多两种类型的功能说明，并且所示内容需拥有完整清晰的边界； <br>  |
| Bad case <br>  | 既展示信息又展示按钮，并且功能边界模糊 <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/66933734a55342c6a746e234a6474d60~tplv-goo7wpa0wc-image.image) | 此处内容超过限制尺寸，并且每个功能功能边界模糊，导致层级过多； |
|  | 展示信息过多导致信息模糊杂糅 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1758c2532f004503a9555b5d3fd77453~tplv-goo7wpa0wc-image.image) | 此处设计为区分功能优先级，显示与交互功能混乱，致使设计不符 |
#### 官方占用设计资源
| **面积展示** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/62f9a79a394a46c1ad5357a3fcfa7892~tplv-goo7wpa0wc-image.image) |  |  |  |
| --- | --- | --- | --- | --- |
| **功能定位** | 此功能区为官方功能使用，右侧常驻快捷功能全局快捷功能位，及部分服务于活动活动语音等功能； |  |  |  |
| **功能解析** | 该区域是系统侧给玩家提供的重要的功能入口，其承担着重要的点击和显示空间 |  |  |  |
| **图标清单** <br>  | **名称** | **图例** | **尺寸** | **描述** |
|  | 更多 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a52269640fe44779a2d09b4b8082762c~tplv-goo7wpa0wc-image.image) | 28*28 | 用于展开更多按钮 |
|  | 拍照 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3508ae0aa2cc4bc697e0c73e30ac7447~tplv-goo7wpa0wc-image.image) | 28*28 | 用于打开拍照 |
|  | 背包 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/91aa033b249b4e7e9ba38ee972be67b3~tplv-goo7wpa0wc-image.image) | 28*28 | 用于打开背包 |
|  | 表情 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d2d649bbe00a4752addaf8ca4a9e370e~tplv-goo7wpa0wc-image.image) | 28*28 | 用于打开表情 |
| 其他功能 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ea2f6f2374c1402cb8c189a30ec5fde9~tplv-goo7wpa0wc-image.image) <br> ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4d33028cb00142b4acb902dbd2328d9b~tplv-goo7wpa0wc-image.image) <br> ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/6dfec29c89e5421c921ca1724d304768~tplv-goo7wpa0wc-image.image) <br>  |  |  |  |
#### 火人显示区
| **面积展示** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b1d972df92e44e358b372bd760ffb08c~tplv-goo7wpa0wc-image.image) |  |  |
| --- | --- | --- | --- |
| **功能定位** | 此区域展示小火人、火人名称及气泡信息等内容； |  |  |
| **功能解析** | 该区域为显示火人及场景的重要区域，一般情况下不建议在此区域显示UI信息； |  |  |
#### 官方社交功能
| **面积展示** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d8fa021ed67342ea891f1ab7bcd6edec~tplv-goo7wpa0wc-image.image) |  |  |
| --- | --- | --- | --- |
| **功能定位** | 此区域主要以社交功能为基础，分别包含文字社交和语音社交两种此区域展示小火人、火人名称及气泡信息等内容； |  |  |
| **功能解析** | 该功能在官方框架内包含了按钮及消息显示功能 |  |  |
#### HUD功能区域
| **面积展示** <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1e7a5b03a7ed4bb1adf48483395f4f6e~tplv-goo7wpa0wc-image.image) |  |  |
| --- | --- | --- | --- |
| **功能定位** | 该区域负责操控小火人的移动、跳跃等信息 |  |  |
| **按钮规范** | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/34fb0612a37c4944ae942de0911ef2b5~tplv-goo7wpa0wc-image.image) | 主功能区 | **功能：​**通常为基础的常用功能，是玩法中较为高频触发的功能点； <br> **特点：​**易点击、高频、功能多样； |
|  |  | 次功能区 <br>  | **功能：​**配合当前主要的基础操作，附加的操作内容，可作为场景物件交互的结束； <br> **特点：​**触发频率低、功能常驻、内容量多； |
|  |  | 非常驻式选择 | **功能：​**配合选择场景中交互物触发的选择； <br> **特点：​**需要带有一定的条件显示，选择后消失并带有一定的功能反馈； |
| A区定位 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/22f62f41289849cfa1c013c875a0b087~tplv-goo7wpa0wc-image.image) | 互斥功能解析 | A区设计为“身体状态” <br> 同一时间身体只能处于同一种身体状态，若漂浮则身体中则其他的跳跃则会隐藏 <br>  |
| B区定位 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/0de127e9b76a42debaa9197509afb762~tplv-goo7wpa0wc-image.image) | 互斥功能解析 | B区设计为“手持” <br> 同一时间内小火人仅能做一种手持行为，新增的行为会默认丢弃上一个行为； |
## 弹窗框架
弹窗作为交互设计中重要的组成部分，需要对弹窗的形式大小和内容进行规范显示

| ### 横竖屏统一弹窗 |  |  |  |
| --- | --- | --- | --- |
| 说明 <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8d5d9ec8329141a0ad71de091d800ff9~tplv-goo7wpa0wc-image.image) |  |  |
| **特点** | 该方案属于兼容方案中小型弹窗，可用于提示性、选择性等内容量较少的功能使用 |  |  |
| **说明** | 建议方案为相对外径尺寸，内部标题、正文已经按钮的相对位置，在具体使用的过程中可进行微调，但整体结构和层级需保持一致性 |  |  |
| 示例 <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a9177efa30f042d2930ad7d16ba6c452~tplv-goo7wpa0wc-image.image) |  |  |
| ### 横竖屏差异弹窗 |  |  |  |
| --- | --- | --- | --- |
| **说明** | 若UGC世界采用单横屏或单竖屏的显示方案，则可按照具体的需求适当增加宽或高的显示范围； |  |  |
| 示例 <br>  | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3443f32928364836b9bd286270b03d2f~tplv-goo7wpa0wc-image.image) |  |  |
以下列举了一些关于弹窗设计和表现的示例

| 问题描述 | 错误示例 | 正确示例 | 说明 |
| --- | --- | --- | --- |
| 图片位置和宽高比不对 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ce80062070434b8cbed2874e6000806d~tplv-goo7wpa0wc-image.image) | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e73124ff5b894122956d4d2dfd61a1a2~tplv-goo7wpa0wc-image.image) | 图片保持原有宽高比及正确位置 |
| 文字超框和错位问题 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/d254654f86704c5a9533a000ace0708e~tplv-goo7wpa0wc-image.image) | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/84e135a4f9c14293b51f4578afdf496a~tplv-goo7wpa0wc-image.image) | 文字不能超框按照原有的内容显示 |
| 交互按钮不可过小或重叠 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/0c9f0c51477745abaf1002fdf1ac8590~tplv-goo7wpa0wc-image.image) | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/5d46bd15ad4b421aa9f41b4609f210d1~tplv-goo7wpa0wc-image.image) | 不合适的交互按钮会导致无法触发或中断玩法 |
| 层级错误，无遮罩分离弹窗及主场景 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ffda1ca44a3d435fa0d168d3f20d40b5~tplv-goo7wpa0wc-image.image) | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3b939c9a110c44ffa999869450849d71~tplv-goo7wpa0wc-image.image) | 不合适的层级会使界面中产生显示和热区重叠，会导致流程中断 |
## 风格建议
整体风格需要界面保持一致且效果风格明显，如以下游戏方案
| ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4200e0cd0cdb410dbe26090a1749cdd1~tplv-goo7wpa0wc-image.image) | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/558a97e4d84f49639ed9b8bc7115fbc8~tplv-goo7wpa0wc-image.image) | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/423f9d7b54794acb9b3cd223ad91a36f~tplv-goo7wpa0wc-image.image) |
| --- | --- | --- |
Bad case
| 问题描述 | 世界截图 | 说明 |
| --- | --- | --- |
| 设计不能单独显示孤立的图标和文字 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a1114ccd11be4eb1bb687d76eac15357~tplv-goo7wpa0wc-image.image) | 孤立的图标和文字会使界面的层次和丰富程度略显单调，导致设计表现力不足； |
| 设计风格未保持一致，图标和血条比例失衡 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f9a85170211848c9ad14c8d8e543b763~tplv-goo7wpa0wc-image.image) | 上半部的UI和下半部的UI表现风格需要一致，可以看到上半部类似卡通下半部更偏向3D古风，差异明显；另外自身设计血条和图标已经遮挡住大部分NPC的面积，导致BUG的出现； |
| 战力信息不整体，碎片感强，右侧入口功能过多过于复杂，导致学习成本增加和表现力较差 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1f7ccb4673e34dbd9119e79de784e07a~tplv-goo7wpa0wc-image.image) | 在玩法设计中，要区分功能的主次和优先级，使玩家能快速理解和适应 |
| HUD按钮与官方按钮规范标准差异明显 | ![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c8d47db6ef894aed98e4769707fc9679~tplv-goo7wpa0wc-image.image) | HUD按钮应该与官方按钮保持统一，使世界与世界之间的衔接更为紧密； |
## 
