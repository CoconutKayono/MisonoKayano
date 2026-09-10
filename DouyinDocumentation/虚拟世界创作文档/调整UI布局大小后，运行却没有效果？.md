问：对UI界面元素的大小进行了调整，但是本地运行之后，发现UI界面依然是调整前的样式，并且结束调试后，UI又恢复到了调整前的布局大小

答：这可能是因为当前UI界面使用了SDK内提供的[UI横竖屏](/s196aspp/148wljf8)，你可以将UI界面上挂载的 **Douyin UIHVAdapterinOnePrefab / Douyin UIHVAdapterinTwoPrefab / Douyin Canvas Adapter** 移除后再进行调整，并在调整完成后，若需要UI支持横竖屏适配，那么可以再次按照适配步骤挂载相应的脚本组件。
