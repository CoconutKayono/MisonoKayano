> 原文：[Transform.DetachChildren](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.DetachChildren.html)

# [Transform](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Transform.html).DetachChildren

public void DetachChildren();

### 描述

解除目标对象所有子对象的父级关系。

每个直接子对象都会被移动到根层级，同时保留其内部层级。这对于在不销毁子对象的情况下销毁层级根对象很有用，并且比逐个解除每个子对象的父级关系更高效。相关资源：Transform.parent 可用于解除或更改单个 Transform 的父级。

### 示例

~~~csharp
{
     GameObject  root = new  GameObject ("Root");
    AddChildTransforms(root.transform, new[] { "Child1", "Child2", "Child3" });
    // Destroying an object destroys its children as well. To avoid this,
    // the children must first be detached. We can't safely detach children
    // while iterating through its child list, so we need to extract them into
    // a separate list as a pre-pass.
    List< Transform > children = new List< Transform >();
    for(int i=0; i<root.transform.childCount; ++i)
    {
        children.Add(root.transform.GetChild(i));
    }
    // Now we can safely deparent each child.
    foreach ( Transform  child in children)
    {
        child.SetParent(null, true);
    }
     Assert.AreEqual (0, root.transform.childCount);
    // Destroying the root no longer destroys the children
     Object.Destroy (root.gameObject);
}

{
     GameObject  root = new  GameObject ("Root");
    AddChildTransforms(root.transform, new[] { "Child1", "Child2", "Child3" });
    // This has the same effect as the above loops.
    root.transform.DetachChildren();
     Assert.AreEqual (0, root.transform.childCount);
    // Destroying the root no longer destroys the children
     Object.Destroy (root.gameObject);
}
~~~


