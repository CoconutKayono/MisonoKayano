# Burst Arm Neon Intrinsics 参考

> 原文：[Burst Arm Neon intrinsics reference](https://docs.unity3d.com/6000.7/Documentation/Manual/burst/csharp-burst-intrinsics-neon.html)

以下表格列出了 Burst 中可用的主要 Arm Neon Intrinsic 操作。**操作**列包含该类 Intrinsics 的主要命名前缀。有关每种操作可用的完整 Intrinsics 列表，请参阅 [`Unity.Burst.Intrinsics.Arm.Neon` API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Burst.Intrinsics.Arm.Neon.html)。

有关如何使用这些 Intrinsics 的信息，请参阅 [[03-处理器特定SIMD扩展]]。

### Intrinsics 类型创建和转换

| 操作 | 说明 |
| --- | --- |
| `vcreate` | 创建向量 |
| `vdup_n` | 复制（splat）值 |
| `vdup_lane` | 复制（splat）向量元素 |
| `vmov_n` | 复制（splat）值 |
| `vcopy_lane` | 从另一个向量元素插入向量元素 |
| `vcombine` | 将两个向量合并为一个更大的向量 |
| `vget_high` | 获取向量的高半部分 |
| `vget_low` | 获取向量的低半部分 |

### 算术

| 操作 | 说明 |
| --- | --- |
| `vadd` | 加法 |
| `vaddv` | 对向量各元素求和 |
| `vaddl` | 长加法 |
| `vaddlv` | 对向量各元素执行长加法 |
| `vaddw` | 宽加法 |
| `vhadd` | 减半加法 |
| `vrhadd` | 舍入减半加法 |
| `vqadd` | 饱和加法 |
| `vsqadd` | 将有符号值累加到无符号饱和值 |
| `vuqadd` | 将无符号值累加到有符号饱和值 |
| `vaddhn` | 加法并返回高半部分的窄化结果 |
| `vraddhn` | 舍入加法并返回高半部分的窄化结果 |
| `vpadd` | 成对加法（向量） |
| `vpaddl` | 有符号成对长加法 |
| `vpadal` | 有符号成对长加法并累加 |
| `vsubl` | 长减法 |
| `vsubw` | 宽减法 |
| `vhsub` | 减半减法 |
| `vqsub` | 饱和减法 |
| `vsubhn` | 减法并返回高半部分的窄化结果 |
| `vrsubhn` | 舍入减法并返回高半部分的窄化结果 |

### 乘法

| 操作 | 说明 |
| --- | --- |
| `vmul` | 乘法（向量） |
| `vmul_n` | 向量乘标量 |
| `vmul_lane` | 乘法（向量） |
| `vmull` | 长乘法（向量） |
| `vmull_n` | 向量长乘标量 |
| `vmull_lane` | 长乘法（向量） |
| `vmulx` | 浮点扩展乘法 |
| `vmla` | 乘加到累加器（向量） |
| `vmla_lane` | 向量乘加标量 |
| `vmla_n` | 向量乘加标量 |
| `vmlal` | 长乘加（向量） |
| `vmlal_lane` | 长乘加标量 |
| `vmlal_n` | 长乘加标量 |
| `vmls` | 从累加器执行乘减（向量） |
| `vmls_lane` | 向量乘减标量 |
| `vmls_n` | 向量乘减标量 |
| `vmlsl` | 长乘减（向量） |
| `vmlsl_lane` | 长乘减标量 |
| `vmlsl_n` | 长乘减标量 |
| `vqdmull` | 有符号饱和加倍长乘法 |
| `vqdmull_lane` | 向量饱和加倍长乘标量 |
| `vqdmull_n` | 向量饱和加倍长乘标量 |
| `vqdmulh` | 饱和加倍乘法并返回高半部分 |
| `vqdmulh_lane` | 向量饱和加倍乘法并返回高半部分，再乘标量 |
| `vqdmulh_n` | 向量饱和加倍乘标量并返回高半部分 |
| `vqrdmulh` | 饱和舍入加倍乘法并返回高半部分 |
| `vqrdmulh_lane` | 向量饱和舍入加倍乘法并返回高半部分，再乘标量 |
| `vqrdmulh_n` | 向量饱和舍入加倍乘标量并返回高半部分 |
| `vqdmlal` | 饱和加倍长乘加 |
| `vqdmlal_lane` | 向量饱和加倍长乘加标量 |
| `vqdmlal_n` | 向量饱和加倍长乘加标量 |
| `vqdmlsl` | 有符号饱和加倍长乘减 |
| `vqdmlsl_lane` | 向量饱和加倍长乘减标量 |
| `vqdmlsl_n` | 向量饱和加倍长乘减标量 |
| `vqrdmlah` | 饱和舍入加倍乘加并返回高半部分（向量） |
| `vqrdmlah_lane` | 饱和舍入加倍乘加并返回高半部分（向量） |
| `vqrdmlsh` | 饱和舍入加倍乘减并返回高半部分（向量） |
| `vqrdmlsh_lane` | 饱和舍入加倍乘减并返回高半部分（向量） |
| `vfma` | 浮点融合乘加到累加器（向量） |
| `vfma_n` | 浮点融合乘加到累加器（向量） |
| `vfma_lane` | 浮点融合乘加到累加器（向量） |
| `vfms` | 从累加器执行浮点融合乘减（向量） |
| `vfms_n` | 从累加器执行浮点融合乘减（向量） |
| `vfms_lane` | 从累加器执行浮点融合乘减（向量） |
| `vdiv` | 浮点除法（向量） |

### 数据处理

| 操作 | 说明 |
| --- | --- |
| `vpmax` | 成对取最大值 |
| `vpmaxnm` | 浮点成对取最大数（向量） |
| `vpmin` | 成对取最小值 |
| `vpminnm` | 浮点成对取最小数（向量） |
| `vabd` | 绝对差 |
| `vabdl` | 长绝对差 |
| `vaba` | 绝对差并累加 |
| `vabal` | 长绝对差并累加 |
| `vmax` | 最大值 |
| `vmaxnm` | 浮点最大数 |
| `vmaxv` | 对向量各元素取最大值 |
| `vmin` | 最小值 |
| `vminnm` | 浮点最小数 |
| `vminv` | 对向量各元素取最小值 |
| `vabs` | 绝对值 |
| `vqabs` | 饱和绝对值 |
| `vneg` | 取负 |
| `vqneg` | 饱和取负 |
| `vcls` | 统计前导符号位 |
| `vclz` | 统计前导零位 |
| `vcnt` | 逐字节统计置位位数 |
| `vrecpe` | 倒数估计 |
| `vrecps` | 倒数迭代步 |
| `vrecpx` | 浮点倒数指数 |
| `vrsqrte` | 倒数平方根估计 |
| `vrsqrts` | 倒数平方根迭代步 |
| `vmovn` | 提取窄化结果 |
| `vmovl` | 提取长化结果 |
| `vqmovn` | 饱和提取窄化结果 |
| `vqmovun` | 有符号饱和提取无符号窄化结果 |

### 比较

| 操作 | 说明 |
| --- | --- |
| `vceq` | 按位比较相等 |
| `vceqz` | 按位比较是否等于零 |
| `vcge` | 大于或等于比较 |
| `vcgez` | 与零比较，大于或等于零 |
| `vcle` | 小于或等于比较 |
| `vclez` | 与零比较，小于或等于零 |
| `vcgt` | 大于比较 |
| `vcgtz` | 与零比较，大于零 |
| `vclt` | 小于比较 |
| `vcltz` | 与零比较，小于零 |
| `vcage` | 浮点绝对值大于或等于比较 |
| `vcagt` | 浮点绝对值大于比较 |
| `vcale` | 浮点绝对值小于或等于比较 |
| `vcalt` | 浮点绝对值小于比较 |

### 位运算

| 操作 | 说明 |
| --- | --- |
| `vtst` | 测试位是否非零 |
| `vmvn` | 按位取反 |
| `vand` | 按位与 |
| `vorr` | 按位或 |
| `vorn` | 按位或非 |
| `veor` | 按位异或 |
| `vbic` | 按位清除 |
| `vbsl` | 按位选择 |

### 移位

| 操作 | 说明 |
| --- | --- |
| `vshl` | 左移（寄存器） |
| `vqshl` | 饱和左移（寄存器） |
| `vqshl_n` | 饱和左移（立即数） |
| `vqshlu_n` | 无符号饱和左移（立即数） |
| `vrshl` | 舍入左移（寄存器） |
| `vqrshl` | 饱和舍入左移（寄存器） |
| `vshl_n` | 左移（立即数） |
| `vshll_n` | 长左移（立即数） |
| `vshr_n` | 右移（立即数） |
| `vrshr_n` | 舍入右移（寄存器） |
| `vshrn_n` | 右移并窄化（立即数） |
| `vqshrun_n` | 有符号饱和右移并窄化为无符号（立即数） |
| `vqrshrun_n` | 有符号饱和舍入右移并窄化为无符号（立即数） |
| `vqshrn_n` | 有符号饱和右移并窄化（立即数） |
| `vrshrn_n` | 舍入右移并窄化（立即数） |
| `vqrshrn_n` | 有符号饱和舍入右移并窄化（立即数） |
| `vsra_n` | 有符号右移并累加（立即数） |
| `vrsra_n` | 有符号舍入右移并累加（立即数） |
| `vsri_n` | 右移并插入（立即数） |
| `vsli_n` | 左移并插入（立即数） |

### 浮点

| 操作 | 说明 |
| --- | --- |
| `vcvt` | 转换为其他精度或定点数，向零舍入 |
| `vcvta` | 转换为整数，舍入到最近值，遇到中点时远离零 |
| `vcvtm` | 转换为整数，向负无穷舍入 |
| `vcvtn` | 转换为整数，舍入到最近值，遇到中点时取偶数 |
| `vcvtp` | 转换为整数，向正无穷舍入 |
| `vcvtx` | 转换为较低精度，舍入到最近值，遇到中点时取奇数 |
| `vcvt_n` | 转换为定点数或从定点数转换，向零舍入 |
| `vrnd` | 舍入到整数，向零 |
| `vrnda` | 舍入到整数，遇到中点时远离零 |
| `vrndi` | 舍入到整数，使用当前舍入模式 |
| `vrndm` | 舍入到整数，向负无穷 |
| `vrndn` | 舍入到整数，遇到中点时取偶数 |
| `vrndp` | 舍入到整数，向正无穷 |
| `vrndx` | 精确舍入到整数 |

### 加载和存储

| 操作 | 说明 |
| --- | --- |
| `vld1` | 从内存加载向量 |
| `vst1` | 将向量存储到内存 |
| `vget_lane` | 获取向量元素 |
| `vset_lane` | 设置向量元素 |

### 排列

| 操作 | 说明 |
| --- | --- |
| `vext` | 从两个向量中提取向量 |
| `vtbl1` | 查找表向量 |
| `vtbx1` | 查找表向量扩展 |
| `vqtbl1` | 查找表向量 |
| `vqtbx1` | 查找表向量扩展 |
| `vrbit` | 反转位顺序 |
| `vrev16` | 反转 16 位半字中的元素 |
| `vrev32` | 反转 32 位字中的元素 |
| `vrev64` | 反转 64 位双字中的元素 |
| `vtrn1` | 转置向量（主向量） |
| `vtrn2` | 转置向量（次向量） |
| `vzip1` | 交错合并向量（主向量） |
| `vzip2` | 交错合并向量（次向量） |
| `vuzp1` | 解交错向量（主向量） |
| `vuzp2` | 解交错向量（次向量） |

### 加密

| 操作 | 说明 |
| --- | --- |
| `CRC32` | 循环冗余校验（CRC）计算。 |
| `SHA1` | SHA1 计算。 |
| `SHA256` | SHA256 计算。 |
| `AES` | AES 计算。 |

### 杂项

| 操作 | 说明 |
| --- | --- |
| `vsqrt` | 平方根 |
| `vdot` | 点积 |
| `vdot_lane` | 点积 |

## 相关资源

- [[03-处理器特定SIMD扩展]]

---

## 文档导航

- 上一页：[[03-处理器特定SIMD扩展]]
- 目录：[[00-Burst Intrinsics]]
- 下一页：[[13-Burst Editor窗口参考]]
