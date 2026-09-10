> V2.2.0及其后续版本SDK已支持在Unity内配置物体Layer层级，配置和使用方式与Unity官方一致

# 官方 Layer 层
目前SDK已将 **0-21层** 定义为官方Layer层，创作者若要使用官方第9层（关闭物体与摄像机之间的碰撞），必须要确保层级命名与官方命名保持一致，不可自定义Layer层的名字。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/f64b7b1e76b44e8b9139e3e2db618bad~tplv-goo7wpa0wc-image.image" width="300px" /></div>

# 自定义 Layer 层
SDK内将 22-31层 定义为创作者可自定义的层级，创作者可根据项目需求来设置物体的Layer层规则。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/4f29874442c24f08860fc9d176c9180a~tplv-goo7wpa0wc-image.image" width="300px" /></div>

# 动态调整Layer层
你可以通过在代码中直接设置Layer层数字来动态修改物体的Layer层级，而不是通过设置layer层级名字来修改，例如：

```Lua
---@var obj:UnityEngine.GameObject
---@end
function Start()
    obj.layer = 22
end
```

# 注意事项

* 若是在项目中使用到Layer层，需要注意整个项目的文件夹路径上不能出现中文，否则会出现报错问题。
* 能够与Actor产生碰撞的Layer层目前固定为 0、3、7、9、10、18，若需要让物体与Actor产生碰撞，建议使用0层，也就是默认层。
