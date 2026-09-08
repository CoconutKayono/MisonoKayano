# 消息系统（Messaging System）

新的 UI 系统使用了一套旨在取代 **SendMessage** 的消息系统。它是纯 C# 的实现，专门用来解决 SendMessage 的一些问题。它通过自定义接口工作：在 MonoBehaviour 上实现相应接口，即表示该组件能够接收消息系统发来的回调。发起调用时，需要指定一个目标 GameObject；调用会派发给该 GameObject 上所有实现了指定接口的组件。消息系统允许携带自定义数据，并指定事件在 GameObject 层级中的传播范围——是只在目标 GameObject 上执行，还是同时向子级、父级扩散。此外，消息框架还提供了辅助函数，用来查找实现了指定消息接口的 GameObject。

消息系统是通用的，不仅服务于 UI 系统，也适用于一般游戏代码。添加自定义消息事件很简单，它们与 UI 系统的事件处理走的是同一套框架。

## 定义自定义消息

如果你想定义一条自定义消息，其实很简单。在 `UnityEngine.EventSystems` 命名空间中有一个名为 **IEventSystemHandler** 的基础接口。凡是继承自该接口的类型，都可作为消息系统的事件接收目标。

```csharp
public interface ICustomMessageTarget : IEventSystemHandler
{
    // functions that can be called via the messaging system
    // 可以通过消息系统调用的函数
    void Message1();
    void Message2();
}
```

一旦定义了此接口，就可以由 MonoBehaviour 实现。实现后，它就定义了在对此 MonoBehaviour 的 GameObject 发出给定消息时要执行的函数。

```csharp
public class CustomMessageTarget : MonoBehaviour, ICustomMessageTarget
{
    public void Message1()
    {
        Debug.Log ("Message 1 received");
    }

    public void Message2()
    {
        Debug.Log ("Message 2 received");
    }
}
```

既然已经有了能接收消息的脚本，下一步就是发出消息。通常，发送消息是为了响应某个低耦合的事件。例如 UI 系统中的 PointerEnter、PointerExit，以及由用户输入触发的各种事件，都是这样派发的。

发送消息需要使用一个静态辅助类。它需要三个参数：消息的目标对象、用户自定义数据，以及指向目标接口中具体方法的委托（functor）。

```csharp
ExecuteEvents.Execute<ICustomMessageTarget>(target, null, (x,y)=>x.Message1());
```

此代码将在目标 GameObject 上实现了 `ICustomMessageTarget` 接口的任何组件上执行 `Message1` 函数。`ExecuteEvents` 类的脚本文档涵盖了 Execute 函数的其他形式，例如在子级或父级中执行。

---

相关文档：[[01-SupportedEvents-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
