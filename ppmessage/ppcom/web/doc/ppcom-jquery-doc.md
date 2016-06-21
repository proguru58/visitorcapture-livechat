# Web SDK

PPMESSAGE提供了丰富的SDK供开发者选择和使用，Web SDK主要针对PPMESSAGE注册用户的Web应用系统集成PPMESSAGE系统应用内在线客服系统用户端界面的接口。

## PPMESSAGE简介

PPMESSAGE是一个即插即用的云客户服务系统。依托其在线云系统，为网站和移动应用提供统一的在线客服系统。PPMESSAGE提供用户端嵌入代码、客服座席端应用以及PPMESSAGE平台服务接口。用户端嵌入代码支持 Web，Android，iOS，可以快速集成到网站和手机应用之中；平台服务接口是PPMESSAGE开放的服务的访问最底层协议，使用这些接口可以用来与PPMESSAGE进行深度集成，例如同步用户数据，创建和管理客服分组、获取历史消息等；客服座席端应用由PPMESSAGE单独提供，支持各种PC平台（Windows，Mac OS X，Linux），主流浏览器（IE、Safari、Chrome、Firefox），主流移动操作系统（Android、iOS、Windows Phone）；座席人员通过使用座席客户端进行在线服务。另外通过PPMESSAGE的后台服务管理配置可以管理服务团队的欢迎信息，离线信息，用户端界面风格，消息分流策略等。

## 名词解释
在PPMESSAGE系统及其文档描述中出现以下名词，其所指的含义，这些含义可能与常识不同。为了避免混淆，在这里进行列举并解释。

### 注册用户

在PPMESSAGE官网完成注册流程，即成为PPMESSAGE的注册用户。

### 客服团队

客服团队是由注册用户在注册过程中创建的，其目的是为网站或APP提供在线客服功能。客服团队由管理员和客服共同组成。

### 管理员

管理员是客服团队的管理者。在这里，我们默认PPMESSAGE的注册用户就是客服团队的管理员。

### 客服

客服是由管理员在客服团队中创建的，是客服团队客服工作的主要承担者，其职责是根据管理员的要求做好网站或app的客服工作。

### 用户

即网站或APP的用户，也是客服团队的服务对象（如，某电子商务商城的买家）。用户可以在网站或APP向客服团队咨询问题，然后由客服团队来解答其提出的问题。

## 集成与使用

Web SDK帮助用户在Web端集成PPMESSAGE的客户端界面，通过Web SDK可以设置当前浏览网页的用户信息。

### 配置集成
在申请到`KEY`和`SECRET`之后，可以选择两种方案进行Web集成。

#### 代码嵌入

```javascript
window.ppSettings = {
	//appKey，必填字段
	app_key: "xxxxxx",
	//appSecret，必填字段
	app_secret: "xxxxxx"
}
<script>(function(){var w=window,d=document;function l(){var a=d.createElement("script");a.type="text/javascript";a.async=!0;a.src="https://ppmessage.cn/ppcom/assets/pp-library.min.js";var b=d.getElementsByTagName("script")[0];b.parentNode.insertBefore(a,b)}w.attachEvent?w.attachEvent("onload",l):w.addEventListener("load",l,!1);})()</script>
```

#### 文件加载
如果使用API获取PPMESSAGE更多功能，请使用直接Javascript脚本文件加载方法。从而能够确保使用任何PPMESSAGE SDK接口之前PPMESSAGE脚本已经加载完毕。

```javascript
<script src="https://ppmessage.cn/ppcom/assets/pp-library.min.js" type="text/javascript"></script>
```

#### 使用在线工具
使用在线工具集成，即选择了代码嵌入的集成方法。


### 更多配置和API

- 配置选项
在`window.ppSettings`中还可以进行其它配置，来更方便的创建和显示PPMESSAGE的客服指示图标，如下所示：

