
自定义脚本文件夹路径下必须要创建index脚本，否则在上传世界时，将会报错！

Douyin Script Loader组件中Custom Scripts Folder字段指向文件夹是创作者可自定义的lua代码目录。
具体使用方法如下：
1. 在Unity3D Project视图中右键创建一个文件夹。
2. 在文件夹中创建一个lua文件命名为index.lua。
3. 拖拽创建的文件夹到DouyinScriptLoader的Inspector面板自定义脚本文件夹字段中。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/31dbe3650bff47f48ea0a02cbf7d2549~tplv-goo7wpa0wc-image.image" width="453px" /></div>

当场景加载完成后官方Module Script目录下的index.lua会被先执行，之后自定义目录下的index.lua 会被执行。在自定义脚本目录下组织你的lua文件并通过index.lua加载执行它们。
在Module Scripts目录中通过require函数来引入目录中的文件代码。假设目录结构如下图所示。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/05e9bbb2c3fd42b3816adb6b5ccbc1dd~tplv-goo7wpa0wc-image.image" width="455px" /></div>

```Lua
-- Custom Scripts Folder index.lua

local Config = require("Config/GameConfig.lua");

require("ItemSystem/ItemManager.lua");

print("use config ",Config);
```

除了在index.lua中使用require导入需要的lua文件以外，也可以使用相对路径来加载。以下面代码为例，在ItemManager文件中使用Config文件夹下的GameConfig文件定义的配置数据。
```Lua
-- Custom Scripts Folder ItemSystem/ItemManager.lua

-- Use relative path to import config file
local Config = require("../Config/GameConfig.lua");

_G.ItemManager={}

function ItemManager:GetItem(id)
  
end

return ItemManager;
```


使用相对路径时，路径是基于脚本自身所在的目录来判断加载路径的，比如：A脚本和B脚本都放在一个目录下，其中A脚本是module script，B脚本中要引入A脚本，那么B脚本中只需要` require “A” `即可，不需要再编写完整的路径。

