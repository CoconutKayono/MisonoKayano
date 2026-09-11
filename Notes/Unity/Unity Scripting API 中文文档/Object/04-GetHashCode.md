> 原文：[Object.GetHashCode](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.GetHashCode.html)

# Object.GetHashCode

```csharp
public int GetHashCode();
```

## 返回值

`int`：对象的哈希码。

## 描述

返回对象的哈希码。哈希码对该对象保持稳定，即使修改对象字段也不会变化，因此可以安全地把对象用作 `Dictionary` 或 `HashSet` 等基于哈希的集合的键。哈希码与 `Object.Equals` 一致：两个相等的引用会返回相同哈希码。

---

## 文档导航

- 上一页：[[03-GetEntityId]]
- 目录：[[00-Object]]
- 下一页：[[05-ToString]]
