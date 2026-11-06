# URP 深度图解：生成记录

使用方式：内置 image_gen 工具；未使用 CLI/API 回退。两张图片用于概念讲解，不按精确几何比例绘制。已人工检查文字、坐标、投影关系和公式。

笔记中的资产目录：`E:/MisonoKayano/MisonoKayano/Notes/Unity Shader/Games101学习笔记/URP-depth-images/`。

## 图 1：轴向深度与直线距离

文件：`axial-depth-vs-distance.png`

最终生成提示词：

```text
Use case: scientific-educational.
Asset type: a high-resolution Chinese textbook diagram for a Unity URP Markdown learning note. Create ONE landscape diagram, approximately 1536 by 1024. Clean ivory-white background, crisp navy typography, teal axial distances, orange sightline distances, muted purple construction lines; restrained textbook design, no decorative objects. Text must be sharp simplified Chinese. Title: "轴向深度 ≠ 到相机的直线距离". Subtitle: "俯视图 · 相机前方是 −Z，图中向右；横向 +X，图中向上".
Required exact geometry: a camera optical center O at lower-left, A directly horizontally to the right of O, B vertically above A. Triangle OAB is right-angled at A. OA represents 10 units; AB represents 6 units, so the displayed aspect ratio OA:AB is 10:6. Use near-orthographic flat diagram, NOT perspective illustration. For layout guidance O around (230,700), A around (1070,700), B around (1070,196). All coordinates are illustrative, leave room for labels.
Draw teal horizontal OA and a teal horizontal dimension line underneath it labeled "轴向深度 E = 10". Draw orange diagonal OB, accurately ending at B, labeled "直线距离 |OB| ≈ 11.66" offset above the line with no overlap. Draw purple dashed AB and a small right-angle marker at A. Extend the vertical line through A and B faintly and label "同一深度平面 z = −10" to its right; describe this as the top-view intersection of the plane, do not make it look like a ray. AB label "横向偏移 6". Label origin "相机 O" with a small camera icon to the LEFT of the origin. Label A "A (0, 0, −10)" below-right; label B "B (6, 0, −10)" above or right. Faint horizontal forward arrow extends past A labeled "相机前向 −Z". O is z=0, NOT near clip plane.
At bottom place two uncluttered summary boxes: teal box "A、B 的轴向深度相同：E = 10"; orange box "直线距离不同：|OA| = 10，|OB| ≈ 11.66". Add a small footer "沿前向量深度，沿视线量距离". No invented numbers, no other formulas, no watermarks, no arrows that end at the wrong point. This is a conceptual schematic, not measured scene data.
```

## 图 2：射线与深度重建

文件：`ray-depth-reconstruction.png`

最终生成提示词：

```text
Use case: scientific-educational.
Asset type: a high-resolution Chinese textbook schematic for the same Unity URP Markdown guide. Create ONE landscape diagram approx 1536 by 1024. Ivory-white background, crisp navy simplified-Chinese text, teal correct target/depth, orange ray, red wrong point, muted dashed construction lines. Use a sparse mathematically accurate textbook layout, NOT a perspective illustration.
Title "为什么 normalize(ray) × eyeDepth 会走不够远？"
Subtitle "透视相机 · 眼空间深度 E = 10"
Main flat top-view geometry: camera O at lower-left. Horizontal rightward direction is −Z (camera forward); up is +X. One orange ray from O goes diagonally upper-right. Correct target P=(6,0,−10), on this ray, at horizontal distance 10 and vertical displacement 6 from O. Wrong point Q must lie ON THE SAME RAY BETWEEN O AND P, at 0.857493 of the O-to-P segment: Q≈(5.145,0,−8.575). Thus Q is left and below P. Do not put Q at same horizontal coordinate or same height as P. Example pixel placement O(190,670), P(1090,130), Q(962,207). Show clear green/teal dot P with callout "正确位置 P" and "(6, 0, −10)"; red dot Q with callout "错误位置 Q". Separate callouts with thin leader lines so no collision.
From Q drop a red dashed VERTICAL perpendicular to the horizontal forward axis; from P drop a teal dashed VERTICAL perpendicular to that axis. Each endpoint gets a small right-angle marker. Under horizontal axis, dimension O to Q's foot "错误的轴向深度 ≈ 8.57", dimension O to P's foot on a separate lower level "目标轴向深度 = 10". Along the diagonal segment OQ put label "沿单位射线走 10". Mark diagonal QP segment visibly as remaining distance, with small label "还没到目标平面". Vertical line through P is faint and labeled "z = −10". Draw small camera icon left of O and label "相机 O". Forward arrow on baseline "−Z".
Bottom two formula cards, exact text: red card "错误：normalize(rayVS) × E"; teal card "正确：rayVS × (E / (−rayVS.z))". Footer "E 是前向投影长度，不是沿射线的路程". Render formulas legibly and keep all text within margins. No arbitrary extra symbols, no duplicate points, no watermarks. Conceptual diagram, not an empirical plot.
```

