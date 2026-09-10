public static void Alert(string title, string message, string confirm, Action confirmCallback, string cancel, Action cancelCallback)
# 参数
| 参数 | 参数描述 |
| --- | --- |
| title | 弹窗的标题 |
| message | 弹窗的消息按钮 |
| confirm | 确认按钮的文本 |
| confirmCallback | 确认按钮点击后的回到函数 |
| cancel | 取消按钮的文本 |
| cancelCallback | 取消按钮点击后的回调函数 |
# 描述
弹出一个弹窗，可以设置标题，内容，确认按钮，取消按钮。
