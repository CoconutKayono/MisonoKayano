# AssetBundleCreateRequest 类

继承关系：`object` → `YieldInstruction` → `AsyncOperation` → `AssetBundleCreateRequest`

命名空间：`UnityEngine`

程序集：`Unity.AssetBundleModule.dll`

## 描述

[AssetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 的异步加载请求。

其他资源：[AssetBundle.LoadFromFileAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.LoadFromFileAsync.html)、[AssetBundle.LoadFromMemoryAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.LoadFromMemoryAsync.html)、[AssetBundle.LoadFromStreamAsync](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.LoadFromStreamAsync.html)、[AsyncOperation](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AsyncOperation.html)

## 属性

| 属性 | 说明 |
| --- | --- |
| [assetBundle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundleCreateRequest-assetBundle.html) | 正在加载的 Asset 对象（只读）。 |

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

相关文档：[[00-AssetBundleModule]]、[[01-AssetBundle-中文文档]]

这个页面是否对你有帮助？请为其评分：

在此页面报告问题
