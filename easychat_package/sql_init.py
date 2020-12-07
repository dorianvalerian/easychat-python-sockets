import mysql.connector


def initialise_db(server_pwd):
    global con
    con=mysql.connector.connect(
        host="localhost",
        user="root",
        #region
        password=server_pwd
        #endregion
    )

    cur = con.cursor()

    cur.execute("SHOW DATABASES like 'easychat'")
    count3=0
    for i in cur:
        count3+=1

    if count3==0:
        cur.execute("CREATE DATABASE easyChat")
        

    cur.execute("USE easyChat")

    cur.execute("show tables like 'chatrecord'")
    count1=0
    for i in cur:
        count1+=1

    cur.execute("show tables like 'lastchat'")
    count2=0
    for i in cur:
        count2+=1

    if count1==0:
        cur.execute("CREATE TABLE chatrecord (time varchar(50), name VARCHAR(255), message VARCHAR(255))")

    if count2==0:
        cur.execute("CREATE TABLE lastchat (time varchar(50), name VARCHAR(255), message VARCHAR(255))")
        cur.execute("insert into lastchat values('NULL','NULL','NULL')")
        con.commit()
