想要在Lua脚本中调用Unity API，需要注意如下事项：

* 先确定想要使用的 Unity API 是否被SDK支持，可查看 [SDK API白名单](/4j78bceb/kw7xp55s)
* 在使用 API 时需要书写API所在的完整命名空间
* 如果想要使用 GetComponent/AddComponent 需要在参数中增加 typeof 来获取 Unity 类

可以参考如下示例：

```Go
function Start()
    local obj = self.gameObject
    local collider = obj:AddComponent(tyepeof(UnityEngine.BoxCollider))
    local rigidbody = obj:GetComponent(typeof(UnityEngine.Rigidbody))
end
```


