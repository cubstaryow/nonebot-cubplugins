from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    MessageSegment,
    Bot
)
from nonebot.params import Matcher , RegexGroup
from nonebot import on_regex

from lxml import html
from nonebot import logger

jlcshop = on_regex(
    r"^立创搜索\s+(\S*)"
)
bashapi = "https://so.szlcsc.com/global.html?k="

@jlcshop.handle()
async def jlcshopfunc(
    bot:Bot,
    event:MessageEvent,
    matcher:Matcher,
    args : list = RegexGroup()
): 
    if args[0] != "":
        msg_list =[]
        firstdata=None
        apirun = bashapi + args[0].strip()
        resp ,_,__= await api("get",apirun)
        parsed_html = html.fromstring(str(resp))
        jlcdata = list(parsed_html.xpath(bashxpath))
        if len(jlcdata) == 0:
            await matcher.send("[立创商城解析]\n>搜索无结果")
            return
        else:
            await matcher.send("[立创商城解析]\n>正在解析...请耐心等待...")
        for num in range(1,len(jlcdata)+1):
            xheader = xpathheader.replace("%num%" , f'{num}')
            msg = ""
            for xpathstr in xpathheadstr:

                data:list = list(parsed_html.xpath(xheader+xpathstr))
                if len(data) == 0 : continue
                msg+= f"\n{data[0].strip()}"
                msg = msg.strip()
            for xpathstr in xpathdatastr:
                data0:list = list(parsed_html.xpath(xheader+xpathstr[0]))
                data1:list = list(parsed_html.xpath(xheader+xpathstr[1]))
                data0 = data0 if len(data0)!=0 else [""]
                data1 = data1 if len(data1)!=0 else [""]
                msg+= f"\n{data0[0].strip()}\t{data1[0].strip()}"
                msg = msg.strip()

            image :list = list(parsed_html.xpath(xheader+xpathimagestr))
            imagedata = None
            if (len(image) != 0 ):
                if not image[0].startswith("http") :
                    image = []
                else:
                    try :
                        imagedata = (await api("get",image[0].strip()))[0]
                    except:
                        image = []
            data = (
                ((MessageSegment.image((imagedata))) if len(image) !=0 else "[图片不存在]\n")
                +
                msg.strip()
            )
            if len(jlcdata) == 1 : firstdata = data
            else: await msglist_add(msg_list,data)
            if num>=10:
                await msglist_add(msg_list,"只展示前十条数据,详细请参考网页数据")
                break
        if len(msg_list) == 0:
            await matcher.send(firstdata)
        else:
            await sendfm(msg_list,bot,event,matcher)
            

async def msglist_add( msg_list, data ):
    msg_list.append(
        {
            "type": "node",
            "data": {
                "nickname": "cubV5-立创商城搜索解析器",
                "user_id": 2809973673,
                "content": data
                }
            }
        )

async def sendfm(msg_list,bot,event,matcher):
    if isinstance(msg_list,list):
        await bot.send_forward_msg(group_id=event.group_id, messages=msg_list)  # type: ignore

    else:
        await matcher.finish(msg_list)

xpathheader = '//div[@id="shop-list"]/table[%num%]'

bashxpath = '//div[@id="shop-list"]/table'
xpathimagestr = '//a[@class="one-to-item-link"]/img/@xpath' #项目图片
xpathheadstr = [
    '//div[2]//ul[1]/li[1]/a/@title',            #项目标题
    '//div[2]//ul[1]/li[1]/a/@href',             #项目地址
    '//div[2]//ul[1]/li[2]/span[1]/@title',    #品牌
    '//div[2]//ul[1]/li[3]/span[1]/@title',    #封装
    '//div[2]//ul[1]/li[4]/div/@title'    #描述
]
xpathdatastr = [
    [
        '//div[2]//ul[2]/li[1]/span[1]/text()',
        '//div[2]//ul[2]/li[1]/span[2]/text()'
    ],
    [
        '//div[2]//ul[2]/li[2]/span[1]/text()',
        '//div[2]//ul[2]/li[2]/span[2]/text()'
    ],
    [
        '//div[2]//ul[2]/li[3]/span[1]/text()', 
        '//div[2]//ul[2]/li[3]/span[2]/text()'
    ],
    [
        '//div[2]//ul[2]/li[4]/span[1]/text()', 
        '//div[2]//ul[2]/li[4]/span[2]/text()'
    ], 
    [
        '//div[2]//ul[3]/li[1]/span/text()', 
        '//div[2]//ul[3]/li[1]/a/text()'    
    ],
    [
        '//div[2]//ul[3]/li[2]/span[1]/text()', 
        '//div[2]//ul[3]/li[2]/span[2]//text()'
    ]
]

#内置 APIManager核心
import aiohttp
async def api(
    method:str,
    url:str,
    headers:dict = {},
    cookies:dict = {},
    data:dict = {}
):
    '''异步api调用,复用代码
    '''
    #logger.info(url)
    async with aiohttp.ClientSession() as session:
        async with (
            session.post(url=url,data=data,headers=headers,cookies=cookies) if method == "post" else
            session.get(url=url,headers=headers,cookies=cookies)  
            ) as response:
            type:str = check_type(response.content_type)
            resp = (
                    await response.json() if type == "json" else
                    await response.text() if type == "text" else
                    await response.content.read() if type in ["image","octet-stream"] else
                    f"httpcode:{response.status}\nAPI Data parsing failed")
            for cookie in response.cookies.values():
                cookies[cookie.key] = cookie.coded_value
            return resp , cookies , type

def check_type(type:str):
    content_type =  type.split("/")
    if  content_type[0] == "application":
        return content_type[-1]
    else:
        return content_type[0]
