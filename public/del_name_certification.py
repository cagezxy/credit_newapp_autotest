# coding:utf-8
import pymysql


class connetDB():
    def __init__(self, type=1):
        # 连接测试环境数据库
        try:
            if type == 1:
                self.conn = pymysql.connect(host='001yeyun.xxxxx',
                                            port=3317,
                                            user='yeyun',
                                            password='yeyun',
                                            database='crs',
                                            charset='utf8')
            if type == 2:
                self.conn = pymysql.connect(host='001yeyun.xxxxx2',
                                            port=3317,
                                            user='yeyun',
                                            password='yeyun',
                                            database='crs',
                                            charset='utf8')
        except Exception:
            print("mysql error ")

    # 查询
    def select(self, sql):
        select_sql = sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(select_sql)
            print("检查sql: %s" % select_sql)
            rs = cursor.fetchall()
            if len(rs) < 1 or len(rs) == False:
                print("没有符合的数据")
            else:
                return rs
        except:
            print("查询出错")
        finally:
            cursor.close()

    # 更新
    def update(self, sql):
        update_sql = sql
        cursor = self.conn.cursor()
        # try:
        print("检查sql: %s" % update_sql)
        cursor.execute(update_sql)
        # 提交到数据库执行
        self.conn.commit()
        # except:
            # 发生错误时回滚
            # print("更新错误，进行回滚")
            # self.conn.rollback()
        # finally:
           # cursor.close()

    # 关闭
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    type = int(input("输入测试环境地址：1：测试空间 2：开发空间\n"))
    db = connetDB(type)
    sql = "del and uid='2001';"
    db.update(sql)
    db.close()
