# 理解 ECS 工作流（Understand the ECS workflow）

> 来源：[Unity Package 官方文档 · Introduction to the ECS workflow](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-intro.html)

使用 Unity 实体组件系统（ECS）框架创建应用的工作流，无论从原理还是实现上，都与创建面向对象 Unity 应用的工作流不同。在使用该框架创建项目之前，先理解 ECS 工作流会很有帮助。

## 创建子场景（Create a subscene）

ECS 使用[子场景（subscenes）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/conversion-subscenes.html)来容纳应用的内容。你将 GameObject 和 MonoBehaviour 组件添加到子场景中，[烘焙器（bakers）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/baking-baker-overview.html)将 GameObject 和 MonoBehaviour 组件转换为实体和 ECS 组件。

## 创建 ECS 组件

[组件（Components）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-components.html)存储应用的数据。要创建应用中的行为，[系统（systems）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-systems.html)提供读取和写入 ECS 组件数据的逻辑。ECS 工作流是数据导向的，因此最佳实践是先规划好数据布局并创建 ECS 组件，然后再编写系统或创建实体。

不同类型的 ECS 组件用途不同。更多信息，请参阅[组件类型（Component types）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/components-type.html)。

## 创建实体

实体（Entities）表示应用中存在的不同事物。要在编辑器中创建实体，你需要向子场景添加 GameObject。[烘焙（baking）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/baking-overview.html)过程会将这些 GameObject 转换为实体。可选地，为了将 ECS 组件附加到转换后的实体上，你可以创建烘焙器（baker）。创建烘焙器时，你要定义它服务于哪个 MonoBehaviour 组件，然后编写代码，使用该 MonoBehaviour 组件的数据创建 ECS 组件并将其附加到转换后的实体上。你也可以从烘焙器创建额外的实体，并同样为它们附加 ECS 组件。在此工作流中，MonoBehaviour 组件称为创作组件（authoring component）。

> **提示**：组织上的好习惯是，为你创建的任何创作组件在类名后追加 `Authoring`。

你也可以在运行时创建实体。文档的 [ECS 工作流](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-tutorial.html)部分中的生成器（spawner）代码示例，展示了如何设置一个在运行时实例化实体的生成器系统。

## 创建系统

[系统（Systems）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-systems.html)创建应用中的行为。为此，它们可以查询并变换 ECS [组件](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-components.html)数据、创建和销毁实体，以及向实体添加或移除 ECS 组件。默认情况下，当你创建系统时，Unity 会实例化它并将其添加到默认[世界（world）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-worlds.html)中。

不同类型的系统用途不同。更多信息，请参阅[系统类型（System types）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-systems.html#system-types)。

## 优化系统

默认情况下，你在[系统](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/concepts-systems.html)中编写的任何代码都在主线程上同步运行。如果系统影响许多实体的数据，并且会从多线程中受益，最佳实践是创建 [Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest/index.html) 兼容的[作业（jobs）](https://docs.unity3d.com/6000.0/Documentation/Manual/JobSystem.html)，并尽可能调度它们并行运行。Burst 会将你的 C# 代码编译为优化的原生 CPU 代码，作业则让你可以将工作分发到多个线程，利用多个处理器。

如果系统做的工作不多，例如只处理少量实体的组件数据，那么并行调度作业的开销可能超过多线程带来的性能收益。要判断你的某个作业是否属于这种情况，请使用 [CPU Profiler](https://docs.unity3d.com/6000.0/Documentation/Manual/Profiler.html) 测量 Unity 在开启和关闭多线程的情况下运行作业代码所需的时间。如果调度开销导致 Unity 使用多线程运行作业代码的时间更长，请尝试以下方法优化作业：

- 在主线程上运行作业。更多信息，请参阅 [Run](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.IJobEntityExtensions.Run.html)。
- 如果系统是非托管 [ISystem](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/systems-isystem.html)，请用 [SystemAPI.Query](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.SystemAPI.Query.html) 加普通 `foreach` 替换作业。然后你可以将 [BurstCompile](https://docs.unity3d.com/Packages/com.unity.burst@latest/index.html?subfolder=/manual/compilation-burstcompile.html) 属性应用于包含 `SystemAPI.Query` 的函数，对查询和你的代码进行 Burst 编译。

## 其他资源

- [ECS 工作流示例](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-tutorial.html)
