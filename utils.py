# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2020/05/26 11:50:59
@Author  :   JRICKL 
@Version :   1.0
@Contact :   leeejjjie@gmail.com
@Desc    :   None
'''

# here put the import lib
import requests
import json
from datetime import datetime
import time
import pickle
import os


def captcha_recognition(img_path):
    """验证码识别

    自己建了一个验证码识别的服务器，准确率大概80%左右
    服务器不一定稳定，建议使用一些打码平台的打码服务
    """
    with open(img_path, 'rb') as f:
        imgBytes = f.read()
    files = {
        'imgBytes': imgBytes
    }
    res = requests.post(
        'http://47.113.124.109:5000/api/captcha', files=files).json()
    if res['success'] == True:
        return res['res']
    else:
        return False


def QQCR_captcha_recognition(img_path, cfg):
    """QQ超人打码平台验证码识别

    QQ超人打码平台提供的验证码识别服务，识别率一般，但稳定
    价格的话充值两块钱应该可以用很久
    """
    with open(img_path, 'rb') as f:
        imgByte = f.read()
    hex_imgdata = ''.join(["%02X" % x for x in imgByte]).strip()
    # user_info_url = 'http://api2.sz789.net:88/GetUserInfo.ashx'
    recognition_url = 'http://api2.sz789.net:88/RecvByte.ashx'
    data = {
        'username': cfg.QQCR['username'],
        'password': cfg.QQCR['password'],
        'softId': cfg.QQCR['softId'],
        'imgdata': hex_imgdata
    }
    return json.loads(requests.post(recognition_url, data=data).content)['result']


def vx_info(cfg, info='每日报平安打卡成功！', img_url=None):
    """vx通知函数

    利用server酱提供的接口，推送每日打卡信息
    server酱的具体使用方法参考：http://sc.ftqq.com/3.version
    """
    if cfg.sckey != '':
        api = 'https://sc.ftqq.com/{}.send'.format(cfg.sckey)
        # 是否发送打卡详情图片
        if img_url:
            data = {
                'text': '每日报平安打卡',
                'desp': '时间:{}，{} ![check]({})'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), info, img_url)
            }
        else:
            data = {
                'text': '每日报平安打卡',
                'desp': '时间:{}，{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), info)
            }
        res = requests.get(api, data)
        if res.status_code == 200:
            return res.json()['errmsg']
        else:
            return False
    else:
        return None


def log(info, cfg):
    """写日志函数

    """
    
    with open(cfg.log_path, 'a+', encoding='utf-8') as f:
        f.write(time.asctime(time.localtime(time.time())) + '\n' + info + '\n')


class SM(object):
    """SM.MS 图床类

    使用sm.ms图床可以将打卡详情通过server酱发送到你的微信，方便确认是否打卡成功
    sm.ms是由个人创建的免费图床，存在人工审核方式
    所以存在信息泄露的可能性，毕竟打卡详情界面个人信息较多，请谨慎使用
    目前逻辑是将上传图片的delete_url保存在本地，请求该链接即可删除截图
    """

    def __init__(self):
        self.upload_url = 'https://sm.ms/api/v2/upload'
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.img_log_path = os.path.join(self.basedir,'img_log.pkl')
        if not os.path.exists(self.img_log_path):
            delete_list = []
            with open(self.img_log_path, 'wb') as f:
                pickle.dump(delete_list, f)

    def upload(self,img_path):
        with open(img_path, 'rb') as f:
            file_obj = f.read()
        file = {'smfile': file_obj}
        upload_result = requests.post(self.upload_url, files=file)
        if upload_result.status_code == 200:
            res = upload_result.json()
            # print(res)
            with open(self.img_log_path, 'rb') as f:
                delete_list = pickle.load(f)
            if res['success'] == True:
                delete_list.append(res['data']['delete'])
                with open(self.img_log_path, 'wb') as f:
                    pickle.dump(delete_list, f)
                return res['data']['url']
            else:
                return False
        else:
            return False

    def delete(self):
        with open(self.img_log_path, 'rb') as f:
            delete_list = pickle.load(f)
        while len(delete_list) != 0:
            url = delete_list.pop()
            res = requests.get(url)
        delete_list =[]
        with open(self.img_log_path,'wb') as f:
            pickle.dump(delete_list,f)


if __name__ == "__main__":
    sm = SM()
    sm.upload('./check_img.png')
    a = input('suspend')
    sm.delete()