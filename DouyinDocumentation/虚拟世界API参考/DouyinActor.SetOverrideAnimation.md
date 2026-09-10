public void SetOverrideAnimation(string key, AnimationClip clip, Action<AnimationEvent> callback= null)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| key | 用于标识要重载的动画的唯一键名。 |
| clip | 要设置的动画剪辑对象 |
| callback | 可选参数，是一个回调函数。当动画事件触发时，会调用该回调函数并传 AnimationEvent 对象，方便开发者在特定的动画事件发生时执行自定义逻辑。默认值为 null，表示不设置回调。 |
# 描述
设置重载动画。
