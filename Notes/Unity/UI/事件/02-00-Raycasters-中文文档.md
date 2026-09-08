# Raycasters（射线投射器）

射线投射器（Raycaster）是一种组件，用于确定特定屏幕空间位置下有哪些对象，例如鼠标点击或触摸的位置。它的工作方式是：从屏幕向场景中投射一条射线，并识别与该射线相交的对象。射线投射器对于检测用户与 UI 元素、2D 对象或 3D 对象的交互至关重要。

不同类型的对象需要使用不同类型的射线投射器：

- [Graphic Raycaster](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-GraphicRaycaster.html)：检测 Canvas 上的 UI 元素。
- [Physics 2D Raycaster](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Physics2DRaycaster.html)：检测 2D 物理元素。
- [Physics Raycaster](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-PhysicsRaycaster.html)：检测 3D 物理元素。

Event System 使用射线投射器来确定输入事件的发送位置。当场景中存在已启用（enabled）的射线投射器时，Event System 会使用它来确定在给定的屏幕空间位置处，哪个对象离屏幕最近。如果同时激活了多个射线投射器，系统会对所有射线投射器执行投射，并按距离对结果排序。
