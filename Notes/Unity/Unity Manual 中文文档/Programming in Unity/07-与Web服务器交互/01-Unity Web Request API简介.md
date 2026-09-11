# Unity Web Request API 简介

> 原文：[Introduction to the Unity web request APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-intro.html)

[`UnityWebRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.html) 是 Unity 用于在运行时与 Web 服务通信、传输文件和流式传输数据的 HTTP/HTTPS 网络 API。

Unity Web Request 系统的常见用途包括：

- 在运行时下载内容，例如：
  - 从远程服务器下载 AssetBundle，可使用常规的 [AssetBundle](https://docs.unity3d.com/6000.7/Documentation/Manual/AssetBundlesIntro.html) 或 [Addressables](https://docs.unity3d.com/Packages/com.unity.addressables@latest) 系统。
  - 下载用于配置、本地化和实时调优的文本或 JSON。
  - 下载动态内容使用的图片（作为 [Texture](https://docs.unity3d.com/6000.7/Documentation/Manual/Textures.html)）和音频（作为 [AudioClip](https://docs.unity3d.com/6000.7/Documentation/Manual/class-AudioClip.html)）。
  - 通过远程清单在构建时或运行时应用补丁。
- 将数据上传到服务器，例如：
  - Player 指标。
  - 保存的游戏状态。
  - 错误、异常日志和崩溃报告。
  - 自定义遥测数据和分析数据。
- 与内容分发网络、身份验证和安全服务、支付平台、多人游戏服务、诊断服务及远程构建管线集成。
- 实现低流量的网络多人游戏和回合制游戏，例如国际象棋。

## 架构

Unity Web Request 系统由两层组成：

- [High-Level API](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-hlapi.html)（HLAPI）封装 Low-Level API，为常见操作提供方便的接口。
- [Low-Level API](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-llapi.html)（LLAPI）为更高级的操作提供最大的灵活性。

该系统将一次 HTTP 事务拆分为以下操作：

- 向服务器发送数据。
- 从服务器接收数据。
- HTTP 流程控制，例如重定向和错误处理。

这些操作分别由特定类型的对象管理。可以使用这些对象自定义和控制事务的不同方面：

- [`UploadHandler`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandler.html) 对象负责处理向服务器传输数据。
- [`DownloadHandler`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandler.html) 对象负责处理从服务器接收的数据，包括接收、缓冲和后处理。
- [`UnityWebRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.html) 对象管理前面两个对象，并处理 HTTP 流程控制。可以在此对象中定义自定义 Header 和 URL，同时从中读取错误和重定向信息。

![UnityWebRequest 数据流架构](UnityWebRequestArchitecture.png)

> [!NOTE]
> 用户代码发送的数据会经过 `UploadHandler`，再经过 `UnityWebRequest`，最后到达 HTTP Web 服务器。服务器返回的数据会经过 `UnityWebRequest`，再经过 `DownloadHandler`，最后到达用户代码。

一次 HTTP 事务的高级流程如下：

1. 创建一个 [`UnityWebRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.html) 对象。
2. 配置 `UnityWebRequest` 对象：
   - 设置自定义 Header。
   - 设置 HTTP verb，例如 `GET`、`POST` 和 `HEAD`。所有平台都允许使用自定义 verb。
   - 设置 URL。
3. （可选）创建 Upload Handler，并将其附加到 Web Request：
   - 提供要上传的数据。
   - 提供要上传的 HTTP form。
4. （可选）创建 Download Handler，并将其附加到 Web Request。
5. 发送 Web Request：
   - 在 [Coroutine](https://docs.unity3d.com/6000.7/Documentation/Manual/Coroutines.html) 中，可以对 [`UnityWebRequest.SendWebRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.SendWebRequest.html) 调用的结果执行 `yield`，等待请求完成。
6. （可选）从 Download Handler 读取接收到的数据。
7. （可选）从 `UnityWebRequest` 对象读取错误信息、HTTP 状态码和响应 Header。

如需查看说明这些步骤的详细代码示例，请参阅 [`UploadHandlerRaw`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandlerRaw.html) 的 API 文档。

## 其他资源

- [Web Request High-Level API 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-hlapi.html)
- [Web Request Low-Level API 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-llapi.html)


---

## 文档导航

- 上一页：[[00-与Web服务器交互]]
- 目录：[[00-与Web服务器交互]]
- 下一页：[[02-Web Request高级API参考]]
