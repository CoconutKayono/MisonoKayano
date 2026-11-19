# TextMesh Pro：从直觉到使用的 FAQ

**阅读目标：**看到一块文字时，能解释它如何从字符串变成像素；遇到方框、模糊、裁切或卡顿时，知道先检查哪一层。

本文参考 GAMES101 从基础原理走向应用的组织方式，采用“观察现象 → 提出问题 → 建立模型 → 做实验 → 回到工程”的路线。下面的类比、实验与 FAQ 是原创学习讲解，技术依据为 uGUI 2.7 官方文档，并非 GAMES101 课程内容或 Unity 官方译文。

如果只有五分钟，读完 **Why、What 和第一次使用**；如果正在排错，直接跳到 FAQ。没有图形学基础也可以读，数学只用于解释一个边界。

## Why：为什么需要 TextMesh Pro？ {#why}

### 从一个字开始：放大“你好”会发生什么？

想象把一张写着“你好”的小截图放大八倍。截图保存的是一格格像素。放大后，最近邻采样会露出方块；用双线性过滤把相邻像素混合，边缘又可能变软。**过滤能平滑已有信息，却不能凭空补回没有记录的轮廓细节。**

但游戏里的文字不是一张固定尺寸的截图。同一句话可能出现在手机按钮上、不同分辨率的窗口中、世界空间的角色头顶，还要缩放、描边、发光。与此同时，文字还要自动换行、对齐、支持中文和表情。问题因此分成两类：**怎样画得清楚，以及怎样排得正确。**

### 能不能直接把字体纹理做得很大？

可以提高质量，但会付出纹理空间和生成成本。只有数字和英文时，字符集合较小；中文界面、玩家昵称和多语言内容，会把问题推向另一种规模。假设同格式单张图集从 1024 × 1024 增加到 2048 × 2048，像素数量会变为四倍。实际显存还与纹理格式、mipmap、图集数量有关。

于是我们希望：**用有限的纹理记录足够有用的轮廓信息，让着色器在屏幕上重新判断边缘；同时把字体选择和排版交给专门的文本组件。**这就是理解 TMP 的入口。

### TMP 解决了哪几件事？

| 想解决的问题 | TMP 提供的能力 | 仍要自己决定的事情 |
|---|---|---|
| 字体缩放、变换后边缘质量不稳定 | SDF 字体与相应着色器 | 图集分辨率、采样字号、目标屏幕尺度 |
| 每个文字效果都单独做图片很麻烦 | 材质控制描边、底层投影等效果 | 选择支持该效果的着色器、合理内边距 |
| 对齐、换行、溢出和间距不好控制 | 文本布局、丰富的属性和富文本标签 | 文本框大小、布局规则和交互需求 |
| 一个字体资源装不下所有字符 | 动态字体、后备字体与多图集等机制 | 字符覆盖、包体、内存和首次生成成本 |

不要把这张表读成“用了 TMP 就一定更快”。SDF 改善的是轮廓表示与渲染方式；频繁生成字形、重新排版、打断合批，仍然可能很贵。实际性能需要看 Profiler。[继续核对：TMP 概述](../pages/39-index.html)、[SDF 字体](../pages/84-FontAssetsSDF.html)。

### 为什么描边也能从同一张纹理得到？

如果只记录“这里有墨／这里没墨”，描边需要另找边界。如果记录“离边界有多远”，就可以把判断条件从“在字里面”改成“在字里面，或距离字的边缘足够近”。同一份距离信息因此可以服务于字面和描边。具体效果还取决于 TMP 所选着色器，不能把所有着色器视为同一个功能集合。

## What：TextMesh Pro 是什么？ {#what}

### 先画出一条完整的路径 {#pipeline}

<div class="pipeline" role="img" aria-label="字符串经过字体查找、排版和网格生成，再由材质和渲染器输出到屏幕">
<div><b>① 字符串</b><small>“你好，Unity”<br>文本和标签</small></div><i>→</i>
<div><b>② 字体与字形</b><small>找到对应字形<br>不够时查后备字体</small></div><i>→</i>
<div><b>③ 排版与网格</b><small>位置、换行、对齐<br>字符的顶点与 UV</small></div><i>→</i>
<div><b>④ 材质与渲染</b><small>采样图集、判断边缘<br>Canvas 或场景渲染</small></div>
</div>

这是理解标准 TMP 工作流的简化图，不包含所有文字塑形或渲染内部步骤。它的用途是帮助定位问题：方框先看字体与字形，换行先看排版，颜色和描边先看材质，整个对象不可见先看渲染与布局。

TMP 是 Unity 中用于显示、排版和渲染文字的一套组件与资源。在当前 uGUI 2.7 文档中，其内容位于 TextMesh Pro 章节。它既能生成 Canvas 上的 UI 文字，也能生成场景中的文字网格。

