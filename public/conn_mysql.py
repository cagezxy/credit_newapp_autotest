# coding:utf-8
import pymysql
import logging


class connetDB():
    def __init__(self):
        # 连接测试环境数据库
        try:
            self.conn = pymysql.connect(host='001.yeyun.test.xxxxx',
                                        port=3317,
                                        user='qa',
                                        password='qa',
                                        database='yeun',
                                        charset='utf8')
        except Exception:
            logging.critical("mysql error ", exc_info=True)

    # 查询
    def select(self, sql):
        select_sql = sql
        cursor = self.conn.cursor()
        try:
            cursor.execute(select_sql)
            logging.info("检查sql: %s" % select_sql)
            rs = cursor.fetchall()
            if len(rs) < 1 or len(rs) is False:
                logging.warning("没有符合的数据")
            else:
                return rs
        except:
            logging.critical("查询出错", exc_info=True)
        finally:
            cursor.close()

    # 更新
    def update(self, sql):
        update_sql = sql
        cursor = self.conn.cursor()
        try:
            logging.info("检查sql: %s" % update_sql)
            cursor.execute(update_sql)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # 发生错误时回滚
            logging.critical("更新错误，进行回滚", exc_info=True)
            self.conn.rollback()
        finally:
            cursor.close()

    # 关闭
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = connetDB()
    sql = "select * from  ;"
    db.select(sql)
    db.close()
