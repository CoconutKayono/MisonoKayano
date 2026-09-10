抖音虚拟世界SDK支持 Unity 内置的 UGUI 系统，所以各位开发者可直接使用 UGUI 来设计世界的UI界面，下面将向各位创作者展示如何创建2个UI按钮和1张UI贴图，并通过UI按钮来打开/关闭UI贴图。
# 打开逻辑

1. 在 Hirarchy 面板上点击鼠标右键，然后按照 UI->Legacy->Button 来创建一个按钮。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f8425461709b49a69be2e9cfddbeaae8~tplv-goo7wpa0wc-image.image" width="2940px" /></div>


2. 在按钮的 Inspector 属性面板上调整它的位置和大小。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e12ae0b89a314954ad6e0e0ef4fc70d1~tplv-goo7wpa0wc-image.image" width="2940px" /></div>


3. 更换按钮的背景图和文本（若不想要文本，也可以直接删除Button的Text子级）。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/9c91b84ea031481587ba71856495a298~tplv-goo7wpa0wc-image.image" width="300px" /></div>


4. 在 Hirarchy 面板上点击鼠标右键，然后按照 UI->Image 来创建一个Image UI。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ceb91325e2574eed8a403bdd108590d7~tplv-goo7wpa0wc-image.image" width="300px" /></div>


5. 调整 Image 的大小、位置、以及Source Image。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c36f3f6a99b848a1877e084ea7feb925~tplv-goo7wpa0wc-image.image" width="300px" /></div>


6. 选择刚才创建的按钮，在 Inspector 面板上找到 On Click，然后点击+号，即可添加一个点击事件。将 Image 拖入到事件的 Object 属性中，并选择 GameObject 的 SetActive 方法，并对勾选框打勾。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c0979b5923d541cabe80a38a5cdae960~tplv-goo7wpa0wc-image.image" width="2940px" /></div>

# 关闭逻辑

1. 选中 Image，创建一个按钮作为它的子级。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4cdacd93f9ee4225bf8a8fda2921602d~tplv-goo7wpa0wc-image.image" width="300px" /></div>


2. 调整按钮的大小，位置，以及使用的图片。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b5969904d9674183b5e39b8e2a99eb20~tplv-goo7wpa0wc-image.image" width="500px" /></div>


3. 同样的步骤，给新增加的按钮添加一个点击事件。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/55ad1e8569774509ba831bfd69e89b96~tplv-goo7wpa0wc-image.image" width="300px" /></div>


4. 将 Image 拖入 Object 属性上，并选择GameObject 的 SetActive 方法，但这里不要对勾选框进行打勾。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/55173b32edb248fda6ae087e539a59ad~tplv-goo7wpa0wc-image.image" width="300px" /></div>


5. 选中 Image，并在 Inspector 面板上取消启用勾选。

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/760a2ee6b4e942d89bb39b0d87bf19f7~tplv-goo7wpa0wc-image.image" width="300px" /></div>

完成上述内容后，即可在测试场景查看效果。
注：别忘记给场景添加 Douyin World Root组件哦～
<video src=https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/86793f9702074331ae4ae4fd41302660~tplv-goo7wpa0wc-image.image></video>


