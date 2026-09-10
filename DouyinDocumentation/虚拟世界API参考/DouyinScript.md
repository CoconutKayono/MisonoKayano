# 描述
DouyinScript 是抖音开发的用户生成内容（UGC）组件。它实现了类似 Unity 的 MonoBehaviour 组件的功能，允许您创建包含逻辑代码的预制件。
# 公开属性
| [douyinObject](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0o9fmrru) | 逻辑对象，面板不可见 |
| --- | --- |
| [douyinActor](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=faiu71jn) | 当 DouyinScript 作为角色脚本挂载到角色 GameObject 上时，该属性返回对应的 DouyinScript |
# 公开方法
| [SendMessageToOwner](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=aahe4ifa) | 发送网络事件给当前脚本对应的主权人 |
| --- | --- |
| [SendMessageToAll](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=irjzzgik) | 发送网络事件给所有人，包括自己 |
| [SendMessageToTarget](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vugq9ty9) | 发送网络事件给某人 |
| [SendMessageToOthers](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=jxgh9s9u) | 发送网络事件给房间内其他玩家，不包括自己 |
| [OwnerCall](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=y31jtrrg) | 非主权方调用主权方的函数 |
| [TargetCall](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=xernotd7) | 调用任意人的函数 |
| [RequestOwnership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=m0zecpga) | 请求主权 |
| [SetOwnership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ff90w68j) | 把所有权转移给指定的 Actor |
| [HasOwnership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=pgzk6tms) | 是否有主权 |
| [SetOwner](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=c6gki6bo) | 设置一个对象的同步 owner，只有 owner 才能执行成功 |
| [IsOwner](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=idfmrew3) | 判断对象是否为 Owner |
| [GetOwner](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=65m23jlf) | 获取一个对象的 Owner |
| [RequestControllership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=si3krz3d) | 申请控制权 |
| [ReleaseControllership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=zbleia96) | 释放控制权 |
| [SetControllership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=adtq5riq) | 把控制权转移给指定的 Actor |
| [HasControllership](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=8rye7zci) | 是否有控制权 |
| [IsController](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=646jwgvg) | 判断是否为控制者 |
| [SetController](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vm9wfpel) | 设置物体的控制者 |
| [GetController](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=kkewf2zw) | 获取当前物体的控制者 |
| [GetDouyinScript](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=seawu27s) | 获得同物体上的 DouyinScript，同名返回第一个 |
| [GetDouyinScripts](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qkbrmo2u) | 获得同物体上的 DouyinScript 数组 |
| [EnableInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hlfisjn1) | 设置为可交互，包括 3D 交互和 2D 交互 |
| [DisableInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5xrtc5aq) | 禁止交互 |
| [IsSpawned](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ujkzd8q4) | 判断某一个 DouyinScript 里面的网络对象有没有完成 spawn |
| [Respawn](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=zt2qnp75) | 重生   DouyinScript  对象，根据场景初始状态，设置对象的位置和旋转 |
| [AddInteractorButton](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=nlwpau4n) | 新增C区按钮 |
| [RemoveInteractorButton](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qttifwbx) | 移除指定的C区按钮 |
| [RemoveInteractorButtonAt](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=xkw7tsyx) | 移除指定index的C区按钮 |
| [RemoveAllInteractorButtons](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=heurt0wy) | 移除该脚本对象内添加的所有的C区按钮 |
| [SetAnimationEvent](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0797s1vh) | 设置一个动作的Animation Event回调，当播放此动作时会触发回调函数 |
# 消息
| [Awake](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4zrfyo3d) | 当脚本实例被加载时，会调用  Awake |
| --- | --- |
| [Start](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=2sjj38rn) | 当在第一次调用任何 Update 方法之前启用脚本时，会在框架上调用 Start。 |
| [Update](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ucdmgkgx) | 如果启用了 MonoBehaviour，则每帧都会调用更新 |
| [FixedUpdate](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=bmz3et7s) | 用于物理计算的帧速率独立的   MonoBehavior.FixedUpdate  消息 |
| [LateUpdate](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9aws7zd6) | 如果启用了 Behaviour，则每帧都会调用 LateUpdate |
| [OnDisable](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=p77tlbl3) | 当行为被禁用时，将调用此函数 |
| [OnEnable](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=tkl5wpui) | 当对象变为启用和活动状态时，将调用此函数 |
| [OnCollisionEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3nbib8mg) | 当此碰撞器/刚体开始接触另一个刚体/碰撞器时，将调用 OnCollisionEnter |
| [OnCollisionExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ttf8eu2m) | 当此碰撞器/刚体停止接触另一个刚体/碰撞器时，将调用 OnCollisionExit |
| [OnTriggerEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=h0aiasm7) | 当一个 GameObject 与另一个 GameObject 碰撞时，Unity 会调用 OnTriggerEnter |
| [OnTriggerExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=j4ht1u7r) | 当 Collider 停止接触触发器时，会调用 OnTriggerExit |
| [OnNetSpawned](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=tzydi4x1) | 对象的网络属性初始化之后 |
| [OnOwnershipRequest](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=isb7h6vh) | 请求主权的事件 |
| [OnOwnershipTransferred](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hmuqupj3) | 当主权转移时 |
| [OnControllershipTransferred](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=jeym283w) | 当控制权转移时 |
| [OnNetDestroy](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=8b9w6fs8) | 网络对象销毁前触发 |
| [OnVariablesSynced](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=m9meqh48) | 同步变量需要更新时触发 |
| [OnUIPointerDown](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3ljmzlkc) | 当指定类型的按钮被按下时触发 |
| [OnUIPointerUp](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=l5o1p15i) | 当指定类型的按钮被抬起时触发 |
| [OnUIPointerClick](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3v6eyeva) | 当指定类型的按钮完成一次点击时触发 |
| [OnUILong](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rahusvtf)[Press](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rahusvtf) | 当指定类型的按钮被长按时触发 |
| [OnUIDrag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rh9np5q2) | 当指定类型的按钮被拖拽时触发 |
| [OnFocus](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rkthadki) | 获得焦点对象，在交互队列的前三个对象即为焦点对象 |
| [OnLostFocus](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ddidri7e) | 丢失焦点对象 |
| [On3DTouchBegin](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fi8qgglf) | 3D 触摸开始 |
| [On3DTouchDrag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hncpfebz) | 3D 触摸拖拽 |
| [On3DTouchEnd](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=kmf37d91) | 3D 触摸结束 |
| [On3DClick](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=m7khu2j6) | 3D 触摸点击 |
| [OnInteract](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=huh8o26j) | 当有玩家与之交互时触发，物体上需要挂上基础交互组件，交互规则符合组件配置内容 |
| [OnDrop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=gdm353po) | 当被玩家丢弃时触发，调用 API 时触发 |
| [OnTheft](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=r3e8wwcu) | 当被玩家抢夺时触发，调用  API 时触发 |
| [OnPickUp](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=f02clll3) | 当被玩家捡起时触发，调用 API    时触发 |
| [OnRespawn](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=x07fohd6) | 物体重生时，目前是低于世界配置重生高度时重生 |
| [OnSeatEntered](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ta91mikg) | 当被玩家坐下时，调用 API 时触发 |
| [OnSeatExited](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=v15cv54qv) | 当被玩家从座位上站起离开时，调用 API  时触发 |
| [OnActorTriggerEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=17w2a3ql) | 当 Actor  的胶囊进入触发碰撞器时触发 |
| [OnActorTriggerExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=slnd13pv) | 当 Actor 的胶囊离开触发碰撞器时触发 |
| [OnActorCollisionEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ywr01ahn) | 当 Actor 的胶囊进入碰撞器时触发 |
| [OnActorCollisionExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0kcgldxq) | 当 Actor 的胶囊离开碰撞器时触发 |
| [OnPlayerJoined](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hdyk1nw1) | 当有玩家加入房间时 |
| [OnPlayerRejoined](OnPlayerRejoined) | 当有玩家断线重连时触发 |
| [OnPlayerLeft](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ew7h5waz) | 当有玩家离开房间时 |
| [OnPlayerTriggerEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=bv23oebl) | 当玩家的胶囊进入触发碰撞器时触发 |
| [OnPlayerTriggerExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=erxr8cl1) | 当玩家的胶囊立刻触发碰撞器时触发 |
| [OnActorSpawned](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=13e1jmon) | Actor 出生 Spawn 的事件 |
| [OnActorDespawned](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=lp9btbzo) | Actor 销毁 Despawn 的事件 |
| [OnActorRespawn](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0u198v8g) | Actor 重生 |
| [OnMouseDown](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ovvw2doc) | 当用户在 Collider 上按下鼠标按钮时，将调用 OnMouseDown |
| [OnMouseDrag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=76vkhwsu) | 当用户点击 Collider 并仍然按住鼠标时，将调用 OnMouseDrag |
| [OnMouseExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=s7eczjz3) | 当鼠标不再位于 Collider 上方时调用 |
| [OnMouseEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4x6fka8b) | 当鼠标进入碰撞器时调用 |
| [OnMouseOver](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5fq6y07g) | 当鼠标位于碰撞器上方时，每一帧都会调用 |
| [OnMouseUp](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=kicj7b0o) | 当用户释放鼠标按钮时，会调用 OnMouseUp |
| [OnMouseUpAsButton](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fuyxnutr) | 仅当鼠标在按下时所在的 Collider 上释放时，才会调用 OnMouseUpAsButton |
| [OnPointerClick](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=w8lwl90e) | 如果您希望接收 OnPointerClick 回调，则需要实现该接口 |
| [OnPointerDown](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=y19hstwk) | 如果您希望接收 OnPointerDown 回调，则需要实现该接口 |
| [OnPointerEnter](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=34qqyawl) | 如果您希望接收 OnPointerEnter 回调，则需要实现该接口 |
| [OnPointerExit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vtc9kpib) | 如果您希望接收 OnPointerExit 回调，则需要实现该接口 |
| [OnPointerUp](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rnpqyut4) | 如果您希望接收 OnPointerUp 回调，则需要实现该接口 |
| [OnBeginDrag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1k78jj7x) | 如果您希望接收 OnBeginDrag 回调，则需要实现该接口 |
| [OnCancel](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=sseambc3) | 如果您希望接收 OnCancel 回调，则需要实现该接口 |
| [OnDrag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hj0zvp38) | 如果您希望接收 OnDrag 回调，则需要实现该接口 |
| [OnUnityDrop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=kp1r2zx1) | 如果您希望接收 OnUnityDrop 回调，则需要实现该接口 |
| [OnEndDrag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=964lr3tg) | 如果您希望接收 OnEndDrag 回调，则需要实现该接口 |

