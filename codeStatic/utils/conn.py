import pymysql
# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', db='code_stat',charset="utf8")
# 创建游标
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)