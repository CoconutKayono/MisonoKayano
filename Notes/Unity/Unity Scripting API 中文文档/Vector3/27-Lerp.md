> 原文：[Vector3.Lerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Lerp.html)

# [Vector3](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.html).Lerp

## 声明

~~~csharp
public static Vector3 Lerp(Vector3 a, Vector3 b, float t);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| a | Start value. This value is returned when t = 0 . |
| b | End value. This value is returned when t = 1 . |
| t | Value used to interpolate between a and b . Values greater than one are clamped to 1 . Values less than zero are clamped to 0 . |

## 返回

Vector3 Interpolated value. This value always lies on a line between points a and b .

## 描述

在两个点之间线性插值。

## 示例

~~~csharp
// This example creates three primitive cubes. Using linear interpolation, one cube moves along the line between the others.
// Because the interpolation is clamped to the start and end points, the moving cube never passes the end cube, and remains at the end position after the interpolation frame limit is reached.    
// Attach this script to any  GameObject  in your scene. 

using UnityEngine;

public class LerpExample :  MonoBehaviour 
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
        CubeMove.transform.position =  Vector3.Lerp (CubeStart.transform.position, CubeEnd.transform.position, interpolationRatio);
        
        // Reset elapsedFrames to zero after it reaches maxFrameReset
        elapsedFrames = (elapsedFrames + 1) % (maxFrameReset);  

    }
}
~~~

~~~csharp
// A longer example of  Vector3.Lerp  usage.
// Drop this script under an object in your scene, and specify 2 other objects in the "startMarker"/"endMarker" variables in the script inspector window.
// At play time, the script will move the object along a path between the position of those two markers.

using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    // Transforms to act as start and end markers for the journey.
    public  Transform  startMarker;
    public  Transform  endMarker;

    // Movement speed in units per second.
    public float speed = 1.0F;

    //  Time  when the movement started.
    private float startTime;

    // Total distance between the markers.
    private float journeyLength;

    void Start()
    {
        // Keep a note of the time the movement started.
        startTime =  Time.time ;

        // Calculate the journey length.
        journeyLength =  Vector3.Distance (startMarker.position, endMarker.position);
    }

    // Move to the target end position.
    void  Update ()
    {
        // Distance moved equals elapsed time times speed..
        float distCovered = ( Time.time  - startTime) * speed;

        // Fraction of journey completed equals current distance divided by total distance.
        float fractionOfJourney = distCovered / journeyLength;

        // Set our position as a fraction of the distance between the markers.
        transform.position =  Vector3.Lerp (startMarker.position, endMarker.position, fractionOfJourney);
    }
}
~~~

## 相关资源

- [Slerp](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.Slerp.html)
- [LerpUnclamped](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Vector3.LerpUnclamped.html)

---

## 文档导航

- 上一页：[[26-Dot]]
- 目录：[[00-Vector3]]
- 下一页：[[28-LerpUnclamped]]




