# -*- coding: utf-8 -*-
from public.login_logout import driver
from public.common_method import *
import unittest


class CreditLoanMarket(unittest.TestCase):
    """打开app的 文章超市页面"""
    @classmethod
    def setUpClass(self):
        print("开始文章页面内容测试\n")
        self.driver = driver
        # login_logout.login()

    @classmethod
    def tearDownClass(self):
        # login_logout.logout()
        # self.driver.quit()
        print("\n结束文章页面内容测试\n")

    @unittest.skipIf(False, '暂不执行')
    def test_01_loanMarket(self):
        """打开文章页面"""
        try:
            openIndex(self.driver, "文章超市", 2)
            loc = (By.ID, 'com.yeyun.app.demoapp:id/viewBarLeftTitle')
            ele = find_element(self.driver, loc, ele_type=1, wait_time=5)
            print("---进入 " + ele.text)
            self.assertEqual(ele.text, "文章超市", "没有打开 文章超市 界面")
            # 判断页面中 是否加载了h5内容
            loc2 = (By.ID, 'app')
            ele2 = find_element(self.driver, loc2, ele_type=1, wait_time=5)
        except Exception as e:
            print("打开 文章超市 页面有异常，err: %s" % e)
            get_screenshot(self.driver)
            self.assertFalse(True)
        finally:
            # 返回到首页
            openIndex(self.driver, "文章超市", 2)

    @unittest.skipIf(False, '暂不执行')
    def test_02_othersAction(self):
        """执行随机动作"""
        try:
            random_actions(self.driver)
        except Exception as e:
            print("执行随机动作出错，err: %s" % e)
            get_screenshot(self.driver)
            self.assertFalse(True)


if __name__ == "__main__":
    unittest.main()