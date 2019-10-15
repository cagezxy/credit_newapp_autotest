# -*- coding: utf-8 -*-
import re
import logging
from public.login_logout import driver
from public.common_method import *
import unittest


class CreditLoanMarket(unittest.TestCase):
    """打开app的 余额页面"""

    @classmethod
    def setUpClass(self):
        logging.info("开始 余额页面 内容测试\n")
        self.driver = driver
        # login_logout.login()

    @classmethod
    def tearDownClass(self):
        # login_logout.logout()
        # self.driver.quit()
        logging.info("\n结束 余额页面 内容测试\n")

    def get_certification_status(self, *cer_titles):
        try:
            cer_title_tmp = cer_titles
            cer_stat_list = []
            for cer_title in cer_title_tmp:
                loc = (By.XPATH, '//android.view.View[@text="%s"]/following-sibling::android.view.View[2]' % cer_title)
                ele = find_element(self.driver, loc, ele_type=1, wait_time=3)
                cer_stat_list.append(ele.text)
            return cer_stat_list
        except Exception as e:
            logging.critical("获取检测或认证状态失败", exc_info=True)

    @unittest.skipIf(False, '暂不执行')
    def test_01_creditPage(self):
        """打开余额，获取各个检测认证状态"""
        try:
            openIndex(self.driver, "余额", 3)
            cer_stat_list = self.get_certification_status('黑名单', '通讯录', 'xxx', 'fund', 'social', '违章')
            logging.info(cer_stat_list)
            if len(cer_stat_list) == 6:
                self.black_cer = cer_stat_list[0]
                self.addr_cer = cer_stat_list[1]
                self.tele_cer = cer_stat_list[2]
                self.fund_cer = cer_stat_list[3]
                self.social_cer = cer_stat_list[4]
                self.car_cer = cer_stat_list[5]
            else:
                logging.warning("检测和认证状态，数据长度不对")
        except Exception as e:
            logging.critical("打开 余额 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_02_getCertification(self):
        """打开余额提现页面，获取实名认证结果，未实名则进行实名"""
        try:
            loc = (By.XPATH, '//android.widget.Image[@text="立即提现按钮"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 跳到余额提现页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "余额提现", "没有打开余额提现页面")
            tmp = self.get_certification_status('实名认证')
            self.name_cer = tmp[0]
            if self.name_cer == "去认证":
                loc3 = (By.XPATH, '//android.view.View[@text="实名认证"]')
                ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
                ele3.click()
                # 如果是去认证状态，点击进入实名认证
                loc4 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
                logging.info("---进入 " + ele4.text)
                self.assertEqual(ele4.text, "实名认证", "没有打开 实名认证 页面")
                # 输入姓名
                loc5 = (By.XPATH, '//android.widget.EditText[@text="请输入真实姓名"]')
                ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
                ele5.clear()
                ele5.send_keys("张义凤")
                # 输入身份证号
                loc6 = (By.XPATH, '//android.widget.EditText[@text="请输入身份证号码"]')
                ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
                ele6.clear()
                ele6.send_keys("342626196902205368")
                # 提交验证
                loc7 = (By.XPATH, '//android.widget.Button[@text="提交验证"]')
                ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
                ele7.click()
                # 进入验证成功界面
                loc8 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
                logging.info("---进入 %s 验证成功" % ele8.text)
                self.assertEqual(ele8.text, "实名认证", "没有打开 实名认证验证成功 页面")
                # 判断验证成功界面是否出现了 所需的提示
                loc9 = (By.XPATH, '//android.widget.EditText[@text="**凤"]')
                ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=5)
                # 点击返回
                self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 余额提现 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(True, '暂不执行')
    def test_03_openBlack(self):
        """点击黑名单，进入黑名单检测页面"""
        try:
            # 点击余额页面中的黑名单
            loc = (By.XPATH, '//android.view.View[@text="黑名单"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=3)
            ele.click()
            # 打开黑名单检测
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "黑名单检测", "没有打开黑名单检测")
            # 点击返回
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 黑名单检测 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(True, '暂不执行')
    def test_04_openAddr(self):
        """点击通讯录，进入到通讯录界面"""
        try:
            # 点击余额页面中的通讯录
            loc = (By.XPATH, '//android.view.View[@text="通讯录"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=3)
            ele.click()
            # 打开黑名单检测
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "通讯录", "没有打开通讯录页面")
            # 点击返回
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 通讯录 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_05_telecom(self):
        """点击xxx检测"""
        try:
            # 判断首页中的 xxx检测是不是出现
            loc = (By.XPATH, '//android.view.View[@text="xxx"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
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
            # 密码
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
            # 短信验证码弹窗 有可能出现，爬虫任务如果是复用的话，则不会有验证码弹窗，
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
            else:
                logging.info("---进入 xxx爬去成功报告页面")
            ele12.click()
        except Exception as e:
            logging.critical("创建xxx订单有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_06_openFund(self):
        """点击fund，进入到fundh5界面"""
        fund_city = "fund中心"
        phone = "123343435455"
        password = "1123321"
        try:
            tmp = self.get_certification_status("fund")
            self.fund_cer = tmp[0]
            # fund认证状态为 认证过期、未认证的，才可以进行检测
            if self.fund_cer != "已认证":
                # 点击fund
                loc = (By.XPATH, '//android.view.View[@text="fund"]')
                ele = find_element(self.driver, loc, ele_type=1, wait_time=3)
                ele.click()
                # 打开fund
                loc2 = (By.XPATH, '//android.widget.TextView[@text="fund省份"]')
                ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=15)
                logging.info("---进入 " + ele2.text)
                self.assertEqual(ele2.text, "fund省份", "没有打开 fund省份 页面")
                # 搜索fund中心
                loc3 = (By.XPATH, '//android.widget.EditText[@text="搜索"]')
                ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
                ele3.clear()
                # 输入fund后进入到 fund界面
                ele3.send_keys(fund_city)
                loc4 = (By.XPATH, '//android.view.View/android.view.View[contains(@text, %s)]' % fund_city)
                ele4 = find_element(self.driver, loc4, ele_type=3, wait_time=5)
                ele4.click()
                # 打开fund 账号密码界面
                loc5 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=15)
                logging.info("---进入 " + ele5.text)
                self.assertIn(ele5.text, "%s" % fund_city, "没有打开 %s 页面" % fund_city)
                # 输入手机号
                loc6 = (By.XPATH, '//android.widget.EditText[@text="请输入手机号"]')
                ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
                ele6.clear()
                ele6.send_keys(phone)
                # 输入密码
                loc7 = (By.XPATH, '//android.widget.EditText[@text="请输入密码"]')
                ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
                ele7.clear()
                ele7.send_keys(password)
                # 点击提交
                loc8 = (By.XPATH, '//android.widget.Button[@text="提交"]')
                ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
                ele8.click()
                # 打开爬取数据页面
                loc9 = (By.XPATH, '//android.widget.TextView[@text="%s数据采集中"]' % fund_city)
                ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=60)
                logging.info("---进入 " + ele9.text)
                # 点击完成按钮，回到余额页面
                self.assertEqual(ele9.text, "%s数据采集中" % fund_city, "没有打开 %s数据采集中 页面" % fund_city)
                loc11 = (By.XPATH, '//android.view.View[@text="fund余额 (元)"]')
                ele11 = find_element(self.driver, loc11, ele_type=1, wait_time=120)
                loc12 = (By.XPATH, '//android.view.View[@text="完成"]')
                ele12 = find_element(self.driver, loc12, ele_type=1, wait_time=5)
                if ele11 == 0 or ele12 == 0:
                    self.assertFalse(True, "没有打开 fund成功的报告页面")
                ele12.click()
            else:
                pass
        except Exception as e:
            logging.critical("打开 fund 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_07_openSocial(self):
        """点击social页面，进入socialh5页面"""
        social_city = "ttttttsocial"
        idno = "3301286737378838383"
        password = "444444444"
        try:
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            tmp = self.get_certification_status("social")
            self.soc_cer = tmp[0]
            # 认证状态为 认证过期、未认证的，才可以进行检测
            if self.soc_cer != "已认证":
                # 点击social
                # 由于 social 被挡住了，需要往上滑动一部分， 否则点击的位置不对
                loc = (By.XPATH, '//android.view.View[@text="social"]')
                ele = find_element(self.driver, loc, ele_type=1, wait_time=3)
                ele.click()
                # 打开socialh5
                loc2 = (By.XPATH, '//android.widget.TextView[@text="social省份"]')
                ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=15)
                logging.info("---进入 " + ele2.text)
                self.assertEqual(ele2.text, "social省份", "没有打开 social省份 页面")
                # 搜索social
                loc3 = (By.XPATH, '//android.widget.EditText[@text="搜索"]')
                ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
                ele3.clear()
                # 输入social 后进入到 social界面
                ele3.send_keys(social_city)
                loc4 = (By.XPATH, '//android.view.View/android.view.View[contains(@text, %s)]' % social_city)
                ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
                ele4.click()
                # 打开social 账号密码界面
                loc5 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=15)
                logging.info("---进入 " + ele5.text)
                self.assertIn(ele5.text, "%s" % social_city, "没有打开 %s 页面" % social_city)
                # 输入用户名
                loc6 = (By.XPATH, '//android.widget.EditText[@text="请输入用户名"]')
                ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
                ele6.clear()
                ele6.send_keys(idno)
                # 输入密码
                loc7 = (By.XPATH, '//android.widget.EditText[@text="通过注册获取"]')
                ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
                ele7.clear()
                ele7.send_keys(password)
                # 点击提交
                loc8 = (By.XPATH, '//android.widget.Button[@text="提交"]')
                ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
                ele8.click()
                # 打开爬取数据页面
                loc9 = (By.XPATH, '//android.widget.TextView[@text="%s数据采集中"]' % social_city)
                ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=120)
                logging.info("---进入 " + ele9.text)
                # 点击完成按钮，回到余额页面
                self.assertEqual(ele9.text, "%s数据采集中" % social_city, "没有打开 %s数据采集中 页面" % social_city)
                loc11 = (By.XPATH, '//android.view.View[@text="医保余额 (元)"]')
                ele11 = find_element(self.driver, loc11, ele_type=1, wait_time=120)
                loc12 = (By.XPATH, '//android.view.View[@text="完成"]')
                ele12 = find_element(self.driver, loc12, ele_type=1, wait_time=5)
                if ele11 == 0 or ele12 == 0:
                    self.assertFalse(True, "没有打开 social的报告页面")
                ele12.click()
            else:
                pass
        except Exception as e:
            logging.critical("打开 social 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_08_openCar(self):
        """打开违章页面"""
        car_no = "88888"
        phone_no = createPhone()
        try:
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            # 点击违章
            loc = (By.XPATH, '//android.view.View[@text="违章"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=3)
            ele.click()
            # 打开车违章h5页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=15)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "违章", "没有打开 违章 页面")
            # 输入车牌号
            loc3 = (By.XPATH, '//android.widget.EditText[@text="请输入车牌号"]')
            ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
            ele3.clear()
            ele3.send_keys(car_no)
            # 输入手机号
            loc4 = (By.XPATH,  '//android.widget.EditText[@text="接收违章短信的手机号"]')
            ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
            ele4.clear()
            ele4.send_keys(phone_no)
            # 点击查询
            loc5 = (By.XPATH, '//android.widget.Button[@text="查询"]')
            ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
            ele5.click()
            loc6 = (By.XPATH, '//android.widget.TextView[@text="违章详情"]')
            ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=120)
            logging.info("---" + ele6.text)
            self.assertEqual(ele6.text, "违章详情", "没有打开 违章详情 界面")
            loc7 = (By.XPATH, "//android.view.View[@text='完成']")
            ele7 = scroll_local(self.driver, loc7, "完成")
            ele7.click()
        except Exception as e:
            logging.critical("打开 违章页面 有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_09_withdrawMoney(self):
        """打开余额提现页面，走完贷款产品去申请流程"""
        try:
            loc = (By.XPATH, '//android.widget.Image[@text="立即提现按钮"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 跳到余额提现页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "余额提现", "没有打开余额提现页面")
            # 获取实名认证状态
            tmp = self.get_certification_status('实名认证')
            self.name_cer = tmp[0]
            # 获取xxx认证状态
            tmp2 = self.get_certification_status('xxx认证')
            self.tele_cer = tmp2[0]
            # 当实名和xxx都认证时，才能进行下一步跳转
            if self.name_cer == "已认证" and self.tele_cer == "已认证":
                loc3 = (By.XPATH, '//android.widget.Button[@text="下一步"]')
                ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
                ele3.click()
                loc4 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
                logging.info("---进入 " + ele4.text)
                self.assertEqual(ele4.text, "余额提现", "没有打开余额提现-去申请页面")
                loc5 = (By.XPATH, '//android.widget.Button[@text="去申请"]')
                ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
                ele5.click()
                loc6 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarLeftTitle')
                ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
                logging.info("---进入 " + ele6.text)
                self.assertEqual(ele6.text, "文章超市", "没有打开 文章超市 界面")
                # 判断页面中 是否加载了h5内容
                loc7 = (By.ID, 'app')
                ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
            else:
                loc3 = (By.XPATH, '//android.widget.Button[@text="下一步"]')
                ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
                ele3.click()
                handle_alert(self.driver, "确认", number=1, wait_time=5)
        except Exception as e:
            logging.critical("打开 余额提现 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "余额", 3)

    @unittest.skipIf(False, '暂不执行')
    def test_10_othersAction(self):
        """执行随机动作"""
        try:
            random_actions(self.driver)
        except Exception as e:
            logging.critical("执行随机动作出错", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()