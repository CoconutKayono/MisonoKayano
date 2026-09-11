> 原文：[Transform.Find](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.Find.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).Find

public Transform Find(string n);

### 参数

| 参数 | 描述 |
| --- | --- |
| n | 搜索字符串，可以是直接子对象的名称，也可以是用于查找后代对象的层级路径。 |

### 返回

Transform 找到的子 Transform。如果找不到名称匹配的子对象，则为 Null。

### 描述

按名称 n 查找子对象并返回它。

如果找不到名称为 n 的子对象，则返回 null。如果 n 包含“/”字符，则会像路径名一样访问 Transform 层级。注意：如果 GameObject 名称中包含“/”，Find 将无法正常工作。注意：Find 不会递归向下遍历 Transform 层级。注意：Find 可以查找非活动 GameObject 的 Transform。

### 示例

~~~csharp
using UnityEngine;
using System.Collections;

public class ExampleClass :  MonoBehaviour 
{
    public  GameObject  player;
    public  Transform  gun;
    public  Transform  ammo;

    //Invoked when a button is clicked.
    public void Example()
    {
        //Finds and assigns the child named "Gun".
        gun = player.transform.Find("Gun");

        //If the child was found.
        if (gun != null)
        {
            //Find the child named "ammo" of the gameobject "magazine" (magazine is a child of "gun").
            ammo = gun.transform.Find("magazine/ammo");
        }
        else  Debug.Log ("No child with the name 'Gun' attached to the player");
    }
}
~~~

另一个示例：

~~~csharp
// ExampleClass has a  GameObject  with three spheres attached.
// Two of these are children of the  GameObject .  The third
// transform, sphere3, is a child of sphere2.  Find() does
// not find this child.

using UnityEngine;

public class ExampleClass :  MonoBehaviour 
{
    void Start()
    {
         Transform  result;

        for (int i = 1; i < 4; i++)
        {
            string sph;

            sph = "sphere" + i.ToString();
            result = gameObject.transform.Find(sph);

            if (result)
            {
                 Debug.Log ("Found: " + sph);
            }
            else
            {
                //Find() does not find sphere3
                 Debug.Log ("Did not find: " + sph);

                //But we can access it with '/' character or by using GetChild()
                 Transform  newresult;
                newresult = gameObject.transform.Find("sphere2/sphere3");

                if (newresult)
                {
                     Debug.Log ("But now found:" + sph);
                }
            }
        }
    }
}
~~~