```javascript
<script>
window.ppSettings = {
	//appKey，必填字段
	app_key: "xxxxxx",
	//appSecret，必填字段
	app_secret: "xxxxxx",
	
    //第三方用户email，可选字段，不填的话，将会以匿名用户身份收发信息
	user_email: "somebody.web@ppmessage.cn",
    //用户姓名，可选字段，在客服端会显示此处填写的用户姓名
    user_name: "张三",
    //用户头像，可选字段，在客服端会显示此处填写的用户头像
    user_icon: "http://xxxx.com/avatar.png",
	//语言配置，可选字段，zh-CN:"中文"，en:"英文", 默认为中文
	language: "zh-CN",

	//界面配置，可选字段
	view: {
        //聊天泡泡图标距离网站最底侧的间距，默认为"20px"
        launcher_bottom_margin: "20px",
        //聊天泡泡图标距离网站最右侧的间距，默认为"20px"
        launcher_right_margin: "60px",
        //是否显示右下角的PPMESSAGE聊天泡泡图标
        launcher_is_show: true
	}
};
</script>
```

- 启动`PPMESSAGE`

```javascript
PP.boot({
    app_key: app_key,
    app_secret: app_secret
}, function(isSucess, errorCode) {
   //回调函数
});
```

- 显示`PPMESSAGE`消息面板

```javascript
/**
 * @description 显示 PPCom
 * @return 无返回值
 */
PP.show();
```

- 隐藏`PPMESSAGE`消息面板

```javascript
/**
 * @description 隐藏 PPMESSAGE
 * @return 无返回值
 */
PP.dismiss();
```

- 更新`PPMESSAGE`

```javascript
/**
 * @description 更新 PPMESSAGE
 * @return 无返回值
 */
PP.update({
    app_key: app_key,
    app_secret: app_secret,
    user_email: xxx@qq.com
});
```

**说明：**参数可选，不填写参数的话，则默认使用`window.ppSettings`来更新`PPMESSAGE`，当重新设置`window.ppSettings.user_email`的时候，必须调用此函数来更新`PPMESSAGE`

- 关闭`PPMESSAGE`

```javascript
PP.shutdown();
```

**说明：**当用户注销的时候，可以调用此接口销毁用户数据，此接口将会移除掉`PPMESSAGE`

### 错误码

当`window.ppSettings`的配置信息有误而导致`PPMESSAGE`无法正常显示的时候，`PPMESSAGE`会在浏览器的`console`中打印出相应的错误信息和错误码。

下面是所有可能出现的错误码所对应的错误描述信息。

Error Code(错误码) | Error description(错误描述)
----------------- | -------------------------------
10000             | appKey 或者 appSecret 填写有误
10001             | 找不到 user_email 对应的用户，可能未注册或者邮箱填写有误
10002             | PPMessage 暂时还无法运行在 IE9 或以下版本中
10003             | 服务不可用
10004             | user_email 不是正确的邮箱的格式

## 一键安装工具简介

一键安装工具是个代码安装工具，如果您不清楚如何手动将我们的应用集成到您的网站，您可以选择使用一键安装工具，通过填写一些必要的参数，我们来帮助您将应用集成到您的网站，实现一键安装。

>安装需要您的网站服务器开启FTP或者SSH服务，需要提供FTP或SSH账号密码，您可以与您的网站管理员取得联系并获得这些。
>
>安装前请您联系您的网站管理员做好备份

## 一键安装工具使用
首先登录我们的网站，点击应用集成下面的方案二：一键安装 按钮，如下图所示：

![team integrate](img/autoinstall_step_1.png)

点击后您将看到一键安装面板。填入正确参数后点击连接按钮，如下图所示：

![team manualinstall](img/autoinstall_step_2.png)

可以看到一共需要6个参数，分别代表：

登录方式: 登录您服务器的方式(FTP或者SSH, 默认FTP)

主机: 登录您服务器的主机地址(IP地址或者虚拟主机地址)

用户名: 登录您服务器的账户名

密码: 登录您服务器的密码

团队 Key: 使用PPMessage服务的key值 (团队Key，系统自动为您填写)

团队 Secret: 使用PPMessage服务的secret值 (团队Secret，系统自动为您填写)

正确连接到服务器后，您将看到服务器下的文件，选择您想添加插件的网页

![team script install](img/autoinstall_step_3.png)

选择完毕后请点击开始安装按钮。如下图所示：

![begin install](img/autoinstall_step_4.png)

完成安装会弹出安装成功对话框，至此安装完成。如果仍然有疑惑请联系我们客服

>安装速度主要取决于您服务器网络状况的好坏。

>如果您不确定想安装的文件夹或者文件，您可以考虑直接在确定网站所在的根目录下点选文件夹，我们将对整个文件夹安装。
