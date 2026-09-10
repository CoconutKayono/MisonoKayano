public Quaternion GetBoneRotation(HumanBodyBones humanBoneId)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| humanBoneId | 一个枚举类型的参数，代表人体骨骼的标识。它用来指定要获取旋转信息的具体骨骼。 |

# 返回
Quaternion
指定骨骼在世界空间中的旋转信息。
若 DouyinService.Proxy 为 null，则返回 Quaternion.identity，表示无旋转状态。

# 描述
获取 [Actor ](https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219https://arcosite.bytedance.net/sites/1724838533199/67e3b8b7505b920501ed9205/editor/680da496fe7e0d0504f399c5?docLang=zh&bv=67e3b8b8505b920501ed9219)特定骨骼的旋转信息。

