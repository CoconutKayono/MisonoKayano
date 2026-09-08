# Entities 1.4 新特性（What's new in Entities 1.4）

> 来源：[Unity Package 官方文档 · What's new in Entities 1.4](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/whats-new.html)

本部分包含 Entities 1.4 中新增功能、改进和已修复问题的信息。

有关 Entities 1.4 所做更改的完整列表，请参阅 [Changelog](https://docs.unity3d.com/Packages/com.unity.entities@6.6/changelog/CHANGELOG.html)。

## 弃用的 API

在此版本中，以下 API 被标记为过时（obsolete）：

- `Entities.ForEach` 和 `Job.WithCode` 方法被标记为过时。

请改用以下 API：

- 使用 [IJobEntity](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.IJobEntity.html) 和 [SystemAPI.Query](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.SystemAPI.Query.html) 代替 `Entities.ForEach`。
- 使用 [IJob](https://docs.unity3d.com/6000.1/Documentation/ScriptReference/Unity.Jobs.IJob.html) 代替 `Job.WithCode`。

- [IAspect](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.IAspect.html) 接口被标记为过时。请改用 [Component](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/components-read-and-write.html) 和 [EntityQuery](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.EntityQuery.html) API。
- [ComponentLookup.GetRefRWOptional](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ComponentLookup-1.GetRefRWOptional.html) 和 [GetRefROOptional](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ComponentLookup-1.GetRefROOptional.html) 方法被标记为过时。这些方法是为 Aspect 源码生成而设计的，仅用于内部用途。请改用 [TryGetRefRO](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ComponentLookup-1.TryGetRefRO.html) 和 [TryGetRefRW](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ComponentLookup-1.TryGetRefRW.html) 方法，以获得更好的安全性和清晰度。

以上所有 API 在 Entities 1.x 包中仍受支持，但将在未来某个 Entities 主版本中移除。

有关升级到 Entities 1.4 的更多信息，请参阅[升级指南](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/upgrade-guide.html)。

## 改进

此版本在可用性、性能和工作流方面进行了改进，同时扩展了 API 能力和文档覆盖范围。

**System Inspector 窗口改进：**

- Queries 选项卡现在会显示执行查询时的以下组件状态：Disabled（禁用）、Present（存在）、Absent（缺失）和 None（无）。
- 新增 **Dependencies** 选项卡，显示系统依赖哪些组件。
- Query 窗口改进：窗口会用适当的图标高亮预制件，以区别于其他实体。

- [WorldUnmanaged](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.WorldUnmanaged.html) 结构体新增 [GetSystemTypeIndex(SystemHandle SystemHandle)](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.WorldUnmanaged.GetSystemTypeIndex.html#Unity_Entities_WorldUnmanaged_GetSystemTypeIndex_Unity_Entities_SystemHandle_) 方法，可让你从 `SystemHandle` 获取 `SystemTypeIndex`。

**[RemoteContentCatalogBuildUtility.PublishContent](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.Content.RemoteContentCatalogBuildUtility.PublishContent.html) 方法改进：**

- 该方法现在会为所有对象和场景创建内容集（content sets），并使用 `UntypedWeakReferenceId.ToString` 方法的结果作为内容集的名称。这样可以下载特定对象和场景的依赖。对于子场景（subscenes），内容集以 GUID 命名，并包含头部、所有实体分段（entity section）文件，以及内容存档中的任何 Unity 对象引用。
- 该方法现在会在远程内容文件夹的根目录创建 `DebugCatalog.txt` 文本文件，其中包含所有重映射（remapping）信息。该文件显示每个文件如何被重映射到其缓存位置、其 `RemoteContentId` 是什么，还会列出 Publish 步骤中定义的所有内容集。
- 该方法现在接受可枚举的文件列表，而不是目录名。这确保内容更新只包含目录中指定的文件，而不是文件夹中的所有文件。

**安全组件访问：** 新的 [ComponentLookup.TryGetRefRW](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ComponentLookup-1.TryGetRefRW.html) 和 [ComponentLookup.TryGetRefRO](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ComponentLookup-1.TryGetRefRO.html) 方法让你可以通过一次方法调用安全地检查组件是否存在，并从实体中检索它。

**自定义编辑器增强：** 在 `WeakReferencePropertyDrawer` 类中添加了 `OnGUI` 重写，确保 `WeakObjectReference`、`WeakObjectSceneReference`、`EntitySceneReference` 和 `EntityPrefabReference` 字段正确显示。

**世界引导（World bootstrapping）管理：** 为使用 [ICustomBootstrap](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ICustomBootstrap.html) 的类型或程序集新增了 [DisableBootstrapOverridesAttribute](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.DisableBootstrapOverridesAttribute.html) 属性，以防止意外的引导实现。

**Buffer API 改进：** 在 `ArchetypeChunk` 结构体中添加了 [GetBufferAccessorRO](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ArchetypeChunk.GetBufferAccessorRO.html) 和 [GetBufferAccessorRW](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ArchetypeChunk.GetBufferAccessorRW.html) 方法。这些方法让调用者可以显式请求缓冲区组件的特定访问模式，而不是依赖缓冲区类型句柄的隐式访问模式。这让用户可以从读写缓冲区类型句柄请求只读访问，而不会引入不必要的写入依赖。

**高级 Buffer 处理：** 在 `ArchetypeChunk` 结构体中添加了新的 [GetUntypedBufferAccessorReinterpret<T>](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ArchetypeChunk.GetUntypedBufferAccessorReinterpret.html) 方法，它与现有的 [GetDynamicComponentDataArrayReinterpret<T>](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.ArchetypeChunk.GetDynamicComponentDataArrayReinterpret.html) 方法等价，但专为缓冲区组件设计。这让你可以从运行时类型的 `DynamicComponentTypeHandle` 创建编译时类型的 `BufferAccessor<T>`，包括在类型可以安全地内存别名化（aliasable）时，创建与句柄中存储类型不同的访问器。

## 性能改进

- 优化了以下方法的性能：[SetSharedComponentManaged](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.EntityCommandBuffer.SetSharedComponentManaged.html)、[IEntitiesPlayerSettings.GetFilterSettings](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.Build.IEntitiesPlayerSettings.GetFilterSettings.html)。
- [TypeManager.Initialize](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.TypeManager.Initialize.html) 方法在大型项目（包含许多不引用 `Unity.Entities.dll` 的程序集）的 Player 构建启动时，速度大约快两倍。
- 该方法现在不再在启动时扫描所有 Player 程序集，查找继承自 `UnityEngine.Object` 的类型（例如 MonoBehaviour、ScriptableObject）。如果 Unity 因为项目中的某个类型未在 TypeManager 中注册而报错（例如，因为你需要在查询中使用它），请使用 [\[assembly: RegisterUnityEngineComponentType(typeof(YourParticularType))\]](https://docs.unity3d.com/Packages/com.unity.entities@6.6/api/Unity.Entities.RegisterUnityEngineComponentTypeAttribute.html) 显式注册它。
- 改进了 `ChunkEntityEnumerator` 构造函数的性能，但在 Mono 上使用参数 `useEnabledMask = false` 运行的情况除外——这种情况下比之前版本慢约两倍。如果你的应用使用此类参数调用该构造函数，请改用 `for` 循环。

## 文档改进

- 新增了使用 [UnityObjectRef](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/reference-unity-objects.html) API 存储 `UnityEngine.Object` 类型引用的文档。
- 扩展了 [LinkedEntityGroup](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/linked-entity-group.html) 缓冲区以及 [实体中的变换（Transforms in entities）](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/transforms-intro.html)的文档。

## 其他资源

- [升级指南](https://docs.unity3d.com/Packages/com.unity.entities@6.6/manual/upgrade-guide.html)
- [Changelog](https://docs.unity3d.com/Packages/com.unity.entities@6.6/changelog/CHANGELOG.html)
