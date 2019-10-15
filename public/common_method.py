# -*- coding: utf-8 -*-
import logging
import os
import random
import string
import time
import requests
import logging
# 获取屏幕分辨率
from datetime import date, timedelta
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def find_element(driver, loc, ele_type=1, wait_time=10):
    """
    分装查找元素的方法， 使用智能等待来查找元素
    :param wait_time: 等待时间设置,默认10s
    :param driver: 实例
    :param loc: loc: 定位方式以及元素，如(By.XPATH, '//android.webkit.WebView[@text="风险报告"])
    :param ele_type:
        1：元素加载到dom中，
        2：元素加载dom并且可见，直到元素消失，用于打开页面后有弹窗的情况
        3. 元素加载到dom中，并且可见
    :return: 返回 webelement对象
    """
    ele = 1  # 1默认标识找到，0标识没有找到元素
    if ele_type == 1:
        try:
            ele = WebDriverWait(driver, wait_time, 0.5).until(
                EC.presence_of_element_located(loc))
        except Exception as e:
            ele = 0
            logging.warning("没有定位到元素，定位方式: " + format(loc) + "errmsg: %s" % e)
    elif ele_type == 2:
        try:
            ele = WebDriverWait(driver, wait_time, 0.5).until_not(
                EC.visibility_of_element_located(loc))
        except Exception as e:
            ele = 0
            logging.warning("没有定位到元素，定位方式: " + format(loc) + "errmsg: %s" % e)
    elif ele_type == 3:
        try:
            ele = WebDriverWait(driver, wait_time, 0.5).until(
                EC.visibility_of_element_located(loc))
        except Exception as e:
            ele = 0
            logging.warning("没有定位到元素，定位方式: " + format(loc) + "errmsg: %s" % e)
    elif ele_type == 4:
        try:
            ele = WebDriverWait(driver, wait_time, 0.5).until(
                EC.presence_of_all_elements_located(loc))
        except Exception as e:
            ele = 0
            logging.warning("没有定位到元素，定位方式: " + format(loc) + "errmsg: %s" % e)
    return ele


def open_page(driver, title_tmp, loc):
    """
    判断是否打开了 一个新的页面
    :param title_tmp: 页面标题
    :param driver: driver 实例
    :param loc: 定位方式及内容
    :return:
    """
    title_flag = False
    try:
        ele = find_element(driver, loc, ele_type=1, wait_time=10)
        '''判断title，返回布尔值'''
        if ele.is_displayed():
            if ele.text == title_tmp:
                logging.info("打开了页面： %s" % ele.text)
                title_flag = True
        else:
            get_screenshot(driver)
            assert False, "没有打开 %s 页面"
    except Exception as e:
        return title_flag


def get_size(driver):
    """
    获取屏幕尺寸
    :param driver:
    :return:
    """
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    # logging.info(x,y)
    return (x, y)


# 向左滑动
def swipe_left(driver, t):
    l = get_size(driver)
    x1 = int(l[0] * 0.75)
    y1 = int(l[1] * 0.5)
    x2 = int(l[0] * 0.25)
    driver.swipe(x1, y1, x2, y1, t)


# 向右滑动
def swipe_right(driver, t):
    l = get_size(driver)
    x1 = int(l[0] * 0.25)
    y1 = int(l[1] * 0.5)
    x2 = int(l[0] * 0.75)
    driver.swipe(x1, y1, x2, y1, t)


# 向上滑动
def swipe_up(driver, t, y1=0.8, y2=0.4):
    l = get_size(driver)
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.8)
    y2 = int(l[1] * 0.4)
    driver.swipe(x1, y1, x1, y2, t)


# 向下滑动
def swipe_down(driver, t):
    l = get_size(driver)
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.25)
    y2 = int(l[1] * 0.75)
    driver.swipe(x1, y1, x1, y2, t)


# 查找元素，没找到滑动
def scroll_local(driver, loc, button_msg, wait_time=10):
    """
    :param wait_time:
    :param driver: driver 实例
    :param loc: 定位方式以及元素，如(By.XPATH, '//android.webkit.WebView[@text="报告"])
    :param button_msg:  可以是 定位元素的标签 或者随意写
    :return: 返回 一个webelement 对象
    """
    # 获取屏幕高度，根据高度来获取每次滑动的高度
    l = get_size(driver)
    y = int(l[1])
    x = 1
    while x <= 10:
        # js="var q=document.documentElement.scrollTop=1000"
        # driver.execute_script(js)
        try:
            logging.info("尝试滑动查找元素,次数 %d" % x)
            ele = WebDriverWait(driver, wait_time, 0.5).until(
                EC.visibility_of_element_located(loc))
            if ele.is_displayed():
                logging.info("滑动查找到的元素：%s" % button_msg)
                break
            else:
                driver.execute_script("window.scrollBy(0,%d)" % y)
                time.sleep(1)
        except Exception as e:
            logging.critical("滑动查找元素失败,次数 %d, err: %s" % (x, e))
            driver.execute_script("window.scrollBy(0,%d)" % y)
            x = x + 1
            time.sleep(1)
    return ele


