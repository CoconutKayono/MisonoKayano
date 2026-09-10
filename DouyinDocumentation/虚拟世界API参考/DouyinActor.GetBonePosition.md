public Vector3 GetBonePosition(HumanBodyBones humanBoneId)
# 参数
| 参数  | 参数描述 |
| --- | --- |
| humanBoneld | 一个枚举类型的参数，用于指定要获取位置的人体骨骼。HumanBodyBones 枚举定义了人体各个骨骼的标识符 |

# 返回
Vector3
指定骨骼在世界空间中的位置。
如果 DouyinService.Proxy 为 null，则返回 Vector3.zero（即坐标为 (0, 0, 0)的位置）。

# 描述
获取 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)指定人体骨骼在世界空间中的位置。

