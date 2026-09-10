public void PlayAnimation(Animation clip, Action<AnimationEvent> cb ＝ null, DouyinAnimatorMask mask ＝ DouyinAnimatorMask.WholeBody)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| clip | 指定要播放的动画剪辑 |
| cb | 可选参数，是一个回调函数。当动画事件触发时，会调用该回调函数并传 AnimationEvent 对象，方便开发者在特定的动画事件发生时执行自定义逻辑。 <br> 默认值为 null，表示不设置回调。 |
| mask | 可选参数，默认为 DouyinAnimatorMask.WholeBody。 <br> 用于指定动画应用的身体部位遮罩，决定动画影响的身体范围。 |
# 描述
播放一个动作，支持使用 Animation Event，可传回调函数。
DouyinAnimatorMask
WholeBody 系统姿态层，用于全身动画；
Head 系统姿态层，用于全身动画；
UpperBody 系统姿态层，用于上半身动画；
LowerBody 系统姿态层，用于下半身动画；
Arms 系统姿态层，用于双臂动画；
LeftArm 系统姿态层，用于左臂动画；
RightArm 系统姿态层，用于右臂动画；
LeftHand 系统姿态层，用于左手动画；
RightHand 系统姿态层，用于右手动画；

