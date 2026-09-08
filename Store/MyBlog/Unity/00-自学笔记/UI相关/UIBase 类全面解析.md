# UIBase 类全面解析（为什么这样设计）

> 本文对 `UIBase` 逐段补充“为什么要这个、是怎么想出来的”注释。整体上，这是一个**非 MonoBehaviour 的 UI 逻辑基类**：UI 类继承它，但不挂在 GameObject 上，而是由框架统一管理生命周期、对象池、异步加载与级联操作。

## 一、总体设计思想（先回答“为什么这样设计”）

1. **逻辑与 GameObject 解耦**：不继承 `MonoBehaviour`，避免 Unity 生命周期函数和序列化的干扰；UI 的创建、更新、销毁全部由框架接管，方便做对象池（复用）和异步加载。
2. **组合模式（UI 树）**：`Parent` + `ChildList` 让 UI 组成树，父 UI 可以级联操作子 UI（排序、显隐、更新列表）。
3. **脏标记合并帧内多次变化**：`m_updateListDirty`、`m_isSortingOrderDirty` 保证“一帧内改 10 次，只处理 1 次”，避免每帧全量遍历。
4. **对象池 + 懒加载**：事件驱动、异步工具等“可能不用”的对象，用的时候才从池里取（`MemoryObject.Spawn`），销毁时释放回池（`MemoryObject.Release`），减少 GC。
5. **命名约定驱动资源加载**：`CreateWidgetByType` 用 `typeof(T).Name` 当资源路径，省掉每个调用点写路径；因此类型名不能被混淆——这就是 `#if ENABLE_OBFUZ` + `[ObfuzIgnore]` 存在的原因。
6. **异步永远可取消**：异步加载都传 `gameObject.GetCancellationTokenOnDestroy()`，UI 销毁时自动取消未完成的加载，防止“资源加载完了 UI 却没了”的泄漏与空引用。
7. **列表项差量复用**：`AdjustItemNum` 只增删差值，不整表重建；异步版本再按每帧预算（`maxNumPerFrame`）分帧创建，防止卡帧。
8. **全屏遮挡优化**：被全屏 UI 盖住的界面触发 `OnHidden` 停止更新/渲染，关闭后触发 `OnVisible`。

## 二、逐段代码注释

### 文件头与命名空间

```csharp
using System;
using System.Collections.Generic;
using Cysharp.Threading.Tasks;   // UniTask：零 GC 分配的异步方案；比协程轻、可取消、可等待
using DGame;                      // 项目内公共库（DLogger、MemoryObject、UIType 等）
using UnityEngine;
#if ENABLE_OBFUZ
using Obfuz;
#endif
```

### 类声明

```csharp
namespace GameLogic
{
    /// <summary>
    /// UI基类
    /// </summary>
#if ENABLE_OBFUZ
    // 为什么忽略类型名混淆：CreateWidgetByType 用 typeof(T).Name 作为资源路径。
    // 如果混淆器改了类名，资源加载就找不到对应路径，整个命名约定体系会崩。
    // ApplyToChildTypes = true：继承它的所有 UI 类同样不能被改类型名。
    [ObfuzIgnore(ObfuzScope.TypeName, ApplyToChildTypes = true)]
#endif
    public abstract class UIBase
    {
        // 为什么抽象：UIBase 只提供公共能力与生命周期骨架，不允许直接 new，
        // 必须由具体窗口/组件类继承并实现自己的逻辑。

        protected UIBase m_parent = null;

        /// <summary>
        /// UI父节点
        /// </summary>
        public UIBase Parent => m_parent;
        // 为什么要有父节点：构成 UI 树。
        // 子 UI 需要向父级上报变化（如 MarkUpdateDirty 向上级联），
        // 框架也需要从根向子树级联操作（排序、显隐）。
```

### 自定义数据（开窗传参）

