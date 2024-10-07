import pymysql


def getDb():
    connection = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Mmt17211314@",
        db="xxq",
        charset='utf8mb4'
    )
    return connection


def execSql(sql):
    connection = getDb()

    # 2.创建游标
    cursor = connection.cursor()

    # 4.执行sql
    affect_row = cursor.execute(sql)
    print(f"受影响行数为{affect_row}")
    if affect_row > 0:
        print("增加成功")
    else:
        print("增加失败")
    # 5.提交更改
    connection.commit()
    # 6.关闭游标对象
    cursor.close()
    # 7.关闭连接对象
    connection.close()
    return affect_row


def selectSql(sql):
    # 2.创建游标
    connection = getDb()
    cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)

    # 3.定义sql
    # sql = "select * from users where email=%s"

    # 4.执行sql 并且返回得到结果的行数
    row_num = cursor.execute(sql)
    # 5.调用fetchone()获取一条记录
    # row = cursor.fetchone()
    # 6.关闭游标对象
    rows = cursor.fetchall()
    cursor.close()
    # 7.关闭连接对象
    connection.close()
    return rows
