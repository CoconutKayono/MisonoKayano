# DOTween术语表

## 术语

`Tweener`（补间器）：接管一个值，并为其制作动画的补间。  
`Sequence`（序列）：一种特殊的补间。它不接管值，而是接管其他补间，将它们作为一个整体进行动画。  
`Tween`（补间）：对 Tweener 与 Sequence 的统称。  
`Nested tween`（嵌套补间）：包含在 Sequence 内部的补间。

> [!NOTE] 术语代码示例
> 
> ```cs
> using DG.Tweening;
> using UnityEngine;
> 
> public class NomenclatureDemo : MonoBehaviour
> {
>     // Tween 是统称，可以用来声明变量，它既可以是 Tweener 也可以是 Sequence
>     private Tween myTween;
> 
>     void Start()
>     {
>         // ----- Tweener：控制一个值（这里是 Transform 的位置） -----
>         Tweener moveTweener = transform.DOMoveX(5f, 1f);
>         // 此时 moveTweener 就是一个 Tweener，负责把 x 从当前位置动画到 5
> 
>         // ----- Sequence：控制一组 Tween，让它们按顺序/并行动画 -----
>         Sequence mySequence = DOTween.Sequence();
>         mySequence.Append(transform.DOScale(Vector3.one * 2f, 0.5f)); // 先放大
>         mySequence.Append(transform.DORotate(new Vector3(0, 180, 0), 0.5f)); // 再旋转
> 
>         // 上面的 moveTweener 和 mySequence 都叫 Tween（统称）
>         myTween = mySequence; // 这样赋值完全合法
> 
>         // ----- Nested tween（嵌套补间）：Sequence 内部包含的 Tween -----
>         // mySequence 里的 DOScale 和 DORotate 就是嵌套在 Sequence 里的两个 Tween
>     }
> }
> ```
> 

## 前缀

前缀非常重要，善用它们才能最大程度地发挥 IntelliSense 的威力，请务必牢记：

`DO` —— 所有补间快捷方式的统一前缀（即那些可以直接从已知对象上启动的操作，例如 `Transform` 或 `Material`），同时也是 `DOTween` 主类的前缀。

```cs
transform.DOMoveX(100, 1);
transform.DORestart();
DOTween.Play();
```

`Set' —— 所有可以链式挂接到补间上的设置项前缀（From 除外，因为 From 虽然以设置的形式应用，但本质上并非真正的设置）。

```cs
myTween.SetLoops(4, LoopType.Yoyo).SetSpeedBased();
```

`On` —— 所有可以链式挂接到补间上的回调函数前缀。

```cs
myTween.OnStart(myStartFunction).OnComplete(myCompleteFunction);
```

> [!NOTE] 前缀对应代码示例
> ```cs
> using DG.Tweening;
> using UnityEngine;
> 
> public class PrefixDemo : MonoBehaviour
> {
>     void Start()
>     {
>         // DO 前缀：直接在对象上启动一个动画（快捷方式）
>         transform.DOMoveY(3f, 1f);
>         // 还有 DOTween 类的静态方法也用 DO 前缀
>         DOTween.Play();
> 
>         // Set 前缀：链式追加设置（配置动画的表现）
>         transform.DOMoveX(5f, 1f)
>             .SetEase(Ease.OutBounce)   // 缓动类型
>             .SetLoops(3, LoopType.Yoyo) // 循环方式
>             .SetDelay(0.5f);           // 延迟开始
> 
>         // On 前缀：链式追加回调（动画事件）
>         transform.DOScale(Vector3.zero, 0.3f)
>             .OnStart(() => Debug.Log("开始缩小"))
>             .OnComplete(() => Destroy(gameObject)); // 缩小结束后销毁对象
>     }
> }
> ```