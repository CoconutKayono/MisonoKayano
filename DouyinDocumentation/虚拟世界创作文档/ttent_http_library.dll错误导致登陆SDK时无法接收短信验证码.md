问：导入SDK后，在登陆抖音账号时，无法接收到手机验证码，同时Unity控制台中报错，显示找不到ttent_http_library.dll
答：该报错截图如下
<div style="text-align: center"><img src="https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/8904fea98e75472e9695a0d177ef57dd~tplv-goo7wpa0wc-image.image" width="1096px" /></div>

解决方案是按照路径找到该dll，然后使用depends打开这个dll文件
