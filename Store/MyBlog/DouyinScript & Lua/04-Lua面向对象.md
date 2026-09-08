
```lua
--[[

基类：BaseClass

用途：提供统一的类定义、继承、实例化与删除能力。

  

使用说明：

1. 定义类：MyClass = BaseClass:DefineClass("MyClass" [, SuperClass])

2. 构造函数：function MyClass:__init(a, b) ... end

3. 实例化：local obj = MyClass.New(a, b)

4. 析构函数：function MyClass:__delete() ... end

5. 删除实例：obj:Delete()

6. 继承：传入第二个参数 SuperClass 即可实现方法继承

   - 注意：不自动调用父类 __init/__delete，若需要请在子类显式调用：

     SuperClass.__init(self, ...)

     SuperClass.__delete(self)

  

规则：

1) 不自动级联调用父类 __init/__delete，是否调用父类由子类决定（与 Demo 用法一致）

2) 移除冗余日志，仅保留必要的参数校验

]]

  

local _class = {}

  

-- 继承IBaseClass接口（仅拷贝字段，后续由BaseClass自身实现覆盖）
BaseClass = {}

for k, v in pairs(IBaseClass) do

    if k ~= "__cname" and k ~= "__ctype" then

        BaseClass[k] = v

    end

end

BaseClass.__cname = "BaseClass"

BaseClass.__ctype = ClassType.class

  

-- 定义类

function BaseClass:DefineClass(classname, super)

    assert(type(classname) == "string" and #classname > 0, "BaseClass: 类名必须是非空字符串")

    if super ~= nil then

        assert(type(super) == "table" and super.__ctype == ClassType.class, "BaseClass: 父类必须是合法类")

    end

  

    local class_type = {

        __init = function(_) end,

        __delete = function(_) end,

        __cname = classname,

        __ctype = ClassType.class,

        super = super

    }

  

    local vtbl = {}

    _class[class_type] = vtbl

  

    -- 类表：函数写入虚表，非函数写入类表

    setmetatable(class_type, {

        __newindex = function(t, k, v)

            if type(v) == "function" then

                vtbl[k] = v

            else

                rawset(t, k, v)

            end

        end,

        __index = vtbl

    })

  

    -- 继承：子类虚表 -> 父类虚表

    if super then

        setmetatable(vtbl, { __index = _class[super] })

    end

  

    -- 创建实例

    class_type.New = function(...)

        local obj = {

            _class_type = class_type,

            __ctype = ClassType.instance,

            __cname = classname,  -- 让实例也能访问类名

            _isDestroyed = false

        }

        setmetatable(obj, {

            __index = function(_, k)

                return _class[class_type][k]

            end

        })

  

        -- 调用当前类 __init（不自动级联）

        -- 直接从 class_type 获取，因为它有 __index 指向 vtbl

        local init_func = class_type.__init

        if init_func then

            init_func(obj, ...)

        end

  

        -- 提供实例删除方法

        if _class[class_type].Delete == nil then

            _class[class_type].Delete = function(self)

                if self._isDestroyed then return end

                BaseClass:Delete(self)

            end

        end

  

        return obj

    end

  

    return class_type

end

  

-- 调用当前类的 __init 转发（保留，供需要时使用）

function BaseClass:__init(c, obj, ...)

    assert(c and c.__ctype == ClassType.class, "BaseClass.__init: c 非法")

    assert(obj and obj.__ctype == ClassType.instance, "BaseClass.__init: obj 非法")

    c.__init(obj, ...)

end

  

-- 调用当前类的 __delete 转发（保留，供需要时使用）

function BaseClass:__delete(c, obj)

    assert(c and c.__ctype == ClassType.class, "BaseClass.__delete: c 非法")

    assert(obj and obj.__ctype == ClassType.instance, "BaseClass.__delete: obj 非法")

    c.__delete(obj)

end

  

-- 实例删除（不自动级联，是否调用父类由子类显式处理）

function BaseClass:Delete(self)

    assert(self and self.__ctype == ClassType.instance, "BaseClass.Delete: 仅能删除实例")

    if self._isDestroyed then return end

  

    local c = self._class_type

    if c and c.__delete then

        c.__delete(self)

    end

  

    self._class_type = nil

    self._isDestroyed = true

end
```