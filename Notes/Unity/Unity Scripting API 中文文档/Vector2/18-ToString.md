> 原文：[Vector2.ToString](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.ToString.html)

# [Vector2](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector2.html).ToString

## 声明

~~~csharp
public string ToString();
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| format | 格式字符串。 |
| formatProvider | 格式提供程序。 |

## 返回值

返回操作结果。

## 描述

将此向量格式化为字符串。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    void Start()
    {
         Vector2  vector = new  Vector2 (1, 2);
         Debug.Log (vector.ToString()); // output displayed as: "(1.00, 2.00)"
    }
}
~~~

---

## 声明

~~~csharp
public string ToString(string format);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| format | 格式字符串。 |
| formatProvider | 格式提供程序。 |

## 返回值

返回操作结果。

## 描述

将此向量格式化为字符串。

---

## 声明

~~~csharp
public string ToString(string format, IFormatProvider formatProvider);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| format | 格式字符串。 |
| formatProvider | 格式提供程序。 |

## 返回值

返回操作结果。

## 描述

将此向量格式化为字符串。

---

## 文档导航

- 上一页：[[17-Set]]
- 目录：[[00-Vector2]]
- 下一页：[[19-Angle]]


