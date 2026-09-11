> 原文：[Vector3.LerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.LerpUnclamped.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).LerpUnclamped

## 声明

~~~csharp
public static Vector3 LerpUnclamped(Vector3 a, Vector3 b, float t);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | Start value. This value is returned when t = 0 . |
| b | End value. This value is returned when t = 1 . |
| t | Value used to interpolate between or beyond a and b . |

## 返回

Vector3 Interpolated value. This value always lies on a line that passes through points a and b .

## 描述

在两个向量之间线性插值，允许超出端点。

## 示例

~~~csharp
// This example creates three primitive cubes. Using linear interpolation, one cube moves along the line that passes through the others.
// Because the interpolation is not clamped to the start and end points, the moving cube passes the end cube after the interpolation frame limit is reached.    
// Attach this script to any  GameObject  in your scene. 

using UnityEngine;

public class LerpUnclampedExample :  MonoBehaviour 
{
    // Number of frames in which to completely interpolate between the positions
    int interpolationFramesCount = 300; 
    int elapsedFrames = 0;

    // Number of frames to reset the moving cube to the start position
    int maxFrameReset = 900;

     GameObject  CubeStart;
     GameObject  CubeEnd;
     GameObject  CubeMove;


    void Start()
    {
        // Create the cubes
        CubeStart =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        CubeStart.transform.position = new  Vector3 (-5,0,0);

        CubeEnd =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        CubeEnd.transform.position = new  Vector3 (5,0,0);

        CubeMove =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
        CubeMove.transform.position =  CubeStart.transform.position;
    }

    void  Update ()
    {
        float interpolationRatio = (float)elapsedFrames / interpolationFramesCount;

        // Interpolate position of the moving cube, based on the ratio of elapsed frames
        CubeMove.transform.position =  Vector3.LerpUnclamped (CubeStart.transform.position, CubeEnd.transform.position, interpolationRatio);
        
        // Reset elapsedFrames to zero after it reaches maxFrameReset
        elapsedFrames = (elapsedFrames + 1) % (maxFrameReset);  

    }
}
~~~

## 相关资源

- [Lerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Lerp.html)
- [SlerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.SlerpUnclamped.html)

---

## 文档导航

- 上一页：[[27-Lerp]]
- 目录：[[00-Vector3]]
- 下一页：[[29-Max]]




