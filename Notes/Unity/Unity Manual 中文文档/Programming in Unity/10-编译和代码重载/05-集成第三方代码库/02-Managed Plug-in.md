# Managed Plug-in

> 原文：[Managed plug-ins](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-managed.html)

Managed Plug-in 是在 Unity 外部创建并编译的 [.NET 程序集](https://docs.unity3d.com/6000.7/Documentation/Manual/dotnet-profile-support.html)，通常使用 Visual Studio 等工具编译为动态链接库（DLL）。

这与标准 C# Script 的处理过程不同：Unity 将标准 C# Script 作为源文件存储在 Unity Project 的 `Assets` 文件夹中，并在它们发生变化时重新编译；DLL 则已经预编译，不会改变。你可以像使用标准 Script 一样，把编译好的 `.dll` 文件添加到 Project 中，并将其中的 Class 附加到 **GameObject** 上。

关于 C# 中的 Managed Code，详见 Microsoft 的 [What is managed code?](https://docs.microsoft.com/en-us/dotnet/standard/managed-code) 文档。

Managed Plug-in 只包含 .NET Code，因此无法访问 .NET Library 不支持的功能。不过，Managed Code 可以被 Unity 用来编译 Script 的标准 .NET 工具访问。

在 Unity 中使用 DLL 比使用 Script 需要完成更多步骤。不过，在以下情况下，创建并将 `.dll` 文件添加到 Unity Project 可能很有用：

- 希望在代码中使用 Unity 不支持的 Compiler。
- 希望在 `.dll` 文件中添加第三方 .NET Code。
- 希望在不提供 Source 的情况下向 Unity 提供 Code。

本页说明创建 Managed Plug-in 的通用方法，以及如何创建 Managed Plug-in 并使用 Visual Studio 设置 Debug Session。

## 创建 Managed Plug-in

要创建 Managed Plug-in，需要创建 DLL。为此，你需要合适的 Compiler，例如：

- [Visual Studio](https://visualstudio.microsoft.com/)
- [MsBuild](https://docs.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2019)
- [.NET SDK](https://docs.microsoft.com/en-us/dotnet/core/sdk)

并非所有能生成 .NET Code 的 Compiler 都与 Unity 兼容，因此在投入大量工作之前，应先用一些可用 Code 测试该 Compiler。关于 Unity 当前支持的 .NET Profile，详见 [.NET profile support](https://docs.unity3d.com/6000.7/Documentation/Manual/dotnet-profile-support.html)。

创建 DLL 的方法取决于 DLL 是否包含 Unity API Code：

- 如果 DLL 包含 Unity API Code，需要在编译前让 Compiler 可以使用 Unity 自己的 DLL：

  1. 查找 Unity DLL：

     - 在 Windows 上，前往：`C:\Program Files\Unity\Hub\Editor\<version-number>\Editor\Data\Managed`
     - 在 macOS 上：

       1. 在计算机上找到 `Unity.app` 文件。macOS 上 Unity DLL 的路径为：`/Applications/Unity/Hub/Editor/<version-number>/Unity.app/Contents/Resources/Scripting/Managed`
       2. 右键单击 `Unity.app`。
       3. 选择 **Show Package Contents**。

  2. `Managed` 文件夹包含分别用于所有 Editor 和 Engine Code 的 `UnityEditor.dll` 与 `UnityEngine.dll` facade assembly。引用它们即可让 Script 使用 Editor 或 Engine API。不要尝试直接引用单独的 Module Assembly，因为 Unity 不支持这种方式。某些 Namespace 还需要引用 Unity Project 中编译好的 Library（例如 `UnityEngine.UI`）。该 Library 位于 Project Folder 的 `~\Library\ScriptAssemblies` 目录中。

- 如果 DLL 不包含 Unity API Code，或者你已经使 Unity DLL 可用，请按照所用 Compiler 的文档编译 `.dll` 文件。编译 DLL 的确切选项取决于所使用的 Compiler。例如，在 macOS 上，Roslyn Compiler `csc` 的命令行可能如下：

`csc /r:/Applications/Unity/Hub/Editor/<version-number>/Unity.app/Contents/Resources/Scripting/Managed/UnityEngine.dll /target:library /out:MyManagedAssembly.dll /recurse:*.cs`

在此示例中：

- 使用 `/r` 选项指定要包含在 Build 中的 Library 路径，本例中为 `UnityEngine` Library。
- 使用 `/target` 选项指定所需的 Build 类型；`library` 表示构建 DLL。
- 使用 `/out` 指定 Library 名称，本例中为 `MyManagedAssembly.dll`。
- 添加要包含的 Source File 名称。使用 `/recurse` 方法，将当前工作目录及其子目录中所有以 `.cs` 结尾的文件添加进来。生成的 `.dll` 文件会出现在与 Source File 相同的文件夹中。

## 使用 Managed Plug-in

编译 DLL 后，可以像添加其他 Asset 一样，将 `.dll` 文件拖入 Unity Project。之后你可以：

- 展开 Managed Plug-in，查看 Library 中的各个 Class。
- 将继承自 `MonoBehaviour` 的 Class 拖到 GameObject 上。
- 从其他 Script 中直接使用非 `MonoBehaviour` Class。

![展开 DLL 后显示其中的 Class](managed-plugin.png)

## 使用 Visual Studio 创建 DLL

本节说明：

- 如何使用 Visual Studio 构建并集成一个简单的 DLL 示例。
- 如何为 Unity 中的 DLL 准备 Debug Session。

### 设置 Project

1. 打开 Visual Studio 并创建一个新 Project。
2. 选择 **File** > **New** > **Project** > **Visual C#** > **.Net Standard** > **Class Library (.NET Standard)**。
3. 为新 Library 添加以下信息：

   - **Name**：Namespace（本例中使用 `DLLTest` 作为名称）。
   - **Location**：Project 的 Parent Folder。
   - **Solution name**：Project 的 Folder。

4. 让 Script 可以使用 Unity DLL。在 Visual Studio 中，打开 Solution Explorer 里 **References** 的上下文菜单，选择 **Add Reference** > **Browse** > **Select File**。
5. 选择所需的 `.dll` 文件，该文件位于 UnityEngine 文件夹中。

### 编写 DLL Code

1. 在 Solution Browser 中，将默认 Class 重命名为 `MyUtilities`。
2. 将其中的 Code 替换为以下内容：

```csharp
using System;   
using UnityEngine;

namespace DLLTest {

    public class MyUtilities {
    
        public int c;

        public void AddValues(int a, int b) {
            c = a + b;  
        }
    
        public static int GenerateRandom(int min, int max) {
            System.Random rand = new System.Random();
            return rand.Next(min, max);
        }
    }
}
```

3. Build Project，生成 DLL 文件及其 Debug Symbol。

## 在 Unity 中 Debug DLL

要为 DLL 设置 Debug Session：

1. 在 Unity 中创建一个新 Project，并将构建好的 `.dll` 文件（例如 `<project folder>/bin/Debug/DLLTest.dll`）复制到 Assets 文件夹。
2. 在 Assets 文件夹中创建一个名为 `Test` 的 C# Script。
3. 将其内容替换为一个 Script：该 Script 创建 DLL 中 Class 的新实例，使用其 Function，并在 **Console** 窗口显示输出。例如，要为上一节的 DLL 创建测试 Script，请复制以下 Code：

```csharp
using UnityEngine;
using System.Collections;
using DLLTest;

public class Test : MonoBehaviour {

     void Start () {
        MyUtilities utils = new MyUtilities();
        utils.AddValues(2, 3);
        print("2 + 3 = " + utils.c);
     }
    
     void Update () {
        print(MyUtilities.GenerateRandom(0, 100));
     }
}
```

4. 将此 Script 附加到 Scene 中的 GameObject，然后单击 Play。

Unity 会在 Console 窗口显示 DLL Code 的输出。

## 编译 Unsafe C# Code

[Unsafe C# Code](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/unsafe) 可以直接访问内存。默认情况下不会启用它，因为 Compiler 无法验证它是否会引入安全风险。

你可能希望使用 Unsafe Code 来：

- 使用 Pointer 访问内存。
- 分配 Raw Memory。
- 使用 Pointer 调用 Method。

要启用编译 Unsafe C# Code 的支持，请前往 **Edit** > **Project Settings** > **Player** > **Other Settings**，然后启用 **Allow Unsafe Code**。

更多信息请参阅 Microsoft 的 [unsafe code 文档](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code)。

## 其他资源

- [[00-Native Plug-in]]
- [Plugins for desktop](https://docs.unity3d.com/6000.7/Documentation/Manual/plug-ins-for-desktop.html)
- [Native plug-in interface](https://docs.unity3d.com/6000.7/Documentation/Manual/native-plugin-interface.html)
- [.NET profile support](https://docs.unity3d.com/6000.7/Documentation/Manual/dotnet-profile-support.html)

---

## 文档导航

- 上一页：[[01-导入和配置Plug-in]]
- 目录：[[00-集成第三方代码库]]
- 下一页：[[04-为桌面平台构建Plug-in]]
