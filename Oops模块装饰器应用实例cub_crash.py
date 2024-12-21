from nonebot import on_command
from nonebot.params import CommandArg , Matcher
from nonebot_plugin_Oops import CubbotError  , oops_listen

oops_text = on_command(
    "cubcrash"
)

@oops_text.handle()   #直接在此添加装饰器nonebot会报错无法获取函数参数表
async def crash_text(
    matcher: Matcher,
    data: list = CommandArg()
):
    @oops_listen()
    async def run():
        msg = "这是一个手动触发的错误,可以忽略"
        if len(data) != 0 : msg = data[0]
        raise CubbotError(msg)
    
    
    return await run()