### 几个看起来相似的名词，分别负责什么？

| 名词 | 直觉 | 它负责什么 |
|---|---|---|
| 字符（Character） | 你输入了哪个符号 | 文本中的字符身份，例如 Unicode 码位 |
| 字形（Glyph） | 这个符号具体长什么样 | 字体中用于表现字符的形状；字符与字形不总是一一对应 |
| 字体文件（TTF/OTF 等） | 字体的原始设计资料 | 提供轮廓、度量和字体特性等数据 |
| TMP Font Asset | TMP 的字体资料包 | 字符与字形表、度量、图集和相关配置 |
| Font Atlas | 很多字形拼在一起的一张纹理 | 提供渲染所需采样数据，可能有多张 |
| Material / Shader | 最后怎么着色 | 字面颜色、距离判断、描边和其他支持的效果 |
| TextMeshProUGUI | Canvas 上的文本显示组件 | 配合 Rect Transform 和 Canvas Renderer |
| TextMeshPro | 场景中的文本显示组件 | 使用 Mesh Renderer，不要求放在 Canvas 下 |
| TMP_Text | 两种显示组件的共同基类 | 脚本中访问共享的文本属性与方法 |

“把 TTF 拖进项目”与“把字体配置给 TMP”是两个步骤。通常需要从字体文件创建 TMP Font Asset，再把它赋给文本对象的 Font Asset。改变 Font Size 是改变显示字号，不是在重新导入 TTF。[字体资源](../pages/13-FontAssets.html)和 [TMP_Text API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_Text.html)提供具体定义。

### SDF：把“有没有墨”换成“离边界多远” {#sdf}

把字的轮廓想象成海岸线。普通位图像是在每个采样位置记“陆地／海水”或覆盖程度；SDF 则记录到海岸线的距离，并用正负号区分两侧。

为便于讲解，本文约定字内距离为正，字外为负，轮廓上为 0。这个符号约定用于教学，具体存储与着色器实现可以采用其他约定。纹理中的值经过归一化后常用灰度表达，所以你在图集中看到的是字形周围的灰度渐变，不是最终文字颜色。

<div class="equation"><b>d &gt; 0</b>：字内　｜　<b>d = 0</b>：轮廓　｜　<b>d &lt; 0</b>：字外</div>

GPU 采样距离纹理后，着色器以边界阈值重建轮廓，并在边界附近加入与屏幕采样尺度相适应的平滑过渡。用抽象表达写，就是 <code>alpha ≈ smoothstep(-w, w, d)</code>。这里 <code>w</code> 表示过渡宽度，不是实际 TMP Shader 的完整代码。想增加外描边，可在 <code>-t ≤ d &lt; 0</code> 的区域着另一种颜色；<code>t</code> 控制向外延伸的距离。

**SDF 不是每帧把 TTF 的向量轮廓重新画一遍，也不是无限分辨率。**它仍是离散纹理：源图集太小、细笔画采样不足、字特别小或极端放大时，信息与屏幕像素都会形成限制。复杂汉字尤其值得在目标设备上检查。[官方 SDF 说明](../pages/84-FontAssetsSDF.html)可对照其图集和渲染结果。

### 动手实验：同一份小图集，放大后有什么区别？ {#experiment}

<div id="sdf-lab" class="lab">
<p>下图用圆环代替字母 O，并从同一个 24 × 24 采样网格构造位图和 SDF。拖动滑块，先看轮廓，再看描边。</p>
<div class="lab-controls"><label for="lab-size">显示尺寸 <output id="lab-size-value">192 px</output><input id="lab-size" type="range" min="48" max="256" step="16" value="192"></label><label for="lab-outline">SDF 外描边 <output id="lab-outline-value">0.8 单位</output><input id="lab-outline" type="range" min="0" max="2" step="0.1" value="0.8"></label></div>
<div class="lab-canvases"><figure><canvas id="lab-nearest" width="280" height="280" role="img" aria-label="位图最近邻采样的圆环">需要支持 Canvas 的浏览器。</canvas><figcaption>位图 · 最近邻<br>放大时可见像素阶梯</figcaption></figure><figure><canvas id="lab-linear" width="280" height="280" role="img" aria-label="位图双线性采样的圆环"></canvas><figcaption>位图 · 双线性<br>混合已有覆盖值</figcaption></figure><figure><canvas id="lab-sdf" width="280" height="280" role="img" aria-label="SDF 重建的圆环及外描边"></canvas><figcaption>SDF · 双线性 + 阈值<br>由距离重建边缘</figcaption></figure></div>
<p id="lab-status" aria-live="polite">拖动滑块可比较三种显示。</p><p class="lab-note">这是 CPU Canvas 实现的二维教学模型，不是 Unity 或 TMP 的实时输出。位图同样由解析形状进行子像素覆盖采样；SDF 在固定网格上采样距离，之后双线性插值。它展示“保存的数据不同”，不构成性能或质量基准。小圆环比复杂汉字容易重建。</p>
</div>

