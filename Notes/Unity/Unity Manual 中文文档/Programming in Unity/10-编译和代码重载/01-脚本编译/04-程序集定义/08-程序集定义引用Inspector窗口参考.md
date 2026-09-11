# Assembly Definition Reference Inspector 窗口参考

> 原文：[Assembly Definition Reference Inspector window reference](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AssemblyDefinitionReferenceImporter.html)

Assembly Definition Reference 是定义对 Assembly Definition 引用的资源。在文件夹中创建 Assembly Definition Reference 资源，可以将该文件夹中的脚本包含到被引用的 Assembly Definition 中，而不是创建新程序集。除非子文件夹有自己的 Assembly Definition 或 Assembly Definition Reference 资源，否则还会包含子文件夹中的脚本。

![Inspector 中的 Assembly Definition Reference 资源](asmdef-17.png)

*图：Inspector 中的 Assembly Definition Reference 资源。*

| Property | Description |
| --- | --- |
| **Use GUID** | 控制 Unity 如何序列化对 Assembly Definition Reference 资源的引用。启用此属性后，Unity 将引用保存为资源的 GUID，而不是 Assembly Definition 名称。建议使用 GUID 而不是名称，因为这样可以更改 Assembly Definition 资源的名称，而不必更新引用它的其他 Assembly Definition 和 Reference。 |
| **Assembly Definition** | 被引用的 Assembly Definition 资源。 |

## 其他资源

[[02-创建程序集定义#create-asmref|创建 Assembly Definition Reference 资源]]

---

## 文档导航

- 上一页：[[07-程序集定义Inspector窗口参考]]
- 目录：[[00-程序集定义]]
- 下一页：[[06-程序集定义文件格式]]
