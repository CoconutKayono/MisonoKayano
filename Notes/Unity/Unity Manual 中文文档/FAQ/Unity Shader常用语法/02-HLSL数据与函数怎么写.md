# 02｜HLSL 数据与函数怎么写

## 场景：看懂 float3 与 .xyz

~~~c
float time = 1.0;
float2 uv = float2(0.2, 0.8);
float3 position = float3(1, 2, 3);
half4 color = half4(0.2, 0.6, 1.0, 1.0);

float2 flipped = uv.yx;       // (0.8, 0.2)
half3 rgb = color.rgb;        // 前三个分量
half3 gray = color.rrr;       // 把 r 复制三次
color.rgb *= 0.5;             // 只改 RGB
~~~

float2/3/4 是向量类型，不是数组长度标记。.xyzw 与 .rgba 是同一组分量的不同名字，这种分量选取称为 swizzle。一次选取中不要混写两套字母，如 .xg。[Microsoft 分量运算](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-per-component-math)

| 类型                | 常见用途                |
| ----------------- | ------------------- |
| float、float2/3/4  | 位置、UV、深度、时间相关计算     |
| half、half2/3/4    | 容许较低精度的颜色、光照与部分方向数据 |
| int、uint          | 索引、计数、位运算           |
| bool              | 条件判断                |
| float3x3、float4x4 | 矩阵                  |

half 的实际精度与执行方式依平台、编译目标和设置而异，不保证处处更快；世界大坐标、细小 UV 偏移等敏感量优先用 float。旧教程里的 fixed 不建议作为本专题 URP 代码的默认选择。

## 场景：运算看似一样，含义不同

~~~c
float3 a = float3(1, 2, 3);
float3 b = float3(2, 3, 4);
float3 componentProduct = a * b;  // (2,6,12)，逐分量乘
float projection = dot(a, b);    // 20，点积
float3 perpendicular = cross(a, b); // (-1,2,-1)
float3 world = mul((float3x3)GetObjectToWorldMatrix(), a);
~~~

- * 对向量做逐分量乘；HLSL 中矩阵的 * 也不要当作数学矩阵乘法使用。
- dot 返回标量；cross 对两个三维向量返回三维向量。
- mul 才用于这里的矩阵乘法，参数顺序影响几何意义。
- 1/2 是整数除法，结果为 0；写 0.5 或 1.0/2.0 表示浮点结果。

矩阵构造与含义详见 [[../Unity Shader技术美术的线性代数/02-矩阵就是基向量的去向|矩阵与基向量]]。

## 场景：把重复效果写成函数

**放在 HLSLPROGRAM 内、其他函数外：**

~~~c
float Remap01(float x, float low, float high)
{
    // 约定 high > low
    return saturate((x - low) / max(high - low, 0.00001));
}

void SplitMask(float mask, out float inside, out float outside)
{
    inside = saturate(mask);
    outside = 1.0 - inside;
}

void Darken(inout half3 color, half amount)
{
    color *= 1.0h - saturate(amount);
}
~~~

| 参数修饰 | 数据方向 | 场景 |
| --- | --- | --- |
| in 或省略 | 传入 | 读取 UV、颜色 |
| out | 函数写出 | 同时返回多个结果 |
| inout | 先读入再改写 | 修改调用者的局部变量 |

out 输出应在每条执行路径赋值；不要返回未初始化的局部变量。HLSL 不是 C#，这里没有 MonoBehaviour、GetComponent 或材质对象的方法调用。

## 场景：条件与循环

~~~c
float mask = uv.x > 0.5 ? 1.0 : 0.0;

if (_Strength > 0.5)
{
    color.rgb *= 2.0;
}

float total = 0.0;
for (int i = 0; i < 4; ++i)
{
    total += samples[i]; // 片段：samples 必须是已声明并初始化的数组
}
~~~

if 是运行时条件；#if 是编译前的条件处理，见第 08 篇。不是所有 if 都会很慢，也不是把它换成 lerp 就一定更快；涉及昂贵采样时尤其不能盲目把两条路径都算一遍。

[unroll]、[loop] 是给编译器的循环属性，先测性能再使用，不要把它们当固定优化咒语。

## 场景：把数据组织成结构

~~~c
struct SurfaceInfo
{
    half3 color;
    float3 normalWS;
};

SurfaceInfo s;
s.color = half3(1, 0, 0);
s.normalWS = float3(0, 1, 0);
~~~

普通内部结构体可以没有语义标记；连接 GPU 输入/输出阶段的结构体则需要 POSITION、TEXCOORD 等语义，下一篇详解。

HLSL 的类型与内置函数可从 [Microsoft HLSL 参考](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl) 查起；矩阵调用规则见 [mul](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-mul)。

导航：[[00-按使用场景查语法|场景目录]] · 上一篇：[[01-搭建Shader与暴露材质参数]] · 下一篇：[[03-顶点变形与空间数据传递]]
