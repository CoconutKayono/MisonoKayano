# Web Request 低级 API 参考

> 原文：[Web request low-level API reference](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-llapi.html)

High-Level Web Request API 会尽量减少样板代码的数量，而 Low-Level Web Request API 提供了更多灵活性和控制能力。

本节列出 Low-Level API 的关键成员及其适用场景。通常，使用 Low-Level API 时，需要创建一个 [`UnityWebRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.html)，并根据具体的下载和上传场景，为其附加专用的 [`DownloadHandler`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandler.html) 或 [`UploadHandler`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandler.html) 对象。

High-Level API 和 Low-Level API 并不是互相排斥的。如果需要对常见操作进行更多控制，始终可以自定义通过 High-Level API 创建的 `UnityWebRequest` 对象。

## 实例化 UnityWebRequest 对象

与其他对象一样，可以通过 [`UnityWebRequest` 构造函数](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest-ctor.html)实例化 `UnityWebRequest`。创建 `UnityWebRequest` 时，可以选择是否同时创建 Upload Handler 或 Download Handler，并且有多种构造函数签名可供使用。`UnityWebRequest` 还提供了用于配置 Request、跟踪其状态和检查结果的属性。

更多信息请参阅 [`UnityWebRequest`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.html) API 参考。

## Download Handler

专用 Download Handler 可以处理特定的下载场景，并控制传入数据的处理方式。以下 Download Handler 都派生自 [`DownloadHandler`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandler.html) 基类：

| Handler 类型 | 描述 |
| --- | --- |
| [`DownloadHandlerBuffer`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandlerBuffer.html) | 用于存储简单数据。这是最简单的 Download Handler，适用于大多数使用场景。它将接收到的数据存储在原生代码缓冲区中。下载完成后，可以将缓冲数据作为字节数组或文本字符串访问。 |
| [`DownloadHandlerFile`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandlerFile.html) | 专门用于将大型文件下载并保存到磁盘，同时保持较低的内存占用。它会直接将下载的字节写入文件，因此无论文件大小如何，内存使用量都很低。与其他 Download Handler 的区别在于，需要从保存的文件中读取数据，而不是从 Handler 本身读取。 |
| [`DownloadHandlerTexture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandlerTexture.html) | 专门针对下载用作 Unity [`Texture`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Texture.html) 对象的图片进行了优化。相比先用 `DownloadHandlerBuffer` 下载图片文件的原始字节、再使用 `Texture.LoadImage` 创建 Texture，这种方式效率更高。 |
| [`DownloadHandlerAssetBundle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandlerAssetBundle.html) | 专门针对下载 Unity AssetBundle 进行了优化。它可以直接将数据流式传输到 Unity 的资源系统，并在结果中生成一个 [`AssetBundle`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AssetBundle.html) 对象。 |
| [`DownloadHandlerAudioClip`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandlerAudioClip.html) | 专门针对下载音频文件进行了优化。相比用 `DownloadHandlerBuffer` 下载原始字节、再从这些字节创建 [`AudioClip`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/AudioClip.html)，这种方式效率更高。 |
| [`DownloadHandlerScript`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandlerScript.html) | 用于实现自定义、可编写脚本的 Download Handler 的抽象基类。继承此类后，可以接收 UnityWebRequest 系统的回调，并在数据从网络到达时执行自定义处理。 |

`UnityWebRequest` 有一个 [`disposeDownloadHandlerOnDispose`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest-disposeDownloadHandlerOnDispose.html) 属性，默认值为 `true`。如果该属性为 `true`，调用 [`UnityWebRequest.Dispose`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.Dispose.html) 时，也会调用所附加 Download Handler 的 [`DownloadHandler.Dispose`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.DownloadHandler.Dispose.html)。如果需要让 Download Handler 的引用比关联的 `UnityWebRequest` 存在得更久，请将 `disposeDownloadHandlerOnDispose` 设置为 `false`。

## Upload Handler

Upload Handler 可以更详细地控制上传过程。以下 Upload Handler 都专门派生自 `UploadHandler` 基类：

| Handler 类型 | 描述 |
| --- | --- |
| [`UploadHandlerRaw`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandlerRaw.html) | 在构造时接收一个数据缓冲区。当该缓冲区是字节数组时，系统会将其复制到原生代码内存中。当远程服务器准备接收 Request Body 数据时，`UnityWebRequest` 系统会使用这个缓冲区。如果缓冲区以 `NativeArray` 提供，则不会执行复制。 |
| [`UploadHandlerFile`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandlerFile.html) | 允许将文件内容作为 Request Body 发送。使用此 Handler 可以在不占用大量内存的情况下向服务器发送大型文件。由于 Handler 会持续从文件读取数据并发送，因此任意时刻只会有文件的一小部分保留在内存中。 |

如果没有直接在 `UnityWebRequest` 上设置 `Content-Type` Header， [`UploadHandler.contentType`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandler-contentType.html) 属性的值会被用作 Web Request 的 `Content-Type` Header 值。如果在 `UnityWebRequest` 对象上设置了 `Content-Type` Header，则会忽略 Upload Handler 对象上的 `Content-Type`。如果两者都没有设置 `Content-Type`，系统默认将其设置为 `application/octet-stream`。

`UnityWebRequest` 还有一个 [`disposeUploadHandlerOnDispose`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest-disposeUploadHandlerOnDispose.html) 属性，默认值为 `true`。如果该属性为 `true`，调用 [`UnityWebRequest.Dispose`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UnityWebRequest.Dispose.html) 时，也会调用所附加 Upload Handler 的 [`UploadHandler.Dispose`](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Networking.UploadHandler.Dispose.html)。如果需要让 Upload Handler 的引用比 `UnityWebRequest` 存在得更久，请将 `disposeUploadHandlerOnDispose` 设置为 `false`。

## 其他资源

- [Unity Web Request API 简介](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-intro.html)
- [Web Request 高级 API 参考](https://docs.unity3d.com/6000.7/Documentation/Manual/web-request-hlapi.html)


---

## 文档导航

- 上一页：[[02-Web Request高级API参考]]
- 目录：[[00-与Web服务器交互]]
- 下一页：[[../08-使用Unity Properties处理类型数据/00-使用Unity Properties处理类型数据]]
