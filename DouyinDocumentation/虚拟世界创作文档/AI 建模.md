目前市面上有各种各样的AI建模产品和插件，本篇教程将分享混元-3D AI建模产品，相对于其他AI建模产品而言，该产品上手难度较低，支持低模拓扑，且在国内即可免费使用。
## 产品地址
混元3D：https://3d.hunyuan.tencent.com/
## 工具使用

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b4daf4e5a33d44dca38a51889e90ce05~tplv-goo7wpa0wc-image.image)
目前工具支持文生3D和图生3D等2种模式，也可以直接在灵感广场下载预设好的模型使用。
在生成模型时，模型面数越高，生成的模型越精细；但若是要用在世界内，需要使用较低面数的模型，因为模型面数越高，内存越大，加载越慢。
## 3D Studio
> 3D Studio需要申请使用权益，按照提示申请即可

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/c3267826116a440285dab22eac34f439~tplv-goo7wpa0wc-image.image)
这里要重点介绍的是混元3D的3D Studio，因为3D Studio支持低模拓扑。
这里以生成道具为例子，在3D Studio中，选择道具进入设计页面。


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/b89d29b3069049eca9ea3b8583a7fe7e~tplv-goo7wpa0wc-image.image)


</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a642f94b7025424c9be4e9c7ec51bee0~tplv-goo7wpa0wc-image.image)


</div>
</div>

输入文本，并选择自己想要的风格，然后点击立即生成，即可生成一张概念图。


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/29f5daab01a848a885661ba9bfa57f4c~tplv-goo7wpa0wc-image.image)


</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/06188007598f46ff938d4fd906ba77b3~tplv-goo7wpa0wc-image.image)


</div>
</div>

选择几何生成，使用刚才生成的概念图，选择想要的模型面数，点击立即生成后，等待模型生成即可。


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/cbc95255531941f29e908d18ea32cbb9~tplv-goo7wpa0wc-image.image)


</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/e92d9c4c830342b2bfaabca8b0e4e371~tplv-goo7wpa0wc-image.image)


</div>
</div>

选择低模拓扑来减少模型面数，这里的模型面数选择低，选择拓扑三角面，点击立即生成后，等待模型生成即可。


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/a57c9575507347d9994eb3464e2480d2~tplv-goo7wpa0wc-image.image)


</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.5000);margin-left: 16px;">

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/5b5599aa557749ed99103b142b63ca97~tplv-goo7wpa0wc-image.image)


</div>
</div>

这里，我们没有选择展UV（可以根据需求自己选择），而是直接生成纹理，选了一张图片，使用了图生纹理；在生成模型后，可根据需求下载对应格式的内容，比如：obj格式的模型。

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/28c7133280a54cd98926a467d3200e31~tplv-goo7wpa0wc-image.image)
如果此时，直接将fbx格式的模型导入Unity，你会发现模型是一个白模，你可以在Unity中选中导入的模型，然后在Inspector面板上选择 Materials，然后点击 Textures 的 Extract Texures... 并选择与模型相同的文件夹目录，等待片刻即可完成材质贴图修复。










