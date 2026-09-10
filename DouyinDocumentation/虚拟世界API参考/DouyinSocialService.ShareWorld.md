public static void ShareWorld(string templateId, Action<bool> callback)
# 描述
该函数用于将当前的游戏世界分享给他人。
# 参数
| 参数名称 | 参数描述 |
| --- | --- |
| templateId | 用于选择分享内容的模板 ID。此 ID 必须预先在平台设置并通过审核。 <br> 如果该字段为空字符串 `""`（默认值），则会使用官方提供的世界分享模板。 |
| callback | 分享操作完成后触发的回调函数。该函数会接收一个布尔值参数，用于表明分享是否成功： <br>  <br> * `true`：分享成功 <br> * `false`：分享失败 |

