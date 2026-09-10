# IL2CPP 脚本后端

> 原文：[IL2CPP scripting back end](https://docs.unity3d.com/6000.7/Documentation/Manual/scripting-backends-il2cpp.html)

IL2CPP 是 Unity 的 AOT 编译流程，会将 C# Intermediate Language 转换为 C++，再编译为目标平台的 Native Code。部分不支持 Mono 和 JIT 的平台要求使用 IL2CPP。

使用 IL2CPP 时，需要注意构建时间、代码剥离、反射和 AOT 相关限制。

| 页面 | 说明 |
| --- | --- |
| [[01-IL2CPP简介]] | 了解 IL2CPP 的 AOT 流程。 |
| [[02-IL2CPP托管Stack Trace]] | 配置 IL2CPP 托管 Stack Trace。 |
| [[03-IL2CPP运行时代码检查]] | 了解运行时代码检查。 |
| [[04-额外IL2CPP编译器参数]] | 配置额外编译器参数。 |
| [[05-Linux IL2CPP交叉编译器]] | 使用 Linux 交叉编译器。 |
| [[06-IL2CPP限制]] | 了解 AOT 限制。 |

---

## 文档导航

- 上一页：[[00-IL2CPP脚本后端]]
- 目录：[[00-IL2CPP脚本后端]]
- 下一页：[[01-IL2CPP简介]]
