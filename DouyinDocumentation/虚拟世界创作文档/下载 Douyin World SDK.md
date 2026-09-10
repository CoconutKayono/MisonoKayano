# 下载
在正式创作之前，还需要先下载SDK，并搭建配置好创作环境。
| 名称 | 下载链接 |
| --- | --- |
| **抖音虚拟世界 SDK** | [https://vcreate.douyin.com/api/sdk/world](https://vcreate.douyin.com/api/sdk/world)  |
| **官方API文档** | https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=azx6jlfl |
# 创建项目

1. 在Unity Hub中点击**项目**，并**新建项目**。 

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8b8637ed4f764857b382ddf058b69cba~tplv-goo7wpa0wc-image.image)

2. 在创建项目页面下，选择**Universal 3D**模板（URP模板），注意看上面是否是 **2021.3.14f1** 版本，首次创建项目会提示需要下载一个模板工程，点击下载模板。 

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/28a08221747c4fe58aaf28a469703bb3~tplv-goo7wpa0wc-image.image)

3. 给新建的项目设置名字和路径，点击**创建项目**，创建项目需要一定时间，请耐心等待。 

> 注：请创建本地项目，不要创建云项目

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/84cf65041bd24469886ec1533e81d8a8~tplv-goo7wpa0wc-image.image)

* 如果弹出这个面板可点击**继续**，这个报错没有影响，这样就完成了工程创建。 


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">


<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8207e60e396340b5883ddd72dcf2a2a2~tplv-goo7wpa0wc-image.image" width="264px" /></div>

<div style="text-align: center">中文报错-点击“继续”</div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">


<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/81e2eb84408d404fa8f4725ec36f9901~tplv-goo7wpa0wc-image.image" width="264px" /></div>

<div style="text-align: center">英文报错-点击"Continue"</div>



</div>
</div>

# 导入Douyin World SDK

1. 在开始前，可以先把默认的界面语言改为中文，按照以下流程点击“Edit-Preference-Languages-Editor language-简体中文” ，待加载完成后即可切换为中文界面（注意：创建和使用文件夹时，请使用英文目录和路径）


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/406e0a2d25634af581280daf7f434b85~tplv-goo7wpa0wc-image.image" width="325px" /></div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ab81482ce7244a50a834fe649c455ae1~tplv-goo7wpa0wc-image.image)


</div>
</div>


2. 完成项目创建后，将下载好的 DouyinWorld SDK的 Unity Package 拖入Assets文件夹内，此时会弹出资源导入面板，点击"**导入**"完成导入。 


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.3333);">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4de95998c7c64e8680f055f0eaffebcf~tplv-goo7wpa0wc-image.image" width="264px" /></div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.3333);margin-left: 16px;">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/11bc7e517b534f50947d5f12c669a0b6~tplv-goo7wpa0wc-image.image" width="264px" /></div>



</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.3333);margin-left: 16px;">

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a5b9d2c1819741e1a0abc84f54421d4e~tplv-goo7wpa0wc-image.image" width="264px" /></div>



</div>
</div>


3. 导入成功后，SDK就安装好了，我们可以在 Unity 菜单栏看到**抖音虚拟创作SDK**。 

<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/009acc31a3474c9387ded77655f91094~tplv-goo7wpa0wc-image.image" width="2560px" /></div>

安装完SDK后，我们就可以开始创建世界了！ 