```csharp
        protected System.Object[] m_userDatas;

        /// <summary>
        /// 自定义数据
        /// </summary>
        public System.Object UserData => m_userDatas != null && m_userDatas.Length >= 1 ? m_userDatas[0] : null;
        // 为什么只取第 0 个：绝大多数开窗场景只传一个参数，
        // 提供 UserData 作为最常用的便捷入口，避免调用方每次写 [0]。

        /// <summary>
        /// 自定义数据集
        /// </summary>
        public System.Object[] UserDatas => m_userDatas;
        // 为什么还要全量版本：少数窗口需要多个参数（如"打开背包 + 指定页签 + 来源按钮"），
        // 提供数组版本而不为每种参数组合设计构造函数/重载。
```

### Unity 组件包装

```csharp
        /// <summary>
        /// 窗口的实例资源对象
        /// </summary>
        // ReSharper disable once InconsistentNaming
        public virtual GameObject gameObject { get; protected set; }

        /// <summary>
        /// 窗口的位置组件
        /// </summary>
        // ReSharper disable once InconsistentNaming
        public virtual Transform transform { get; protected set; }

        /// <summary>
        /// 窗口的矩阵位置组件
        /// </summary>
        // ReSharper disable once InconsistentNaming
        public virtual RectTransform rectTransform { get; protected set; }

        // 为什么这样写：
        // 1) 逻辑类不继承 MonoBehaviour，所以需要自己持有组件引用；
        // 2) protected set：引用只能由框架/基类在创建时赋值一次，子类不能乱改；
        // 3) virtual：UIWidget 等派生类的"窗口组件"可能和父窗口不同（比如子面板有自己
        //    的 RectTransform），允许派生类覆盖。

        /// <summary>
        /// UI类型
        /// </summary>
        public virtual UIType Type => UIType.None;
        // 为什么需要类型：框架要根据 UI 类型做管理，例如"是否全屏遮挡"、
        // "属于哪个层级"；基类默认 None，具体窗口 override 返回自己的类型。

        /// <summary>
        /// 资源是否准备完毕
        /// </summary>
        public bool IsPrepared { get; protected set; }
        // 为什么：异步创建时资源可能还没加载完，调用方要等 IsPrepared 为 true 才能操作；
        // 也防止"资源未就绪就去 Find 子节点/注册事件"。

        /// <summary>
        /// 资源是否被销毁
        /// </summary>
        internal bool IsDestroyed { get; set; }
        // 为什么手动标记销毁：这个类不是 MonoBehaviour，不能依赖 Unity 对销毁对象的
        // "假 null" 判定；异步回调里必须靠 IsDestroyed 判断 UI 是否已经没了，
        // 否则会继续操作已销毁的界面。

        protected virtual bool Visible { get; set; }
        // 为什么可见性是"受控属性"而不是直接改 gameObject.SetActive：
        // 可见性由框架驱动（被全屏 UI 覆盖也算不可见），
        // 与 OnVisible/OnHidden 生命周期配合，做遮挡优化。
```

### 子组件列表与更新列表（脏标记）

```csharp
        /// <summary>
        /// UI子组件列表
        /// </summary>
        internal readonly List<UIWidget> ChildList = new List<UIWidget>();
        // 为什么：组合模式。窗口持有所有子 widget，排序/显隐/销毁时可以统一级联。
        // readonly：引用本身不能换，防止被整体替换导致框架引用错乱。

        /// <summary>
        /// 存在Update更新的UI子组件列表
        /// </summary>
        protected List<UIWidget> m_updateChildList = null;

        /// <summary>
        /// 是否重建更新列表
        /// </summary>
        protected bool m_updateListDirty = true;
        // 为什么要有这两个字段：大部分子 widget 不需要每帧 Update。
        // 如果每帧都遍历 ChildList 全量判断，浪费；所以只维护"需要更新"的子列表，
        // 增删子级时把 m_updateListDirty 置 true，下一帧重建一次（脏标记合并）。

        /// <summary>
        /// 是否标记脏排序
        /// </summary>
        protected bool m_isSortingOrderDirty = false;
        // 为什么：一帧内可能多次修改 sortingOrder，每次都级联到子树很浪费；
        // 置脏后由框架在合适时机统一处理一次。
```

### 生命周期虚方法（框架调度骨架）

