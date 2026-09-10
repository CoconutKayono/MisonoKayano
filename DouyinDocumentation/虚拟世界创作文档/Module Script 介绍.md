之前我们有介绍过Douyin Script，通过Douyin Script组件来加载的lua文件，这样就具备类似Unity 的Mono Behaviour组件的功能以及数据序列化的能力。
但是，其他作用的lua文件例如：lua配置文件、公共基础库和第三方库该如何整合到Douyin world 工程中呢？我们称这类lua文件为**”Module Script“**，本章节将介绍如何加载和管理Module Script。
# Douyin Script Loader组件
用来加载和管理Module Script的组件叫做"Douyin Script Loader组件"，如下图所示：
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/694dbf996c2148e4a202d2836c88fc03~tplv-goo7wpa0wc-image.image" width="264px" /></div>

具体使用方法如下：

1. 在一个对象上添加Douyin World Root 组件以后，会自动添加Douyin Script Loader组件。
2. 该组件有一个默认配置项和一个自定义配置项：

默认配置项：指的是Douyin Scripts Folder字段，这个文件夹指向的是Douyin world 提供的官方Module Script目录。你可以点击查看该目录中的lua文件并修改它们。如果你编辑修改了官方Module Script，请注意备份，因为在SDK升级时候，它们可能会被重置或者移除。官方Module Script的介绍请查看[官方 Module Script](/s196aspp/ba7j8gvf)。
自定义配置项：指的是Custom Scripts Folder字段，可配置每个场景自定义Module Script的目录位置。
# Module Script是如何存储和加载的？
Douyin Script Loader管理的Module Script会在Unity场景保存时，序列化成二进制数据保存到Unity场景中。每个场景在被创建后会创建新的Lua虚拟机，之后加载执行Douyin Script Loader管理的lua文件。
场景加载完成后，Douyin Scripts Folder 中的index.lua 文件会先于Custom Scripts Folder 的index.lua 文件被执行。 这两个目录中的index.lua 文件会优先于所有Douyin Script管理的lua文件被执行。
每个场景只允许一个Douyin Script Loader实例，添加Douyin World Root组件时自动挂载。

