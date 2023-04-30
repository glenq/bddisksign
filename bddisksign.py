import requests
import smtplib
import os  # 用于导入系统变量
import sys  # 实现 sys.exit
import logging  # 用于日志输出
import time  # 时间
#from email.mime.text import MIMEText
#from email.header import Header

logging.basicConfig(level=logging.INFO, format='%(message)s')  # Info级日志
logger = logging.getLogger(__name__)  # 主模块

def issvip(cookie):
    headers = {
        'User-Agent': 'netdisk;11.19.11;M2012K11AC;android-android;11;JSbridge4.4.0;jointBridge;1.1.0',
        'Referer': 'https://pan.baidu.com/disk/main',
        'Cookie': cookie,
    }

    info_url = 'https://pan.baidu.com/rest/2.0/membership/user/info?method=query&clienttype=0&app_id=250528&web=1&dp-logid=84670500916096520014'
    
    response_json = requests.get(url=info_url, headers=headers).json()
 
    if response_json['error_code'] == 0:
        is_svip = response_json['user_info']['is_svip']
        username= response_json['user_info']['username']        
        print('用户：'+username+', svip状态：' + str(is_svip))
    else:
        print(response_json)
 

def check_in(cookie):
    headers = {
        'User-Agent': 'netdisk;11.19.11;M2012K11AC;android-android;11;JSbridge4.4.0;jointBridge;1.1.0',
        'Referer': 'https://pan.baidu.com/act/task/mainpage',
        'Cookie': cookie,
    }

    sign_url = 'https://pan.baidu.com/pmall/points/signin'
    check_url = 'https://pan.baidu.com/pmall/points/balance'
    param = {
        'channel': 'android_11_M2012K11AC_bd-netdisk_1024328u',
        'time': int(time.time())
    }

    response_json = requests.get(url=sign_url, params=param, headers=headers).json()
#    print(response_json)
    check_json = requests.get(url=check_url, params=param, headers=headers).json()
    balance = check_json['balance']
    if response_json['errno'] == 0:
        points = response_json['points']
#        dic = {
#            'points': points,
#            'balance': balance
#        }
        print('本次签到获取积分：'+str(points)+'，总积分：'+str(balance))
        print('休息三秒，执行下一个账号'.center(50, '='))
        time.sleep(3)
#        return dic
    else:
        print(response_json)
#    return "error"

# return list[bd_ck]
def get_bdck():  # 方法 获取 bd_ck值 [系统变量传递]
    if "bd_ck" in os.environ:  # 判断 bd_ck是否存在于环境变量
        bd_ck_list = os.environ['bd_ck'].split('&')  # 读取系统变量 以 & 分割变量
        if len(bd_ck_list) > 0:  # 判断 bd_ck 数量 大于 0 个
            return bd_ck_list  # 返回 bd_ck [LIST]
        else:  # 判断分支
            logger.info("bd_ck变量未启用")  # 标准日志输出
            sys.exit(1)  # 脚本退出
    else:  # 判断分支
        logger.info("未添加bd_ck变量")  # 标准日志输出
        sys.exit(0)  # 脚本退出


# 任务完成发送邮件函数
def send_email(rs):
    # 登录
    smtp_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)
    smtp_obj.login('', '')

    # 邮件内容
    str_success = ''
    str_fail = "sign fail, check script"
    for info in rs:
        get_now = info['points']
        balance = info['balance']
        str_success = str_success + f'get {get_now}积分，目前总积分{balance}\n'

    if len(rs) != 0:
        msg = MIMEText(str_success, 'plain', 'utf-8')
        msg['Subject'] = Header("bd disk sign success", 'utf-8')
    else:
        msg = MIMEText(str_fail, 'palin', 'utf-8')
        msg['Subject'] = Header("bd disk sign fail", 'utf-8')
    smtp_obj.sendmail("", [""], msg.as_string())


if __name__ == '__main__':
    bdcklist = get_bdck()
    for ck in bdcklist:
        issvip(ck)
        check_in(ck)
#        rs = check_in(ck)
#        print(rs)
#       send_email(rs)
