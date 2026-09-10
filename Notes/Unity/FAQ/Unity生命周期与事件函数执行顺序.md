# Unity 生命周期与事件函数执行顺序

## 快速结论

一个正常启用的 `MonoBehaviour` 实例，典型执行顺序是：

```text
Awake → OnEnable → Start
                    ↓
        FixedUpdate / Update / LateUpdate
                    ↓
                OnDisable
                    ↓
                OnDestroy
```

> 注意：不同 GameObject 上同名事件函数之间的先后顺序，默认不保证。若确实需要控制脚本之间的顺序，应使用 Script Execution Order 或显式初始化流程。

## 函数与执行次数

| 函数 | 执行时机 | 执行次数 |
| --- | --- | ---: |
| `Awake()` | 脚本实例初始化时 | 每个脚本实例 1 次 |
| `OnEnable()` | GameObject 激活且脚本组件启用时 | 每次启用 1 次，可多次 |
| `Start()` | 第一次 `Update` 前 | 每个脚本实例最多 1 次 |
| `FixedUpdate()` | 固定物理时间步 | 每个渲染帧可能 0、1 或多次 |
| `Update()` | 每个渲染帧 | 启用期间通常每帧 1 次 |
| `LateUpdate()` | 所有 `Update()` 执行后 | 启用期间通常每帧 1 次 |
| `OnDisable()` | 组件或 GameObject 被禁用时 | 每次禁用 1 次，可多次 |
| `OnDestroy()` | 组件或 GameObject 即将销毁时 | 通常 1 次 |

## 1. Awake

```csharp
void Awake()
{
    // 初始化自身数据、缓存组件引用
}
```

适合用于：

- 初始化字段和内部状态；
- `GetComponent`、缓存自身组件引用；
- 建立脚本自身需要的引用。

规则：

- 每个 `MonoBehaviour` 实例只调用一次；
- GameObject 在场景加载时处于 inactive，`Awake` 会延迟到它第一次激活时调用；
- 脚本组件本身 disabled 时，只要 GameObject 激活，`Awake` 仍可能被调用；
- 重新启用组件不会再次调用 `Awake`；
- 不要依赖不同 GameObject 之间的 `Awake` 先后顺序。

## 2. OnEnable

```csharp
void OnEnable()
{
    // 注册事件、开启监听、启动功能
}
```

以下情况可能触发 `OnEnable`：

```csharp
gameObject.SetActive(true);
enabled = true;
```

前提是 GameObject 和脚本组件最终都处于启用状态。

例如：

```text
首次激活：OnEnable
禁用：    OnDisable
再次激活：OnEnable
再次禁用：OnDisable
```

`OnEnable` 可以执行多次。第一次执行时，它通常发生在 `Awake` 之后、`Start` 之前；后续重新启用时，`Start` 不会重新执行。

## 3. Start

```csharp
void Start()
{
    // 初始化依赖其他脚本已经完成 Awake 的内容
}
```

规则：

- 每个脚本实例最多调用一次；
- 如果脚本在初始化时 disabled，`Start` 会延迟到它第一次启用时调用；
- 之后反复禁用和启用，不会再次调用 `Start`；
- `Start` 一定在该场景对象的 `Awake` 完成后执行；
- 运行时通过 `Instantiate` 创建的对象，其 `Awake`、`OnEnable`、`Start` 通常会在当前帧结束前执行。

一个常见的初始化安排是：

```text
B.Awake()：初始化 B 自己的数据
A.Start()：读取 B 已经初始化好的数据
```

## 4. FixedUpdate、Update、LateUpdate

```csharp
void FixedUpdate()
{
    // 物理逻辑，例如 Rigidbody.AddForce
}

void Update()
{
    // 输入和普通游戏逻辑
}

void LateUpdate()
{
    // 摄像机跟随、需要等待 Update 完成的逻辑
}
```

常见的相对顺序是：

```text
FixedUpdate → Update → LateUpdate
```

### FixedUpdate

- 按固定时间间隔执行，由 `Time.fixedDeltaTime` 控制；
- 一帧可能执行 0 次、1 次或多次；
- 适合刚体、力、碰撞等物理相关计算；
- 不要把依赖渲染帧的输入或 UI 更新主要放在这里。

### Update

- 在脚本启用且 GameObject 激活时执行；
- 通常每个渲染帧执行一次；
- 适合输入处理、计时器和普通游戏逻辑。

### LateUpdate

- 通常在所有 `Update` 执行完后调用；
- 适合摄像机跟随、角色朝向修正等需要等待其他对象更新完毕的逻辑。

## 5. OnDisable

```csharp
void OnDisable()
{
    // 取消事件注册、停止监听、关闭临时功能
}
```

以下情况会触发：

- `enabled = false`；
- `gameObject.SetActive(false)`；
- 父 GameObject 被禁用；
- 组件或 GameObject 被销毁；
- 场景卸载。

`OnDisable` 与 `OnEnable` 通常成对出现，因此可以执行多次。

## 6. OnDestroy

```csharp
void OnDestroy()
{
    // 最终清理
}
```

常见触发情况：

- `Destroy(gameObject)`；
- 场景卸载；
- 退出应用或停止 Play Mode。

Unity 官方文档特别说明：如果 GameObject 从未激活过，可能不会调用它的 `OnDestroy`。

## 完整示例

```csharp
using UnityEngine;

public class LifeCycleDemo : MonoBehaviour
{
    private void Awake()
    {
        Debug.Log("Awake");
    }

    private void OnEnable()
    {
        Debug.Log("OnEnable");
    }

    private void Start()
    {
        Debug.Log("Start");
    }

    private void FixedUpdate()
    {
        Debug.Log("FixedUpdate");
    }

    private void Update()
    {
        Debug.Log("Update");
    }

    private void LateUpdate()
    {
        Debug.Log("LateUpdate");
    }

    private void OnDisable()
    {
        Debug.Log("OnDisable");
    }

    private void OnDestroy()
    {
        Debug.Log("OnDestroy");
    }
}
```

首次启动时通常看到：

```text
Awake
OnEnable
Start
FixedUpdate / Update / LateUpdate
FixedUpdate / Update / LateUpdate
...
```

禁用后再启用时通常看到：

```text
OnDisable
OnEnable
```

不会重新调用：

```text
Awake
Start
```

## 实践建议

| 需求 | 推荐位置 |
| --- | --- |
| 初始化自身数据 | `Awake` |
| 缓存自身组件 | `Awake` |
| 注册/取消事件 | `OnEnable` / `OnDisable` |
| 读取其他脚本的初始化结果 | `Start` |
| 普通逐帧逻辑 | `Update` |
| 刚体和物理计算 | `FixedUpdate` |
| 摄像机跟随 | `LateUpdate` |
| 最终清理 | `OnDestroy` |

## 官方资料

- [Unity 6.0：Event function execution order](https://docs.unity3d.com/6000.0/Documentation/Manual/execution-order.html)
- [MonoBehaviour.Awake](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.Awake.html)
- [MonoBehaviour.OnEnable](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.OnEnable.html)
- [MonoBehaviour.Start](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.Start.html)
- [MonoBehaviour.OnDisable](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.OnDisable.html)
- [MonoBehaviour.OnDestroy](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MonoBehaviour.OnDestroy.html)

