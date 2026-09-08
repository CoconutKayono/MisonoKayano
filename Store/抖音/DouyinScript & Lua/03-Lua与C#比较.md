---

---
---

Douyin World SDK使用Lua作为脚本开发语言以支持玩家及创作者动态添加游戏世界和玩法内容。Douyin World 使用UnityEngine进行开发构建。 Unity引擎使用C#作为开发语言， Douyin World 将UnityEngine 提供的API 进行了到lua的映射。 Douyin World使用C#的函数签名方式提供了API文档，消息通知函数采用类型标注的lua函数声明方式。​

## 静态函数​

例如: 类型 [UnityEngine.GameObject](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/GameObject.html) 查看Unity官方文档中有4个静态方法如下​

| [CreatePrimitive](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/GameObject.CreatePrimitive.html) ​              | 使用原始网格渲染器和适当的对撞机创建游戏对象。​            |
| ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| [Find](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/GameObject.Find.html) ​                                    | 通过名称找到游戏对象并将其返回。​                   |
| [FindGameObjectsWithTag](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/GameObject.FindGameObjectsWithTag.html)​ | 返回一系列有效的游戏对象标记标签。如果找不到游戏对象，则返回空数组。​ |
| [FindWithTag](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/GameObject.FindWithTag.html)​                       | 返回一个主动游戏标签标签。如果找不到游戏对象，则返回null。​    |
```cs
// 他们的声明形式为 :​
public static GameObject CreatePrimitive(PrimitiveType type); ​
public static GameObject Find(string name); ​
public static GameObject\[] FindGameObjectsWithTag(string tag); ​
public static GameObject FindWithTag(string tag); ​
```

对于函数声明有static标注的函数 ==在lua中使用类型加"."的调用方式。==​

```lua
function Start()​
	-- call class static function​
	local objFinded = UnityEngine.GameObject.Find("ObjectName");​
end​
```
​

## 成员函数​

还是以[UnityEngine.GameObject]为例，如下成员函数。​

| [GetInstanceID](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/Object.GetInstanceID.html)​   | 获取对象的实例ID。​                              |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| [GetComponent](https://docs.unity3d.com/2021.3/Documentation/ScriptReference/GameObject.GetComponent.html)​ | 如果游戏对象附加了一个类型的组件，则返回类型的组件，如果没有，则返回null。​ |

以上成员函数属于GameObject类型的实例化对象。 必须要先拿到或者创建对象实例后才能调用。==注意成员函数用":"号调用。==​

```lua

function Start()​

	-- 调用成员函数​
	
	-- 获取类实例对象​
	local objFinded = UnityEngine.GameObject.Find("ObjectName");​
	
	if objFinded then​
		-- 如果找到则打印其实例ID
		print(string.format("object instance id:%d",objFinded:GetInstanceID() ));​
	end​
	
	-- 如果没找到，则创建新的实例
	local newObj = UnityEngine.GameObject.CreatePrimitive(UnityEngine.PrimitiveType.Plane);​
	print(string.format("newObj instance id:%d",newObj:GetInstanceID() ));​

end​
```
​

## 使用C#类型

C#语言使用命名空间来避免类型名称冲突，lua没有命名空间的概念，在Douyin World 里lua用表来模拟命名空间，将不同命名空间下的C#类型放到了不同的表中以避免命名冲突。 如GameObject属于UnityEngine命名空间， NGUI中的Button属于UnityEngine.UI 命名空间​

​
```lua
function Start()​
	-- create new GameObject, below is equal C#'s call. "var obj = new UnityEngine.GameObject("buttonObj"); "​
	local obj = UnityEngine.GameObject("buttonObj");​
	
	-- add a unity component to it ​
	local buttonInst = obj:AddComponent(typeof(UnityEngine.UI.Button));​
	buttonInst.onClick:AddListener(function()​
	print("buttonInst clicked");​
	end);​
end​

​

-- Or you can simplify the type lookup​

local GameObject = UnityEngine.GameObject;​
local Button = UnityEngine.UI.Button;​
function Start()​
local obj = GameObject("buttonObj");​
local buttonInst = obj:AddComponent(typeof(Button));​
buttonInst.onClick:AddListener(function()​
	print("buttonInst clicked");​
end);​

end​​

```

## 属性对比：静态属性与非静态属性

C#中属性的访问，静态属性属于类型，用类型加"."号访问， 非静态属性用实例对象加"." 号访问。​

```lua
function Start()​

	-- check network is ready, the 'isNetworkSettled' is static property​
	if DouyinNetService.isNetworkSettled then​
		print("netowrk is settled");​
	end​
	-- access none static property​
	local player = DouyinPlayerService.GetPlayerById(1001);​
	if player then​
		print("player id property ",player.playerID);​
	end​

end​
```
​
## 数组对比​

如下C#中数组的使用​

```cs
public void Awake()​
{​
	GameObject[] objs = GameObject.FindGameObjectsWithTag("Actor");​
	for(int i=0; i<objs.Length; ++i)
	{​
		Debug.Log($"obj id:{objs[i].GetInstanceID()}");​
	}​
}​
```
​
lua中使用C#导出的数组,C#的数组是以索引0开始。

```lua

local GameObject = UnityEngine.GameObject;​

function Awake()​
	local objs = GameObject.FindGameObjectsWithTag("Actor");​
	for i=0,objs.Length-1 do​
	print("obj id:",objs[i]:GetInstanceID());​
	end​
end​
```

​

​