# iOS 发布工具
---
编译，打包，发布到服务器， 你只需要一个简单的命令，`ipublish`就能全部帮你搞定这些。
### Install

python 2.7

```
pip install ipublish
```

### Require
1. Xcode 9.0

2. 创建 `ExportOptions.plist` 文件`[Require]`  
	在工程的根目录创建一个`ExportOptions.plist`文件，下图是 	`ExportOptions.plist` 的一个例子，你可以根据自己的情况去修改
	
	![](souces/exportoption.png)
	
	你也可以使用`Xcode`手动构建，在导出的`ipa`文件同目录下，你会发现生成的`ExportOptions.plist`文件，然后拷贝到工程根目录，就可以一劳永逸。
3. 如果你还不太清楚`ExportOptions.plist`相关的信息，你可以配置好`Xcode`证书之后使用
	
	```
	ipublish --init
	```

### Quick Start

1. __publish__

	快速体验
		
	```
	cd /path/of/your/ios/project
	ipublish
	```
	
2. __发布到fir.im__
	
	添加 __fir.im__ 的 __api_token__
	* 如果你想上传到你的fir.im账户上，你需要在[fir.im](fir.im)账户上拿到你的`api_token`，然后把它添加到程序中
	
		```
		ipublish-fir api_token
		```
	* 你也可以直接编译项目，程序依然会记录你的`api_token`，就像这样
	
		```
		ipublish -f api_token
		# or
		ipublish --fir api_token
		```
		
	以上两种方式任选一种，之后的操作，你只需要在你的工程根目录下执行就可以了
	
	```
	ipublish
	```
	
	如果你需要更新你的fir.im 的api_token，
	
	```
	ipublish-fir api_token
	```
	
3. __发布到蒲公英__
	
	[蒲公英](https://www.pgyer.com/doc/view/api)平台的操作，基本和fir.im是一样的，同样是添加蒲公英的 __api_key__
	
	```
	ipublish-pgy api_key
	# or
	ipublish -p api_key
	# or
	ipublish --pgy api_key
	```
	
4. __发布到自己服务器__
	
	如果你希望发布到自己的服务器，你需要自己写上传脚本，然后像下面这样，但目前只支持`python`编写的脚本
	
	```
	ipublish --upload script.py
	```
	当然同一目录下，程序依然会记录你的上传脚本，所以后面的操作，你依然可以使用以下命令一键编译并上传到自己的服务器。
	
	```
	ipublish
	```
	这里有一个自定义服务器的上传脚本例子，你可以参考[upload.py](./upload.py)
	
5. __发布规则__

	1. 默认上传，即不加参数编译上传
		
		```
		ipublish
		```
		* 程序默认优先发布到自定义服务器，如果你使用过自定义服务器的上传脚本，并且目录下有上传脚本的话。
		* 其次会发布到 fir.im 平台，如果不满足自定义服务器发布的条件，并且你程序记录过你 fir.im 账户的`api_token`。
		* 如果前面两个发布的条件都不满足，程序会选择蒲公英平台上传，当然在这之前程序必须记录了你的蒲公英账户的`api_key`。
		* 如果以上条件统统不满足，当然不会上传。
	
	2. __选择发布__
	
		选择上传的前提是程序之前记录过上传相关的信息，如果你满足所有的上传条件，但是不想选择默认的上传方式。
		
		```
		ipublish -f	#上传到fir.im，程序中必须记录过 api_token
		# or
		ipublish -p	#上传到蒲公英，程序中必须记录过 api_key
		```
		为了保证自定义上传的顺利进行，如果你要选择自定义上传，必须传入脚本文件
		
		```
		ipublish --upload upload.py	#上传自定义平台
		# or
		ipublish
		```
	3. __无需发布__
		
		如果你不想发布到任何服务器，只是导出`ipa`，你可以尝试下面的操作
		
		```
		ipublish -b
		```

* 感谢我的朋友[Shayne](https://github.com/FCF5646448)提供给我的意见。*