```csharp
        /// <summary>
        /// 代码自动生成绑定
        /// </summary>
        protected virtual void ScriptGenerator()
        {
        }
        // 为什么单独一个方法：代码生成器（如自动生成 Find/绑定成员代码）生成的代码
        // 放在这里，与手写逻辑隔离；重新生成时只覆盖这一块，不会冲掉手写代码。

        /// <summary>
        /// 绑定UI成员元素
        /// </summary>
        protected virtual void BindMemberProperty()
        {
        }
        // 为什么和 ScriptGenerator 分开：自动生成的绑定是一次性的，手写的成员绑定
        //（如"根据配置决定哪个节点显示"）放在这里，两者职责不同。

        /// <summary>
        /// 注册事件
        /// </summary>
        protected virtual void RegisterEvent()
        {
        }

        /// <summary>
        /// 窗口创建
        /// </summary>
        protected virtual void OnCreate()
        {
        }

        /// <summary>
        /// 窗口刷新。
        /// </summary>
        protected virtual void OnRefresh()
        {
        }
        // 为什么要这一串虚方法：
        // 1) 构造函数里不能安全操作 GameObject（组件还没赋上、可能抛异常），
        //    所以创建逻辑必须放到框架调用的 OnCreate；
        // 2) 每个阶段一个虚方法，子类按需覆盖，框架统一按固定顺序调度，
        //    避免子类之间逻辑散落、顺序不可控；
        // 3) OnCreate（只做一次）与 OnRefresh（每次打开都刷数据）分开，
        //    因为"首次创建"和"重复打开刷新"是两种不同语义。

        /// <summary>
        /// 是否需要Update
        /// </summary>
        protected bool m_hasOverrideUpdate = true;

        /// <summary>
        /// 窗口更新
        /// </summary>
        protected virtual void OnUpdate() => m_hasOverrideUpdate = false;
        // 这是本类最巧的一个设计：运行时自动探测"子类是否覆盖了 OnUpdate"。
        //
        // 思路：
        // - 基类实现把 m_hasOverrideUpdate 置 false；
        // - 如果子类覆盖了 OnUpdate 且不调用 base.OnUpdate()，标记保持 true；
        // - 框架据此判断"这个 UI 需要进 Update 列表"。
        //
        // 为什么不用别的方式：
        // - 用反射检测重写：慢，而且对热更新/代码裁剪不友好；
        // - 让子类手动声明"我要 Update"：容易忘、容易漏。
        // 这个技巧把"有没有覆盖"变成一次运行时自动发现。
        //
        // 约定：子类覆盖 OnUpdate 时不要调用 base.OnUpdate()，否则标记会被清掉。

        /// <summary>
        /// 窗口销毁
        /// </summary>
        protected virtual void OnDestroy()
        {
        }
```

### 排序级联

```csharp
        /// <summary>
        /// 当触发窗口的层级排序。
        /// </summary>
        protected void _OnSortingOrderChange()
        {
            m_isSortingOrderDirty = false;

            if (ChildList != null)
            {
                for (int i = 0; i < ChildList.Count; i++)
                {
                    ChildList[i]?.OnSortingOrderChange();
                }
            }

            OnSortingOrderChange();
        }
        // 为什么下划线前缀：约定"框架内部调度入口"。子类只覆盖下面那个虚方法，
        // 不用管"清脏标记 + 级联子级"这些样板逻辑。

        /// <summary>
        /// 触发窗口的层级排序
        /// </summary>
        protected virtual void OnSortingOrderChange()
        {
        }
        // 为什么级联：嵌套 UI（如"弹窗里再弹确认框"）的排序变化必须向下传播，
        // 否则子面板会盖错层级。

        /// <summary>
        /// 当因为全屏遮挡触发或者窗口可见性触发窗口的显隐
        /// </summary>
        protected virtual void OnVisible()
        {
        }

        /// <summary>
        /// 界面不可见的时候调用
        /// 当被上层全屏界面覆盖后，也会触发一次隐藏
        /// </summary>
        protected virtual void OnHidden()
        {
        }
        // 为什么有这两个回调：性能优化。
        // 被全屏 UI 盖住的界面不需要渲染和更新，框架在遮挡发生时调 OnHidden
        //（通常在这里停止动画/定时器），遮挡解除后调 OnVisible 恢复。
        // 注意：OnHidden 只是"不可见"，不是销毁，状态要保留。
```

### 子级增删与更新列表重建

