# 开启WebGL模式
**平台上线WebGL模式，选择开启这个模式，IOS设备下世界的画质模糊会得到极大的改善，同时延迟也有缓解。**
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/05a6d8befce4449ca6748d1af16e8afc~tplv-goo7wpa0wc-image.image" width="1086px" /></div>



* 开启方式：可在创作后台-性能分析-右上角选择是否开启该模式
   * 自动：按照每0.5天灰度1/4用户，在结束灰度后，若不符合性能数据标准，所选世界将会继续保持云游戏状态
   * 全量：将当前所选世界线上版本直接开启WebGL模式
   * 关闭：不使用WebGL模式
* 开启前提：性能分析-内存均值 小于 1300MB，否则将会引起手机发烫等问题
* 启用影响：用户首次进入世界加载会有点长，后续加载将会正常。
* shader标准：#pragma target 3.0 不能大于 3.0 

* 针对世界性能优化，创作者可参考 [世界性能](/s196aspp/bw4mzji9)

# WebGL测试
因为WebGL模式开启后将会对世界渲染产生影响，所以在对已上线的世界开启前需要检查是否有影响，若出现问题需要进行修复。
创作者可按照如下步骤对线上世界进行检查：

1. 在后台选择世界，进入版本管理
2. 点击线上版本右侧的体验版本二维码，选择WebGL模式，使用IOS设备进行扫码测试
3. 查看扫码测试世界是否正常，若有显示问题，可进行对世界进行一次云处理，云处理结果将会显示出相关问题
4. 若有问题，结合云处理结果进行修复
5. 若无问题，可按照需求选择是否开启WebGL模式

![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/edcf6a4cc1fd429abe9758b9828ac15f~tplv-goo7wpa0wc-image.image)
# 注意事项
在开启WebGL后，可能会对项目的表现效果产生一些影响，主要为：

* 部分Text字体不兼容，需要手动调整为其他字体
* 项目中所使用的Shader中，若target大于3.0，将会出现材质异常问题，可以将shader的target调整为3.0即可

