> 原文：[Vector4.ToString](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.ToString.html)

# [Vector4](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector4.html).ToString

## 声明

~~~csharp
public string ToString();
~~~

## 声明

~~~csharp
public string ToString(string format);
~~~

## 声明

~~~csharp
public string ToString(string format, IFormatProvider formatProvider);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| format | 数字格式字符串。 |
| formatProvider | 指定区域性格式的对象。 |

## 返回

`string`：此向量的格式化字符串。默认显示两位数字（`format="F2"`）。

## 描述

将此向量格式化为字符串。默认显示两位数字（`format="F2"`）。更多信息请参阅 Microsoft 关于[标准数字格式字符串](https://learn.microsoft.com/dotnet/standard/base-types/standard-numeric-format-strings)的文档。

## 示例

~~~csharp
using UnityEngine;

public class Example : MonoBehaviour
{
    void Start()
    {
        Vector4 vector = new Vector4(1, 2, 3, 4);
        Debug.Log(vector.ToString()); // output displayed as: "(1.00, 2.00, 3.00, 4.00)"
    }
}
~~~

---

## 文档导航

- 上一页：[[15-Set]]
- 目录：[[00-Vector4]]
- 下一页：[[17-Distance]]

