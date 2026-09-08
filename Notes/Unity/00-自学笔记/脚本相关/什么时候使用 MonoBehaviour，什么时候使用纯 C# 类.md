# 什么时候使用 MonoBehaviour，什么时候使用纯 C# 类

> 适用场景：在 Unity 中写脚本时，如何决定一个类该继承 `MonoBehaviour`，还是写成普通 C# 类。本文结合《2D 肉鸽游戏》教程中的实际例子说明。

## 1. 两者的本质区别

| 对比项 | MonoBehaviour | 纯 C# 类 |
| --- | --- | --- |
| 基类 | 继承 `UnityEngine.MonoBehaviour` | 不继承任何 Unity 类 |
| 创建方式 | 通过 `AddComponent` 挂载，或拖拽到场景/预制体 | 直接 `new` |
| 生命周期 | 由 Unity 引擎调用（`Awake`/`Start`/`Update`/`OnDestroy` 等） | 自己管理，没有自动回调 |
| 与场景关系 | 必须依附 GameObject 存在 | 不依赖场景对象 |
| Inspector 序列化 | 公共/序列化字段可在 Inspector 中显示并配置 | 不能直接在 Inspector 中显示 |
| 协程 | 支持 `StartCoroutine` | 不支持 |
| 单元测试 | 依赖 Unity 运行时，难以测试 | 可在纯 .NET 环境测试，很容易 |
| 典型用途 | 组件、行为、场景交互 | 数据模型、算法、工具类、管理器的核心逻辑 |

一句话理解：

- **MonoBehaviour 的核心是「挂载与生命周期」**——它存在的意义，就是让代码能与场景中的游戏对象绑定，并响应引擎事件。
- **纯 C# 类的核心是「逻辑与数据」**——它不需要知道场景里有什么，只需要完成自己那份工作。

## 2. 快速判断流程

按下面的问题顺序判断即可：

1. 这个类需要挂到 GameObject 上吗？ → 需要 ⇒ **MonoBehaviour**
2. 需要响应 Unity 生命周期（`Update`、`OnCollisionEnter`…）吗？ → 需要 ⇒ **MonoBehaviour**
3. 需要在 Inspector 里拖拽/配置字段吗？ → 需要 ⇒ **MonoBehaviour**
4. 需要作为场景或预制体的一部分被保存吗？ → 需要 ⇒ **MonoBehaviour**（或 ScriptableObject）
5. 以上都不需要，只是数据、算法或纯逻辑？ → **纯 C# 类**

**一句话总结：需要「活」在场景里，就用 MonoBehaviour；只需要「算」或「存」，就用纯 C# 类。**

## 3. 什么时候必须用 MonoBehaviour

- 挂在物体上作为组件（玩家、敌人、摄像机控制、棋盘组件……）
- 使用 `Update` / `FixedUpdate` / `OnCollisionEnter` / `OnTriggerEnter` 等回调
- 启动协程
- 字段需要在 Inspector 中赋值（拖拽引用、调整数值）
- 使用 `OnDestroy` / `OnDisable` 等生命周期做清理

### 反例：不能手动 new 一个 MonoBehaviour

```csharp
// 错误：手动 new 一个 MonoBehaviour 行不通，组件不会生效
var player = new PlayerController();

// 正确：通过 AddComponent 或拖拽挂载
var player = gameObject.AddComponent<PlayerController>();
```

MonoBehaviour 组件必须依附在 GameObject 上，由 Unity 来创建和管理实例。

## 4. 什么时候适合用纯 C# 类

- **数据模型**：单元格数据、玩家状态、存档数据
- **纯逻辑/算法**：随机生成、寻路、回合计数、伤害计算
- **与场景无关的管理器核心**：不依赖场景对象，可独立测试
- **事件总线、服务定位器**等工具型类

### 教程实例：TurnManager

在 [[04-添加回合系统]] 中，`TurnManager` 就是一个纯 C# 类：

