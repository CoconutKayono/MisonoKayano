Douyin Script Loader组件中Douyin Scripts Folder字段指向的文件夹是官方Module Script目录。
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8ae9f342e7924084b7fd11018ade7cbc~tplv-goo7wpa0wc-image.image" width="738px" /></div>

如上图在ModuleScript目录存在一个index.lua文件。该lua文件会在Douyin world 场景加载完成后执行，如下是index.lua文件的代码部分。可以在该文件中按相对路径引用其他模块：
```Lua
-- Load Global Module

list = require "Common.ParaList"

require "Common.ParaEvent"
```

目前Douyin Scripts Folder包含了Douyin List和Douyin Event 两个lua文件，其中Douyin List.lua 包含了一个链表的实现，可以通过查看Douyin List.lua来了解如何使用。
Douyin Event.lua实现事件的监听和分发，以下是Douyin Event 提供组件 event 的用法示例：
```Lua


local onClicked = event("evtName");

function Start()
    print("register onClicked event listener");
    local evtListener = onClicked:CreateListener(function()
        print("onClicked triggered");
    end);
    onClicked:AddListener(evtListener);
  
          -- if don't want lisen then you can remove it
    -- onClicked:RemoveListener(evtListener);
end

function OnTestEvent()
    -- fire event
    onClicked();
end
```

可以根据自己的需要增加或修改SDK官方目录中的lua文件，请注意备份修改，因为在SDK升级时该目录下的文件可能会被替换或修改。