def handle_alert(driver, alter_msg, number=5, wait_time=10):
    """
    function: 弹窗处理
    1.传driver
    2.number，判断弹窗次数，默认给5次
    3. alter_msg, 弹窗的 按钮文字，如“确定”“取消”
    其它：
    WebDriverWait里面0.5s判断一次是否有弹窗，2s超时
    """
    # x标志位，如果x=0，未找到弹窗
    x = 0
    for i in range(number):
        logging.info("尝试处理弹窗,次数:%d" % (i + 1))
        try:
            loc2 = ("xpath", "//*[@text='%s']" % alter_msg)
            logging.info("---点击 %s ---" % alter_msg)
            ele2 = WebDriverWait(driver, wait_time, 0.5).until(EC.visibility_of_element_located(loc2))
            if ele2.is_displayed():
                x = 1
                ele2.click()
                logging.info("采用 %s按钮" % alter_msg + "关闭弹窗")
                break
        except:
            pass
    if x == 0:
        logging.warning("没有找到相关弹窗，尝试了: %d 次" % (i + 1))
        logging.info("采用 返回键返回，关闭弹窗")
        driver.keyevent(4)
        return x


def other_alert(driver, alert_msg=[], number=1):
    if len(alert_msg) > 0:
        alert_tmp = alert_msg
    else:
        alert_tmp = ["业务出错", "服务异常", "失效", "内部错误"]
    for a_m in alert_tmp:
        loc = (By.XPATH, "//*[contains(text(),'%s')]" % a_m)
        handle_alert(driver, a_m, loc, number)


# 创建截图目录
pic_path = os.path.join(os.getcwd(), 'screenshot')
try:
    os.mkdir(pic_path)
except FileExistsError:
    logging.warning("%s 路径已经存在，继续" % pic_path)
else:
    logging.warning("%s 路径创建失败，继续" % pic_path, exc_info=True)
#  截图


def get_screenshot(driver):
    logging.info("请在screenshot目录中查看相关截图")
    now_time = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    pic_name = now_time + '.png'
    screenshot_name = os.path.join(pic_path, pic_name)
    try:
        driver.get_screenshot_as_file(screenshot_name)
    except Exception as e:
        logging.warning("截图失败", exc_info=True)


# 判断是否回到首页，如果没有，点击返回键，继续判断
def openIndex(driver, tab_title, index, number=5):
    # 判断是不是打开了首页
    # 设置一个最深的嵌套层数：5
    """
    tab_title: 底部tab栏对应的 标题
    index： app底部tab栏的索引，从左往右
            首页：0 内容：1 文章：2 我的：3
    """
    for i in range(number):
        try:
            # logging.info(driver.page_source)
            logging.info("尝试进入 %s 页面, 次数:%d" % (tab_title, i + 1))
            loc = (By.XPATH,
                   '//android.widget.TabWidget[@resource-id="android:id/tabs"]/android.widget.LinearLayout[%d]' % index)
            # loc = (By.XPATH, '//android.widget.TextView[@text="%s"]' % tab_title)
            # loc = (By.ID, 'com.yeyun.app.demoapp:id/tvTitle')
            # ele = find_element(driver, loc, ele_type=4)
            ele = WebDriverWait(driver, 20, 0.5).until(
                EC.presence_of_element_located(loc))
            # ele = driver.find_element_by_xpath("//*[@resource-id='com.yeyun.app.demoapp:id/tvTitle'][@text='我的']")
            # 说明查找到元素
            if ele.is_displayed():
                ele.click()
                if index == 4:
                    ele2 = WebDriverWait(driver, 2, 0.5).until(
                        EC.presence_of_element_located((By.ID,
                                                        'com.yeyun.app.demoapp:id/rlMy')))
                    logging.info("当前页面--" + "我的")
                    break
                elif index == 1:
                    ele2 = WebDriverWait(driver, 2, 0.5).until(
                        EC.presence_of_element_located((By.ID,
                                                        'com.yeyun.app.demoapp:id/viewBarHomeTitle')))
                    logging.info("当前页面--" + ele2.text)
                    if ele2.text == tab_title:
                        logging.info("已经是在%s页面了" % tab_title)
                        break
                elif index == 2 or index == 3:
                    ele2 = WebDriverWait(driver, 2, 0.5).until(
                        EC.presence_of_element_located((By.ID,
                                                        'com.yeyun.app.demoapp:id/viewBarLeftTitle')))
                    logging.info("当前页面--" + ele2.text)
                    if ele2.text == tab_title:
                        logging.info("已经是在%s页面了" % tab_title)
                        break
            else:
                logging.info("点击返回按钮")
                driver.keyevent(4)
        except Exception as e:
            logging.critical("尝试返回%s页面失败, 次数：%d err:%s" % (tab_title, i + 1, e))
            logging.info("点击返回按钮")
            driver.keyevent(4)
            # # 列举几种返回时可能碰到的提示情况
            # # 由于没有办法判断是否出现了弹窗
            # message_list = ['确认', '取消', '总是允许', '知道了']
            # for message in message_list:
            #     handle_alert(driver, message, number=1)


