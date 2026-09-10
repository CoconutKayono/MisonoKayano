function OnUIDrag(UIType ui, Vector2 Pointer , Vector2 PointerDelta)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| ui | 玩家拖动的摇杆类型，通常为UIType.Main |
| Pointer | 摇杆位置，当摇杆位于中心点时返回(0, 0)。横轴和纵轴的取值范围均为-1~1 |
| PointerDelta | 操纵杆的位置增量 |
# 描述
当UI按钮被拖拽时，摇杆触发。

