# 创建 Sequence（补间序列）

`Sequence` 与 Tweener 类似，但它的动画对象不是属性或数值，而是**其他 Tweener 或 Sequence**——它把它们作为一个整体来驱动。

## 特性要点

- 序列可以嵌套在其他序列中，嵌套深度没有限制。
- 序列内的补间不必一个接一个地排列，可以通过 `Insert` 方法让它们重叠。
- 一个补间（Sequence 或 Tweener）只能嵌套进一个序列中，不能在多个序列里复用同一个补间。
- 主序列会接管所有嵌套元素，之后无法单独控制嵌套补间——可以把序列想象成一条电影时间轴：一旦首次启动，它就固定不变了。
- 加入序列的补间不能使用无限循环（但根序列可以）。

> [!IMPORTANT]
> 不要使用空序列。

## 创建步骤

创建序列分两步。

### 第 1 步：获取一个新的 Sequence 并保存引用

```cs
static DOTween.Sequence()
```

返回一个可用的 `Sequence`，你可以保存引用并向其中添加补间。

```cs
Sequence mySequence = DOTween.Sequence();
```

### 第 2 步：向 Sequence 中添加补间、间隔和回调

注意：

- 以下所有方法都必须在序列开始之前调用（通常是创建后的下一帧，除非序列被暂停），否则不会生效。
- 任何嵌套的 `Tweener` / `Sequence` 在加入序列之前都必须完整创建好，因为加入之后它就会被锁定。
- 延迟和循环（非无限）即使在嵌套补间中也能正常工作。

#### Append / AppendCallback / AppendInterval —— 添加到末尾

```cs
Append(Tween tween)
AppendCallback(TweenCallback callback)
AppendInterval(float interval)
```

- `Append`：将给定补间添加到序列的末尾（即当前序列总时长的位置）。
- `AppendCallback`：将给定回调添加到序列的末尾。
- `AppendInterval`：将给定间隔添加到序列的末尾。

```cs
mySequence.Append(transform.DOMoveX(45, 1));
mySequence.AppendCallback(MyCallback);
mySequence.AppendInterval(interval);
```

#### Insert / InsertCallback —— 插入到指定时间位置

```cs
Insert(float atPosition, Tween tween)
InsertCallback(float atPosition, TweenCallback callback)
```

- `Insert`：将给定补间插入到指定的时间位置，从而允许补间重叠，而不是只能一个接一个地排列。
- `InsertCallback`：将给定回调插入到指定的时间位置。

```cs
mySequence.Insert(1, transform.DOMoveX(45, 1));
mySequence.InsertCallback(1, MyCallback);
```

#### Join —— 与最后一项同时播放

```cs
Join(Tween tween)
```

将给定补间插入到序列中最后一个补间或回调的同一时间位置。

```cs
// 旋转补间将与移动补间同时播放
mySequence.Append(transform.DOMoveX(45, 1));
mySequence.Join(transform.DORotate(new Vector3(0,180,0), 1));
```

#### Prepend / PrependCallback / PrependInterval —— 添加到开头

```cs
Prepend(Tween tween)
PrependCallback(TweenCallback callback)
PrependInterval(float interval)
```

- `Prepend`：将给定补间添加到序列的开头，并把其余内容整体向后推移。
- `PrependCallback`：将给定回调添加到序列的开头。
- `PrependInterval`：将给定间隔添加到序列的开头，并把其余内容整体向后推移。

```cs
mySequence.Prepend(transform.DOMoveX(45, 1));
mySequence.PrependCallback(MyCallback);
mySequence.PrependInterval(interval);
```

> [!TIP]
> 你还可以创建只包含回调的序列，把它当作定时器之类的东西来用。

## 示例

```cs
// 获取一个空闲的 Sequence 使用
Sequence mySequence = DOTween.Sequence();
// 在开头添加一个移动补间
mySequence.Append(transform.DOMoveX(45, 1));
// 上一个补间结束后，立即添加一个旋转补间
mySequence.Append(transform.DORotate(new Vector3(0,180,0), 1));
// 让整个序列延迟 1 秒
mySequence.PrependInterval(1);
// 插入一个贯穿整个序列时长的缩放补间
mySequence.Insert(0, transform.DOScale(new Vector3(3,3,3), mySequence.Duration()));
```

与上一个示例相同，但使用链式写法（加换行更清晰）：

```cs
Sequence mySequence = DOTween.Sequence();
mySequence.Append(transform.DOMoveX(45, 1))
  .Append(transform.DORotate(new Vector3(0,180,0), 1))
  .PrependInterval(1)
  .Insert(0, transform.DOScale(new Vector3(3,3,3), mySequence.Duration()));
```
