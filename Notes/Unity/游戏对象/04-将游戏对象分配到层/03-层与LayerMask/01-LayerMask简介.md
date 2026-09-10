# LayerMask 简介

> 原文：[Introduction to layerMasks](https://docs.unity3d.com/6000.7/Documentation/Manual/layermask-introduction.html)

每个 GameObject 都存在于单个 Layer 中，但允许你设置 API 影响哪些 Layer 的 Unity API 并不直接使用 Layer，而是使用 `LayerMask`。

Layer 是标准整数，而 `LayerMask` 是以 bitmask 格式表示的整数：每个 `1` 表示包含对应 Layer，每个 `0` 表示排除对应 Layer。这意味着，将 Layer 传递给需要 `LayerMask` 的 API 时，脚本仍然可以编译，因为 Layer 和 `LayerMask` 使用相同的底层类型。但是，API 调用不会产生你预期的行为。

例如，如果希望对 Layer 9 上的 GameObject 执行 Raycast，却将 `9` 作为 `layerMask` 传递给 `Physics.Raycast`，Unity 实际上会对 Layer 3 和 Layer 0 上的 GameObject 执行 Raycast。这是因为 `9` 的二进制表示为 `00001001`，将其解释为 Mask 时，两个 `1` 位分别位于 Layer 3 和 Layer 0 的位置。

> **注意：** Layer 编号和 `LayerMask` 位掩码虽然都使用整数表示，但含义不同。需要单个 Layer 的编号时使用 Layer 编号，需要选择多个 Layer 的 API 参数时使用按位构造的 `LayerMask`。

---

## 文档导航

- 上一页：[[00-层与LayerMask]]
- 目录：[[../03-层与LayerMask]]
- 下一页：[[02-向LayerMask添加Layer]]
