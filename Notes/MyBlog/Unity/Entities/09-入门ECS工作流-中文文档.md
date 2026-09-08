# 入门 ECS 工作流（Starter ECS workflow）

> 来源：[Unity Package 官方文档 · Starter ECS workflow](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-example-starter.html)

本示例演示了一个基本的实体组件系统（ECS）工作流，包含以下任务：

- 创建 ECS 组件。
- 创建 ECS 系统，用于创建实体并为其添加组件。
- 在 Hierarchy 窗口的 Default World 节点下查看实体。

## 前提条件

本工作流需要一个已安装 Entities 包的 Unity 6 项目。

## 创建 ECS 组件

ECS 有多个组件类型，本示例使用最常见的一种：基于 `IComponentData` 接口的组件。

示例组件类型是一个结构体（struct）。它是非托管类型，与始终为托管类型的 GameObject 组件相比，具有很多性能优势。

要创建 ECS 组件：

1. 创建一个名为 `HelloWorld.cs` 的新 C# 脚本，并将文件内容替换为以下代码示例。

```csharp
using Unity.Entities;
using Unity.Collections;
using UnityEngine;

// This is an example of an unmanaged ECS component.
public struct HelloComponent : IComponentData
{
    // FixedString32Bytes is used instead of string, because
    // struct IComponentData can only contain unmanaged types.
    public FixedString32Bytes Message;
}
```

`HelloComponent` 组件包含一个类型为 `FixedString32Bytes` 的 `Message` 变量。由于 `struct IComponentData` 只能包含非托管类型，你不能使用普通的 C# `string` 类型变量。本示例使用 `FixedString32Bytes` 类型，它是一种非托管类型，并且具有固定大小。

现在项目有了一个可以添加到实体上的 ECS 组件。

## 创建 ECS 系统

在 ECS 中，你使用系统来创建和操作实体及组件。ECS 系统是实现 `ISystem` 接口的结构体。

要创建 ECS 系统：

1. 在 `HelloWorld.cs` 脚本中，添加以下基于 `ISystem` 接口的结构体：

```csharp
public partial struct ExampleSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        var entity = state.EntityManager.CreateEntity();
        // Initialize and add a HelloComponent component to the entity.
        state.EntityManager.AddComponentData(entity, new HelloComponent 
            { Message = "Hello ECS World" });
        // Set the name of the entity to make it easier to identify it.
        // Note: the entity Name property only exists in the Editor.
        state.EntityManager.SetName(entity, "Hello World Entity");
    }

    public void OnUpdate(ref SystemState state)
    {
        // The query retrieves all entities with a HelloComponent component.
        foreach (var message in
                    SystemAPI.Query<RefRO<HelloComponent>>())
        {
            Debug.Log(message.ValueRO.Message);
        }
    }
}
```

2. 进入 Play 模式。
3. 控制台会显示 `Hello ECS World` 消息。

系统在 `OnCreate` 方法中创建了一个新实体，并向该实体添加了一个 `HelloComponent` 组件实例。

在 `OnUpdate` 方法中，系统使用查询表达式查找所有带 `HelloComponent` 组件的实体，并在控制台写出组件中的消息。

## 在 Hierarchy 窗口中查看实体

系统在运行时创建实体，这意味着该实体只在进入 Play 模式后才会在编辑器中可见。由于实体不是 GameObject，它不会显示在子场景节点下。ECS 在 Hierarchy 窗口中提供了 **Editor/Default World** 节点，你可以在这里查看 ECS 世界中的实体。

要查看系统创建的实体：

1. 进入 Play 模式。
2. 在 Hierarchy 窗口中展开 **Default World** 节点。Hierarchy 会显示名为 `Hello World Entity` 的新实体，该名称由 `EntityManager.SetName` 方法定义。
3. 选择新实体，在 Entity Inspector 中查看它。Inspector 会显示 `HelloComponent`。

> 图片说明：显示新实体的 Hierarchy 窗口，以及显示新 ECS 组件的 Inspector。

## 完整代码

这是 `HelloWorld.cs` 脚本的完整代码：

```csharp
using Unity.Entities;
using Unity.Collections;
using UnityEngine;

// This is an example of an unmanaged ECS component.
public struct HelloComponent : IComponentData
{
    // FixedString32Bytes is used instead of string, because
    // struct IComponentData can only contain unmanaged types.
    public FixedString32Bytes Message;
}

public partial struct ExampleSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        var entity = state.EntityManager.CreateEntity();
        // Initialize and add a HelloComponent component to the entity.
        state.EntityManager.AddComponentData(entity, new HelloComponent 
            { Message = "Hello ECS World" });
        // Set the name of the entity to make it easier to identify it.
        // Note: the entity Name property only exists in the Editor.
        state.EntityManager.SetName(entity, "Hello World Entity");
    }

    public void OnUpdate(ref SystemState state)
    {
        // The query retrieves all entities with a HelloComponent component.
        foreach (var message in
                    SystemAPI.Query<RefRO<HelloComponent>>())
        {
            Debug.Log(message.ValueRO.Message);
        }
    }
}
```

## 其他资源

- [ECS 工作流简介](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-intro.html)
- [创作与烘焙工作流示例](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-example-authoring-baking.html)
- [预制件实例化工作流](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-example-prefab-instantiation.html)
- [让系统多线程化](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/ecs-workflow-example-multithreading.html)
