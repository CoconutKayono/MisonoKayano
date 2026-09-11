> 原文：[Transform.hierarchyCapacity](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform-hierarchyCapacity.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).hierarchyCapacity

public int hierarchyCapacity;

### 描述

Transform 层级数据结构的容量。

Unity 会在内部使用独立的紧凑数据结构表示每个 Transform 层级，也就是一个根对象及其所有深层子对象。当 Transform 数量超过容量时，会调整此数据结构的大小。将容量设置为略大于预期最大层级大小的值，可以减少内存使用，并提高超大型层级中 Transform.SetParent 和 Object.Destroy 的性能。相关资源：Transform.hierarchyCount。


