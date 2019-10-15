# -*- coding: utf-8 -*-
from public.login_logout import driver
from public.common_method import *
import unittest
import logging


class CreditMyPage(unittest.TestCase):
    """打开app的 我的 页面"""

    @classmethod
    def setUpClass(self):
        logging.info("开始 我的页面 内容测试\n")
        self.driver = driver
        # login_logout.login()

    @classmethod
    def tearDownClass(self):
        # login_logout.logout()
        self.driver.quit()
        logging.info("\n结束 我的页面 内容测试\n")

    @unittest.skipIf(False, '暂不执行')
    def test_01_1_my(self):
        """打开我的页面"""
        try:
            openIndex(self.driver, "我的", 4)
        except Exception as e:
            logging.critical("打开 我的 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_01_2_nickname(self):
        """点击顶部昵称，进入个人信息"""
        try:
            # 点击顶部昵称
            loc = (By.ID, 'com.yeyun.app.demoapp:id/tvNickName')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 进入到 个人信息界面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            open_page(self.driver, "个人信息", loc2)
            # 找到昵称按钮，点击
            loc3 = (By.ID, 'com.yeyun.app.demoapp:id/llNickname')
            ele3 = find_element(self.driver, loc3, ele_type=1)
            ele3.click()
            # 进入设置昵称
            loc4 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele4.text)
            self.assertEqual(ele4.text, "设置昵称", "没有打开 设置昵称 页面")
            # 设置昵称
            loc5 = (By.ID, 'com.yeyun.app.demoapp:id/etEditNickname')
            ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
            ele5.clear()
            ele5.send_keys("修改" + get_time(1))
            # 点击完成
            loc6 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarRight1_Text')
            ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
            ele6.click()
            loc7 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            open_page(self.driver, "个人信息", loc7)
            # 点击返回
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 个人信息 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_02_order(self):
        """我的订单"""
        # 循环第一页报告，分别点击报告详情
        try:
            # 点击我的订单
            loc = (By.XPATH, '//android.widget.TextView[@text="我的订单"]')
            ele = find_element(self.driver, loc, ele_type=1)
            ele.click()
            # 进入我的订单列表页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "我的订单", "没有打开 我的订单 页面")
            # 获取所有包含文字为 检测的标签，以前确定订单数量
            xpath_name = '//android.webkit.WebView[@text="我的订单"]/android.view.View/android.view.View/android.view.View/android.view.View'
            loc = (By.XPATH, xpath_name)
            ele = find_element(self.driver, loc, ele_type=4, wait_time=5)
            r_l = len(ele)
            # logging.info(r_l)
            if r_l == 0:
                logging.info("页面没有报告")
            else:
                if r_l == 1:
                    r_l == 2
                for i in range(r_l-1):
                    logging.info("正在查看第 %s 个报告" % (i + 1))
                    # 点击每个报告的 报告状态，来进入报告详情页面
                    loc = (By.XPATH, xpath_name + '[%s]/android.view.View[contains(@text, "检测")]' % (i+1))
                    # logging.info(loc)
                    if i != 0 and i % 3 == 0:
                        # 滑动找到元素，如果不使用滑动，则无法找到app 第一页之后的数据
                        swipe_up(driver, 2000, y1=0.95, y2=0.1)
                    # 获取 报告类型
                    # ele = scroll_local(self.driver, loc, "需要点击的报告")
                    # 上面步骤已经获取了所有 “检测” 标签的位置， 根据数组下标来确认 报告类型
                    ele = find_element(self.driver, loc, ele_type=1, wait_time=10)
                    # 获取报告状态， 根据 报告类型的 第一个弟弟同级节点 来获取到 报告状态
                    loc2 = (By.XPATH, xpath_name + '[%s]/android.view.View[contains(@text, "检测")]' % (i+1) + "/following-sibling::android.view.View[1]")
                    ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=10)
                    r_t = ele.text
                    logging.info("-->报告类型为：%s<--" % r_t)
                    r_s = ele2.text
                    logging.info("-->报告状态为：%s<--" % r_s)
                    ele.click()
                    self.handle_reportDetail(r_s, r_t)
                    time.sleep(1)
                    if i == 5:
                        break
        except Exception as e:
            logging.critical("报告页未找到报告，或者查找出错，请检查 ", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_03_coupon(self):
        """打开优惠券页面"""
        try:
            # 点击优惠券
            loc = (By.XPATH, '//android.widget.TextView[@text="优惠券"]')
            ele = find_element(self.driver, loc, ele_type=1)
            ele.click()
            # 进入优惠券页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "优惠券", "没有打开 优惠券 页面")
            # 点击 领取优惠券按钮，弹出弹窗
            loc3 = (By.XPATH, '//android.view.View[@text="关注微信公众号，参与活动领优惠券"]')
            ele3 = find_element(self.driver, loc3, ele_type=1)
            ele3.click()
            handle_alert(self.driver, "稍后再去", number=1)
            # 点击返回
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 优惠券 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_04_help(self):
        """帮助与反馈"""
        try:
            # 点击帮助与反馈
            loc = (By.XPATH, '//android.widget.TextView[@text="帮助与反馈"]')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 进入问题列表
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            self.assertEqual(ele2.text, "帮助中心", "没有打开 帮助中心 界面")
            # 需要先滚动到页面底部
            # 点击反馈意见按钮
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            swipe_up(driver, 2000, y1=0.95, y2=0.1)
            loc3 = (By.XPATH, "//android.widget.Button[@text='反馈意见']")
            ele3 = scroll_local(self.driver, loc3, "反馈意见")
            ele3.click()
            # 进入意见反馈页面
            loc4 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele4 = find_element(self.driver, loc4, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele4.text)
            self.assertEqual(ele4.text, "意见反馈", "没有打开 意见反馈 界面")
            # 点击吐槽内容
            loc5 = (By.ID, 'com.yeyun.app.demoapp:id/etFeedBackContent')
            ele5 = find_element(self.driver, loc5, ele_type=1, wait_time=5)
            ele5.send_keys(createChineseName() + get_time(2))
            # 点击联系方式
            loc6 = (By.ID, 'com.yeyun.app.demoapp:id/etFeedBackContact')
            ele6 = find_element(self.driver, loc6, ele_type=1, wait_time=5)
            ele6.send_keys(createPhone())
            # 点击提交
            loc7 = (By.ID, 'com.yeyun.app.demoapp:id/tvSubmitBtn')
            ele7 = find_element(self.driver, loc7, ele_type=1, wait_time=5)
            ele7.click()
            # 打开反馈成功页面
            loc8 = (By.XPATH, '//android.widget.TextView[@text="反馈成功"]')
            ele8 = find_element(self.driver, loc8, ele_type=1, wait_time=5)
            # 点击关闭按钮
            loc9 = (By.ID, 'com.yeyun.app.demoapp:id/tvClose')
            ele9 = find_element(self.driver, loc9, ele_type=1, wait_time=5)
            ele9.click()
            # 点击返回
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开 帮助与反馈 页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_05_wechat(self):
        """点击微信公众号"""
        try:
            # 点击微信公众号
            loc = (By.ID, 'com.yeyun.app.demoapp:id/llWeChatAccount')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 打开弹窗
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/md_title')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---打开 " + ele2.text)
            self.assertEqual(ele2.text, "公众号已成功复制到剪贴板", "没有打开 微信公众号弹窗")
            # 点击 稍后再去 按钮，返回
            handle_alert(self.driver, "稍后再去")
        except Exception as e:
            logging.critical("打开我的页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 将app置于后台在重新打开，否则后续步骤中直接定位的话，获取不到当前activity的相关内容
            driver.background_app(2)
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_06_share(self):
        """点击 推荐给好友 按钮"""
        try:
            # 点击推荐给好友按钮
            loc = (By.ID, 'com.yeyun.app.demoapp:id/llShare')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 打开弹窗
            loc2 = (By.XPATH, '//android.widget.TextView[@text="选择要分享到的平台"]')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---打开 " + ele2.text)
            self.assertEqual(ele2.text, "选择要分享到的平台", "没有打开 分享界面")
            # 点击取消分享
            loc3 = (By.XPATH, '//android.widget.TextView[@text="取消分享"]')
            ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
            ele3.click()
        except Exception as e:
            logging.critical("打开我的页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 将app置于后台在重新打开，否则直接过去的话，获取不到当前activity的相关内容
            driver.background_app(2)
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_07_protocol(self):
        """点击用户服务与协议"""
        try:
            # 点击 协议按钮
            loc = (By.ID, 'com.yeyun.app.demoapp:id/llUserProtocol')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=10)
            ele.click()
            # 打开协议页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=10)
            logging.info("---进入 " + ele2.text)
            loc3 = (By.XPATH, '//android.webkit.WebView/android.view.View/android.view.View/android.view.View[@text="用户服务协议"]')
            ele3 = find_element(self.driver, loc3, ele_type=1, wait_time=5)
            self.assertEqual(ele3.text, "用户服务协议", "没有打开 用户服务协议 页面")
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开我的页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_08_about(self):
        """点击关于我们"""
        try:
            # 点击关于我们
            loc = (By.ID, 'com.yeyun.app.demoapp:id/llAbout')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            ele.click()
            # 进入关于我们页面
            loc2 = (By.ID, 'com.yeyun.app.demoapp:id/tvAppName')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
            logging.info("---进入 " + ele2.text)
            assert ele2.text is not None, "登录没有成功"
            self.driver.keyevent(4)
        except Exception as e:
            logging.critical("打开我的页面有异常", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "我的", 4)

    @unittest.skipIf(False, '暂不执行')
    def test_09_othersAction(self):
        """执行随机动作"""
        try:
            random_actions(self.driver)
        except Exception as e:
            logging.critical("执行随机动作出错", exc_info=True)
            get_screenshot(self.driver)
            self.assertFalse(True)

    def handle_reportDetail(self, r_s, r_t):
            """报告页点击打开后的处理方法"""
            report_status = ["待支付", "交易成功", "已关闭"]
            report_type = ["黑名单检测", "xxx检测", "通讯录"]
            loc = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=10)
            logging.info("---进入 " + ele.text)
            assert ele.text == "订单详情", "没有打开 订单详情 界面"
            if r_s in report_status:
                if r_s == "待支付":
                    loc = (By.XPATH, '//android.widget.Button[@text="立即支付"]')
                    ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
                    logging.info("---进入 " + ele.text)
                    assert ele.text == "立即支付", "没有找到 立即支付 按钮"
                    # 点击返回
                    driver.keyevent(4)
                elif r_s == "交易成功":
                    if r_t in report_type:
                        loc = (By.XPATH, '//android.widget.Button')
                        ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
                        if ele.text == "查看报告":
                            ele.click()
                            loc = (By.ID, 'com.yeyun.app.demoapp:id/viewBarTitle')
                            ele = find_element(self.driver, loc, ele_type=1, wait_time=10)
                            logging.info("---进入 " + ele.text)
                            assert "报告详情" in ele.text, "没有打开 %s 界面" % ele.text
                        elif ele.text == "报告生成中":
                            pass
                    else:
                        logging.warning("没有找到: %s 报告类型" % r_t)
                    # 点击返回
                    driver.keyevent(4)
                elif r_s == "已关闭":
                    loc = (By.XPATH, '//android.widget.Button[@text="立即检测"]')
                    ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
                    logging.info("---进入 " + ele.text)
                    assert ele.text == "立即检测", "没有找到 立即检测 按钮"
                    # 点击返回
                    driver.keyevent(4)
                else:
                    logging.warning("状态报告异常")
            else:
                logging.warning("没有找到此报告的状态，请检查")


if __name__ == "__main__":
    unittest.main()