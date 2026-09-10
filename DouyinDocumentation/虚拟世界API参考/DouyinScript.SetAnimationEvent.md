public void SetAnimationEvent(AnimationClip clip, Action<AnimationEvent> callback)
# 参数
| 参数 | 描述 |
| --- | --- |
| clip | 要添加动画事件的动画剪辑 |
| callback | 动画事件回调函数。当动画事件触发时，会调用该回调函数并传 AnimationEvent 对象，方便开发者在特定的动画事件发生时执行自定义逻辑。 |
# 描述
设置一个动作的Animation Event回调，当播放此动作时会触发回调函数

