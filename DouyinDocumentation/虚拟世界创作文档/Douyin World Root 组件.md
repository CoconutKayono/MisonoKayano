# 简介
Douyin World Root 组件是抖音虚拟世界SDK提供的基础组件之一，任何世界作品都需要添加该组件才能进行上传流程。
Douyin World Root 组件功能包含： 

1. 出生点配置
2. 玩家基础属性
3. 自定义相机
4. 网格对象生成配置

场景中仅允许存在 **1个 “Douyin World Root”组件**，不可重复添加。 

# 使用方式
Douyin World Root 组件的使用方式非常简单，只需要在场景创建一个空对象（空物体），并将该组件挂载到该空对象上即可。此时，该空物体的位置默认为玩家出生点位置。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ebbe9f4365354ef0988af8a6a5aa82ae~tplv-goo7wpa0wc-image.image" width="300px" /></div>

# 出生点设置
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/3363f9b5b95a47e7a1e369c9a3c7f029~tplv-goo7wpa0wc-image.image" width="300px" /></div>

| **属性名称** | **属性说明** |
| --- | --- |
| 出生顺序  | 1. 随机出生点：默认随机在出生点列表随机一个出生点。  <br> 2. 首个出生点：出生点设置的首个出生点。  <br> 3. 按出生点顺序出生。  |
| 出生点设置  | 默认填入当前Root组件挂载的对象，作为出生点位置，可手动拖入场景中物体作为出生点位置。  |
| 重生高度  | 默认：-100米，低于此阈值的玩家和物体将在出生点重生。  |
| 玩家重生逻辑  | 玩家低于重生高度阈值时的重新生成逻辑。 <br>  <br> 1. 在随机出生点重生（默认） 。 <br> 2. 在首次出生的位置重生。 |
| 物体重生逻辑  | 物体低于重生高度阈值时的重新生成逻辑：  <br>  <br> 1. 重置到初始位置（默认） 。 <br> 2. 销毁。 |
| 游客模式 | 游客出生点：游客模式下用户进入世界后所在的位置。 |
# 玩家基础属性
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/ad4a4bd20a5d4069bc5a2091d7ad8639~tplv-goo7wpa0wc-image.image" width="300px" /></div>

| **属性名称** | **属性说明** |
| --- | --- |
| 玩家移动速度  | 玩家在世界内的移动速度，默认为3米/秒。  <br>  <br> * 不可输入小于0的数，若输入则重置为0。  <br> * 飞行、悬浮速度等同玩家移动速度。  |
| 玩家跳跃高度  | 玩家在世界内的跳跃高度，默认为1米。  <br>  <br> * 不可输入小于0的数，若输入则重置为0。  |
# 自定义相机
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8dd95341697946e8b917849824bd53fb~tplv-goo7wpa0wc-image.image" width="300px" /></div>

| **属性名称** | **属性说明** |
| --- | --- |
| 相机  | 自定义相机默认为空，世界上传后会自动添加符合3C（Character, Controls, Camera）标准的官方相机。  <br>  <br> * 若创作者需要自定义相机，可以将创建的相机拖入列表并配置为自定义相机。  <br> * 没有关联的且自己创建的相机在世界上传后将会被删除。  <br>  <br>  |
注：更多详情请看 [自定义相机](/s196aspp/pwkegq0i)
# 网络对象生成配置
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/98de3c46cad04252ac91dcae478f6c36~tplv-goo7wpa0wc-image.image" width="300px" /></div>

| **属性名称** | **属性说明** |
| --- | --- |
| 网络对象生成  | 网络对象是指需要同步于所有客户端上的对象。 <br> 对于世界中动态生成的网络对象，需要创建Douyin Network Spawn脚本，并与Douyin World Root 关联。  |
| 网络对象  | 创作者可增删网络对象数组，数组中每个元素包含：  <br>  <br> * 主键：长度不限，但必须唯一。  <br> * 游戏对象：可关联场景中的 GameObject，GameObject需挂载[网络同步](https://vcreate.douyin.com/pet/wiki/s196aspp/5gzuf4g9)**组件。** <br>  <br> **注意：一个世界中最多可以共存 10,000 个网络对象。** |
注：更多详情请看 [网络对象生成配置](/s196aspp/5gzuf4g9)
# 横竖屏配置
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/58020b493f8940e2a99e756c324bdb2c~tplv-goo7wpa0wc-image.image" width="300px" /></div>

| **属性名称** | **属性说明** |
| --- | --- |
| 横竖屏支持类型 | * 只支持横屏 <br> * 只支持竖屏 <br> * 支持横竖屏，默认横屏 <br> * 支持横竖屏，默认竖屏 |
注：更多详情请看 [UI横竖屏](/s196aspp/148wljf8)

