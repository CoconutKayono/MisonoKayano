# AssetBundleRecompressOperation 类

继承关系：`object` → `YieldInstruction` → `AsyncOperation` → `AssetBundleRecompressOperation`

命名空间：`UnityEngine`

程序集：`Unity.AssetBundleModule.dll`

## 描述

将 [AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 从一种压缩方式/级别异步重压缩为另一种。

其他资源：[AssetBundle.RecompressAssetBundleAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.RecompressAssetBundleAsync.html)、[AsyncOperation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation.html)

## 属性

| 属性 | 说明 |
| --- | --- |
| [humanReadableResult](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleRecompressOperation-humanReadableResult.html) | 描述重压缩操作结果的字符串（只读）。 |
| [inputPath](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleRecompressOperation-inputPath.html) | 正在被重压缩的 AssetBundle 的路径（只读）。 |
| [outputPath](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleRecompressOperation-outputPath.html) | 重压缩后生成的 AssetBundle 的路径（只读）。 |
| [result](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleRecompressOperation-result.html) | 重压缩操作的结果。 |
| [success](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleRecompressOperation-success.html) | 重压缩操作是否已成功完成：成功为 true，否则为 false（只读）。 |

## 继承的成员（来自 AsyncOperation）

### 属性

| 属性 | 说明 |
| --- | --- |
| [allowSceneActivation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation-allowSceneActivation.html) | 允许场景在就绪后立即激活。 |
| [isDone](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation-isDone.html) | 操作是否已完成？（只读） |
| [priority](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation-priority.html) | 调整异步操作执行顺序的优先级。 |
| [progress](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation-progress.html) | 操作的进度。（只读） |

### 事件

| 事件 | 说明 |
| --- | --- |
| [completed](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation-completed.html) | 当此 AsyncOperation 操作完成时触发。 |

---

相关文档：[[00-AssetBundleModule]]、[[01-AssetBundle-中文文档]]、[[02-AssetBundleCreateRequest-中文文档]]、[[03-AssetBundleManifest-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
