# nonebot-cubplugins
一些稀奇古怪的想法uwu, 不打算发布插件商城

如果你发现了这里, 也欢迎你下载使用owo

不过我不会对此存储库内容进行维护, 因为我用着都能用


# nonebot-plugin-立创商城搜索解析器
顾名思义,解析立创商城的搜索结果

依赖前置: lxml

# nonebot-plugin-APIManager
一站式管理api与cookie的插件

依靠aiohttp

# nonebot-plugin-Oops
nonebot插件运行过程中错误捕获

自动捕获:捕获来自nonebot事件进程的exception属性(只有错误描述)

修改代码:通过try except获取完整的exception属性来进行渲染错误日志

修改代码2:提供了一个装饰器来捕获,不过不能和 @xxx.headle共存,否则nonebot会因获取不到函数参数表而报错

依靠aiohttp