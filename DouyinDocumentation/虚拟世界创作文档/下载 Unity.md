# 简介
抖音虚拟世界运行平台基于 Unity 开发，为方便创作者上传世界资产，我们推出了 DouyinWorld SDK。借助Douyin World SDK 提供的基础组件，即使你没有 Unity 使用经验，也能快速上传虚拟世界资产。 
请注意，Douyin World SDK 支持的 Unity 版本为 **2021.3.14f1**，请务必使用指定版本的Unity，其他版本均无法正常使用 Douyin World SDK。如果你还没有安装该版本，请按照以下流程进行安装。 
# **下载与安装 Unity Hub**

1. [点击此链接下载Unity Hub](https://unity.com/cn/download) **** ，Unity Hub是一个用于管理 Unity 版本和项目的工具，请选择下载对应操作系统的安装包，之后双击安装包进行安装。安装成功后会弹出最新版本的Unity安装界面，这里可直接忽略，因为此处下载的Unity版本并非我们需要的指定版本，我们要安装**Unity 2021.3.14f1** 版本（下方有安装链接）。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a4db4a749dc4458aa82d24a9d274b6d3~tplv-goo7wpa0wc-image.image)

2. **Unity Hub 界面设置成中文**

点击左上角的**Preferences**（偏好设置）按钮，选择**Appearance**(外观)，在语言选择栏选择简体中文。 

<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/30a8eeddce0c4afeb80a0196e4dd186f~tplv-goo7wpa0wc-image.image" width="500px" /></div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/da01607f720c47bfb3c0a9b9692cd448~tplv-goo7wpa0wc-image.image" width="500px" /></div>



</div>
</div>

此后，你还可以根据自己的需求，来调整后续Unity编辑器安装的目录，保存项目的目录等设置。
> 注：目录不要带任何中文或特殊符号
> 注：可按照Unity官方要求注册Unity账号，并登陆Unity Hub

# 安装 Unity 2021.3.14f1

* Windows用户请点击下载链接：[2021.3.14f1 Unity-Windows版本安装包](https://p26-avatar-webassets.byteimg.com/tos-cn-i-14ueo239jh/UnitySetup64-2021.3.14f1.exe)

这里提供的是本地安装包，下载安装包后双击按照操作步骤进行安装即可。
安装完成后，可在Unity Hub上关联所安装的Editor版本。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/1901ff6e6e374b0787c9e958202014ed~tplv-goo7wpa0wc-image.image" width="540px" /></div>


* Mac用户需要注意区分电脑使用的芯片

点击左上角的苹果图标—**关于本机**，查看使用的Mac是Apple芯片还是Intel芯片，选择对应芯片的Unity版本进行安装。 

<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

   <div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/7f94760a165e4b4f95e390fd1252c509~tplv-goo7wpa0wc-image.image" width="200px" />   </div>





</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/469bc05c027240538643ef107802de68~tplv-goo7wpa0wc-image.image" width="100%" /></div>




</div>
</div>

# 个人许可证
Unity可申请免费的个人许可证使用，且当许可证到期后，可继续申请免费个人许可证。

1. 点击左上角的**偏好设置**（Preferences）按钮。 

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/710720791b764b9c885990657708c86b~tplv-goo7wpa0wc-image.image)

2. 在面板中选择**许可证**，然后点击**添加**。 

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/94103d0a066d489bb95f9e90f6487f3b~tplv-goo7wpa0wc-image.image)

3. 选择**获取免费的个人版许可证**。 

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/83affebdc3294e8aa8c04b5675df64c6~tplv-goo7wpa0wc-image.image)

4. 阅读服务条款并单击同意，即可成功添加免费的个人许可证。 

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8f016983480f4e309362e6b241143146~tplv-goo7wpa0wc-image.image)

---


完成以上步骤后，就代表Unity安装完成，接下来请安装 Douyin World SDK。
