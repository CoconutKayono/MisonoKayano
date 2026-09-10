本文档说明 Lua 脚本中不可直接访问或调用的 API、类型和能力范围。未列入黑名单且已在 SDK 白名单文档中登记的能力，可按对应 API 文档正常使用。
## Lua 标准库不可用能力
以下 Lua 标准库能力不可用：

* `package.loadlib`
* `io`
* `os.execute`
* `os.exit`
* `os.getenv`
* `os.remove`
* `os.rename`
* `os.tmpname`
* `os.setlocale`
* 其它未明确开放的 `os` 成员

以下 Lua 标准库能力可用：

* `os.time`
* `os.clock`
* `os.date`
* `os.difftime`
* `debug`
* `load`
* `loadstring`
* `string`
* `math`
* `table`

## xLua API 不可用能力
以下 xLua API 不可用：

* `xlua.load_assembly`
* `xlua.access`
* `xlua.private_accessible`

## C# 命名空间不可用范围
Lua 脚本不可通过 `CS.xxx` 或 `xlua.import_type` 直接访问以下 C# 命名空间：

* `System.IO`
* `System.Reflection.Emit`
* `System.Runtime.InteropServices`
* `UnityEngine.Networking`

以下示例均不可用：
```Lua
xlua.import_type("System.IO.File")
CS.System.IO.File
xlua.import_type("UnityEngine.Networking.UnityWebRequest")
CS.UnityEngine.Networking.UnityWebRequest
```

## C# 类型不可用范围
Lua 脚本不可通过 `CS.xxx` 或 `xlua.import_type` 直接访问以下 C# 类型：

* `System.Diagnostics.Process`
* `System.Diagnostics.ProcessStartInfo`
* `System.Activator`
* `System.AppDomain`
* `System.Environment`
* `System.GC`
* `System.Type`
* `System.Console`

以下示例均不可用：
```Lua
xlua.import_type("System.Diagnostics.Process")
CS.System.Diagnostics.Process
xlua.import_type("System.Activator")
CS.System.Activator
```

## Android / JNI 类型不可用范围
Lua 脚本不可直接访问以下 Android / JNI 相关类型：

* `UnityEngine.AndroidJavaObject`
* `UnityEngine.AndroidJavaClass`
* `UnityEngine.AndroidJavaProxy`
* `UnityEngine.AndroidJavaRunnable`
* `UnityEngine.AndroidJNI`
* `UnityEngine.AndroidJNIHelper`

## UnityWebRequest 不可用范围
Lua 脚本不可使用 `UnityEngine.Networking` 相关能力，包括但不限于：

* `UnityEngine.Networking.UnityWebRequest`
* `UnityEngine.Networking.DownloadHandler`

以下示例不可用：
```Lua
xlua.import_type("UnityEngine.Networking.UnityWebRequest")
CS.UnityEngine.Networking.UnityWebRequest
CS.UnityEngine.Networking.DownloadHandler
```

## 反射相关不可用成员
Lua 脚本中可以使用基础类型信息能力，例如读取类型名称：
```Lua
local t = typeof(CS.UnityEngine.Vector3)
print(t.Name)
```

但不可继续调用反射成员解析、成员调用、类型构造或程序集加载相关能力。
### 成员解析类
以下成员不可用：

* `GetMethod`
* `GetMethods`
* `GetField`
* `GetFields`
* `GetProperty`
* `GetProperties`
* `GetEvent`
* `GetEvents`
* `GetMember`
* `GetMembers`
* `GetConstructor`
* `GetConstructors`
* `GetNestedType`
* `GetNestedTypes`
* `GetDefaultMembers`
* `FindMembers`
* `FindInterfaces`
* `GetInterface`
* `GetInterfaceMap`
* `GetType`
* `GetTypes`
* `GetExportedTypes`
* `GetForwardedTypes`

### 调用与构造类
以下成员不可用：

* `Invoke`
* `InvokeMember`
* `CreateInstance`
* `CreateDelegate`
* `SetValue`
* `GetValue`
* `SetValueDirect`
* `GetValueDirect`
* `SetMethod`
* `GetSetMethod`
* `GetGetMethod`
* `GetAddMethod`
* `GetRemoveMethod`
* `GetRaiseMethod`
* `GetAccessors`
* `AddEventHandler`
* `RemoveEventHandler`

### 类型构造与加载类
以下成员不可用：

* `MakeGenericType`
* `MakeArrayType`
* `MakeByRefType`
* `MakePointerType`
* `MakeGenericMethod`
* `Load`
* `LoadModule`
* `LoadFile`
* `LoadFrom`

### Assembly / Module / Runtime Handle 相关
以下成员不可用：

* `Assembly`
* `Module`
* `DeclaringType`
* `ReflectedType`
* `TypeHandle`
* `MethodHandle`
* `FieldHandle`
* `RuntimeType`
* `DeclaringMethod`
* `GetTypeFromHandle`
* `GetTypeFromProgID`
* `GetTypeFromCLSID`
* `ReturnParameter`
* `GetParameters`

以下示例不可用：
```Lua
local t = typeof(CS.UnityEngine.Vector3)
t:GetMethod("ToString")
```

```Lua
local v = CS.UnityEngine.Vector3(1, 2, 3)
v:GetType():GetMethod("ToString"):Invoke(v, nil)
```

```Lua
typeof(CS.UnityEngine.Vector3).Assembly
```

## 可用能力说明
除本文档列出的黑名单能力外，Lua 脚本可继续使用 SDK 白名单文档中登记的 Unity 官方引擎命名空间和 Douyin 项目组件。常用可用能力包括：

* Lua 基础库：`string`、`math`、`table`
* 时间能力：`os.time`、`os.clock`、`os.date`、`os.difftime`
* 类型基础信息：`typeof` 与类型名称读取
* 常规 Unity 类型访问：例如 `CS.UnityEngine.Vector3`
* SDK 白名单中登记的 Douyin 项目组件

如某个 API 或组件未出现在 SDK 白名单中，且属于本文档列出的黑名单范围，则 Lua 侧不可直接访问或调用。
