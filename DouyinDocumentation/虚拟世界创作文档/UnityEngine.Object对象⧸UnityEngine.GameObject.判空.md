1. **原理**：当UnityEngine.Object/GameObject被销毁时，Lua侧的userdata还在，但是Unity以及C#侧的对象已经被销毁，此时使用xxx == nil无法判断出对象是否为空。解决方案如下
2. 需要先判断Lua对象是否为nil，可以使用 xxx.IsNull() 或者 xxx.Equals(nil) 来判断Unity Object是否为nil
