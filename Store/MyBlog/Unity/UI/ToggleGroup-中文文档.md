# Toggle Group（开关组）

**Toggle Group** 不是一个可见的 UI 控件，而是一种修改一组 [Toggle](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/script-Toggle.html) 行为的方式。属于同一组的 Toggle 会受到约束：同一时间只能有一个处于开启状态——按下其中一个将其开启时，会自动关闭其他 Toggle。

*（图：一个 Toggle Group 示例）*

## 属性

| 属性                         | 功能                                                                                                        |
| -------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Allow Switch Off（允许关闭）** | 是否允许所有 Toggle 同时处于关闭状态？启用后，再次按下当前已开启的 Toggle 会将其关闭，使所有 Toggle 都变为关闭；禁用后，按下已开启的 Toggle 不会改变其状态。 |

## 说明

Toggle Group 的设置方法是：将 Toggle Group 对象拖到组中每个 Toggle 的 *Group* 属性上。

凡是需要从互斥选项中进行选择的场景，Toggle Group 都能派上用场。常见示例包括选择玩家角色类型、速度档位（慢、中、快等）、预设颜色和星期几。场景中可以有多个 Toggle Group 对象，因此如有必要，你可以创建多个独立的组。

与其他 UI 元素不同，带有 Toggle Group 组件的对象不需要是 [Canvas](https://docs.unity3d.com/Packages/com.unity.ugui@2.6/manual/class-Canvas.html) 对象的子级，但 Toggle 本身仍然需要。

请注意：如果在场景加载时或组被实例化时，组内已有多个 Toggle 处于开启状态，Toggle Group 不会立即强制收敛为只开一个。只有当新的 Toggle 被开启时，其他 Toggle 才会被关闭。这意味着你需要自行确保从一开始就只有一个 Toggle 处于开启状态。

---

相关文档：[[Toggle-中文文档]]

这个页面是否对你有帮助？请为其评分：
