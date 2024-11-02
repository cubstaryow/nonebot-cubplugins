from typing import Union
from .callapi import api
from util.plugins_data import initdata,wdata,rdata ,driver
jsonname = "apim-cookies.json"
bashdata = {
    "status":1,
    "cookies":{}
}
initdata(jsonname,bashdata)

class api_manager:
    cookies = rdata(jsonname).get("cookies",{})
    api_list = {}
    
    def __init__(self):
        pass

    def getcookies(self):
        return self.cookies
    
    def add_api_list(
        self,
        apilist:list,
        api_cookiekey:str
    ):
        for temp in apilist:
            method = "get" if len(temp) <=2 else temp[2]
            self.add_api(
                api_name=temp[0],
                api=temp[1],
                method=method,
                api_cookiekey=api_cookiekey
                )
    
    def add_api(
        self,
        api_name:str,
        api:str,
        method: str ="get",
        api_cookiekey:str = "global"
    ):
        self.api_list[api_name]={
            "api" : api,
            "method" : method,
            "key_cookies" : api_cookiekey ,
            "can_use" : True}
    
    def api_switch(
        self,
        api_name:str,
        can_use:bool = True
    ):
        self.api_list[api_name]["can_use"] = can_use
        
    
    @classmethod
    async def apirun(
        cls,
        api_key:str,
        paramstr:str ="",
        data:dict = {},
        headers:dict = {}
    ):
        apiinfo = cls.api_list.get(api_key,{})
        if apiinfo.get("can_use",False):
            apiurl = apiinfo.get("api","")+paramstr
            method = apiinfo.get("method","get")
            key_cookies = apiinfo.get("key_cookies","global")
            cookies = cls.cookies.get(key_cookies,{})
            resp , cls.cookies[key_cookies] ,resptype=await api(
                method=method , url=apiurl , cookies= cookies , data=data ,headers=headers)
            return resp ,resptype
        else:
            return {
                'code':"cubV5-E",
                'msg' : "[APIM-E]API Unreachable"
            } , "json"

apim = api_manager()