先把尺寸调大：最近邻放大的是像素块，双线性位图混合的是覆盖值，SDF 插值的是距离后再判断边界。再增加描边：第三幅图无需更换图集，就能从字外的距离区间生成描边。最后把尺寸调小：再精巧的轮廓表示，也不能让只有几个屏幕像素的字保留全部细节。

<div class="checkpoint"><b>检查理解：</b>如果把灰度 SDF 纹理当成普通颜色图片直接显示，会看到什么？<details><summary>展开答案</summary><p>会看到模糊的距离渐变，而不是目标文字。灰度是编码的数据，需要适配的着色器解释它。字体图集和材质不能随意交叉搭配。</p></details></div>

## How：先做出一个可用的中文标签 {#how}

### 第一次使用：一个能验证结果的小实验 {#first-use}

1. **准备资源。**首次使用时，按提示导入 TMP Essential Resources；也可使用 `Window > TextMeshPro > Import TMP Essential Resources`。Examples & Extras 是额外示例，不是运行基础文本的必选资源。
2. **准备中文字体。**选择包含目标汉字的 TTF/OTF，确认项目可使用它。通过 `Window > TextMesh Pro > Font Asset Creator` 创建 Font Asset。先用小字符集 `你好世界分数0123456789：` 验证整个链条，采用 SDF 生成模式并保存；不要一开始就塞入所有 Unicode 字符。
3. **创建 UI 文本。**通过 `GameObject > UI > Text - TextMeshPro` 或编辑器中对应的 TextMeshPro UI 菜单创建对象。菜单分组会随 Unity 编辑器变化；结果应具有 `TextMeshProUGUI`、`Rect Transform`、`Canvas Renderer`，并位于 Canvas 下。
4. **接上字体。**将刚创建的 Font Asset 指定到文本组件。输入 `你好，Unity` 时，测试字符集还需要包含逗号与英文字符；否则它们可能使用后备字体或变成缺失字形。也可先输入上述字符集覆盖的 `你好世界`。
5. **固定条件。**暂时关闭 Auto Size，给足够大的文本矩形，设明确字号、白色顶点颜色和合适对齐。先证明文字能正确显示，再加入自动布局和效果。
6. **验证覆盖范围。**追加一个没有烘焙的汉字，例如 `猫`。若出现方框，说明“输入了字符”不等于“Font Asset 含有此字形”。这是理解字符覆盖的第一步。
7. **添加效果。**在匹配该字体的材质预设中添加适度描边。需要独立外观时使用独立预设，避免无意修改其他对象共享的材质。

对应文档：[导入资源](../pages/39-index.html)、[创建字体](../pages/82-FontAssetsCreator.html)、[UI 文本组件](../pages/79-TMPObjectUIText.html)。

### 静态、动态与后备字体，按内容选择 {#font-plan}

| 场景 | 一个可起步的配置 | 原因与代价 |
|---|---|---|
| 已知的按钮、标题和固定剧情 | 静态 SDF + 从真实内容提取字符集 | 提前烘焙，运行时不需要为新字形生成图集；新增内容要重新核对字符集 |
| 只有分数、倒计时 | 小型静态数字字体 | 字符少，易控制图集与外观；别忘小数点、负号和单位 |
| 玩家输入的昵称、聊天 | 含足够源字符的动态字体或动态后备字体 | 实际使用时加入字形；要保留源字体，并管理首次生成与图集增长 |
| 多语言 UI | 按语言组织字体资源与后备链 | 控制覆盖和资源加载；注意不同字体的字重、基线与材质 |

这是工程起点，不是每个项目都必须采用的模板。动态字体只会从源字体中取字形，源文件里没有的字仍然生成不了。静态资源的字符集也不等于整个 TTF 的字符集。后备字体允许继续搜索其他资源，但查找和额外材质／图集可能带来开销。[动态字体](../pages/85-FontAssetsDynamicFonts.html)、[后备链](../pages/88-FontAssetsFallback.html)。

### 代码例一：值改变时才更新分数 {#code-score}

将以下代码保存为 `ScoreLabel.cs`，挂到 GameObject 上，在 Inspector 中给 `label` 赋值。游戏逻辑改变分数时调用 `SetScore`，无需每帧把同一个字符串写回去。

