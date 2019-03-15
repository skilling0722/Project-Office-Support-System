import pymysql

def write_memo (user_name, type, title, content, date, time):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    time = date + ' ' + time + ':00'


    inspection="SELECT memo_name FROM Memo_management WHERE member_num=%s AND memo_name=%s"
    cursor.execute(inspection, (user_name, title))
    num = 0

    while (cursor.rowcount != 0):
        num += 1
        cursor.execute(inspection, (user_name, title + '(' + str(num) + ')'))

    if (num != 0):
        title = title + '(' + str(num) + ')'

    insert="INSERT INTO Memo_management VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(insert, (user_name, type, title, content, time))
    
    con.commit()
    con.close()

#def delete_memo (user_name, title):
def delete_memo (user_name, title):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    #delete="DELETE FROM Memo_management WHERE member_num=%s AND memo_name=%s"
    delete="DELETE FROM Memo_management WHERE member_num = %s AND memo_name=%s"
    cursor.execute(delete, (user_name, title))

    con.commit()
    con.close()

def change_memo(user_name, time):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    change = "UPDATE Memo_management SET memo_type = 0 WHERE member_num = %s AND memo_time = %s"
    cursor.execute(change, (user_name, time))

    con.commit()
    con.close()

def get_time(user_name, title):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()
    
    get_time="SELECT memo_time FROM Memo_management WHERE memo_name = %s"

    cursor.execute(get_time, (title))

    time = cursor.fetchone()

    con.commit()
    con.close()
    return time

def alarm_view(user_name, time):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    view = "SELECT memo_name, memo_text, memo_time FROM Memo_management WHERE member_num = %s AND memo_time = %s"
    cursor.execute(view, (user_name, time))

    result = cursor.fetchall()

    con.commit()
    con.close()

    return result

def view_memo(user_name):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    view = "SELECT * FROM Memo_management WHERE member_num = %s"
    #view = "SELECT * FROM Memo_management"
    cursor.execute(view, (user_name))


    result = cursor.fetchall()

    con.commit()
    con.close()

    return result

def count_memo(user_name):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    search = "SELECT * FROM Memo_management WHERE member_num = %s"
    #search = "SELECT * FROM Memo_management"        #회원에 맞는거 탐색으로 변경해야함 ㅇ 

    cursor.execute(search,(user_name))

    count = cursor.rowcount

    con.commit()
    con.close()
    return count

def alarm_to_general(user_name, title):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    change = "UPDATE Memo_management SET memo_type = 0 WHERE member_num = %s AND memo_name = %s"
    cursor.execute(change, (user_name, title))

    con.commit()
    con.close()

def general_to_alarm(time, user_name, title):
    con = pymysql.connect(host= 'root.camyxyxscvxt.ap-northeast-2.rds.amazonaws.com', user= 'porsche', password= 'root1234', db= 'OSS_db', charset= 'utf8mb4')
    cursor = con.cursor()

    change = "UPDATE Memo_management SET memo_type = 1, memo_time = %s WHERE member_num = %s AND memo_name = %s"
    cursor.execute(change, (time, user_name, title))

    con.commit()
    con.close()
