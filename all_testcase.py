# coding=utf-8

import HTMLTestRunner
import os
import time
import unittest
import logging

# 用例路径
case_path = os.path.join(os.getcwd(), 'test_case')
# 报告存放路径
report_path = os.path.join(os.getcwd(), 'report')
# 日志路径
log_path = os.path.join(os.getcwd(), 'logs')
try:
    os.mkdir(report_path)
except FileExistsError:
    logging.warning("%s 路径已经存在，继续" % report_path)
else:
    logging.warning("%s 路径创建失败，继续" % report_path, exc_info=True)
try:
    os.mkdir(log_path)
except FileExistsError:
    logging.warning("%s 路径已经存在，继续" % log_path)
else:
    logging.warning("%s 路径创建失败，继续" % report_path, exc_info=True)


def all_case(case_path):
    testcase = unittest.TestSuite()
    logger.debug(case_path)
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test_*.py', top_level_dir=None)
    logger.debug(discover)
    for test_suite in discover:
        for test_case in test_suite:
            logger.debug(test_case)
            testcase.addTest(test_case)
    return testcase


if __name__ == '__main__':
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    log_name = nowtime + '.log'
    logfile = os.path.join(log_path, log_name)
    # 创建文件handle 以及输出控制台handle
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    logger.addHandler(ch)

    filename = nowtime + '.html'
    rep_path = os.path.join(report_path, filename)
    fp = open(rep_path, 'wb')
    # 定义测试报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'曳云测试app测试报告', description=u'用例执行情况')
    # .login()
    runner.run(all_case(case_path))
    fp.close()
    # login_logout.logout()
