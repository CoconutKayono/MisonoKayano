# 描述
这种对象为持久化数据提供统一的 API。只能存储数值数据，不支持元数据或历史版本数据。
# 公开方法
| [GetData](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=re3zkdbp) | 获取数据。如果键存在，也会返回DouyinOrderedDataInfo |
| --- | --- |
| [SetData](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0pylgya4) | 设置数据。如果操作成功，也会返回DouyinOrderedDataInfo |
| [IncrementData](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0txr6lz7) | 递增与键对应的值，并返回新的值 |
| [UpdateData](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=6m86tgow) | 通过回调函数更新与键对应的数据。回调函数获取当前值，并根据定义的逻辑返回新值。回调函数一旦执行，便不能暂停。 |
| [RemoveData](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=wv4fwgvm) | 删除与键对应的数据。 |
| [GetSortedData](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=mgnn5uzv) | 按顺序获取数据。 |

