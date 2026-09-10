# 描述
您可以通过该类设置游戏中场景环境

# 公开属性
| [JsonAsset](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=6m0cryea) | 返回场景效果参数配置表，该对象通过读取json文件获取，并且不能被创建成一个新类 |
| --- | --- |
| [settings.enableMainLight](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=h4na9j8c) | 启用或配置主光源的属性调整面板 |
| [settings.mainLightType](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vmlx2smh) | 返回或设置主光源的模式。 |
| [settings.mainLightStrength](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=tmgegox4) | 返回或设置主光源的强度 |
| [settings.mainLightDir](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=k2hggtkd) | 返回或设置主光源的方向。 |
| [settings.enableShadow](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=imnm84xl) | 设置或返回光影模式。可用值为 None、Hard 和 Soft。 |
| [settings.shadowStrength](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vmx3p628) | 返回或设置主光源的阴影强度。 |
| [settings.enableCharacterLight](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=x6vy8m4i) | 启用或禁用角色光照照的属性面板。启用后场景内的角色将收此光照影响，未启用则仅受场景光源的影响。 |
| [settings.characterLightColor](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=yr1icjag) | 返回或设置角色光照的颜色。 |
| [settings.characterStrength](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=agy10y59) | 返回或设置角色光照的强度。 |
| [settings.characterRotation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7lhf8mox) | 返回或设置角色光照的方向。 |
| [settings.characterAmbientEnable](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=sassbdtk) | 启用或禁用环境的灯光配置。 |
| [settings.characterCubemapEnable](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=y0qlgogy) | 启用或配置角色的立方体贴图。 |
| [settings.characterAmbient](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4x6m3iid) | 返回或设置环境灯光的颜色。 |
| [settings.fogEnable](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1f8dha39) | 启用或禁用雾相关的配置面板 |
| [settings.fogColor](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=bn3hz1uv) | 返回或设置雾的颜色 |
| [settings.startFog](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ccnf5gyb) | 返回或设置雾的起始距离。 |
| [settings.endFog](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=xvyc3c2z) | 返回或设置雾的结束距离。 |
| [settings.skyMaterial](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4jujrvoa) | 返回或设置天空的材质对象。 |
| [settings.flareEnable](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4k4mhmgv) | 启用或禁用镜头光晕效果面板。 |
| [settings.followCamera](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=tk1dpefm) | 启用或禁用镜头光晕的效果是否跟随主相机 |
| [settings.lenFlare](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=pcyv34tw) | 返回或设置镜头光晕的数据对象。 |
| [settings.lenFlarePosition](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=mv4rtegr) | 返回或设置镜头光晕的位置。 |
| [settings.lenFlareIntensity](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1buqbw50) | 返回或设置镜头光晕的强度。 |
| [settings.lenFlareScale](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7vdv1qu7) | 返回或设置镜头光晕的缩放。 |
| [settings.lenFlareAttenuationDistance](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=epd1wvyg) | 返回或设置镜头光晕的衰减距离。 |
| [settings.lenFlareScaleDistance](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=62wk4lc9) | 返回或设置镜头光晕的缩放距离。 |
| [settings.lenFlareEnableOcclusion](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=29255i9w) | 启用或禁用镜头光晕的遮挡效果。 |
| [settings.lenFlareAllowOffScreen](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=d6wnsrq3) | 启用或禁用镜头光晕是否允许在屏幕外渲染 |
| [settings.enablePostProcess](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=q5sem9bb) | 启用或禁用后处理效果的属性面板 |
| [settings.BloomEnabled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cevew7q3) | 启用或禁用泛光效果 |
| [settings.BloomColor](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=dmilo4ef) | 返回或设置泛光颜色 |
| [settings.BloomThreshold](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1eipj588) | 返回或设置泛光的阈值，定义场景中哪些物体将出现泛光,即场景中物体亮度低于此阈值时将不会显示泛光效果 |
| [settings.BloomIntensity](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=u9r89r5g) | 返回或设置泛光的强度 |
| [settings.BloomScatter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=u91nt7pd) | 返回或设置泛光的范围 |
| [settings.LUT](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qp6gph9o) | 启用或禁用色彩校正的颜色查找表效果 |
| [settings.LutAmount](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=h88ofh5c) | 返回或者设置颜色校正的颜色数量 |
| [settings.SourceLut](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1s6mg2l7) | 返回或者设置颜色校正的贴图 |
| [settings.ImageFiltering](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qaka00xb) | 启用或者禁用图片校色效果 |
| [settings.Color](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=chyxed1y) | 返回或者设置图片校色的颜色 |
| [settings.Contrast](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=saardvnb) | 返回或者设置图片校色的对比度 |
| [settings.Brightness](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fyt2tke7) | 返回或者设置图片校色的亮度 |
| [settings.Saturation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7i106lmu) | 返回或者设置图片校色的饱和度 |
| [settings.ChromaticAberration](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=iz6r8udt) | 启用或者禁用图片色差效果 |
| [settings.Offset](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=184np5cp) | 返回或者设置图片的偏移量 |
| [settings.Distortion](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=uzlf55vi) | 启用或者禁用暗角 |
| [settings.DistortionIntensity](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=bab5wpas) | 返回或者设置暗角强度 |
| [settings.Vignette](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=mwvcm8e6) | 启用或禁用屏幕渐晕效果 |
| [settings.VignetteColor](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/68c24893830327054af6cc3e?docLang=zh&bv=67e3b8b8505b920501ed9219) | 返回或者设置屏幕渐晕颜色 |
| [settings.VignetteAmount](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=pcf2dopd) | 返回或者设置屏幕渐晕强度 |
| [settings.VignetteSoftness](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vdwjtu84) | 返回或者设置屏幕渐晕平滑度 |
| [settings.EnableCustomizedPass](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5dw5nlns) | 启用或者禁用自定义后期处理 |
| [settings.CustomizedPassMaterial](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=f8fwkpgq) | 启用后，自定义后期处理材质 |
# 公开方法
| [LoadJson](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=l6rzhr8n) | 加载一个json asset的数据对象，对环境参数进行配置 |
| --- | --- |
| [Change](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=y795qmo5) | 在规定的时间帧内，将当前环境的切换至目标环境 |

