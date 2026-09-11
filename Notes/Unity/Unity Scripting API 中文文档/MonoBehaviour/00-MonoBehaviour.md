> 原文：[MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html)

# MonoBehaviour

## 描述

MonoBehaviour 是许多 Unity 脚本派生的基类。MonoBehaviour 提供生命周期函数，使 Unity 开发更加容易。

MonoBehaviour 始终作为 GameObject 的 Component 存在，并且可以通过 [GameObject.AddComponent](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/GameObject.AddComponent.html) 实例化。MonoBehaviour 可以通过 [Object.Destroy](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.Destroy.html) 或 [Object.DestroyImmediate](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Object.DestroyImmediate.html) 删除。当父 GameObject 被销毁时，所有组件（包括 MonoBehaviour）都会自动删除。底层组件销毁后，MonoBehaviour 的 C# 对象会继续留在内存中，直到垃圾回收；处于此状态的 MonoBehaviour 的行为类似于 null，例如 `obj == null` 检查会返回 true。不过，此类不支持 null 条件运算符（`?.`）和 null 合并运算符（`??`）。

MonoBehaviour 序列化时，C# 字段的值会按照 Unity 的序列化规则包含在内。序列化数据还包括 MonoScript 引用等内部属性，该引用用于跟踪对象的实现类。代码示例请参阅各个 MonoBehaviour 方法。

注意：在 Editor 中，如果通过 Inspector 中的复选框停用 MonoBehaviour 组件，它将停止接收其事件函数的调用。

