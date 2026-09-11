> 原文：[GameObject.sceneCullingMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-sceneCullingMask.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).sceneCullingMask

## 声明

~~~csharp
public ulong sceneCullingMask;
~~~

## 描述

为 GameObject 定义的场景剔除掩码。（只读）

Unity 使用 [SceneCullingMasks](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.SceneCullingMasks.html) 确定在哪个场景中渲染 GameObject。sceneCullingMask 是存储为无符号 64 位整数 ulong 的位字段。仅当 Scene 掩码中的位（可通过 [EditorSceneManager.GetSceneCullingMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.EditorSceneManager.GetSceneCullingMask.html) 获取）与对象 sceneCullingMask 中的位匹配时，摄像机才会在某个场景中渲染该对象。

~~~csharp
using UnityEngine;
using UnityEditor.SceneManagement;

[ExecuteInEditMode]
public class ExampleClass : MonoBehaviour
{
    void Start()
    {
        // 检查 gameObject 是否在场景中可见。
        if (gameObject.sceneCullingMask ==
            EditorSceneManager.GetSceneCullingMask(gameObject.scene))
        {
            Debug.Log("Object is visible");
        }
        else
        {
            Debug.Log("Object is not visible");
        }
    }
}
~~~

相关资源：[SceneCullingMasks](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.SceneCullingMasks.html)、[Camera.overrideSceneCullingMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Camera-overrideSceneCullingMask.html)、[EditorSceneManager.SetSceneCullingMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.EditorSceneManager.SetSceneCullingMask.html)。

## 示例

~~~csharp
using UnityEngine;
using UnityEditor.SceneManagement;

[ ExecuteInEditMode ]
public class ExampleClass :  MonoBehaviour 
{
    
    void Start()
    {
        //Check if gameObject is visible in scene
        if(gameObject.sceneCullingMask ==  EditorSceneManager.GetSceneCullingMask (gameObject.scene))
        {
             Debug.Log ("Object is visible");
        }
        else
        {
             Debug.Log ("Object is not visible");
        }
    }
}
~~~

## 相关资源

- [SceneCullingMasks](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.SceneCullingMasks.html)
- [Camera.overrideSceneCullingMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Camera-overrideSceneCullingMask.html)
- [EditorSceneManager.SetSceneCullingMask](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/SceneManagement.EditorSceneManager.SetSceneCullingMask.html)


