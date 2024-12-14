import asyncio
from nonebot_plugin_htmlrender import template_to_pic
from pathlib import Path
import traceback
import sys
from nonebot.message import run_postprocessor
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import (
   Bot,  MessageEvent ,MessageSegment,
   GroupMessageEvent
)
from nonebot.matcher import Matcher
from nonebot.exception import FinishedException,RejectedException
from loguru import logger

from nonebot import get_driver
from pydantic import BaseModel
from typing import List, Literal, Optional, Set, Tuple
class config_util(BaseModel):
    superusers: Set[str] = set()
    console: Optional[int|str] = None   #控制台群聊
    cubplugin_datadir : str=""
config: config_util = config_util.parse_obj(get_driver().config.dict())



class CubbotError(Exception):
    """Cubdragon runtime error"""
    
def oops_listen(  ):
    def decorator(oopslisten_func):
        async def wrapper(*args, **kwargs):
            try:
                run_result = await oopslisten_func(*args, **kwargs)
                return run_result
            except:
                matcher = kwargs.get('matcher',Matcher)
                exc_type, _, _ = sys.exc_info()
                if exc_type not in [FinishedException,RejectedException]:
                    img = await crash_oops()
                    await matcher.send(MessageSegment.image(img))
                else:
                    raise exc_type
        return wrapper
    return decorator


async def crash_oops(err_values:Exception = None):
    if err_values == None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        data = traceback.format_exc()
        error = traceback.format_exception(exc_type, exc_value, exc_traceback)[-1]
        error_values = error.split(":",1)[-1]
        data = data.replace('\n','<br>')
    else:
        error_values=err_values
        newline_char = '<br>'
        try:
            data = f'{newline_char.join(err_values.args)}'
        except:
            data = str(err_values.args)
    template_path = str(Path(__file__).parent / "_HTML_template")
    htmlimage = await template_to_pic(
                template_path=template_path,
                template_name="Oops.html",
                templates={
                    "error":error_values,
                    "data": data,
                },
                type="jpeg")
    return htmlimage

@run_postprocessor
async def post_run(event: MessageEvent, matcher,e: Exception) -> None:
    bot:Bot = get_bot()
    img = await crash_oops(e)
    envstr = '私聊'
    envid =event.user_id
    if isinstance(event,GroupMessageEvent):
        envstr = '群'
        envid = event.group_id
    try:       
        if config.console != None:
            await bot.call_api("send_group_msg",group_id = config.console ,
                    message=f"在{envstr}[{envid}]遇到致命错误!"+MessageSegment.image(img)
                )
        await asyncio.sleep(0.3)
        await matcher.send("遇到致命错误,详细信息已经发送至BOT控制台")
    except:
        await matcher.send("错误,Oops模块无法解析报错,请查看控制台")
        raise CubbotError(f"遇到致命程序错误! -{str(e)}")
    else:
        logger.opt(colors=True).warning(
            f"[Oops_debug] 在{envstr}[{envid}] 报错捕获 {str(e)} "
        )