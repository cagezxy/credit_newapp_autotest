# -*- coding: utf-8 -*-
import re
from public import login_logout
from public.login_logout import driver
from public.common_method import *
from public.conn_mysql import connetDB
import unittest
import logging


class CreditHomePage(unittest.TestCase):
    """打开app的首页，并且执行风险检测操作"""

    @classmethod
    def setUpClass(self):
        logging.info("开始首页内容测试\n")
        self.driver = driver
        self.order_list = []
        # login_logout.login()

    @classmethod
    def tearDownClass(self):
        # login_logout.logout()
        # self.driver.quit()
        logging.info("\n结束首页内容测试\n")

    def close_ad(self):
        """关闭广告弹窗"""
        # x = 0
        # try:
        #     # 广告关闭按钮
        #     loc = (By.XPATH, '//android.view.View/android.widget.Image/following-sibling::android.view.View[2]')
        #     ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
        #     if ele.is_displayed():
        #         x = 1
        #         ele.click()
        #         logging.info("点击关闭首页广告")
        # except Exception as e:
        #     logging.error("没有找到广告", exc_info=True)
        # return x
        #### 以下方法暂时使用 ######
        # 模拟点击 首屏广告关闭按钮，如果没有广告，则是点击空白处
        # 或者可以采取 刷新首页来关闭弹窗广告
        # swipe_down(self.driver, 1000)
        l = get_size(self.driver)
        x1 = int(l[0] * 0.49)
        x2 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.79)
        y2 = int(l[1] * 0.8)
        self.driver.tap([(x2, y2)], 100)
        logging.info("点击关闭首页广告")

    @unittest.skipIf(True, '暂不执行')
    def test_01_1_home(self):
        """打开首页"""
        try:
            openIndex(self.driver, "您身边的修复专家", 1)
            self.close_ad()
        except Exception as e:
            logging.error("打开首页有异常，" , exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_01_2_home_credit(self):
        """点击余额变现"""
        try:
            loc = (By.XPATH, '//android.widget.Image[@text="余额按钮"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 跳到 余额提现页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "余额提现", "没有打开余额提现页面")
        except Exception as e:
            logging.error("打开 余额提现页面 有异常 ", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_01_3_home_credit(self):
        """点击提升额度"""
        try:
            loc = (By.XPATH, '//android.view.View[@text="提升额度"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 跳到余额页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarLeftTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "余额", "没有打开余额页面")
        except Exception as e:
            logging.error("打开 余额页面 有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_02_1_blacklist(self):
        """点击黑名单检测"""
        try:
            # 查看黑名单检测是否存在
            loc = (By.XPATH, '//android.view.View[@text="黑名单检测"]')
            ele = find_element(self.driver, loc, ele_type=1)
            ele.click()
            # 打开黑名单检测
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "黑名单检测", "没有打开黑名单检测")
            # 输入姓名
            loc3 = (By.XPATH, '//android.widget.EditText[@text="请输入您的姓名"]')
            ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
            ele3.clear()
            ele3.send_keys(createChineseName())
            # 输入身份证号
            loc4 = (By.XPATH, '//android.widget.EditText[@text="请输入您的身份证号码"]')
            ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
            ele4.clear()
            ele4.send_keys(gennerator())
            # 输入手机号
            loc5 = (By.XPATH, '//android.widget.EditText[@text="请输入手机号"]')
            ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
            ele5.clear()
            ele5.send_keys(createPhone())
            # 点击同意协议, 获取当前节点之前的同级节点
            # loc6 = (By.XPATH, '//android.view.View[@text="我已阅读并同意 "]/preceding-sibling::android.view.View')
            # loc6 = (By.XPATH, '//android.view.View[@text="我已阅读并同意 "]')
            # ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
            # ele6.click()
            # 点击立即检测
            loc7 = (By.XPATH, '//android.widget.Button[@text="立即检测"]')
            ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
            ele7.click()
            # 订单详情
            loc8 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele8.text)
            self.assertEqual(ele8.text, "订单详情", "没有打开订单详情界面")
            # 找到订单号后，用于数据库修改数据
            loc9 = (By.XPATH, '//android.webkit.WebView[@text="订单详情"]//android.view.View[contains(@text, "订单号：")]')
            ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=5)
            order_id_tmp = str(ele9.text)
            order_id = order_id_tmp.split("：")[1]
            logging.info("订单号: %s" % order_id)
            self.order_list.append(order_id)
            # 点击返回
            self.driver.keyevent(4)
            # # 判断是否弹出提示
            # ele10 = WebDriverWait(self.driver, 2, 0.5).until(
            #     EC.presence_of_element_located((By.ID,
            #                                     'com.yeyun.app.demoapp:id/md_title')))
            # logging.info("---" + ele10.text)
            # self.assertEqual(ele10.text, "提示", "没有打开放弃支付界面")
            # # 点击 放弃按钮，返回
            # handle_alert(self.driver, "放弃")
        except Exception as e:
            logging.error("创建黑名单订单有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_02_2_telecom(self):
        """点击xxx检测"""
        try:
            # 判断首页中的 xxx检测是不是出现
            loc = (By.XPATH, '//android.view.View[@text="xxx优化"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 进入xxx风险评估落地页
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "xxx风险评估", "没有打开 xxx风险评估 页面")
            # 勾选协议
            # loc3 = (By.XPATH, '//android.view.View[@text="我已阅读并同意 "]/preceding-sibling::android.view.View')
            # loc3 = (By.XPATH, '//android.view.View[@text="我已阅读并同意 "]')
            # ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
            # ele3.click()
            # 点击立即检测
            loc4 = (By.XPATH, '//android.widget.Button[@text="立即评估"]')
            ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
            ele4.click()
            # 进入 xxxh5页面
            loc5 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=15)
            logging.info("---进入 " + ele5.text)
            self.assertEqual(ele5.text, "xxx", "没有打开 xxxh5 页面")
            # 获取手机号和密码
            info = get_phone_info()
            phone_no = info[0]
            phone_pw = info[1]
            # 输入手机号
            loc6 = (By.XPATH, '//android.widget.EditText[@text="请输入11位手机号"]')
            ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
            ele6.clear()
            ele6.send_keys(phone_no)
            # 收入密码
            loc7 = (By.XPATH, '//android.widget.EditText[@text="必填"]')
            ele7 = find_element(self.driver, loc7, ele_type=3, wait_time=5)
            ele7.clear()
            ele7.send_keys(phone_pw)
            # 点击提交
            loc8 = (By.XPATH, '//android.widget.Button[@text="提交"]')
            ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
            ele8.click()
            # 进入 xxx数据采集中页面
            loc9 = (By.XPATH, '//android.widget.TextView[contains(@text,"数据采集中")]')
            ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=15)
            logging.info("---进入 " + ele9.text)
            self.assertIn("数据采集中", ele9.text, "没有打开 xxx数据采集中 页面")
            # 短信验证码弹窗 有可能出现，
            try:
                loc9 = (By.XPATH, '//android.view.View[@text="请输入短信验证码"]/following-sibling::android.widget.EditText[1]')
                ele9 = find_element(self.driver, loc9, ele_type=3, wait_time=40)
            except Exception as e:
                logging.warning("没有定位到验证码，继续")
                pass
            if ele9 == 0:
                pass
            else:
                logging.info("找到验证码弹窗")
                #获取验证码
                time.sleep(20)
                info = get_phone_info()
                logging.info("获取手机号短信内容 %s" % str(info))
                sms_info = info[2]
                # 正则表达式， 获取6位数字
                pattern = re.compile(r"[0-9]{6}")
                sms_code = pattern.findall(sms_info)[0]
                logging.info("验证码:" + sms_code)
                ele9.clear()
                ele9.send_keys(sms_code)
                # 点击确认
                loc10 = (By.XPATH, '//android.view.View[@text="请输入短信验证码"]/following-sibling::android.view.View[2]')
                ele10 = find_element(self.driver, loc10, ele_type=3, wait_time=5)
                ele10.click()
            # 进入 xxx数据采集中 结果页面， 取页面中  可用余额 (元) 和 完成 2个元素来判断页面是否爬取数据成功
            loc11 = (By.XPATH, '//android.view.View[@text="可用余额 (元)"]')
            ele11 = find_element(self.driver, loc11, ele_type=1, wait_time=200)
            loc12 = (By.XPATH, '//android.view.View[@text="完成"]')
            ele12 = find_element(self.driver, loc12, ele_type=1, wait_time=5)
            if ele11 == 0 or ele12 == 0:
                self.assertFalse(True, "没有打开 xxx爬取成功的报告页面")
            ele12.click()
            #
            # loc13 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            # ele13 = find_element(self.driver, loc13, ele_type=1, wait_time=60)
            # logging.info("---进入 " + ele13.text)
            # self.assertEqual(ele13.text, "订单生成中", "没有打开 订单生成中 界面")
            # # 订单详情
            loc14 = (By.XPATH, '//android.widget.TextView[@text="订单详情"]')
            ele14 = find_element(self.driver, loc14, ele_type=1, wait_time=60)
            logging.info("---进入 " + ele14.text)
            self.assertEqual(ele14.text, "订单详情", "没有打开 订单详情 界面")
            # 点击2次返回，xxx页面
            self.driver.keyevent(4)
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("创建xxx订单有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_02_3_address(self):
        """点击通讯录"""
        try:
            # 打开通讯录检测
            loc = (By.XPATH, '//android.view.View[@text="通讯录"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "通讯录", "没有打开通讯录页面")
            # 点击同意协议, 获取当前节点之前的同级节点
            # loc6 = (By.XPATH, '//android.view.View[@text="我已阅读并同意 "]/preceding-sibling::android.view.View')
            # loc6 = (By.XPATH, '//android.view.View[@text="我已阅读并同意 "]')
            # ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
            # ele6.click()
            # 点击立即检测
            loc7 = (By.XPATH, '//android.widget.Button[@text="立即检测"]')
            ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
            ele7.click()
            # 订单详情
            loc8 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele8.text)
            self.assertEqual(ele8.text, "订单详情", "没有打开订单详情界面")
            # 找到订单号后，用于数据库修改数据
            loc9 = (By.XPATH, '//android.webkit.WebView[@text="订单详情"]//android.view.View[contains(@text, "订单号：")]')
            ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=5)
            order_id_tmp = str(ele9.text)
            order_id = order_id_tmp.split("：")[1]
            logging.info("订单号: %s" % order_id)
            self.order_list.append(order_id)
            # 点击返回
            self.driver.keyevent(4)
            # 判断是否弹出提示
            # ele7 = WebDriverWait(self.driver, 2, 0.5).until(
            #     EC.presence_of_element_located((By.ID,
            #                                     'com.yeyun.app.demoapp:id/md_title')))
            # logging.info("---" + ele7.text)
            # self.assertEqual(ele7.text, "提示", "没有打开放弃支付界面")
            # # 点击 放弃按钮，返回
            # handle_alert(self.driver, "放弃")
        except Exception as e:
            logging.critical("创建通讯录订单有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回首页
            openIndex(self.driver, "曳云测试", 1)

    @unittest.skipIf(True, '暂无此功能')
    def test_03_devices(self):
        """点击设备检测"""
        try:
            # 打开通讯录检测
            ele = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//android.view.View[@text="通讯录"]')))
            ele.click()
            ele2 = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.ID,
                                                'com.yeyun.app.demoapp:id/viewBarTitle')))
            logging.info("---" + ele2.text)
            self.assertEqual(ele2.text, "通讯录检测", "没有打开通讯录检测")
            # 点击同意协议
            ele3 = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.ID,
                                                'agreement')))
            ele3.click()
            # 点击立即检测
            ele4 = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//android.widget.Button[@text="立即检测"]')))
            ele4.click()
            ele5 = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.ID,
                                                'com.yeyun.app.demoapp:id/viewBarTitle')))
            logging.info("---" + ele5.text)
            self.assertEqual(ele5.text, "等待支付", "没有打开支付界面")
            # 找到订单号后，用于数据库修改数据
            tmp = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//android.webkit.WebView[contains(@text,"等待支付")]/android.view.View[6]')))
            logging.info("订单号: %s" % tmp.text)
            self.orderlist.append(tmp.text)
            # 点击返回，取消支付
            self.driver.keyevent(4)
            # 判断是否弹出提示
            ele7 = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located((By.ID,
                                                'com.yeyun.app.demoapp:id/md_title')))
            logging.info("---" + ele7.text)
            self.assertEqual(ele7.text, "提示", "没有打开放弃支付界面")
            # 点击 放弃按钮，返回
            handle_alert(self.driver, "放弃")
        except Exception as e:
            logging.info("创建通讯录订单有异常，err: %s" % e)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回首页
            openIndex(self.driver, "曳云测试", 1)

    @unittest.skipIf(True, '暂不执行')
    def test_04_alterOrderStats(self):
        """修改订单支付状态（数据库仅配置测试环境）"""
        logging.info("需要修改支付状态的订单： %s" % self.orderlist)
        if self.orderlist:
            for order_id in self.orderlist:
                db = connetDB()
                sql = "update  %s" % order_id
                db.update(sql)
                db.close()
        else:
            logging.warning("没有成功创建过订单，无需修改支付状态")

    @unittest.skipIf(False, '暂不执行')
    def test_05_indexBanner(self):
        """首页中部banner"""
        try:
            loc = (By.XPATH, '//android.widget.Image[@text="小贷账本"]/preceding-sibling::android.view.View[1]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 跳到 文章产品的页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            # 判断页面中 是否加载了h5内容
            loc3 = (By.ID, 'app')
            ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
            self.assertEqual(ele2.text, "极速下款", "没有打开 极速下款 页面")
            time.sleep(1)
            # 点击返回，取消支付
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 极速下款 页面 有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(True, '暂无此功能')
    def test_06_loan_book(self):
        """首页--小贷账本"""
        pass

    @unittest.skipIf(False, '暂不执行')
    def test_07_creditCard(self):
        """首页--卡中心"""
        try:
            loc = (By.XPATH, '//android.widget.Image[@text="卡中心"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 跳到 余额提现页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "银联卡中心", "没有打开 银联卡中心 页面")
            time.sleep(1)
            # 点击返回，取消支付
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 银联卡中心 页面 有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_08_moreProduct(self):
        """首页最下方-点击更多按钮"""
        try:
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            loc = (By.XPATH, '//android.view.View[@text="显示更多"]')
            ele = scroll_local(self.driver, loc, "显示更多")
            ele.click()
            # 跳到 余额提现页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarLeftTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "文章超市", "没有打开 文章超市 页面")
        except Exception as e:
            logging.critical("打开 文章超市 页面 有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "您身边的修复专家", 1)

    @unittest.skipIf(False, '暂不执行')
    def test_09_othersAction(self):
        """执行随机动作"""
        try:
            random_actions(self.driver)
        except Exception as e:
            logging.critical("执行随机动作出错 ", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()