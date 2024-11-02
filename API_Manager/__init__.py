from .apim import apim  ,api , jsonname , rdata , wdata ,driver

from nonebot.adapters.onebot.v11 import(
    MessageSegment
)
from nonebot.matcher import Matcher
from plugins.CubDragon_Engine import engine_init
cls_t = engine_init()

async def apim_command_init():
    cls_t.add_command([textapi], "#api调试桥" ,perm=["root"])
    cls_t.add_command([apitext], "#apitext" ,perm=["root"])

cls_t.add_init(apim_command_init, "apimanager")

@driver.on_shutdown
async def _():
    data = rdata(jsonname)
    data["cookies"] = apim.getcookies()
    wdata(jsonname,data)

async def textapi(
    matcher:Matcher,
    data:dict,
    **other
):
    apiname=data[3]
    apidata = data[4] if len(data) >=5 else ""
    apidata = apidata.replace("&amp;",r"&")
    resp ,resptype = await apim.apirun(apiname,paramstr=apidata)
    if resptype == ["image","octet-stream"]:
        msg = MessageSegment.image(resp)
    else:
        msg = str(resp)
    await matcher.send(msg)

async def apitext(
    matcher:Matcher,
    data:dict,
    **other
):
    apiurl = data[1]
    apiurl=apiurl.replace("&amp;",r"&")
    resp ,_,resptype = await api(method="get",url=apiurl)
    if resptype in ["image","octet-stream"]:
        msg = MessageSegment.image(resp)
    else:
        msg = str(resp)
    await matcher.send(msg)