```csharp
using TMPro;
using UnityEngine;

public sealed class ScoreLabel : MonoBehaviour
{
    [SerializeField] private TMP_Text label;
    private int lastScore;
    private bool hasScore;

    public void SetScore(int score)
    {
        if (label == null || (hasScore && score == lastScore))
            return;

        hasScore = true;
        lastScore = score;
        label.SetText("分数：{0:0}", (float)score);
    }
}
```

`TMP_Text` 可引用 UI 与场景中的两种 TMP 显示组件。数值版 `SetText` 接受格式与数值，能避免调用方反复进行字符串拼接；这里真正最先减少的工作是“不更新没变化的值”。这不代表整条 UI 更新路径零分配或零重建。示例使用 float 格式化，适合普通游戏分数；超过 float 连续整数精度范围（约 1677 万）的大整数应选择准确的整数转字符串方式，并仍只在数值改变时更新。[SetText API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_Text.html#TMPro_TMP_Text_SetText_System_String_System_Single_)。

### 代码例二：打字机效果先设置全文，再控制可见数量 {#code-reveal}

逐帧截取字符串容易把富文本标签截断，也会反复改变输入。可先交给 TMP 完整文本，再增加 `maxVisibleCharacters`。

```csharp
using System.Collections;
using TMPro;
using UnityEngine;

public sealed class DialogueReveal : MonoBehaviour
{
    [SerializeField] private TMP_Text label;
    [SerializeField, Min(1f)] private float charactersPerSecond = 25f;
    private Coroutine reveal;

    public void Play(string content)
    {
        if (label == null) return;
        if (reveal != null) StopCoroutine(reveal);
        reveal = StartCoroutine(Reveal(content ?? string.Empty));
    }

    private IEnumerator Reveal(string content)
    {
        label.text = content;
        label.maxVisibleCharacters = 0;
        label.ForceMeshUpdate(); // Active text object; get current parsed count.
        int total = label.textInfo.characterCount;
        float shown = 0f;

        while (label.maxVisibleCharacters < total)
        {
            shown += Time.unscaledDeltaTime * Mathf.Max(1f, charactersPerSecond);
            label.maxVisibleCharacters = Mathf.Min(total, Mathf.FloorToInt(shown));
            yield return null;
        }

        label.maxVisibleCharacters = total;
        reveal = null;
    }

    private void OnDisable()
    {
        if (reveal != null) StopCoroutine(reveal);
        reveal = null;
    }
}
```

此示例假设调用时 GameObject 和文本组件处于活动状态，全文已经具备可用字形；未处理停用后自动续播。完整内容先参与布局，所以通常比逐步扩展字符串更容易保持段落位置。这里的计数是 TMP 解析后的字符计数，不保证等于用户感知的每个完整字素：组合字符、复杂文字和 Emoji 序列需要额外验证。`ForceMeshUpdate` 用于这次读取布局数据前同步网格，不应因此放进所有对象的每帧循环。[可见字符数与网格更新 API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_Text.html)。

### 用富文本局部强调，而不是拆成一堆对象

```text
任务：收集 <color=#FFB84D>5</color> 个果实
<b>重要</b>：不要离开营地
按下 <sprite index=0> 继续
```

颜色与粗体标签需要开启 Rich Text；`sprite` 还要求可用的 Sprite Asset，以及正确索引。字体、字号、颜色和图标的局部变化，不一定要拆成多个 GameObject。但复杂的交互区域或不同布局关系，仍可能更适合独立组件。[标签速查](../pages/89-RichTextSupportedTags.html)、[精灵资源](../pages/118-Sprites.html)。

## FAQ：先根据现象定位，再调整参数 {#faq}

<div class="faq-tools"><label for="faq-filter">筛选常见问题</label><input id="faq-filter" type="search" placeholder="例如：方框、模糊、描边、打字机、GC" autocomplete="off"><p id="faq-filter-status" aria-live="polite">可按问题或答案中的关键词筛选。</p><button id="faq-expand" type="button">展开当前问题</button><button id="faq-collapse" type="button">收起当前问题</button></div>

### Q01｜我已经导入了中文 TTF，为什么仍然显示方框？ {#q01}

**直觉：**原始字体像仓库，Font Asset 像拿到柜台上的库存。仓库有货，不代表柜台已摆上。

先看对象的 Font Asset 是否就是你创建的资源；再看缺失汉字是否在 Character Table 中。静态资源需在生成时包含该字符，动态资源需有正确的 Source Font File、允许加入字形且源字体包含该字。最后检查后备链是否提供它。可以用 `你好ABC123猫` 将汉字、英文和数字分开测试，同时读 Console 中的 missing character 警告。**放大字号不会补回缺失字符。**[字体属性](../pages/81-FontAssetsProperties.html)。

### Q02｜动态字体是不是能显示所有文字？ {#q02}

不能。“动态”指按使用需求生成字形，不是在线下载或创造源字体不存在的字形。还会受图集空间、允许扩展的配置以及资源加载影响。先确认源字体覆盖目标字符，再确认动态生成与后备资源。不要在验证成功后删掉动态字体依赖的源文件。[动态字体](../pages/85-FontAssetsDynamicFonts.html)。

### Q03｜静态和动态怎样选，中文是不是必须用动态？ {#q03}

中文并不天然要求动态。固定 UI 和已知剧情可从真实文本提取字符集，静态烘焙；不可预测的聊天、昵称更适合动态或动态后备。项目可以同时使用多种策略。决定因素是“字符是否事先可知”和运行成本，而不是语言名称。[字体创建器](../pages/82-FontAssetsCreator.html)。

### Q04｜后备字体为什么导致同一句话中某些字看起来不一样？ {#q04}

字符从不同字体资源找到时，字重、设计风格、度量和材质可能不同。先查该字实际来自主字体还是后备字体，再比较两者的字号度量与材质。优先选择风格兼容的字体，并检查同屏混排。后备的作用是补充覆盖，不能保证外观自动一致。[后备链](../pages/88-FontAssetsFallback.html)。

### Q05｜图集已经很大，为什么还放不下中文？ {#q05}

一张图集空间有限。字符数量、采样字号、字形尺寸和 Padding 会共同占用它。先去掉从未使用的字符，再在目标字号下权衡采样质量。若使用支持扩展的动态资源，可检查 Multi Atlas Textures；每增加图集也可能增加内存和渲染成本。不要只通过增大图集解决所有问题。[生成设置](../pages/81-FontAssetsProperties.html)。

### Q06｜用了 SDF，文字为什么还是模糊？ {#q06}

按顺序隔离：确认 Font Asset 与材质匹配且使用 SDF 模式；将对象缩放恢复到简单设置，移除大幅 Softness 和效果；检查图集对当前显示尺寸是否足够。若文字被摄像机或 Render Texture 先渲染成低分辨率位图，之后再放大，最后一步仍会损失质量。极小文字又受屏幕像素限制。拿同一文本在简单 Canvas 上对照，可以分清“字体问题”与“后续渲染问题”。[SDF](../pages/84-FontAssetsSDF.html)、[Canvas](../pages/49-UICanvas.html)。

### Q07｜细汉字笔画消失、尖角变圆，应该调 Font Size 吗？ {#q07}

先区分**显示字号**和**生成图集时的采样字号**。若字形细节在生成图集中已经缺失，显示时把 Font Size 加大也不会重新生成源轮廓。重新生成时检查采样字号、图集大小和 SDF 模式，再在目标设备的小字号下测试。提高过采样能帮助生成距离数据，但不能消除所有最终分辨率限制。[字体创建器](../pages/82-FontAssetsCreator.html)。

### Q08｜Padding、Margin 和描边 Width 都像“加宽”，有什么区别？ {#q08}

Padding 给图集字形周围留采样和效果余量；Margin 决定文本在容器中的可用布局区域；Outline Width 是着色器中的视觉效果参数。它们属于三个位置。增加 Margin 不会增加 SDF 纹理的有效距离范围，增加 Padding 也不等于缩进文本。[创建器](../pages/82-FontAssetsCreator.html)、[文本组件](../pages/79-TMPObjectUIText.html)、[距离场着色器](../pages/121-ShadersDistanceField.html)。

### Q09｜描边、阴影或发光被切掉，先检查什么？ {#q09}

先暂时关闭 Mask/RectMask2D，看裁切是否来自 UI 遮罩；再减小效果宽度，判断是否超出字形可用采样与网格范围。随后检查字体生成的 Padding、文本的 Extra Padding，以及着色器支持的效果范围。Extra Padding 可以减轻网格边界裁切，不能补造原图集没有的距离信息。切在文本框边界与切在每个字的边界，常对应不同问题。[字面与效果](../pages/121-ShadersDistanceField.html)。

### Q10｜修改一个标签的颜色或描边，为什么其他标签也变了？ {#q10}

它们可能共享同一材质预设。需要整组统一改动时，共享是正确行为；只修改某个对象的外观时，使用独立材质预设或明确管理的实例。大量独立材质也可能打断合批，所以先划分真实的样式种类，再复用预设。仅想改变文本整体颜色，优先考虑组件的 Vertex Color。[颜色与预设](../pages/79-TMPObjectUIText.html#color)。

### Q11｜为什么设置红色后显示成黑色，或渐变颜色很奇怪？ {#q11}

最终字面颜色受顶点颜色、材质字面颜色和纹理等相乘影响。红色乘绿色可得到黑色，任何颜色乘黑色都会为黑色。诊断时将 Vertex Color 与材质 Face Color 暂时设为白色，检查 Alpha，再逐项恢复。渐变也会与基础顶点颜色相乘，不是自动替换所有颜色。[颜色渐变](../pages/119-ColorGradients.html)。

### Q12｜普通文字完全不可见，但也没出现方框，如何排查？ {#q12}

先换成确定被字体覆盖的 `ABC123`，设白色且不透明，关闭裁切和复杂效果。UI 文本检查 Canvas、对象活动状态、Rect Transform 尺寸／位置、CanvasGroup Alpha、遮罩和层级遮挡；场景文字检查摄像机是否看向它、Layer、材质和深度遮挡。字体缺字通常会留下警告或占位表现，整块不可见时不要只盯着字体图集。[UI 文本](../pages/79-TMPObjectUIText.html)、[三维文本](../pages/80-TMPObject3DText.html)。

### Q13｜TextMeshPro 与 TextMeshProUGUI 选哪个？ {#q13}

菜单、HUD、按钮标题以及使用 Canvas 布局／遮罩的文字，通常选 TextMeshProUGUI。独立场景文字可以选 TextMeshPro。**World Space Canvas 里的文字仍然是 UI 文本**，不因处于三维世界就必须改为 TextMeshPro。判断依据是渲染和布局路径，而不是你能否在场景里看到它。[两种对象](../pages/10-TMPObjects.html)。

### Q14｜为什么写成 `UnityEngine.UI.Text` 的脚本不能接 TMP？ {#q14}

它们是不同的组件类型。将公共显示文本引用改为 `TMP_Text`，并引入 `using TMPro;`；需要 UI 专用功能时可用 `TextMeshProUGUI`。然后在 Inspector 重新指定组件引用，已有序列化引用不一定自动迁移。输入框使用 `TMP_InputField`，别把文本显示组件当输入组件。[TMP_Text API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_Text.html)、[TMP_InputField API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_InputField.html)。

### Q15｜为什么 Auto Size 让相邻按钮的字大小不一致？ {#q15}

Auto Size 为每个对象在自身可用空间内寻找能容纳文本的字号。不同长度或不同容器得到不同结果是预期行为。需要整组视觉一致时，使用统一字号和布局约束；必须自动缩放时，限制 Min/Max 并验证最长语言。Auto Size 会增加排版尝试，对频繁变化的文本要考虑成本。[字体与 Auto Size](../pages/79-TMPObjectUIText.html#font)。

### Q16｜想自动换行，却出现省略号或直接被截断？ {#q16}

换行与溢出分别回答“如何分行”和“空间不够时怎么办”。先查看 Text Wrapping Mode，再看 Overflow，最后核对文本矩形的实际宽高、Margin 与父布局。省略号、截断和分页是不同策略。仅启用换行不保证容器高度能放下全部行。[换行与溢出](../pages/79-TMPObjectUIText.html#wrapping-and-overflow)。

### Q17｜垂直居中后视觉上仍然偏上或偏下？ {#q17}

排版框与可见笔画的几何中心不是同一个东西。字体的 Ascender、Descender、Baseline 等度量会影响布局；不同语言的可见区域也不同。先比较 Middle 与 Midline／几何相关对齐方式，再看混用后备字体是否带来不同度量。全项目改字体度量会影响所有使用者，应先证明问题来自度量。[行度量](../pages/83-FontAssetsLineMetrics.html)、[对齐](../pages/79-TMPObjectUIText.html#alignment)。

### Q18｜如何让背景跟着文字变大，为什么布局不停跳？ {#q18}

可以使用 Layout Group、Content Size Fitter 和 TMP 提供的首选尺寸组成布局。先明确“谁控制文本宽度，谁控制容器高度”。若父布局组控制子对象尺寸，子对象又用适配器控制同一轴，可能争夺控制权；自动字号再改变文本尺寸时，问题更难判断。先固定字号与宽度，让一个控制者负责每个轴，再逐步加功能。[适应内容大小](../pages/73-HOWTO-UIFitContentSize.html)。

### Q19｜富文本标签为什么被直接显示，或半句话突然全变色？ {#q19}

确认 Rich Text 开启、标签拼写与属性值正确，并检查结束标签的作用范围。先用 `<color=#FF0000>红色</color> 普通文字` 验证。若用户输入需按字面显示，按产品需求关闭标签解析或进行明确处理，不要把任意输入都当排版指令。`<noparse>` 适用于需要展示标签的特定文本片段。[标签速查](../pages/89-RichTextSupportedTags.html)、[禁止解析](../pages/105-RichTextNoParse.html)。

### Q20｜Emoji 或 `<sprite>` 为什么不显示？ {#q20}

先分清两条路：Unicode Emoji 查字体／表情后备支持；`<sprite>` 标签从 Sprite Asset 取图像，需正确的资源、索引或名称。彩色 Emoji 还依赖相应资源与配置；组合序列是否得到一个完整图形不能只靠单个字符测试。优先在目标平台验证，而不是用浏览器显示结果推断 Unity 一定相同。[彩色表情](../pages/09-ColorEmojis.html)、[内嵌精灵](../pages/112-RichTextSprite.html)。

### Q21｜改成 TMP 后仍然有卡顿和 GC，先优化什么？ {#q21}

先用 Profiler 确认 CPU、GC、布局或渲染哪个部分上涨。典型起点是：值未变化时不更新，避免每帧拼字符串，限制 Auto Size，检查动态字形首次生成、布局重建和材质数量。数值更新可尝试 `SetText` 格式重载，稳定标签可缓存引用。TMP 不会替你阻止业务代码生成临时字符串，也不会让整个 Canvas 免于重建。[UI Profiler](../pages/78-ProfilerUI.html)。

### Q22｜用了后备字体或多图集，Draw Call 为什么增多？ {#q22}

不同图集、材质及遮罩状态可能需要不同渲染批次；实际合批还受层级、裁切和 Canvas 条件影响。先在 UI Profiler 中读 Batch Breaking Reason，而不是假设“一个文本对象必定一次绘制”。减少不必要的材质变体、按真实字符覆盖组织字体，再验证效果。[UI Profiler](../pages/78-ProfilerUI.html)、[后备字体](../pages/88-FontAssetsFallback.html)。

### Q23｜编辑器正常，打包后中文缺字或效果消失？ {#q23}

检查构建实际包含的 Font Asset、图集、材质、源字体和后备资源，特别是按需加载的资源是否已经加载。动态字体仍需要源字体；启用字体子集化后，子集外字符不会因为它们曾存在于完整字体中而自动可用。再比对目标平台的材质／着色器和构建日志。若问题只在某种字符出现，用最小文本在真实构建中复现。[字体子集化](../pages/86-FontAssetsSubsetting.html)。

### Q24｜打字机效果为什么会跳行、闪烁，或露出半个标签？ {#q24}

逐帧用 `Substring` 改变文本，可能改变换行位置并截断富文本。先设置完整文本，再控制 `maxVisibleCharacters`，可让布局基于完整内容。还要检查垂直对齐与 Visible Descender 设置；复杂 Emoji、组合文字要按实际文本测试。示例见本文 [打字机代码](#code-reveal)。

### Q25｜设置 text 后立即读 characterCount，为什么还是旧值？ {#q25}

文本数据变了，不意味着所有布局与网格都已在同一时刻更新。需要同步读取解析结果时，可对活动对象调用 `ForceMeshUpdate()`，再读 `textInfo`。常规显示通常让组件按正常更新流程处理即可；不要为了保险每帧强制更新全部文本。父级 Canvas 布局刷新与文本自身网格更新也不完全是同一件事。[网格更新 API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_Text.html#TMPro_TMP_Text_ForceMeshUpdate_System_Boolean_System_Boolean_)。

### Q26｜中文输入框有拼音组合输入，应该读哪个 text？ {#q26}

使用 `TMP_InputField` 管理编辑，而不是从它内部显示文本的 TMP 组件读取最终业务值。通常读 `inputField.text`，并按需求使用 `onValueChanged`、`onEndEdit` 或提交相关事件。IME 组合阶段不等于用户已确认的最终字符串，应在目标平台测试组合、删除、焦点切换与提交，不要只测试英文按键。[输入框 API](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_InputField.html)。

### Q27｜换个 Font Asset 就能解决阿拉伯文、RTL 和所有复杂排版吗？ {#q27}

字形覆盖、文字塑形与双向排版是不同问题。字体有字形只是第一步，连字、组合、阅读方向和标点顺序还取决于文本生成路径及其支持程度。不要把 Enable RTL Editor 的显示／编辑行为当成完整语言塑形保证。应使用实际语言样本测试项目所用的标准或高级文本生成器，并核对其约束。[UI 文本](../pages/79-TMPObjectUIText.html#text-input)、[高级文本生成器迁移](../pages/87-FontAssetsMigration.html)。

### Q28｜打开 Advanced Text Generator 后，静态字体为什么要迁移？ {#q28}

uGUI 2.7 文档明确说明，高级文本生成器不支持静态字体资源。启用相关路径后，应按迁移工具说明转换或更换资源，而不是继续沿用“静态图集一定可用”的假设。转换可能把字体子集数据嵌入构建，还应检查字体许可及保留图集／旧表的选择。本文前面的 SDF 模型和小例子以标准 TMP 使用路径为起点，并不说明所有生成器具有完全相同的资源要求。[官方迁移说明](../pages/87-FontAssetsMigration.html)。

## 把知识变成排错顺序 {#diagnosis}

| 观察到什么 | 先隔离哪一层 | 一个最小验证 |
|---|---|---|
| 方框／某些字缺失 | 字体覆盖与后备链 | 测 `ABC123你好猫`，看字符表与 Console |
| 整块不见 | 对象、布局与渲染 | 白色不透明、足够大矩形、关闭遮罩 |
| 字边糊或笔画丢失 | 图集采样与最终屏幕尺度 | 简单 Canvas、匹配材质、禁用额外软化 |
| 描边被切 | 遮罩、图集余量与网格 | 关闭遮罩，再减小描边 |
| 换行／居中异常 | 文本矩形、度量与布局 | 固定字号和尺寸，对齐只改一个选项 |
| 首次输入卡顿 | 动态字形生成与资源加载 | 比较同字符第一次和第二次出现 |
| 持续更新卡顿 | 业务更新、排版与 Canvas | 停止文本写入，对比 Profiler |

每次先改一个变量。若同时换字体、改字号、开自动布局、换材质，即使问题消失，也不知道真正原因。

## 三个练习与自检 {#exercises}

1. **字符覆盖实验。**生成只包含 `AB12你好` 的静态字体，输入 `AB12你好猫`，预测哪个位置缺字；配置包含 `猫` 的后备字体，再观察风格与批次。学到的是“查找路径”，不是猜字号。
2. **缩放实验。**保持显示对象不变，只更换不同生成采样条件的 Font Asset；再保持 Font Asset 不变，改变显示字号。分别记录尖角、小笔画和描边。你应该能区分采样字号、显示字号与屏幕像素。
3. **更新实验。**让同一个计分标签在“每帧写入”和“值改变才写入”之间切换，使用 Profiler 比较；再单独开关 Auto Size。记下设备与条件，不凭肉眼判断哪个实现更省。

<details class="checkpoint"><summary>自检：为什么聊天框可能需要动态字体，而固定菜单不一定需要？</summary><p>聊天字符不可预测，需要运行时补字形；固定菜单可以提前提取字符集并烘焙。动态的便利来自运行时生成与源字体依赖，并非免费的无限字符库。</p></details>

<details class="checkpoint"><summary>自检：增大 Font Size 能修好所有模糊问题吗？</summary><p>不能。它只改变显示尺寸；源图集采样、材质、后续低分辨率渲染和屏幕像素仍可能限制质量。先找到信息在哪一步丢失。</p></details>

## 下一步读哪一页？ {#reading}

| 你想继续理解什么 | 建议入口 |
|---|---|
| 第一次创建文本与字体 | [创建文本](../pages/10-TMPObjects.html) → [字体创建器](../pages/82-FontAssetsCreator.html) |
| Inspector 中每个选项 | [UI 文本对象完整属性表](../pages/79-TMPObjectUIText.html)／[三维文本对象](../pages/80-TMPObject3DText.html) |
| 中文与多语言覆盖 | [动态字体](../pages/85-FontAssetsDynamicFonts.html) → [后备字体](../pages/88-FontAssetsFallback.html) → [子集化](../pages/86-FontAssetsSubsetting.html) |
| SDF 与视觉效果 | [SDF 字体](../pages/84-FontAssetsSDF.html) → [着色器](../pages/35-Shaders.html) → [距离场属性](../pages/121-ShadersDistanceField.html) |
| 局部颜色、字号、图标 | [富文本标签速查](../pages/89-RichTextSupportedTags.html) → [精灵资源](../pages/118-Sprites.html) |
| 自动布局与性能 | [适应内容大小](../pages/73-HOWTO-UIFitContentSize.html) → [UI Profiler](../pages/78-ProfilerUI.html) |

## 依据与说明 {#references}

教学组织参考 [GAMES101 课程介绍](https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html)中从基础原理到实际应用、建立全局理解的取向。本文不复述其课程或模仿授课者个人语言。

技术说明基于本地保存的 [uGUI 2.7 TextMesh Pro 官方文档](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/manual/TextMeshPro/index.html)及对应的字体、对象、着色器、富文本和 Profiler 页面。上文链接优先连接到本地手册，便于离线核对。脚本成员另核对了 [TMP_Text](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_Text.html)、[TextMeshProUGUI](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TextMeshProUGUI.html) 与 [TMP_InputField](https://docs.unity3d.com/Packages/com.unity.ugui@2.7/api/TMPro.TMP_InputField.html) API。

版本依据：uGUI 2.7.0；核对日期：2026-10-01。菜单会因编辑器而异。交互实验不调用 Unity，示例代码需在实际 Unity 工程中挂载、赋值并验证。本文的推导、工程起步配置与排错建议属于学习性说明，不能取代目标项目中的性能与平台测试。
