# 描述
该类提供了将日志上报到后台的接口。
# 注意事项

1. 此类日志接口仅限在 DS 服务器环境下调用，在客户端调用将不会生效。
2. 单条日志消息限制：8KB。
3. 在单个房间内，每帧最多可上报 20 条日志，每秒最多可上报 200 条日志。

# 公开方法
| [Debug](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fidrvelv) | 开发阶段使用的调试日志，用于辅助定位问题；不会上报到后台。 |
| --- | --- |
| [Log](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=r2g7gjia) | 通用日志，用于记录常规运行信息、简单流程节点与基础状态，内容轻量无特殊优先级。 |
| [Info](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=3md8voy6) | 信息日志，用于记录关键流程、状态变化与重要事件，便于追踪与排查问题。 |
| [Warning](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=fz34weux) | 警告日志。表示出现了需要关注的异常或潜在风险，但通常不会立即中断当前流程。 |
| [Error](https://vcreate.douyin.com/tutorial?book=4j78bceb&doc=psmvgk4y) | 错误日志。表示发生功能异常或关键流程失败，可能导致部分功能不可用，需要尽快处理。 |