其他资源：[在 Manual 中停用 GameObject](https://docs.unity3d.com/6000.7/Documentation/Manual/DeactivatingGameObjects.html)。

## 成员

| 本地链接 | API名 | 中文说明 |
| --- | --- | --- |
| [[01-destroyCancellationToken]] | destroyCancellationToken | 获取在销毁 MonoBehaviour 时取消的 CancellationToken。 |
| [[02-didAwake]] | didAwake | 指示 Awake 是否已在此 MonoBehaviour 上调用。 |
| [[03-didStart]] | didStart | 指示 Start 是否已在此 MonoBehaviour 上调用。 |
| [[04-print]] | print | 将消息输出到 Unity 控制台。 |
| [[05-runInEditMode]] | runInEditMode | 允许 MonoBehaviour 在编辑器中运行。 |
| [[06-useGUILayout]] | useGUILayout | 指定是否为此 MonoBehaviour 添加额外的 GUI 布局阶段。 |
| [[07-Awake]] | Awake | 在脚本实例加载时调用。 |
| [[08-CancelInvoke]] | CancelInvoke | 取消此 MonoBehaviour 上的所有 Invoke 调用，或取消指定方法的 Invoke。 |
| [[09-FixedUpdate]] | FixedUpdate | 每个固定帧率帧调用一次。 |
| [[10-Invoke]] | Invoke | 在指定延迟后调用方法。 |
| [[11-InvokeRepeating]] | InvokeRepeating | 在指定延迟后调用方法，并按指定间隔重复调用。 |
| [[12-IsInvoking]] | IsInvoking | 检查指定方法是否正在等待 Invoke。 |
| [[13-LateUpdate]] | LateUpdate | 如果 Behaviour 已启用，则每帧调用一次。 |
| [[14-OnAnimatorIK]] | OnAnimatorIK | 用于设置动画 IK（反向运动学）的回调。 |
| [[15-OnAnimatorMove]] | OnAnimatorMove | 用于处理动画移动、修改根运动的回调。 |
| [[16-OnApplicationFocus]] | OnApplicationFocus | 当应用获得或失去焦点时发送给所有 GameObject。 |
| [[17-OnApplicationPause]] | OnApplicationPause | 播放中的应用因失去或重新获得焦点而暂停或恢复时发送给所有 GameObject。 |
| [[18-OnApplicationQuit]] | OnApplicationQuit | 应用退出前发送给所有活动的 GameObject。 |
| [[19-OnAudioFilterRead]] | OnAudioFilterRead | 如果实现 OnAudioFilterRead，Unity 会在音频 DSP 链中插入自定义滤波器。 |
| [[20-OnBecameInvisible]] | OnBecameInvisible | 当 Renderer 不再被任何摄像机看到时调用。 |
| [[21-OnBecameVisible]] | OnBecameVisible | 当 Renderer 被摄像机看到时调用。 |
| [[22-OnChildRectTransformDimensionsChange]] | OnChildRectTransformDimensionsChange | 子 RectTransform 的尺寸发生变化时调用。 |
| [[23-OnCollisionEnter]] | OnCollisionEnter | 此 Collider/Rigidbody 开始接触另一个 Rigidbody/Collider 时调用。 |
| [[24-OnCollisionEnter2D]] | OnCollisionEnter2D | 传入的 Collider 与此对象的 Collider 接触时发送（仅限 2D 物理）。 |
| [[25-OnCollisionExit]] | OnCollisionExit | 此 Collider/Rigidbody 停止接触另一个 Rigidbody/Collider 时调用。 |
| [[26-OnCollisionExit2D]] | OnCollisionExit2D | 另一个对象上的 Collider 停止接触此对象的 Collider 时发送（仅限 2D 物理）。 |
| [[27-OnCollisionStay]] | OnCollisionStay | 每帧为接触另一个 Collider 或 Rigidbody 的每个 Collider 或 Rigidbody 调用。 |
| [[28-OnCollisionStay2D]] | OnCollisionStay2D | 另一个对象上的 Collider 接触此对象的 Collider 的每一帧发送（仅限 2D 物理）。 |
| [[29-OnControllerColliderHit]] | OnControllerColliderHit | CharacterController 在移动过程中碰撞 Collider 时调用。 |
| [[30-OnDestroy]] | OnDestroy | 当 MonoBehaviour 将被销毁时调用。 |
| [[31-OnDisable]] | OnDisable | Behaviour 被禁用时调用。 |
| [[32-OnDrawGizmos]] | OnDrawGizmos | 用于绘制可视化 Gizmos 的回调。 |
| [[33-OnDrawGizmosSelected]] | OnDrawGizmosSelected | 选中 GameObject 时用于绘制 Gizmos 的回调。 |
| [[34-OnEnable]] | OnEnable | 对象启用并处于活动状态时调用。 |
| [[35-OnGUI]] | OnGUI | 处理 GUI 事件。 |
| [[36-OnJointBreak]] | OnJointBreak | 关节断裂时调用。 |
| [[37-OnJointBreak2D]] | OnJointBreak2D | 2D 关节断裂时调用。 |
| [[38-OnMouseDown]] | OnMouseDown | 用户在 Collider 上按下鼠标按钮时调用。 |
| [[39-OnMouseDrag]] | OnMouseDrag | 用户在 Collider 上按住鼠标按钮并拖动时调用。 |
| [[40-OnMouseEnter]] | OnMouseEnter | 鼠标进入 Collider 时调用。 |
| [[41-OnMouseExit]] | OnMouseExit | 鼠标离开 Collider 时调用。 |
| [[42-OnMouseOver]] | OnMouseOver | 鼠标停留在 Collider 上时调用。 |
| [[43-OnMouseUp]] | OnMouseUp | 用户在 Collider 上释放鼠标按钮时调用。 |
| [[44-OnMouseUpAsButton]] | OnMouseUpAsButton | 用户在同一个 Collider 上按下并释放鼠标按钮时调用。 |
| [[45-OnParticleCollision]] | OnParticleCollision | 粒子系统中的粒子碰撞 Collider 时调用。 |
| [[46-OnParticleSystemStopped]] | OnParticleSystemStopped | 粒子系统停止播放时调用。 |
| [[47-OnParticleTrigger]] | OnParticleTrigger | 粒子系统触发器事件发生时调用。 |
| [[48-OnParticleUpdateJobScheduled]] | OnParticleUpdateJobScheduled | 粒子系统安排粒子更新作业时调用。 |
| [[49-OnPostRender]] | OnPostRender | 摄像机完成场景渲染后调用。 |
| [[50-OnPreCull]] | OnPreCull | 摄像机剔除场景前调用。 |
| [[51-OnPreRender]] | OnPreRender | 摄像机开始渲染场景前调用。 |
| [[52-OnRenderImage]] | OnRenderImage | 对最终图像进行后处理时调用。 |
| [[53-OnRenderObject]] | OnRenderObject | 在渲染对象时调用。 |
| [[54-OnTransformChildrenChanged]] | OnTransformChildrenChanged | 此 Transform 的子项发生变化时调用。 |
| [[55-OnTransformParentChanged]] | OnTransformParentChanged | 此 Transform 的父项发生变化时调用。 |
| [[56-OnTriggerEnter]] | OnTriggerEnter | 另一个 Collider 进入此 Collider 的触发器时调用。 |
| [[57-OnTriggerEnter2D]] | OnTriggerEnter2D | 另一个 Collider2D 进入此 Collider2D 的触发器时调用。 |
| [[58-OnTriggerExit]] | OnTriggerExit | 另一个 Collider 离开此 Collider 的触发器时调用。 |
| [[59-OnTriggerExit2D]] | OnTriggerExit2D | 另一个 Collider2D 离开此 Collider2D 的触发器时调用。 |
| [[60-OnTriggerStay]] | OnTriggerStay | 另一个 Collider 持续停留在此 Collider 的触发器中时调用。 |
| [[61-OnTriggerStay2D]] | OnTriggerStay2D | 另一个 Collider2D 持续停留在此 Collider2D 的触发器中时调用。 |
| [[62-OnValidate]] | OnValidate | 脚本加载或 Inspector 中的值发生变化时调用，用于验证数据。 |
| [[63-OnWillRenderObject]] | OnWillRenderObject | 对象将由摄像机渲染时调用。 |
| [[64-Reset]] | Reset | 在脚本首次附加到 GameObject 或重置时调用。 |
| [[65-Start]] | Start | 在首次帧更新之前调用。 |
| [[66-StartCoroutine]] | StartCoroutine | 启动协程。 |
| [[67-StopAllCoroutines]] | StopAllCoroutines | 停止此 MonoBehaviour 启动的所有协程。 |
| [[68-StopCoroutine]] | StopCoroutine | 停止指定协程。 |
| [[69-Update]] | Update | 如果 Behaviour 已启用，则每帧调用一次。 |

## 相关资源

- [Deactivating GameObjects](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/../Manual/DeactivatingGameObjects.html)

---

## 文档导航

- 上一页：无
- 目录：[[00-MonoBehaviour]]
- 下一页：[[01-destroyCancellationToken]]



