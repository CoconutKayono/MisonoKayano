问：在使用 Douyin/World/ENV/World_Lit shader时，将 NormalScale 参数设置为1后，如果出现模型面光照异常，该如何解决？
答：有2种解决方案。

1. 弄一张RG为0.5 BA都为1 Normalmap贴上，然后将取消勾选贴图的SRGB
2. 把NormalScale设置为0


