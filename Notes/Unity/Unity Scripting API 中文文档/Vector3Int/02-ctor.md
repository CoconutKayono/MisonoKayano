> 原文：[Vector3Int.Constructor](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3Int-ctor.html)

# [Vector3Int](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3Int.html) 构造函数

## 声明

~~~csharp
public Vector3Int(int x, int y, int z);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| x | Vector3Int 的 X 分量。 |
| y | Vector3Int 的 Y 分量。 |
| z | Vector3Int 的 Z 分量。 |

## 描述

使用 x、y、z 分量初始化并返回新的 Vector3Int 实例。

## 示例

~~~csharp
// Attach this script to a GameObject.
// Attach a Tilemap component to the GameObject.
using UnityEngine;
using UnityEngine.Tilemaps;

public class Vector3IntCtorExample : MonoBehaviour
{
    Vector3Int m_Position;
    Tilemap m_Tilemap;
    Tile m_Tile;

    void Start()
    {
        m_Position = new Vector3Int(1, 5, -2);
        m_Tilemap = GetComponent<Tilemap>();
        m_Tile = ScriptableObject.CreateInstance<Tile>();
    }

    void Update()
    {
        if (!m_Tilemap.HasTile(m_Position))
            m_Tilemap.SetTile(m_Position, m_Tile);
    }
}
~~~

## 声明

~~~csharp
public Vector3Int(int x, int y);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| x | Vector3Int 的 X 分量。 |
| y | Vector3Int 的 Y 分量。 |

## 描述

使用 x 和 y 分量初始化并返回新的 Vector3Int 实例，并将 z 设置为零。

---

## 文档导航

- 上一页：[[01-back]]
- 目录：[[00-Vector3Int]]
- 下一页：[[03-down]]
