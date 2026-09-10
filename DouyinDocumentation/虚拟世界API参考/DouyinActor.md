在阅读此章节前，强烈建议参阅[玩家与合养精灵](unknown)章节，以了解更多关于玩家（Player）和合养精灵（Actor）的背景信息。
# 描述
控制对象类，目前对应着在世界内的每个精灵对象，可通过 isPet 属性来判断是否是精灵。

* 可以获得显示相关的一系列属性，包括显示名称、位置、移动相关信息、形象相关信息；
* 包含操控对象的一些函数，比如设置速度、改变动作等；
* 可以使用 Tag 相关 API 给对象赋予一些数据，从而进行对象管理。 （Tag相关API当前版本无法使用，请期待该功能上线）

# 公开事件
| [onActorLoaded](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cs75db1k) | 切换 Actor 形象时回调 |
| --- | --- |
| [onFallingGround](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=i25yt848) | Actor 落地的事件 |
| [onJump](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=q1965vus) | Actor 起跳的事件 |
| [onFlyStart](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=kklapio3) | Actor 开始飞行的事件 |
| [onFlyStop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=s2gpm5be) | Actor 结束飞行的事件 |
| [onEmotionPlay](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fanzxd58) | Actor使用表情事件  |
| [onActionPlay](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0rolu5i4) | Actor使用动作事件 |
| [onDuoInteractionStart](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=xz7wj6hk) | Actor开始播放双人动作事件 |
| [onDuoInteractionEnd](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=nnvt6hqp) | Actor结束播放双人动作事件 |
| [onDuoInteractionWaiting](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=85j0mr0c) | Actor开始等待播放双人动作事件 |
| [onHoldHandStart](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=674uhhiy) | Actor进入牵手状态事件 |
| [onHoldHandStop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qu4xfaai) | Actor结束牵手状态事件 |
| [onPickup](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rge3cy42) | Actor捡起物体的事件 |
| [onDrop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=yaoegdu4) | Actor丢弃物体的事件 |
| [onSitDown](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cpdx08f7) | Actor坐下的事件 |
| [onStandUp](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=e9kivlog) | Actor站起的事件 |
| [onSwimStart](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0d1q1kt3) | Actor开始游泳的事件 |
| [onSwimStop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=v1enxult) | Actor停止游泳的事件 |
# 公开属性
| [velocity](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=49l5tmtz) | 移动方向和速度 |
| --- | --- |
| [gameObject](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ycv6iitl) | 获取关联 GameObject 实例 |
| [position](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=j07i11gp) | 位置 |
| [rotation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=mftqeeow) | 朝向 |
| [scale](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=yq3nonru) | 获取/设置 Actor 的缩放，角色的大小限制（0，2）之间 |
| [actorID](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3bfhnwa7) | Actor 实例 ID，用来判断是否是同一个玩家（重复进房间会变化） |
| [displayName](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=c4hns27o) | Actor 的名称 |
| [isPet](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=eb82p310) | 是否为精灵 |
| [douyinPet](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qbpyritm) | 当 isPet 为 true 的时候，返回当前 Actor 关联的 DouyinPet；否则返回 null |
| [isLocal](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=vyqs1452) | 返回这个 Actor 是否是 Local 玩家 |
| [flySpeed](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9drnbvxk) | 飞行水平速度 |
| [flyVerticalSpeed](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=nci8xepz) | 飞行垂直速度 |
| [flyMaxHeight](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=o1zkrdpj) | 飞行最大高度 |
| [flyMinHeight](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=xa7filgb) | 飞行最小高度 |
| [speed](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=zjf6teki) | 移动速度 |
| [gravityScale](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7sngght0) | 设置重力缩放系数 |
| [minSlopeAngleLimit](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=93svd90q) | 当前 Actor 在斜坡上最小能站立的角度 |
| [allowPushByOtherActor](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=t63tgjcc) | 当前 Actor 是否能被其他 Actor 推动 |
| [allowAccessUserPanel](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=hqn5xh7i) | 开启/禁用用户3D点击，访问用户的信息面板，默认开启 |
| [jumpHeight](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=406pzvd4) | 获取或设置当前Actor的跳跃高度 |
| [disableActorCollider](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=qcpxoeoe) | 用于禁用精灵（Actor）之间的碰撞 |
# 公开方法
| [GetBonePosition](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=julpwmpn) | 获取 Actor 的人骨位置信息 |
| --- | --- |
| [GetBoneRotation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=673zzwll) | 获取 Actor 的人骨角度信息 |
| [GetBoneTransform](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rclrmecl) | 获取 Actor 的人骨下的 Transform 对象 |
| [SetOverrideAnimationController](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=39c8qy9n) | 设置重载的动画状态机 |
| [SetOverrideAnimation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3gl0qwvf) | 设置重载动画，重载为 nil，就会还原，支持使用 Animation Event，可传回调函数 |
| [PlayAnimation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7413u189) | 播放一个动作，支持使用 Animation Event，可传回调函数 |
| [StopAnimation](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ikxejg4j) | 停止播放动作 |
| [ShowNameplate](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cz85elvo) | 显示/隐藏 Actor 名字片 |
| [GetNameplate](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=jdppomk9) | 获取名字片对象 |
| [Interact](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=yvmc4xy3) | 交互，该方法最对本地玩家有效 |
| [GetPickupInHand](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=avz7h14d) | 返回 Actor 特定手的 Pickup 物件，这个函数仅针对 local actor 生效，没有 pickup 时返回 null |
| [IsPickup](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rax5ci8t) | 手中是否有物体 |
| [Pickup](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=254e6j2i) | 拾取指定物体，该方法只对本地玩家有效 |
| [Drop](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ujb7efpi) | 丢弃指定物体，该方法只对本地玩家有效 |
| [PlayEmoji](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=59jv8cnf) | 播放表情 |
| [Respawn](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=i7qqgjjo) | 角色重生 |
| [Teleport](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0qhvx4lj)（重载方法） | 传送 |
| [SetActorTag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rjjzjfbt) | 给 Actor 增加标签，无需权限，任何人都可以添加 |
| [GetActorTag](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0rsjjdby) | 获取 Actor 标签 |
| [ClearActorTags](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=duw394oq) | 清除指定 tag，如果参数为空则清除所有 Tags，无需权限，任何人都可清除 |
| [GetState](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5ztbs02k) | 获取 Actor 状态 |
| [ChangeState](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=ll3bkx63) | 切换到某个状态 |
| [GetStateEnabled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rrjub021) | 获取 Actor 状态是否生效 |
| [SetStateEnabled](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=bwxykkmb) | 设置 Actor 状态是否生效 |
| [Jump](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9kps1gi9) | 跳跃 |
| [IsGrounded](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cozz86cy) | 判断 Actor 是否在地面的参数 |
| [CanMove](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=b61tym57) | 判断当前 Actor 是否能移动 |
| [StopMove](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0jc2q401) | 停止移动，相当于取消上个 Api 的持续移动效果 |
| [MoveContinuously](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3v7k9lgc) | 向某个方向移动，参数是移动速度的倍速（相当于一直朝某个方向推动摇杆，只能平面移动），该方法只对本地玩家有效 |
| [IsSitting](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=yfszkzx1) | 获取玩家是否坐着 |
| [SitDown](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9lnzzdb2) | 坐下，该方法只对本地玩家有效 |
| [StandUp](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=m4p08wfb) | 站起，该方法只对本地玩家有效 |
| [SetFlyMode](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7yfqkcj0) | 设置飞行模式 |
| [StartFly](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=peope8v0) | 开始飞行 |
| [StopFly](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9rxwitu3) | 停止飞行 |
| [CanFly](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=phem353b) | 是否能飞行 |
| [IsFlying](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9q8hgybw) | 当前是否飞行 |
| [CanSwim](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=99nfc8kl) | 是否能游泳 |
| [IsSwimming](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cei728b0) | 当前是否在游泳 |
| [Immobilize](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=x3xy7wo9) | 是否可以通过摇杆移动 |
| [SetAlpha](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1tvonxhf) | 设置当前 Actor 的透明度，alpha 取值范围[0-1] |
| [SetVisible](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=gh5fy2f8) | 是否隐藏当前 Actor  |
| [EnableInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5nbxxaqg) | 把当前对象设置为可交互对象 |
| [DisableInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=t2wuf899) | 把当前对象移除掉可交互对象 |
| [CalculatePalmTransform](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=by55sch5) | 计算当前 Actor 手部挂点 |
| [EnableFly](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=tgnah6wh) | 开启飞行/悬浮 |
| [DisableFly](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=2jpwykdn) | 禁止飞行/悬浮 |
| [EnableHoldHand](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=860cpfce) | 开启牵手行为 |
| [DisableHoldHand](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=poqilqxg) | 禁止牵手行为 |
| [IsHoldHand](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=wofh2of3) | 当前 Actor 是否处于牵手状态 |
| [CanHoldHand](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=jnqpay69) | 当前 Actor 是否可以牵手 |
| [GetHoldHandState](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=8yxbrsdp) | 返回牵手状态的枚举类型 |
| [StopHoldHand](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=4jt3bg7r) | 结束当前 Actor 的牵手状态 |
| [InviteDuoInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=7ef5mu3k) | Actor发起一次多人交互 |
| [AcceptDuoInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=wve7l398) | Actor接受其他Actor发起的交互 |
| [IsDuoInteractionWaiting](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=a63xnec8) | Actor等待多人交互，当发起多人交互，其他Actor没有接受多人交互的时候，会处于等待状态。 |
| [StopDuoInteractionWaiting](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=cvnyhrki) | 停止交互等待 |
| [StartDuoInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9ow44xu4) | Actor开始多人交互，交互的对象是传入的actor |
| [StopDuoInteraction](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=voy0maex) | 退出双人交互，如果是引导者，停止所有的双人交互；如果是跟随者，停止跟随者后续的所有双人交互 |
| [IsDuoInteracting](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=8myrbqxu) | Actor正在多人交互交互中 |
| [NetSpawn](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rgltipmz) | 动态生成和Actor绑定的网络对象，Actor销毁时，该Actor创建的网络对象也会被销毁 |
| [SetJumpAudioClip](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=wp5s436f) | 设置跳跃的音效 |
| [SetFootstepAudioClips](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=yq8a0l6x) | 设置脚步声。传入的数组应包含两个音效，分别对应：左脚的声音、右脚的声音。 |
| [SetSpeed](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=t9oqg6bw) | 设置精灵移动速度，并自动联动行走动画的播放速度；速度高于默认基础速度时动画相应加快，避免"脚步打滑"，否则保持原速。 |


