# -*- encoding: utf-8 -*-
'''
@File    :   mrbpa.py
@Time    :   2020/05/26 16:47:18
@Author  :   JRICKL 
@Version :   1.0
@Contact :   leeejjjie@gmail.com
@Desc    :   None
'''

# here put the import lib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from utils import *
from config import Config
import time
import platform
import sys
import os

class MRBPA(object):
    """ Daily Report
    """

    def __init__(self, cfg):
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.portal_url = "https://idas.uestc.edu.cn/authserver/login?service=http%3A%2F%2Fportal.uestc.edu.cn%2F"
        self.mrbpa_url = 'http://eportal.uestc.edu.cn/new/index.html'
        self.FirefoxOptions = Options()
        self.FirefoxOptions.add_argument('--headless')
        # 无痕模式
        self.FirefoxOptions.add_argument('--incognito')
        if platform.system().lower() == 'linux':
            execution_path = os.path.join(self.basedir,'geckodriver')
        elif platform.system().lower() == 'windows':
            execution_path = os.path.join(self.basedir,'geckodriver.exe')
        else:
            sys.exit()
        self.browser = webdriver.Firefox(options=self.FirefoxOptions,executable_path=execution_path)
        self.browser.set_window_size(1920,1080)
        self.cfg = cfg
        
        self.main()
        
    def main(self):
        while(True):
            # 登录，尝试10次
            for i in range(10):
                login_res = self.login(self.cfg)
                if login_res:
                    break
            # 检查是否成功登录信息门户
            if not login_res:
                info = '未成功登录信息门户,请及时检查打卡信息'
                log(info, self.cfg)
                vx_info(self.cfg, info)
                break
            # 打卡，尝试10次
            for i in range(10):
                check_res = self.check()
                if check_res:
                    break
                else:
                    self.auto_clock()
            if not check_res:
                info = '未成功打卡，请及时检查打卡信息'
                log(info, self.cfg)
                vx_info(self.cfg,info)
                break
            break
        self.browser.quit()

        if login_res and check_res:
            if self.cfg.use_sm:
                sm = SM()
                sm.delete()
                sm_res = sm.upload(os.path.join(self.basedir,'check_img.png'))
                if sm_res:
                    vx_info(self.cfg,img_url = sm_res)
                else:
                    info = '打卡成功，但由于sm.ms图床问题，未获取截图'
                    vx_info(self.cfg,info)
            else:
                vx_info(self.cfg)
        
    def login(self, cfg):

        try:
            self.browser.get(self.portal_url)
            self.browser.find_element_by_id('username').send_keys(cfg.username)
            self.browser.find_element_by_id('password').send_keys(cfg.password)
            captcha = self.browser.find_element_by_id('captchaImg')
            captcha.screenshot(os.path.join(self.basedir,'screenshot.png'))
            if self.cfg.QQCR['username']:
                cap = QQCR_captcha_recognition(os.path.join(self.basedir,'screenshot.png'), self.cfg)
            else:
                cap = captcha_recognition(os.path.join(self.basedir,'screenshot.png'))
            self.browser.find_element_by_id('captchaResponse').send_keys(cap)
            self.browser.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div[2]/div/div[3]/div/form/p[4]/button').click()
            time.sleep(2)
            try:
                self.browser.find_element_by_id("msg")
                info = '验证码打码失败'
                log(info, self.cfg)
                return False
            except NoSuchElementException:
                try:
                    self.browser.find_element_by_xpath(
                        '/html/body/div/div[1]/div[1]/img')
                    info = '登录信息门户成功'
                    log(info, self.cfg)
                    return True
                except:
                    info = '获取页面元素失败，重启……'
                    log(info, self.cfg)
                    return False
        except NoSuchElementException:
            info = '登录失败'
            log(info, self.cfg)
            return False

    def auto_clock(self):
        try:
            self.browser.get(self.mrbpa_url)
            # 点击‘仍然访问’
            self.browser.find_element_by_xpath(
                '/html/body/div[2]/div[3]/a').click()
            time.sleep(5)
            # 点击研究生健康
            self.browser.find_element_by_xpath(
                '/html/body/article[5]/section/div[2]/div[1]/div[2]/pc-card-html-4786696181714491-01/amp-w-frame/div/div[2]/div/div[1]/widget-app-item[1]/div/div').click()
            # 切换到弹出页
            self.browser.switch_to.window(self.browser.window_handles[-1])
            time.sleep(3)
            # 点击新增
            self.browser.find_element_by_xpath(
                '/html/body/main/article/section/div[2]/div').click()
            time.sleep(3)
            # 点击保存
            self.browser.find_element_by_xpath('//*[@id="save"]').click()
            time.sleep(5)
            # 点击确认
            self.browser.find_element_by_xpath(
                '/html/body/div[29]/div[1]/div[1]/div[2]/div[2]/a[1]').click()
            return True
        except NoSuchElementException:
            info = '获取页面元素失败，重启……'
            log(info, self.cfg)
            return False

    def check_img(self):
        # 将打卡详情界面截图
        try:
            # 点击详情
            self.browser.find_element_by_xpath(
                '/html/body/main/article/section/div[3]/div[2]/div[2]/div/div[4]/div[2]/div/table/tbody/tr[1]/td[1]/a').click()
            time.sleep(5)
            self.browser.get_screenshot_as_file(
                os.path.join(self.basedir,'check_img.png'))
            return True
        except NoSuchElementException:
            info = '获取页面元素失败，重启……'
            log(info, self.cfg)
            return False

    # check 是否打卡成功
    def check(self):
        try:
            self.browser.get(self.mrbpa_url)
            time.sleep(3)
            # 点击‘仍然访问’
            self.browser.find_element_by_xpath(
                '/html/body/div[2]/div[3]/a').click()
            time.sleep(10)
            # 点击研究生健康
            self.browser.find_element_by_xpath(
                '/html/body/article[5]/section/div[2]/div[1]/div[2]/pc-card-html-4786696181714491-01/amp-w-frame/div/div[2]/div/div[1]/widget-app-item[1]/div/div').click()
            self.browser.switch_to.window(self.browser.window_handles[-1])
            time.sleep(5)
            # 点击新增
            self.browser.find_element_by_xpath(
                '/html/body/main/article/section/div[2]/div').click()
            time.sleep(5)
            # 获取弹出框中的信息
            context = self.browser.find_element_by_xpath(
                '/html/body/div[11]/div[1]/div[1]/div[2]/div[1]/div').get_attribute('textContent')
            time.sleep(3)
            # 点击确认取消弹出框
            self.browser.find_element_by_xpath(
                '/html/body/div[11]/div[1]/div[1]/div[2]/div[2]/a').click()
            if context == '今日已填报！':
                info = '打卡成功，今日已填报！'
                log(info, self.cfg)
                res = self.check_img()
                if res:
                    info = '已发送截图信息'
                    log(info, self.cfg)
                return True
            else:
                info = '获取页面元素失败，重启……'
                log(info, self.cfg)
                return False
        except NoSuchElementException:
            return False


if __name__ == "__main__":
    cfg = Config()
    s = MRBPA(cfg)