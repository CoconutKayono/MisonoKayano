> 原文：[GameObject.GetComponentIndex](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.GetComponentIndex.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).GetComponentIndex

## 声明

~~~csharp
public int GetComponentIndex(Component component);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| component | 要搜索的组件。 |

## 返回值

如果指定组件存在，则返回其索引；否则返回 -1。

## 描述

获取指定组件在附加到 GameObject 的组件数组中的索引。