```csharp
        internal void AddChild(UIWidget child)
        {
            if (ChildList != null)
            {
                ChildList.Add(child);
                MarkUpdateDirty();
            }
        }

        internal void RemoveChild(UIWidget child)
        {
            if (ChildList != null)
            {
                if (ChildList.Remove(child))
                {
                    MarkUpdateDirty();
                }
            }
        }

        private void MarkUpdateDirty()
        {
            m_updateListDirty = true;
            Parent?.MarkUpdateDirty();
        }
        // 为什么 Add/Remove 之后要置脏：子级集合变了，"需要 Update 的子列表"就失效了。
        // 为什么还要向上级联：父 UI 也持有包含本 UI 的更新列表，
        // 本 UI 的 Update 状态变化会波及父级，所以一直冒泡到根，统一重建。
```

### 查找子组件

```csharp
        #region FindChildComponent

        protected Transform FindChild(string path)
            => FindChildImp(rectTransform, path);

        private Transform FindChild(Transform trans, string path)
            => FindChildImp(trans, path);

        /// <summary>
        /// 查找子组件
        /// </summary>
        /// <typeparam name="T">组件类型</typeparam>
        /// <param name="path">子节点路径</param>
        /// <returns>找到的组件</returns>
        public T FindChildComponent<T>(string path) where T : Component
            => FindChildComponentImp<T>(rectTransform, path);

        protected T FindChildComponent<T>(Transform trans, string path) where T : Component
            => FindChildComponentImp<T>(trans, path);

        private static Transform FindChildImp(Transform trans, string path) => trans.Find(path);

        private static T FindChildComponentImp<T>(Transform trans, string path) where T : Component
            => trans.Find(path)?.gameObject.GetComponent<T>();
        // 为什么：
        // 1) 提供"从自身 rectTransform 开始"和"从任意节点开始"两个入口，前者是
        //    最常见的用法（查自己下面的子节点），后者用于查兄弟/其他分支；
        // 2) 实现做成 private static：纯函数，不依赖实例状态，两个重载复用同一份逻辑；
        // 3) 路径查找（transform.Find）比 GetComponentsInChildren 全量遍历精准且快，
        //    这也是 UI 框架绑定成员的常见方式（配合编辑器/生成器写死路径）。

        #endregion
```

### UI 事件（懒加载 + 对象池）

```csharp
        #region UIEvent

        private GameEventDriver m_eventDriver;

        protected GameEventDriver EventDriver =>
            m_eventDriver == null ? m_eventDriver = MemoryObject.Spawn<GameEventDriver>() : m_eventDriver;
        // 为什么懒加载：不是每个 UI 都会注册事件。用的时候才从对象池拿，
        // 避免每个 UI 都无条件持有一个事件管理器（浪费内存，还增加初始化成本）。
        // 为什么用对象池（MemoryObject.Spawn）：事件驱动对象高频创建/销毁，
        // 池化复用避免 GC 分配。

        /// <summary>
        /// 添加UI事件
        /// </summary>
        /// <param name="eventID">事件ID</param>
        /// <param name="handler">事件处理函数</param>
        public void AddUIEvent(int eventID, Action handler)
            => EventDriver.AddUIEvent(eventID, handler);

        // 下面 1~6 个参数的重载：事件系统按 eventID 分发，参数个数不同只是把
        // "带几个参数的回调"包装进统一的事件驱动里，避免调用方自己写委托转换。
        public void AddUIEvent<T>(int eventID, Action<T> handler)
            => EventDriver.AddUIEvent(eventID, handler);

        public void AddUIEvent<T1, T2>(int eventID, Action<T1, T2> handler)
            => EventDriver.AddUIEvent(eventID, handler);

        public void AddUIEvent<T1, T2, T3>(int eventID, Action<T1, T2, T3> handler)
            => EventDriver.AddUIEvent(eventID, handler);

        public void AddUIEvent<T1, T2, T3, T4>(int eventID, Action<T1, T2, T3, T4> handler)
            => EventDriver.AddUIEvent(eventID, handler);

        public void AddUIEvent<T1, T2, T3, T4, T5>(int eventID, Action<T1, T2, T3, T4, T5> handler)
            => EventDriver.AddUIEvent(eventID, handler);

        public void AddUIEvent<T1, T2, T3, T4, T5, T6>(int eventID, Action<T1, T2, T3, T4, T5, T6> handler)
            => EventDriver.AddUIEvent(eventID, handler);

        protected void RemoveAllUIEvents()
        {
            MemoryObject.Release(m_eventDriver);
            m_eventDriver = null;
        }
        // 为什么必须"释放回池 + 置 null"：
        // 1) 池对象如果还挂着旧 UI 的委托（委托里持有 this），会形成引用泄漏，
        //    甚至让"已销毁的 UI"继续响应事件；
        // 2) 置 null 后再次访问 EventDriver 会重新从池里取一个干净实例。
        // 这是"获取时懒加载、释放时还回池"的对称设计，销毁顺序和获取顺序相反。

        #endregion
```

