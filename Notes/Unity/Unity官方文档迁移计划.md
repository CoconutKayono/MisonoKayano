# Unity 官方文档迁移计划

> 来源约束：所有页面正文、声明、重载、参数、返回值、描述、示例、相关资源、父子关系、阅读顺序和链接，必须从对应的 Unity 6000.7 官方 URL 获取和核对。本地文件只能作为最终写入目标，不能作为内容来源或校验依据。

| 阶段 | 分支 | 官方来源 | 工作内容 | 完成标准 | 状态 |
| --- | --- | --- | --- | --- | --- |
| 1 | GameObject | Unity 6000.7 ScriptReference | 父页、属性、构造函数、公共方法、静态方法、继承成员及全部子 API | 每个页面逐一从自身官方 URL 抓取，原文结构完整，链接校验通过 | 已完成 |
| 2 | Transform | Unity 6000.7 ScriptReference | 父页、属性、方法、消息、静态成员及全部子 API | 每个页面逐一从自身官方 URL 抓取，原文结构完整，链接校验通过 | 已完成（官方逐页复核） |
| 3 | Vector2 / Vector3 / Vector4 | Unity 6000.7 ScriptReference | 构造函数、属性、静态属性、方法、运算符及全部子 API | 分类和重载严格保持原文顺序 | 已完成 |
| 4 | Vector2Int / Vector3Int | Unity 6000.7 ScriptReference | 构造函数、属性、静态属性、方法、运算符及全部子 API | 分类和重载严格保持原文顺序 | 已完成 |
| 5 | Behaviour / MonoBehaviour | Unity 6000.7 ScriptReference | Behaviour 基类及 MonoBehaviour 全部属性、方法、消息、协程相关 API | 每个消息和重载均独立展开 | 已完成 |
| 6 | CharacterController | Unity 6000.7 ScriptReference | 类说明、属性、公共方法及官方示例 | 严格保留原文结构和内容，仅翻译说明文字 | 已完成 |
| 7 | 总体验证 | Unity 6000.7 官方 URL与校验脚本 | 重新核对父子关系、原文 URL、文件名和本地链接 | 所有目标目录验证通过 | 已完成 |
