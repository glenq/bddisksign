from math import pi
from urllib import response
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from bs4 import BeautifulSoup
import logging
import os
import json

# 配置日志
logging.basicConfig(
    filename='sign21tb.log',  # 日志文件名
    level=logging.INFO,     # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def job():
    logging.info('run job...')
    url = generateUrl()
    logging.info(url)
    #print(url);
    ck = getCookie(url);
    logging.info(ck)
    #print(ck)
    questionLogin(ck);
    printScore(ck)
    findgood(ck)

def findgood(ck):
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = {'current_app_id': '8a80810f497cde5b01499858b3201394', 'goodsCondition.sortName': 'exchangeCount', 'goodsCondition.sortOrder': 'desc'} 
    response = requests.post("https://v4.21tb.com/is/html/storeUser/goods.listRecommendGoods.do",headers=headers, data=data, cookies= ck)
    jsonobj = response.json()["list"];
    if len(jsonobj) > 0:
        goods_array =[]
        for godds in jsonobj:
            goods_name = godds['goodsName']
            credit_price = godds['creditPrice']
            remain_count = godds['remainCount']
            goods_array.append({'goodsName': goods_name, 'creditPrice': credit_price, 'remainCount': remain_count})
            # print(goods_array)
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive - Microsoft\Desktop')
            file_path = os.path.join(desktop_path, 'wicresoft21tb.txt')
            with open(file_path, 'w', encoding='utf-8') as goods_file:
                json.dump(goods_array, goods_file, ensure_ascii=False)
            os.startfile(file_path)
    

def generateUrl():
    respJson = requests.get("https://wsoa.wicresoft.com/Custom/GotoTrainingSystem?userId=B0A012E4-D9AD-4621-9A89-DC572C3F06C1&Jqbkw84S0Nv5ee4https=KcYlo7kPnEMeOyTmqxSdYEMraIuT_dyRFvMhNAKgTg0U.RYlKObpoceugXqgbIPym_n3TO1Ssn8X6ByqjUiRexpo9qJpQaffk6hfYSNbN_kt4");
    url = respJson.json()["results"]
    url = url.replace("http://", "https://")
    return url;

def getCookie(url):
    response = requests.get(url, allow_redirects=False);
    ck = response.cookies
    return ck;

def questionLogin(ck):
    response = requests.post("https://v4.21tb.com/qa/qav2/html/user/question/blocked.do", cookies= ck)
    logging.info(response.json())
    print(response.json())

def printScore(ck):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Cookie":  "; ".join([f"{cookie.name}={cookie.value}" for cookie in ck])
    }
    response = requests.get("https://v4.21tb.com/rtr/html/personCenter/personCenter.loadCredit.do?channel=personal_center_page&_=1691137603435", cookies= ck, headers=head);
    soup = BeautifulSoup(response.content, "lxml")
    #print(response.text)
    score_items = soup.select('.user-int-grade-value')
    infotxt = "累计积分：%s, 可用积分：%s" % (score_items[0].text, score_items[1].text)
    logging.info(infotxt)
    print(infotxt)
    

if __name__ == "__main__":
    logging.info('scheduler begining...')
    #job()
    scheduler = BlockingScheduler()
    job_trigger = CronTrigger(hour='9,10', minute='40', second='0')
    scheduler.add_job(job, job_trigger)
    scheduler.start()
