# 描述
视频播放组件

# 公开属性
| [isSync](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rmjdrfbs) | 是否同步 |
| --- | --- |
| [videoPlaybackMode](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=07dqky8u) | 视频播放方式 |
| [videoUrls](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=n6y4kr3u) | 视频链接列表 |
| [screenRenderer](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=xl5wyffm) | 渲染目标（只读） |
| [totalTime](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=irpdxo4y) | 当前视频总时长· |
| [playingTime](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=2hghhc8b) | 当前视频的播放时长 |
# 公开方法
| [PlayVideo](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=rukxud6e) | 视频开始播放（重头播放） |
| --- | --- |
| [PauseVideo](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=6vrzebte) | 视频暂停 |
| [ResumeVideo](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=a8lm5nk2) | 视频恢复播放（当前的进度开始播放） |
| [PlayeNextVideo](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=1kl0uvir) | 播放下一个视频 |
| [PlayVideoByIndex](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=wgyjcvl6) | 播放指定列表的索引的视频 |
| [SetPlaybackMode](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5ttrpzqz) | 切换视频播放模式 |
# 公开事件
| [onVideoPlayStarted](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=whgj4tft) | 视频开始播放的时间 |
| --- | --- |
| [onVideoPlayPaused](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=5gdgcmaw) | 视频暂停播放的事件 |
| [onVideoPlayResumed](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=uj2arn3m) | 视频恢复播放的事件 |
| [onVideoPlayEnded](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=0nn1dihw) |  视频结束播放的事件 |
| [onAllVideosPlayEnded](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=9urbk58j) | 列表所有视频结束的事件(仅顺序播放模式且没有下一个视频时触发) |