### 创建 UIWidget（同步 / 异步 / 列表复用）

```csharp
        #region Create UIWidget

        /// <summary>
        /// 创建UIWidget 通过父UI位置节点
        /// <remarks>资源实例已存在父物体所以不需要异步创建</remarks>
        /// </summary>
        /// <param name="goPath">父UI位置节点</param>
        /// <param name="visible">是否可见</param>
        /// <typeparam name="T">UIWidget</typeparam>
        /// <returns></returns>
        public T CreateWidget<T>(string goPath, bool visible = true) where T : UIWidget, new()
        {
            var goRootTrans = FindChild(goPath);

            if (goRootTrans != null)
            {
                return CreateWidget<T>(goRootTrans.gameObject, visible);
            }

            return null;
        }

        public T CreateWidget<T>(Transform parentTrans, string goPath, bool visible = true) where T : UIWidget, new()
        {
            var goRootTrans = FindChild(parentTrans, goPath);

            if (goRootTrans != null)
            {
                return CreateWidget<T>(goRootTrans.gameObject, visible);
            }

            return null;
        }

        public T CreateWidget<T>(GameObject goRoot, bool visible = true) where T : UIWidget, new()
        {
            if (goRoot == null)
            {
                return null;
            }

            var widget = new T();

            if (widget.Create(this, goRoot, visible))
            {
                return widget;
            }

            return null;
        }
        // 为什么这些是"同步"的：备注写得很清楚——资源实例已经存在于父物体里
        //（UI 预制体上的固定槽位），不存在加载过程，new + Create 包装即可。
        // 三个重载分别是"自身路径 / 指定节点路径 / 直接给 GameObject"，覆盖常见调用姿势。

        /// <summary>
        /// 通过资源路径创建UIWidget
        /// </summary>
        public T CreateWidgetByPath<T>(Transform parentTrans, string assetLocation, bool visible = true)
            where T : UIWidget, new()
        {
            GameObject goInst = UIModule.ResourceLoader.LoadGameObject(assetLocation, parentTrans);
            return CreateWidget<T>(goInst, visible);
        }
        // 同步版本：调用方确认资源已就绪（或能接受卡顿）时使用。

        /// <summary>
        /// 异步通过资源路径创建UIWidget
        /// </summary>
        public async UniTask<T> CreateWidgetByPathAsync<T>(Transform parentTrans, string assetLocation,
            bool visible = true)
            where T : UIWidget, new()
        {
            if (gameObject == null)
            {
                return null;
            }
            // 为什么先判空：加载前 UI 可能已被销毁，直接返回 null，避免无意义的加载。

            GameObject goInst = await UIModule.ResourceLoader.LoadGameObjectAsync(assetLocation, parentTrans,
                gameObject.GetCancellationTokenOnDestroy());
            // 为什么传这个取消令牌：这是"异步可取消"的关键。
            // 加载期间如果 UI 被销毁，token 会触发取消，加载立即中断，
            // 不会出现"资源加载完了，但 UI 已经没了"的空引用/泄漏。

            return CreateWidget<T>(goInst, visible);
        }

        /// <summary>
        /// 通过预制体创建UIWidget
        /// </summary>
        public T CreateWidgetByPrefab<T>(GameObject goPrefab, Transform parentTrans = null, bool visible = true)
            where T : UIWidget, new()
        {
            var widget = new T();

            if (!widget.CreateByPrefab(this, goPrefab, parentTrans, visible))
            {
                return null;
            }

            return widget;
        }
        // 为什么需要这个：列表项等高频场景通常"预制体引用已持有"，直接实例化，
        // 不需要按路径再查一次资源表。

        /// <summary>
        /// 通过类型名称创建UIWidget
        /// </summary>
        public T CreateWidgetByType<T>(Transform parentTrans, bool visible = true)
            where T : UIWidget, new()
            => CreateWidgetByPath<T>(parentTrans, typeof(T).Name, visible);

        public async UniTask<T> CreateWidgetByTypeAsync<T>(Transform parentTrans, bool visible = true)
            where T : UIWidget, new()
            => await CreateWidgetByPathAsync<T>(parentTrans, typeof(T).Name, visible);
        // 为什么用 typeof(T).Name 当资源路径：这是项目的资源命名约定——
        // "widget 类名 == 资源名"。好处是调用方不用传路径，少写样板；
        // 代价是类名不能被混淆（所以文件头有 ObfuzIgnore）。

        /// <summary>
        /// 调整列表项数量
        /// </summary>
        public void AdjustItemNum<T>(List<T> itemList, int count, Transform parentTrans, GameObject prefab = null,
            string assetLocation = "") where T : UIWidget, new()
        {
            if (itemList == null)
            {
                DLogger.Error($"itemList is null, please check GameObject: {gameObject.name}.{parentTrans.name}!");
                return;
            }

            if (itemList.Count < count)
            {
                int needNCnt = count - itemList.Count;

                for (int i = 0; i < needNCnt; i++)
                {
                    T tempItem = prefab != null
                        ? CreateWidgetByPrefab<T>(prefab, parentTrans)
                        : CreateWidgetByType<T>(parentTrans);
                    itemList.Add(tempItem);
                }
            }
            else if (itemList.Count > count)
            {
                RemoveUnUseItem(itemList, count);
            }
        }
        // 为什么"只补差值/只删多余的"：列表项本质是对象池。
        // 如果每次刷新都整表销毁重建，会产生大量 GC 和实例化开销；
        // 差量增删让列表滚动、数据刷新时只动最小集合。
        // 可以传 prefab（走实例化）或 assetLocation（走路径加载），两种来源二选一。

        /// <summary>
        /// 异步调整列表项数量
        /// </summary>
        public void AsyncAdjustItemNum<T>(List<T> itemList, int count, Transform parentTrans, GameObject prefab = null,
            string assetLocation = "", int maxNumPerFrame = 5, Action<T, int> updateAction = null)
            where T : UIWidget, new()
            => AsyncAdjustItemNumInternal(itemList, count, parentTrans, maxNumPerFrame, updateAction, prefab,
                assetLocation).Forget();
        // .Forget() = fire-and-forget：调用方"启动异步调整但不等待完成"。
        // 为什么默认每帧 5 个：一次性创建几十上百个 widget 会卡掉一帧，
        // 每帧限流 + UniTask.Yield() 把创建分摊到多帧，保证界面流畅。

        /// <summary>
        /// 异步等待调整列表项数量完成
        /// </summary>
        public async UniTask AsyncAwaitAdjustItemNum<T>(List<T> itemList, int count, Transform parentTrans,
            GameObject prefab = null, string assetLocation = "", int maxNumPerFrame = 5,
            Action<T, int> updateAction = null)
            where T : UIWidget, new()
            => await AsyncAdjustItemNumInternal(itemList, count, parentTrans, maxNumPerFrame, updateAction, prefab,
                assetLocation);
        // 为什么还要一个"可等待"版本：有些调用方需要等列表建完再继续
        //（比如列表建好后才定位滚动位置、播入场动画），Forget 版本满足不了。

        private async UniTask AsyncAdjustItemNumInternal<T>(List<T> itemList, int count, Transform parentTrans,
            int maxCntPerFrame, Action<T, int> updateAction, GameObject prefab, string assetLocation)
            where T : UIWidget, new()
        {
            if (itemList == null)
            {
                DLogger.Error($"itemList is null, please check GameObject: {gameObject.name}.{parentTrans.name}!");
                return;
            }

            int createCnt = 0;

            for (int i = 0; i < count; i++)
            {
                T tempT = null;

                if (i < itemList.Count)
                {
                    tempT = itemList[i];   // 已有的直接复用，不重建
                }
                else
                {
                    if (prefab != null)
                    {
                        tempT = CreateWidgetByPrefab<T>(prefab, parentTrans);
                    }
                    else
                    {
                        tempT = await CreateWidgetByPathAsync<T>(parentTrans, assetLocation);
                    }

                    itemList.Add(tempT);
                }

                int index = i;
                // 为什么局部复制一份 index：传统上是为了避免"闭包捕获循环变量"的陷阱
                //（循环变量被多个回调共享、值都变成最后一个）。
                // 虽然这里立即使用、不构成闭包，但保留这个习惯是防御性的。

                if (updateAction != null)
                {
                    updateAction(tempT, index);
                }
                // 为什么把"绑定数据"交给外部回调：创建和显示是两件事。
                // 本方法只负责"凑够数量"，每个 item 显示什么数据由调用方决定，
                // 这样列表逻辑可以在不同 UI 间复用。

                createCnt++;

                if (createCnt >= maxCntPerFrame)
                {
                    createCnt = 0;
                    await UniTask.Yield();   // 让出一帧，下一帧继续创建
                }
            }

            if (itemList.Count > count)
            {
                RemoveUnUseItem(itemList, count);
            }
        }

        private void RemoveUnUseItem<T>(List<T> itemList, int count) where T : UIWidget
        {
            for (int i = itemList.Count - 1; i >= count; i--)
            {
                var item = itemList[i];
                itemList.RemoveAt(i);
                item.Destroy();
            }
        }
        // 为什么从后往前删：RemoveAt 会移动后续元素的下标；
        // 从尾部开始删，前面的下标不受影响，循环不会跳项或越界。

        #endregion
```

