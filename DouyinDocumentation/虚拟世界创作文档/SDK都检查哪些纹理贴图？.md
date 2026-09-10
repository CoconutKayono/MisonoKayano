问：SDK都计算哪些纹理贴图的引用？
答：SDK内检查如下纹理贴图的引用。
| 组件 | 检查项 |
| --- | --- |
| Renderer | MeshRenderer  <br>  <br> * 材质球 |
|  | SkinnedMeashRenderer  <br>  <br> * 材质球 |
|  | SpriteRenderer  <br>  <br> * Sprite 资源 <br> * 材质球 |
| UI <br>  | Image <br>  <br> * Source Image 资源 <br> * 材质球 |
|  | RawImage <br>  <br> * Source Image 资源 <br> * 材质球 |
|  | TextMeshPro - Input Field <br>  <br> * Transition///Sprite Swap---Highlighted Sprite/Pressed Sprite/Selected Sprite/Disable Sprite |
|  | TextMeshPro - Text <br>  <br> * 材质球 |
|  | Text <br>  <br> * 材质球 |
|  | Dropdown - TextMeshPro <br>  <br> * Transition///Sprite Swap---Highlighted Sprite/Pressed Sprite/Selected Sprite/Disable Sprite |
| 特殊渲染组件 <br>  | LineRenderer <br>  <br> * 材质球 |
|  | TrailRenderer <br>  <br> * 材质球 |
|  | DecalProjector <br>  <br> * 材质球 |
| 地形和环境 | Terrain <br>  <br> * 地形贴图 |
|  | Tree（Create->Tree） <br>  <br> * 材质球 |
| Douyinscript | 各组件按钮贴图 |
| 环境组件 | * 立方体贴图 <br> * 天空盒 <br> * 镜头光晕 <br> * LUT贴图 <br> * 后处理材质球 |

