# TransformHandle API 代码示例

> 原文：[TransformHandle API examples](https://docs.unity3d.com/6000.7/Documentation/Manual/transformhandle-examples.html)

本节包含用于展示 `Transform` 与 `TransformHandle` API 差异的代码示例。

## 使用 TransformHandle API

由于 `TransformHandle` 是一个 struct，因此必须先将其赋值给局部变量，然后才能修改其属性。使用 `gameObject.transformHandle` 调用直接修改属性会导致编译错误。这是因为 struct 的属性访问器返回的是 struct 的副本，而不是对它的引用。

例如，可以使用以下方式设置属性的位置：

```csharp
TransformHandle handle = transformHandle;
handle.position = handle.position + Vector3.one;
```

可以直接在属性上调用方法：

```csharp
// Methods can be called directly
transformHandle.SetPositionAndRotation(Vector3.zero, Quaternion.identity);
```

要从 `transform` 组件获取 `TransformHandle`，请使用以下代码：

```csharp
transform.GetTransformHandle()
```

## 示例 1：基本 Transform 操作

使用 `Transform` API 的示例：

```csharp
public class PlayerMovement : MonoBehaviour
{
    public Transform target;
    public Transform parentObject;
    
    void Update()
    {
        // Move position
        transform.position = transform.position + Vector3.forward * Time.deltaTime;
        
        // Look at target
        if (target != null)
            transform.LookAt(target);
        
        // Set parent
        transform.SetParent(parentObject);
        
        // Check hierarchy
        if (transform.IsChildOf(parentObject))
            Debug.Log("Is child of parent");
    }
}
```

使用 `TransformHandle` API 的示例：

```csharp
public class PlayerMovement : MonoBehaviour
{
    public Transform target; // Still use Transform for serialization
    public Transform parentObject;
    
    void Update()
    {
        // Get TransformHandle (required for struct operations)
        TransformHandle selfHandle = transformHandle;
        
        // Move position (must store in variable first)
        selfHandle.position = selfHandle.position + Vector3.forward * Time.deltaTime;
        
        // Look at target
        if (target != null)
            transformHandle.LookAt(target.transformHandle);
        
        // Set parent
        transformHandle.SetParent(parentObject.transformHandle);
        
        // Check hierarchy
        if (transformHandle.IsChildOf(parentObject.transformHandle))
            Debug.Log("Is child of parent");
    }
}
```

## 示例 2：层级导航

使用 `Transform` API 的示例：

```csharp
void ExploreHierarchy(Transform root)
{
    Debug.Log($"Root: {root.name}, Children: {root.childCount}");
    
    // Iterate through children
    foreach (Transform child in root)
    {
        Debug.Log($"Child: {child.name}");
        ExploreHierarchy(child); // Recursive
    }
    
    // Get parent
    if (root.parent != null)
        Debug.Log($"Parent: {root.parent.name}");
}
```

使用 `TransformHandle` API 的示例：

```csharp
void ExploreHierarchy(TransformHandle root)
{
    Debug.Log($"Root children count: {root.childCount}");
    
    // Iterate through direct children
    foreach (TransformHandle child in root.DirectChildren)
    {
        Debug.Log($"Child ID: {child.id}");
        ExploreHierarchy(child); // Recursive
    }
    
    // Get parent
    if (root.parent.IsValid())
        Debug.Log($"Has parent: {root.parent.id}");
}
```

## 示例 3：层级操作、批量操作和自定义迭代

使用 `TransformHandle` API 的示例：

```csharp
using UnityEngine;

// Demonstrates advanced features of the TransformHandle API, including
// state management, batch operations, and manual hierarchy iteration.
public class TransformHandleAdvancedFeatures : MonoBehaviour
{
    // Assign a prefab in the Inspector.
    public GameObject childPrefab;

    void Start()
    {
        // Each method demonstrates a different set of features.
        DemonstrateHandleStateAndManagement();
        DemonstrateBatchOperations();
        DemonstrateManualIteration();
    }

    // Covers checking handle validity, parent status, and un-parenting.
    private void DemonstrateHandleStateAndManagement()
    {
        Debug.Log("--- Part 1: Hierarchy management ---");

        if (childPrefab == null)
        {
            Debug.LogWarning("Child prefab not assigned. Skipping Part 1.");
            return;
        }

        // Create a child object to work with.
        GameObject childGo = Instantiate(childPrefab, transform);
        TransformHandle childHandle = childGo.transformHandle;

        // 1. Use HasParent() for a direct boolean check.
        Debug.Log($"Does child have a parent? {childHandle.HasParent()}");

        // 2. Un-parent the object by setting its parent to TransformHandle.None.
        Debug.Log("Un-parenting the child...");
        childHandle.parent = TransformHandle.None;
        Debug.Log($"Child's parent is now None: " +
            $"{childHandle.parent == TransformHandle.None}");

        // 3. Use IsValid() to check if a handle points to a valid object.
        Debug.Log($"Is the handle valid before destroying? {childHandle.IsValid()}");

        // Destroy the GameObject the handle was pointing to.
        Destroy(childGo);

        // NOTE: IsValid() will return false for this handle in the next frame,
        // as object destruction is delayed until the end of the current frame.
        // This check demonstrates the intended use case for preventing errors.
        if (!childHandle.IsValid())
        {
            Debug.Log("Handle is no longer valid after object was destroyed.");
        }
    }

    // Shows how to use batch operations for improved performance.
    private void DemonstrateBatchOperations()
    {
        Debug.Log("\n--- Part 2: Batch operations ---");

        TransformHandle handle = transformHandle;
        var localPoints = new Vector3[] { Vector3.up, Vector3.right, Vector3.forward };

        Debug.Log($"Local point [0] before TransformPoints: {localPoints[0]}");

        // TransformPoints modifies the array in-place, which is more efficient
        // than transforming each point individually in a loop.
        handle.TransformPoints(localPoints);

        Debug.Log($"World point [0] after TransformPoints: {localPoints[0]}");
    }

    // Demonstrates how to manually iterate through children with an enumerator.
    private void DemonstrateManualIteration()
    {
        Debug.Log("\n--- Part 3: Custom iteration ---");

        // Setup: Create some temporary children for the iteration demo.
        var child1 = new GameObject("Child_A");
        var child2 = new GameObject("Child_B");
        child1.transform.SetParent(transform);
        child2.transform.SetParent(transform);

        // GetDirectChildrenEnumerator provides fine-grained control over iteration.
        Debug.Log("Iterating with GetDirectChildrenEnumerator:");
        var enumerator = transformHandle.GetDirectChildrenEnumerator();
        while (enumerator.MoveNext())
        {
            TransformHandle currentChild = enumerator.Current;
            Debug.Log($"Found child via enumerator.");
        }

        // Clean up the temporary objects created for this demonstration.
        Destroy(child1);
        Destroy(child2);
    }
}
```

## 其他资源

- [[04-TransformHandle类参考]]
- [[03-在Burst中使用TransformHandle]]

---

## 文档导航

- 上一页：[[01-TransformHandle API简介]]
- 目录：[[00-使用非托管API执行Transform操作]]
- 下一页：[[03-在Burst中使用TransformHandle]]
