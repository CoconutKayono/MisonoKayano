function OnPickUp(DouyinActor actor, HandType hand, Matrix4*4 pickUpPoint ＝ Matrix4*4.identify)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| actor | 与载物体进行交互的 Actor |
| hand | 玩家在屏幕上点击的区域 |
| pickupPoint | 玩家点击物体的交点相对于物体原始点的变换矩阵，默认为 Matrix4*4.identify |
# 描述
当物体被 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)捡起时触发，调用 Api 时触发。

