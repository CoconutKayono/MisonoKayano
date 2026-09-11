> 原文：[GameObject.SetActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetActive.html)

# [GameObject](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.html).SetActive

## 声明

~~~csharp
public void SetActive(bool value);
~~~

## 参数

| 参数 | 中文说明 |
| --- | --- |
| value | 要设置的激活状态；true 将 GameObject 设为激活，false 将其设为未激活。 |

## 描述

根据提供的参数在本地激活或停用 GameObject。

SetActive 只设置由 GameObject.activeSelf 表示的 GameObject 本地状态。如果由于父对象未激活而 activeInHierarchy 为 false，改变 GameObject.activeSelf 不会改变 GameObject.activeInHierarchy。

停用 GameObject 会禁用每个组件，包括附加的渲染器、碰撞体、刚体和脚本。例如，Unity 不会再调用附加到已停用 GameObject 的脚本上的 MonoBehaviour.Update。停用 GameObject 也会停止附加到它的所有协程。

注意：如果调用 SetActive 改变了 GameObject.activeInHierarchy 的值，就会在所有附加的 MonoBehaviour 脚本上触发 MonoBehaviour.OnEnable 或 MonoBehaviour.OnDisable。

## 示例

~~~csharp
using UnityEngine;

public class Example :  MonoBehaviour 
{
    private  GameObject [] cubes = new  GameObject [10];
    public float timer, interval = 2f;

    void Start()
    {
         Vector3  pos = new  Vector3 (-5, 0, 0);

        for (int i = 0; i < 10; i++)
        {
            cubes[i] =  GameObject.CreatePrimitive ( PrimitiveType.Cube );
            cubes[i].transform.position = pos;
            cubes[i].name = "Cube_" + i;
            pos.x++;
        }
    }

    void  Update ()
    {
        timer +=  Time.deltaTime ;
        if (timer >= interval)
        {
            for (int i = 0; i < 10; i++)
            {
                int randomValue =  Random.Range (0, 2);
                if (randomValue == 0)
                {
                    cubes[i].SetActive(false);
                }
                else  cubes[i].SetActive(true);
            }
            timer = 0;
        }
    }
}
~~~

## 相关资源

- [GameObject.activeSelf](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject-activeSelf.html)
- [GameObject.SetGameObjectsActive](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.SetGameObjectsActive.html)


