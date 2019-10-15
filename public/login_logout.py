# coding = utf-8

import time
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from public.common_method import handle_alert, find_element, openIndex, open_page
from public.conn_mysql import connetDB
import logging

desired_caps = {
    'platformName': 'Android',
    'deviceName': '4466d856',
    'platformVersion': '8.0',
    'appPackage': 'com.yeyun.app.demoapp',  #曳云测试
    # 'appPackage': 'com.yeyun.app.demoapp.creditloanking', #曳云测试
    'appActivity': 'com.yeyun.app.demoapp.display.act.LaunchActivity',
    "unicodeKeyboard": "True",
    "resetKeyboard": "True",
    'noReset': 'true'  # 每次打开不重新安装apk
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
time.sleep(12)
# driver.implicitly_wait(5)
driver.wait_activity('.display.act.MainActivity', 15)
driver.background_app(2)


class LoginMethod():
    def __init__(self):
        self.driver = driver
        self.phone_num = "17777777777"
        self.sms_code = "777777"

    def get_smsCode(self):
        db = connetDB()
        sql = "select ;" % self.phone_num
        rs = db.select(sql)
        if len(rs):
            for result in rs:
                self.sms_code = result
                break
        else:
            self.sms_code = "777777"
        db.close()
        return self.sms_code

    def login_click(self):
        # 由于以前测试时可能有 没有退出的情况，因此登录前先判断
        # 点击退出按钮
        try:
            loc = (By.ID, 'com.yeyun.app.demoapp:id/tvNickName')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            if ele.is_displayed():
                logging.info("先执行退出动作，在进行登录")
                ele.click()
                # 进入到 个人信息界面
                loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                open_page(self.driver, "个人信息", loc2)
                # 找到退出按钮，点击
                loc3 = (By.ID, 'com.yeyun.app.demoapp:id/tvExit')
                ele3 = find_element(self.driver, loc3, ele_type=1)
                ele3.click()
                handle_alert(self.driver, "确认")
                logging.info("---" + "确认退出登录")
        except Exception as e:
            logging.critical("没有登录状态，进行登录", exc_info=True)
        # 点击 登录/注册按钮
        loc4 = (By.ID, 'com.yeyun.app.demoapp:id/btnLogin')
        ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
        ele4.click()
        logging.info("---点击登录按钮")
        # 点击后跳转页面
        loc5 = (By.ID, 'com.yeyun.app.demoapp:id/tvLoginHint')
        ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
        logging.info("---" + ele5.text)
        assert "手机快捷登录" == ele5.text, "没有打开手机快捷登录"

    def input_phonecode(self):
        # 输入 手机号 和 验证码
        # 输入手机号
        loc = (By.ID, 'com.yeyun.app.demoapp:id/etPhone')
        ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
        ele.clear()
        ele.send_keys(self.phone_num)
        # 点击验证码
        loc2 = (By.ID, 'com.yeyun.app.demoapp:id/tvGetSmsCode')
        ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
        ele2.click()
        # 输入验证码
        loc3 = (By.ID, 'com.yeyun.app.demoapp:id/etSmsCode')
        ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
        ele3.clear()
        self.get_smsCode()
        ele3.send_keys(self.sms_code)
        # 点击同意协议框
        loc4 = (By.ID, 'com.yeyun.app.demoapp:id/cbAgreement')
        ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
        ele4.click()
        # 点击登录按钮
        loc5 = (By.ID, 'com.yeyun.app.demoapp:id/bLogin')
        ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
        ele5.click()
        # 判断是不是已经登录成功显示 手机号
        loc6 = (By.ID, 'com.yeyun.app.demoapp:id/tvNickName')
        ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
        logging.info("---" + ele6.text + "\n")
        assert ele6.text is not None, "登录没有成功"


class LogoutMethod():
    def __init__(self):
        self.driver = driver

    def logout_click(self):
        # 执行退出动作
        try:
            loc = (By.ID, 'com.yeyun.app.demoapp:id/tvNickName')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            if ele.is_displayed():
                logging.info("先执行退出动作，在进行登录")
                ele.click()
                # 进入到 个人信息界面
                loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                open_page(self.driver, "个人信息", loc2)
                # 找到退出按钮，点击
                loc3 = (By.ID, 'com.yeyun.app.demoapp:id/tvExit')
                ele3 = find_element(self.driver, loc3, ele_type=1)
                ele3.click()
                handle_alert(self.driver, "确认")
                logging.info("---" + "确认退出登录")
        except Exception as e:
            logging.critical("没有登录状态，进行登录", exc_info=True)


def login():
    temp = LoginMethod()
    openIndex(driver, "我的", 4)
    temp.login_click()
    temp.input_phonecode()


def logout():
    openIndex(driver, "我的", 4)
    temp = LogoutMethod()
    temp.logout_click()


if __name__ == "__main__":
    login()
    logout()
