# Web Request 高级 API 参考

> 原文：[Web request high-level API reference](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-hlapi.html)

可以使用 High-Level API，使用常见的 HTTP verb（例如 `GET`、`POST` 和 `PUT`）向后端发送简单的 Web Request。下表列出 High-Level API 支持的一些常见操作。每项操作的详细信息和使用示例，请参阅对应的 API 文档。

| 方法 | 描述 |
| --- | --- |
| [`UnityWebRequest.Get`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.Get.html) | 从 HTTP 服务器获取文本或二进制数据（`GET`）。 |
| [`UnityWebRequest.Post`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.Post.html) | 向 HTTP 服务器发送表单（`POST`）。提供了支持两种表单数据提交格式的重载：旧版 [`WWWForm`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/WWWForm.html) 格式，以及推荐的 [`IMultipartFormSection`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.IMultipartFormSection.html) 格式。 |
| [`UnityWebRequest.Put`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.Put.html) | 向 HTTP 服务器上传原始数据（`PUT`）。 |
| [`UnityWebRequestTexture.GetTexture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestTexture.GetTexture.html) | 使用专用的 Web Request，从 HTTP 服务器下载 Unity [`Texture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Texture.html) 图片，并针对该操作进行优化（`GET`）。 |
| [`UnityWebRequestAssetBundle.GetAssetBundle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequestAssetBundle.GetAssetBundle.html) | 使用专用的 Web Request，从 HTTP 服务器下载 Unity [`AssetBundle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 对象，并针对该操作进行优化（`GET`）。 |

这些 High-Level Request 会自动为底层 `UnityWebRequest` 附加适当的 Upload Handler 或 Download Handler。这些 Handler 允许在发送数据前对其进行自定义，并在接收数据后对其进行处理。有关 Upload Handler 和 Download Handler 的更多信息，请参阅 [Low-Level API 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-llapi.html)。

## 其他资源

- [Web Request Low-Level API 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-llapi.html)
- [`UnityWebRequest` 类](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.html)


---

## 文档导航

- 上一页：[[01-Unity Web Request API简介]]
- 目录：[[00-与Web服务器交互]]
- 下一页：[[03-Web Request低级API参考]]
