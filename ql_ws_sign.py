# -*- coding: utf-8 -*
'''
new Env('wicresoft sign');
'''
import requests
from notify import send  # 导入青龙消息通知模块
import socket  # 用于端口检测
import base64  # 用于编解码
import json  # 用于Json解析
import os  # 用于导入系统变量
import sys  # 实现 sys.exit
import logging  # 用于日志输出
from urllib import response
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format='%(message)s')  # Info级日志
logger = logging.getLogger(__name__)  # 主模块

# 返回值 list[ws21tbkey]
def get_ws21tbkey():  # 方法 获取 ws21tbkey值 [系统变量传递]
    if "WS_21tb" in os.environ:  # 判断 JD_WSCK是否存在于环境变量
        wskey_list = os.environ['WS_21tb'].split('&')  # 读取系统变量 以 & 分割变量
        if len(wskey_list) > 0:  # 判断 WSKEY 数量 大于 0 个
            return wskey_list  # 返回 WSKEY [LIST]
        else:  # 判断分支
            logger.info("JD_WSCK变量未启用")  # 标准日志输出
            sys.exit(1)  # 脚本退出
    else:  # 判断分支
        logger.info("未添加JD_WSCK变量")  # 标准日志输出
        sys.exit(0)  # 脚本退出
        
def generateUrl(ws21tbkey):
    respJson = requests.get("https://wsoa.wicresoft.com/Custom/GotoTrainingSystem?"+ws21tbkey);
    url = respJson.json()["results"]
    url = url.replace("http://", "https://")
    return url;

def getCookie(url):
    response = requests.get(url, allow_redirects=False);
    ck = response.cookies
    return ck;

def questionLogin(ck):
    response = requests.post("https://v4.21tb.com/qa/qav2/html/user/question/blocked.do", cookies= ck)
    logger.info(response.json())
    print(response.json())
    
def sendScore(ck):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Cookie":  "; ".join([f"{cookie.name}={cookie.value}" for cookie in ck])
    }
    response = requests.get("https://v4.21tb.com/rtr/html/personCenter/personCenter.loadCredit.do?channel=personal_center_page&_=1691137603435", cookies= ck, headers=head);
    soup = BeautifulSoup(response.content, "lxml")
    
    score_items = soup.select('.user-int-grade-value')
    infotxt = "累计积分：%s, 可用积分：%s" % (score_items[0].text, score_items[1].text)
    logger.info(infotxt)
    send('wicresoft sign', infotxt)
    

def job(wskey):
    url = generateUrl(wskey)
    logger.info(url)
    
    ck = getCookie(url);
    logger.info(ck)
    
    questionLogin(ck);
    sendScore(ck)
  
    
if __name__ == "__main__":
    logger.info('wicresoft sign begining...')
    wslist = get_ws21tbkey()
    for ws in wslist: 
        job(ws)
    