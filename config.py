# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2020/05/26 16:19:58
@Author  :   JRICKL 
@Version :   1.0
@Contact :   leeejjjie@gmail.com
@Desc    :   None
'''

# here put the import lib
import os

class Config():
    """

    信息门户的账号密码为必须
    sckey 是注册server酱时获取的，可以用于微信推送，建议注册一个，推送打卡消息比较方便
    QQCR  是QQ超人打码平台的信息，包括账户和密码还有软件ID，建议使用网上的打码平台，因为自建的验证码识别服务器可能会出问题
    sm图床用于上传打卡详情图片，再通过server酱发送到vx，存在一定信息泄露风险，用户自己权衡是否使用
    """
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    username = ''
    password = ''
    log_path = os.path.join(basedir,'log.txt')
    sckey = ''
    use_sm = True
    QQCR = {
        'username': '',
        'password': '',
        'softId': ''
    }

if __name__ == "__main__":
    cfg = Config()
    print(cfg.log_path)