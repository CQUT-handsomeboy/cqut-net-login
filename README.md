# CQUT校园网登录脚本

## 🐸有待解决的问题

1.  只有在使用JavaScript通过JSEncrypt加密的原密文作为密码项时才能登录，使用Python的pycryptodome库作同样复刻同样操作时却提示错误。

2.  仅仅解决了登录问题，还需要进一步选择运营商，本代码在运营商选择处报错。

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

## 📝问题2 参考思路

由于数据包需要双重URL编码，但是requests会自动编码一层，所以只需要编码一次，此前手动编码了两次，所以错误，使用`netcat`定位问题所在。

但这并没有解决关键问题，认为是登陆成功后保持登陆状态的cookies没有被使用起来，于是无法维持服务端知晓客户端登陆状态，于是使用客户端的cookies进行后续操作，但仍无济于事。

## 🤔逆向思路与工具推荐

1.  `Burp Suite Professional`分析数据包

2.  受到`洛卡尔物质交换定律`的启发，在所有请求-响应中查找你账号的敏感信息

3.	`Netcat`可分析你的数据包构造与原始数据包的差异情况。