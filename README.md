# 

[![SVG Banners](https://svg-banners.vercel.app/api?type=rainbow&text1=重庆理工大学校园网登录脚本🌈&width=800&height=200)](https://github.com/Akshay090/svg-banners)

## 🤔介绍

截止到2025年4月3日，这个程序**首次测试通过**。

## 🚀快速开始

创建一个`.env.json`文件，并填入你的信息。

```jsonc
{
    "account":"<你的学号>", 
    "password":"<你的密码>", // 没用，因为没搞定加密
    "passwordEncrypted":"<你的密码经过公钥加密后的密文>",
    "service":"<你想登录的运营商>" // 中国移动 / 中国电信
}
```

> [!NOTE]  
> 目前的版本暂时没能成功使用python复刻JSEncrypt的RSA加密，所以必须设置passwordEncrypted项，即手动使用公钥（这个公钥是写死的，详见下文）加密你的密码得到密文。**如果你对剩下的这个问题很感兴趣，欢迎PR!**

# 💡升级后的登录逻辑

校园网升级后采用CAS单点登录流程：用户访问校园网时重定向至统一认证中心（如办事大厅），完成认证后返回服务票据（ST），校园网系统验证票据后授权访问。

## 🐸有待解决的问题

1.  只有在使用JavaScript通过JSEncrypt加密的原密文作为密码项时才能登录，使用Python的pycryptodome库作同样复刻同样操作时却提示错误。

## 📝问题1 参考代码

源码：（源码发现在登录页的Script标签中，这个页面使用了Vue2编写，源码未做混淆，逆向较为容易）

```javascript
let encryptor = new JSEncrypt()

// 注意公钥是暴露在源代码中，写死的
encryptor.setPublicKey(
	'-----BEGIN PUBLIC KEY-----'+
	'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDACwPDxYycdCiNeblZa9LjvDzb'+
	'iZU1vc9gKRcG/pGjZ/DJkI4HmoUE2r/o6SfB5az3s+H5JDzmOMVQ63hD7LZQGR4k'+
    '3iYWnCg3UpQZkZEtFtXBXsQHjKVJqCiEtK+gtxz4WnriDjf+e/CxJ7OD03e7sy5N'+
    'Y/akVmYNtghKZzz6jwIDAQAB'+
    '-----END PUBLIC KEY-----'
)

// 使用RSA进行分段加密，存储成列表然后返回为序列化后的JSON字符串
function getSecretParam (p)  {
	let arr = []
	let maxIndex = 0
	for (let i = 0; i <= p.length; i++) {
		if ((i + 1) % 30 === 0) {
			arr.push(encodeURI(encryptor.encrypt(p.substring(maxIndex, i))))
			maxIndex = i
		}
	}
	maxIndex !== p.length &&
	arr.push(
		encodeURI(encryptor.encrypt(p.substring(maxIndex, p.length)))
	)
	return JSON.stringify(arr)
}

```

Python复刻版本详见[encrypt.py](encrypt.py)

## 🔧工具推荐

1.  `Burp Suite Professional`分析数据包

2.	`burp-requests`插件可将请求数据包拷贝为`python` `requests`脚本。

3.	`Netcat`可分析你的数据包构造与原始数据包的差异情况。

# 📚参考资料

> 我们学校是锐捷Portal 运营商应该是走了遭hash的 具体哪个没看过 不过都是通用的 可以Github找找 
>
> __DriveFLY

[IYATT关于CQUT校园网的博客](https://blog.iyatt.com/?p=6815)

[CAS单点登录原理](https://blog.csdn.net/ban_tang/article/details/80015946)

[集美大学锐捷ePortal Web 认证的登录脚本](https://github.com/callmeliwen/RuijiePortalLoginTool)

[Python实现RSA(jsencrypt)加密的两种方式](https://blog.csdn.net/wangzhuanjia/article/details/128382024)