### 红点

```csharp
        #region 红点相关

        /// <summary>
        /// 异步创建红点项
        /// </summary>
        public async UniTask<RedDotItem> CreateRedDotAsync(int redDotNodeID, Transform parent)
        {
            var item = await CreateWidgetByTypeAsync<RedDotItem>(parent);
            item?.Init(redDotNodeID);
            return item;
        }

        /// <summary>
        /// 创建红点项
        /// </summary>
        public RedDotItem CreateRedDot(int redDotNodeID, Transform parent)
        {
            var item = CreateWidgetByType<RedDotItem>(parent);
            item?.Init(redDotNodeID);
            return item;
        }
        // 为什么单独封装一层：红点是高频出现的小 UI 标记，把"创建 widget + 初始化节点ID"
        // 两步封装成一个方法，调用方一行搞定。
        // 为什么 item?.Init：创建可能失败（资源缺失、节点为空），空值保护避免崩。
        // 两个版本：异步用于运行时按需加载；同步用于资源已就绪/编辑器内的场景。

        #endregion
    }
}
```

## 三、常见疑问 / 注意事项

- **`m_hasOverrideUpdate` 的约定**：子类覆盖 `OnUpdate` 时不要调用 `base.OnUpdate()`，否则框架会误以为“没有覆盖”，从而不再调用它。这是这个技巧的隐性约定，代码里值得再注释强调。
- **异步加载失败会向列表加入 null**：`AsyncAdjustItemNumInternal` 中，如果 `CreateWidgetByPathAsync` 返回 null（如加载失败或 UI 已销毁），`itemList.Add(tempT)` 仍会把 null 加进去，后续 `updateAction(tempT, index)` 可能空引用。实际使用时可考虑加判空。
- **`UserData` 与 `UserDatas`**：二者是同一份数组的两种访问方式，传参约定建议在框架文档里写明“第 0 个参数是什么”，否则各窗口的约定会不一致。
- **非 MonoBehaviour 的代价**：好处是可控、可池化、可异步；代价是必须自己管理 `IsDestroyed`、事件释放、取消令牌等。凡是 `AddXxx` 都应有对应的 `RemoveXxx`（这里是 `RemoveAllUIEvents`），对称性是这类框架最容易出错也最需要守住的地方。
