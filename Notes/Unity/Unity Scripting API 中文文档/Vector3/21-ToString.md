> 原文：[Vector3.ToString](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.ToString.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).ToString

## 声明

~~~csharp
public string ToString();
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| format | 数值格式字符串。 |
| format | 数值格式字符串。 |
| formatProvider | An object that specifies culture-specific formatting. |

## 返回

string A formatted string of the given vector.

## 描述

将此向量格式化为字符串。

## 示例

~~~csharp
using UnityEngine;

public class ExampleScript :  MonoBehaviour 
{
    void Start()
    {
        // let Unity show these as (1.00, 2.00, 3.00)
         Vector3  vector = new  Vector3 (1, 2, 3);
         Debug.Log (vector.ToString());

        // unity displays by default (1.23, 5.68, 9.01)
        vector = new  Vector3 (1.234f, 5.678f, 9.012f);
         Debug.Log (vector.ToString());

        // but we can show this using format - 3 numbers after the decimal point
        // (1.234, 5.678, 9.012)
         Debug.Log (vector.ToString("F3"));

        // now let's create some longer numbers
        vector = new  Vector3 (1.0f / 3.0f, - Mathf.PI ,  Mathf.Exp (-2.0f));

        // we get (0.333333, -3.141593, 0.135335)
         Debug.Log ("fractional part is 6: " + vector.ToString("F6"));

        // note how F8 cannot display these numbers as we want
        // (0.33333330, -3.14159300, 0.13533530)
         Debug.Log ("fractional part is 8: " + vector.ToString("F8"));
    }
}
~~~

---

## 声明

~~~csharp
public string ToString(string format);
~~~

## 描述

将此向量格式化为字符串。

---

## 声明

~~~csharp
public string ToString(string format, IFormatProvider formatProvider);
~~~

## 描述

将此向量格式化为字符串。

---

## 文档导航

- 上一页：[[20-Set]]
- 目录：[[00-Vector3]]
- 下一页：[[22-Angle]]

