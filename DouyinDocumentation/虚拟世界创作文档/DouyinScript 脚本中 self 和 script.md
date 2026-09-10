问：DouyinSript 脚本中self和script怎么使用？
答：在Lua脚本中，经常会遇到self和script的调用

* **`self` : **指的是Unity的DouyinScript脚本，在调用官方API的时候，需要使用 `self.变量名` 或`self:函数名` **** 
   * **`self.gameObject` ：**访问当前脚本关联的GameObject对象
   * **`self:HasOwnership()`：**查询当前DouyinActor是否拥有该对象的主权
* **`script`：**DouyinScript中引用的Lua脚本对象，需要调用Lua脚本的函数时，需要使用 `DouyinScript.script.函数名` **** 