```csharp
public class TurnManager
{
    private int m_TurnCount;

    public TurnManager()
    {
        m_TurnCount = 1;
    }

    public void Tick()
    {
        m_TurnCount += 1;
        Debug.Log("Current turn count : " + m_TurnCount);
    }
}
```

为什么它不需要继承 MonoBehaviour？

- 它不需要挂到任何游戏对象上
- 它不需要 `Update`、`Start` 等引擎回调
- 它的工作只是「记录并推进回合数」，由 GameManager 手动 `new` 并调用

而 [[02-添加游戏棋盘]] 中的 `BoardManager`、[[03-添加玩家角色]] 中的 `PlayerController` 则**必须**是 MonoBehaviour：

- 它们要挂载到场景中的 GameObject 上
- 需要在 Inspector 中配置字段（`Width`、`Height`、`GroundTiles`、`WallTiles` 等）
- `PlayerController` 还需要 `Update` 来响应键盘输入

### 纯 C# 类里能不能用 Unity 的东西？

可以。`Debug.Log`、`Vector2Int`、`Random.Range` 这些都可以在纯 C# 类中使用（只要 `using UnityEngine;`）。但要避免让核心逻辑依赖场景对象（比如直接持有某个 GameObject 引用去 `GetComponent`），否则就失去了「可测试、可复用」的意义。

## 5. 混合模式（推荐做法）

常见且干净的结构是：**MonoBehaviour 做「壳」，纯 C# 类做「脑」**。

- **MonoBehaviour 壳**：负责获取组件引用、接收 Unity 事件、把数据转发给核心逻辑
- **纯 C# 核心**：负责游戏规则、数据计算、状态管理，与 Unity API 解耦

教程中的结构就是这样：

```
GameManager (MonoBehaviour)
├── TurnManager（纯 C#）    → new 创建，管理回合数据
├── BoardManager（MonoBehaviour） → 场景中的棋盘组件
└── PlayerController（MonoBehaviour） → 场景中的玩家组件
```

好处：

- 核心逻辑可以被单元测试，不需要打开 Unity
- 换场景、换表现层，不影响核心规则
- 依赖关系清晰：谁创建谁、谁调用谁，一目了然

## 6. 第三种选择：ScriptableObject

当数据需要「保存在工程里、可序列化」，但又不属于某个具体场景时，用 **ScriptableObject**：

- 配置表、数值表（武器参数、食物给予量）
- 可复用的数据资产（事件通道、共享数据）

判断方式：数据要不要存在于 Inspector / 资产中？

- 要，且与场景无关 → **ScriptableObject**
- 要，且属于场景对象 → **MonoBehaviour**
- 不要，只是运行时数据 → **纯 C# 类**

## 7. 常见误区

| 误区 | 说明 |
| --- | --- |
| 所有类都继承 MonoBehaviour | 会让纯逻辑类依赖 Unity 运行时，难以测试、难以复用 |
| 在纯 C# 类里 `new` MonoBehaviour | 组件不会生效，必须用 `AddComponent` |
| 在纯 C# 类里调用协程 / GetComponent | 这些 API 属于 MonoBehaviour / GameObject，纯 C# 类没有 |
| 认为纯 C# 类不能用 `using UnityEngine` | `Debug.Log`、`Vector2Int` 等可以用，但别让核心逻辑依赖场景对象 |
| 用单例 MonoBehaviour 塞下所有数据 | 把数据逻辑混进表现层，后期难以维护 |

## 8. 总结

| 场景 | 选谁 |
| --- | --- |
| 挂在物体上、响应引擎事件、需要 Inspector 配置 | **MonoBehaviour** |
| 纯数据、纯算法、需要可测试的逻辑 | **纯 C# 类** |
| 工程内可配置的数据资产 | **ScriptableObject** |
| 既需要挂场景、又要保持逻辑清晰 | **MonoBehaviour 壳 + 纯 C# 核心（混合）** |
