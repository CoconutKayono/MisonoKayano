# ECS 包（ECS packages）

> 来源：[Unity Package 官方文档 · ECS packages](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-packages.html)

Unity 的数据导向技术栈（DOTS）使用多个包（包括 Entities）以及 Unity 引擎的各个部分，它们协同工作，帮助你编写高性能代码。

你需要使用的主要 Unity 组成部分有：

- **Entities**（本包）：实体、组件、系统（ECS）模式的一种实现。
- [Job System](https://docs.unity3d.com/Manual/JobSystem.html)：用于快速、安全、多线程代码的解决方案。
- [Burst 编译器](https://docs.unity3d.com/Packages/com.unity.burst@latest)：生成高度优化代码的 C# 编译器。
- [Collections](https://docs.unity3d.com/Packages/com.unity.collections@latest)：一组非托管集合类型，例如列表和哈希表。它们在作业和 Burst 编译代码中很有用，因为这些上下文只能访问非托管数据。
- [Mathematics](https://docs.unity3d.com/Packages/com.unity.mathematics@latest)：一个数学库，在 Burst 编译代码中经过了专门优化。

在这些核心组成部分之上，还有以下实体组件系统（ECS）包：

- [Unity Physics](https://docs.unity3d.com/Packages/com.unity.physics@latest)：用于实体的无状态、确定性物理系统。
- [Netcode for Entities](https://docs.unity3d.com/Packages/com.unity.netcode@latest)：用于实体的客户端-服务器网络代码解决方案。
- [Entities Graphics](https://docs.unity3d.com/Packages/com.unity.entities.graphics@latest)：使用可编程渲染管线（SRP）渲染实体。
- [Character Controller](https://docs.unity3d.com/Packages/com.unity.charactercontroller@latest)：包含用于创建基于 ECS 的角色控制器的机制。
