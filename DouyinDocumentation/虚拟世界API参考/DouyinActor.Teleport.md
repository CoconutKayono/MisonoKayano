# 重载一
public void Teleport(Vector3 pos)
## 参数
| 参数  | 参数描述 |
| --- | --- |
| pos | 指定传送的 Position |
## 描述
将当前的  [Actor  ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)传送到指定位置，且无旋转角度。

# 重载二
public void Teleport(Vector3 pos, Quaternion rot)
## 参数
| 参数 | 参数描述 |
| --- | --- |
| pos | 指定传送的 Position |
| rot | 指定传送后的旋转角度 |
## 描述
将当前的 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)传送到指定位置，且可定义传送后的角度。