# 执行随机的动作
def random_actions(driver):
    # ran_count 随机执行的动作数
    # ran_list 执行的动作列表
    # ran_act 随机执行的 动作
    # sample()方法返回随机从列表,随机返回几个
    """
    swipeDown, 下滑
    swipeUp, 上滑
    swipeLeft,左滑
    swipeRight,右滑
    driver.background_app, 将app置于后台然后重新打开
    """
    ran_count = random.randint(1, 4)
    ran_list = [swipe_down(driver, 1000), swipe_up(driver, 1000), driver.background_app(3), swipe_left(driver, 1000),
                swipe_right(driver, 1000)]
    ran_act = random.randint(1, len(ran_list))
    temp = random.sample(ran_list, ran_act)
    for i in range(ran_count):
        for action in temp:
            logging.info("执行随机动作 %s" % action)
            action
            time.sleep(2)


# 创建一个随机8位密码
def create_passwd():
    tmp = random.sample(string.ascii_letters + string.digits, 8)
    password = ''.join(tmp)
    return password


# 获取时间
def get_time(time_type=1):
    """
    输入不同的时间类型，转化时间
    :param time_type: 1.格式 20181201125832 2.格式 2018-12-01 23:21:09 3.时间戳1538271871
    :return: 返回时间
    """
    time_tmp = ""
    if time_type == 1:
        time_tmp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    elif time_type == 2:
        time_tmp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif time_type == 3:
        # 获取时间戳，然后四舍五入
        time_tmp = int(round(time.time()))
    return time_tmp



# 身份证地区编号文件路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DC_PATH = BASE_DIR + "/public/addr.py"


# 随机生成手机号码
def createPhone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153",
               "155", "156", "157", "158", "159", "170", "177", "179", "186", "187", "188", "199"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


# 随机生成身份证号
def getdistrictcode():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DC_PATH = BASE_DIR + "/public/districtcode.txt"
    with open(DC_PATH, 'r', encoding='UTF-8') as file:
        data = file.read()
    districtlist = data.split('\n')
    global codelist
    codelist = []
    for node in districtlist:
        # logging.info(node)
        if node[10:11] != ' ':
            state = node[10:].strip()
        if node[10:11] == ' ' and node[12:13] != ' ':
            city = node[12:].strip()
        if node[10:11] == ' ' and node[12:13] == ' ':
            district = node[14:].strip()
            code = node[0:6]
            codelist.append({"state": state, "city": city, "district": district, "code": code})


# 调用此方法先 生成地区编号的列表
getdistrictcode()


def gennerator():
    if not codelist:
        id = codelist[0]['code']
    id = codelist[random.randint(0, len(codelist))]['code']  # 地区项
    id = id + str(random.randint(1930, 2013))  # 年份项
    da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
    id = id + da.strftime('%m%d')
    id = id + str(random.randint(100, 300))  # ，顺序号简单处理

    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                 '10': '2'}  # 校验码映射
    for i in range(0, len(id)):
        count = count + int(id[i]) * weight[i]
    id = id + checkcode[str(count % 11)]  # 算出校验码
    return id


# 随机生成中文姓名
def createChineseName():
    xing = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

    ming = [
        '的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
        '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
        '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
        '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
        '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
        '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
        '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
        '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
        '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
        '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
        '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性', '马',
        '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让', '母',
        '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军',
        '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
        '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
        '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
        '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
        '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运', '及',
        '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司', '巴',
        '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形', '影',
        '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈', '容',
        '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计', '您',
        '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻', '统',
        '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示', '愿',
        '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社', '算',
        '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息', '功',
        '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图', '具',
        '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引', '食',
        '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试', '怀',
        '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除', '跑',
        '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳', '验',
        '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡',
        '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店', '否',
        '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续',
        '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索',
        '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低',
        '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街',
        '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律',
        '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属',
        '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗',
        '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差',
        '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压',
        '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶',
        '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨',
        '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付',
        '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营',
        '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊', '降',
        '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
        '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预',
        '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误',
        '乾', '坤']

    x = random.randint(1, len(xing)) - 1
    m1 = random.randint(1, len(ming)) - 1
    m2 = random.randint(1, len(ming)) - 1
    return '' + xing[x] + ming[m1] + ming[m2]


if __name__ == "__main__":
    print(createPhone())
    # print(createChineseName())
    # print(gennerator())
    # print(get_phone_info())
    # print(get_time(3))
