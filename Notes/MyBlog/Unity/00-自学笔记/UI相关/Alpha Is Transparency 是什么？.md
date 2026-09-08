## Alpha Is Transparency 是什么？

官方Inpector上的原文

```text
If the alpha channel of your texture represents
transparency,enable this property to dilate the
color channels of visible texels into fully transparent
areas. This effectively adds padding around
transparent areas that prevents filtering artifacts
from forming on their edges.Unity does not support
this property for HDR textures.
This property makes the color data of invisible
texels undefined. Disable this property to preserve
invisible texels' original color data.
```

这句是 Unity 纹理导入设置里 **Alpha Is Transparency（Alpha 是透明度）** 的说明。

> 若纹理的 Alpha 通道表示透明度，启用此属性可将可见纹素（texel）的颜色通道向完全透明的区域扩张，相当于在透明区域外圈填充一圈颜色，从而防止过滤（filtering）在这些边缘处产生伪影。Unity 不支持对 HDR 纹理使用此属性。启用后，不可见纹素的颜色数据将不再有定义；若要保留不可见纹素原有的颜色数据，请禁用此属性。

几个词的处理说明：

- **texel** 译为"纹素"，即纹理元素（texture element），比"像素"更准确，因为这里说的是纹理空间而非屏幕空间。
- **dilate** 译为"扩张"，突出颜色向透明区域"蔓延"的动作，比"膨胀"更贴合图形学语境。
- **filtering artifacts** 译为"过滤伪影"，指 mipmap 或线性过滤时透明边缘出现的灰边/色边问题。

开启它主要解决**显示**上的边缘渗色问题，和 `alphaHitTestMinimumThreshold` 的**点击命中**是两码事——后者仍然要依赖 Read/Write Enabled 和禁用图集打包。

既然它是解决伪影的，那么伪影是什么呢？

简单理解就是模糊，有锯齿等表现。