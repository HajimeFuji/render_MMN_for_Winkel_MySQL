import os
# Flask から importしてflaskを使えるようにする
import sqlite3, datetime as dt
from flask import Flask, render_template, request, redirect, session
import psycopg2

# appの名前でFlaskアプリを作っていく
app = Flask(__name__)
# ここまでおまじない

app.secret_key="sunabaco"

@app.route("/")
def init():
    return render_template('init.html')

# DBへの接続
@app.route("/index")
def index():
    conn = sqlite3.connect("maintenance.db")
    c=conn.cursor()
    c.execute("select name from users where id = 1")
    user_info = c.fetchone()
    c.close()
    return render_template("index.html", user = user_info)

#追加の処理/そとアイテム
@app.route("/add/item/soto",methods=["POST"])
def add_post_item_soto():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    item = request.form.get("item")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("error_soto.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,item,tablename))
        c.execute("create table %s (taskid INTEGER, item_id INTEGER, date DATE, task TEXT, notice DATE, nt_id INTEGER, PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/soto")

#追加の処理/うちアイテム
@app.route("/add/item/uti",methods=["POST"])
def add_post_item_uti():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    item = request.form.get("item")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    print(tb_list)
    print(type(tb_list))
    print(tb_list[0])
    print(type(tb_list[0]))
    print('---xxx------')
    tbname_list = []
    for row in tb_list:
        print(row[0])
        tbname_list.append(row[0])
    # タプルをリストに変換
    print(tbname_list)
    print(type(tbname_list))
    print('---xxx------')
    print(tablename)
    print(type(tablename))
    print(tablename in tbname_list)
    if tablename in tbname_list:
        return render_template("error_uti.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,item,tablename))
        c.execute("create table %s (taskid INTEGER, item_id INTEGER, date DATE, task TEXT, notice DATE, nt_id INTEGER, PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/uti")

#追加の処理/にわアイテム
@app.route("/add/item/niwa",methods=["POST"])
def add_post_item_niwa():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    item = request.form.get("item")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("error_niwa.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,item,tablename))
        c.execute("create table %s (taskid INTEGER, item_id INTEGER, date DATE, task TEXT, photo TEXT, notice DATE, nt_id INTEGER, PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/niwa")

# DBに保存されているものを表示してみよう
@app.route("/list/soto")
def sotoitem_list():
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # c.execute("select name from users where id = ?" , (user_id,))
    # user_name = c.fetchone()[0]
    c.execute("select id, item from items where ios_id = 1")
    # リスト型にする
    item_list=[]
    # print(c.fetchall())
    for row in c.fetchall():
        #rowの要素を連想配列に記述
        item_list.append({"id":row[0],"item":row[1]})
        # print(item_list)
    c.close()
    return render_template("sotoitem_list.html",sotoitem_list = item_list)

@app.route("/list/uti")
def utiitem_list():
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id, item from items where ios_id = 0")
    item_list=[]
    for row in c.fetchall():
        item_list.append({"id":row[0],"item":row[1]})
    c.close()
    return render_template("utiitem_list.html",utiitem_list = item_list)

@app.route("/list/niwa")
def niwaitem_list():
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id, item from items where ios_id = 2")
    item_list=[]
    for row in c.fetchall():
        item_list.append({"id":row[0],"item":row[1]})
    c.close()
    return render_template("niwaitem_list.html",niwaitem_list = item_list)

# DBから通知を表示してみよう－今週の通知
@app.route("/notice/tasklist")
def notice_tasklist():
    today = dt.date.today()
    # today = today.strftime('%Y/%m/%d')
    # print(today)
    time7 = today + dt.timedelta(days=-7)
    # print(time7)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
        # print(row[0])
    # row[0]をtable_nameの変数としてselect
    # noticeがtoday と一致するタスクをセレクト
        c.execute("select items.item, %s.date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0]), (today,time7,))
        ntlist = []
        notice_list = c.fetchall()
        # print("----yyy--------")
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
                # print(ntlist)
                # print("----zzz--------")
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row3[0] is not None:
                nt_list.append({"item":row3[0],"date":row3[1],"task":row3[2],"notice":row3[3],"id":row3[4],"taskid":row3[5]})
                # print(nt_list)

    #noticeをすべてリストできる
        # notice_list = c.fetchall()
        # for row2 in notice_list:
        #     ntlist.append(row2[0])

    # print('------???-------')
    c.close()
    return render_template("notice_list.html",nt_list = nt_list, today = today, time7 = time7)
    # return "該当する通知はありません"

# 今週の通知表示から実施済みタスクを表示しないようにする－今週の通知
@app.route("/notice/tasklist/nt/<int:id>/<int:taskid>",methods=["POST"])
def notice_tasklist_nt(id,taskid):
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
# まず実施済タスクのnt_idを1にupdateする
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect # noticeがtoday と一致するタスクをセレクト
        c.execute("select items.item, %s.date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0]), (today,time7,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"item":row3[0],"date":row3[1],"task":row3[2],"notice":row3[3],"id":row3[4],"taskid":row3[5]})
    conn.commit()
    c.close()
    return render_template("notice_list.html",nt_list = nt_list, today = today, time7 = time7)

# DBから通知を表示してみよう－先週の通知
@app.route("/notice/tasklist/lw")
def notice_tasklist_lw():
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect
    # noticeがtime7-time14 と一致するタスクをセレクト
        c.execute("select items.item, %s.date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0]), (time7,time14,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"item":row3[0],"date":row3[1],"task":row3[2],"notice":row3[3],"id":row3[4],"taskid":row3[5]})
    c.close()
    return render_template("notice_list_lw.html",nt_list = nt_list, time7 = time7, time14 = time14)

# 先週の通知表示から実施済みタスクを表示しないようにする－先週の通知
@app.route("/notice/tasklist/nt_lw/<int:id>/<int:taskid>",methods=["POST"])
def notice_tasklist_nt_lw(id,taskid):
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
# まず実施済タスクのnt_idを1にupdateする
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect　# noticeがtoday と一致するタスクをセレクト
        c.execute("select items.item, %s.date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0]), (time7,time14,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"item":row3[0],"date":row3[1],"task":row3[2],"notice":row3[3]})
    conn.commit()
    c.close()
    return render_template("notice_list_lw.html",nt_list = nt_list, time14 = time14, time7 = time7)

# DBから通知を表示してみよう－来週の通知
@app.route("/notice/tasklist/nw")
def notice_tasklist_nw():
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
    time_p7 = today + dt.timedelta(days=7)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect
    # noticeがtime7-time14 と一致するタスクをセレクト
        c.execute("select items.item, %s.date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0]), (time_p7,today,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"item":row3[0],"date":row3[1],"task":row3[2],"notice":row3[3],"id":row3[4],"taskid":row3[5]})
    c.close()
    return render_template("notice_list_nw.html",nt_list = nt_list, time_p7 = time_p7, today = today)

# 来週の通知表示から実施済みタスクを表示しないようにする－来週の通知
@app.route("/notice/tasklist/nt_nw/<int:id>/<int:taskid>",methods=["POST"])
def notice_tasklist_nt_nw(id,taskid):
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
    time_p7 = today + dt.timedelta(days=7)
# まず実施済タスクのnt_idを1にupdateする
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    # table_name 取得
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect　# noticeがtoday と一致するタスクをセレクト
        c.execute("select items.item, %s.date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0]), (time_p7,today,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"item":row3[0],"date":row3[1],"task":row3[2],"notice":row3[3]})
    conn.commit()
    c.close()
    return render_template("notice_list_nw.html",nt_list = nt_list, time_p7 = time_p7, today = today)

# そとアイテムの編集
@app.route("/edit/soto/<int:id>")
def edit_item_soto(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select item from items where id=?", (id,))
    item = c.fetchone()[0]
    c.close()
    item = {"id":id, "item":item}
    return render_template("edit_item_soto.html" , item = item)
    
# 変更したデータでそとアイテム更新
@app.route("/edit/soto", methods = ["POST"])
def update_item_soto():
    item_id = request.form.get("id")
    item_id = int(item_id)
    item = request.form.get("item")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("update items set item=? where id = ?", (item,item_id))
    conn.commit()
    c.close()
    return redirect("/list/soto")
    
# うちアイテムの編集
@app.route("/edit/uti/<int:id>")
def edit_item_uti(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select item from items where id=?", (id,))
    item = c.fetchone()[0]
    c.close()
    item = {"id":id, "item":item}
    return render_template("edit_item_uti.html" , item = item)
    
# 変更したデータでうちアイテム更新
@app.route("/edit/uti", methods = ["POST"])
def update_item_uti():
    item_id = request.form.get("id")
    item_id = int(item_id)
    item = request.form.get("item")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("update items set item=? where id = ?", (item,item_id))
    conn.commit()
    c.close()
    return redirect("/list/uti")

# にわアイテムの編集
@app.route("/edit/niwa/<int:id>")
def edit_item_niwa(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select item from items where id=?", (id,))
    item = c.fetchone()[0]
    c.close()
    item = {"id":id, "item":item}
    return render_template("edit_item_niwa.html" , item = item)
    
# 変更したデータでにわアイテム更新
@app.route("/edit/niwa", methods = ["POST"])
def update_item_niwa():
    item_id = request.form.get("id")
    item_id = int(item_id)
    item = request.form.get("item")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("update items set item=? where id = ?", (item,item_id))
    conn.commit()
    c.close()
    return redirect("/list/niwa")

# そとリストからアイテムの削除
@app.route("/del/soto/<int:id>")
def del_item_soto(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    # print(table_name)
    # print(type(table_name))
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/soto")

# うちリストからアイテムの削除
@app.route("/del/uti/<int:id>")
def del_item_uti(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/uti")

# にわリストからアイテムの削除
@app.route("/del/niwa/<int:id>")
def del_item_niwa(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/niwa")

# DBに保存されているタスクをリストしてみよう（うち／そと）
@app.route("/tasklist/<int:id>")
def tasklist(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id from items where id = ?" , (id,))
    id = c.fetchone()[0]
    c.execute("select item from items where id = ?" , (id,))
    item = c.fetchone()[0]
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select taskid, date, task, notice, nt_id from %s" % (table_name))
    tasklist = []
    task_list = []
    for row in c.fetchall():
        # print(row[4])
        tasklist = dict({"taskid":row[0],"date":row[1], "task":row[2],"notice":row[3], "nt_id":row[4]})
        if tasklist["nt_id"] == 1:
            tasklist["nt_id"] = "done"
        else:
            tasklist["nt_id"] = "set"
            # print(tasklist)
        task_list.append(tasklist) 
    c.close()
    return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    # return redirect("/login")

# DBに保存されているタスクをリストしてみよう（にわ）
@app.route("/tasklist_niwa/<int:id>")
def tasklist_niwa(id):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select id from items where id = ?" , (id,))
    id = c.fetchone()[0]
    c.execute("select item from items where id = ?" , (id,))
    item = c.fetchone()[0]
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    # print(table_name)
    # table = "table_name"
    c.execute("select taskid, date, task, photo, notice, nt_id from %s" % (table_name))
    tasklist = []
    task_list = []
    for row in c.fetchall():
        tasklist = dict({"taskid":row[0],"date":row[1], "task":row[2],"photo":row[3],"notice":row[4],"nt_id":row[5]})
        if tasklist["nt_id"] == 1:
            tasklist["nt_id"] = "done"
        else:
            tasklist["nt_id"] = "set"
        task_list.append(tasklist) 
    c.close()
    return render_template("tasklist_niwa.html" , task_list = task_list, table_name = table_name, item = item, id = id)
#     else:
#         return redirect("/login")

# 追加の処理/タスク（うち／そと）
@app.route("/add/tasklist/<int:id>",methods=["POST"])
def add_post_task(id):
    # user_id = session["user_id"]
    date = request.form.get("date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
        #()はタプル型
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("insert into %s values (null,?,?,?,?,?)" % (table_name), (id,date,task,notice,nt_id))
    conn.commit()
    c.close()
    # return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    return redirect("/tasklist/%s" %(id))  

# 通知要否の処理/タスク（うち／そと）
@app.route("/edit/tasklist/nt/<int:id>/<int:taskid>",methods=["POST"])
def edit_post_task_nt(id,taskid):
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    conn.commit()
    c.close()
    return redirect("/tasklist/%s" %(id))  

# 追加の処理/タスク（にわ）
@app.route("/add/tasklist_niwa/<int:id>",methods=["POST"])
def add_post_task_niwa(id):
    # user_id = session["user_id"]
    date = request.form.get("date")
    task = request.form.get("task")
    photo = request.form.get("photo")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
        #()はタプル型
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("insert into %s values (null,?,?,?,?,?,?)" % (table_name), (id,date,task,photo,notice,nt_id))
    conn.commit()
    c.close()
    # return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    return redirect("/tasklist_niwa/%s" %(id))  

# # # 編集変更したデータで更新/タスク/うち、そと
@app.route("/edit/tasklist/<int:id>/<int:taskid>")
def edit_tasklist_get(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select date from %s where taskid=?" % (table_name), (taskid,))
    # task_list = c.fetchall()
    # task_list = []
    # for row in c.fetchall():
    #     task_list.append({"taskid":row[0],"date":row[1],"task":row[2],"notice":row[3]})
    date = c.fetchone()[0]
    c.execute("select task from %s where taskid=?" % (table_name), (taskid,))
    task = c.fetchone()[0]
    c.execute("select notice from %s where taskid=?" % (table_name), (taskid,))
    notice = c.fetchone()[0]   
    c.execute("select nt_id from %s where taskid=?" % (table_name), (taskid,))
    nt_id = c.fetchone()[0] 
    c.close()
    task_list = {"taskid":taskid, "date":date, "task":task, "notice":notice, "nt_id":nt_id}
    return render_template("edit_tasklist.html", task_list = task_list, id = id)

@app.route("/edit/tasklist/<int:id>", methods = ["POST"])
def tasklist_update(id):
    taskid = request.form.get("taskid")
    taskid = int(taskid)
    date = request.form.get("date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set date=? where taskid = ?" %(table_name), (date,taskid,))
    c.execute("update %s set task=? where taskid = ?" %(table_name), (task,taskid,))
    c.execute("update %s set notice=? where taskid = ?" %(table_name), (notice,taskid,))
    c.execute("update %s set nt_id=? where taskid = ?" %(table_name), (nt_id,taskid,))
    conn.commit()
    c.close()
    return redirect("/tasklist/%s" %(id))  
    
# # # 編集変更したデータで更新/タスク/にわ
@app.route("/edit/tasklist_niwa/<int:id>/<int:taskid>")
def edit_tasklist_get_niwa(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select date from %s where taskid=?" % (table_name), (taskid,))
    # task_list = c.fetchall()
    # task_list = []
    # for row in c.fetchall():
    #     task_list.append({"taskid":row[0],"date":row[1],"task":row[2],"notice":row[3]})
    date = c.fetchone()[0]
    c.execute("select task from %s where taskid=?" % (table_name), (taskid,))
    task = c.fetchone()[0]
    c.execute("select photo from %s where taskid=?" % (table_name), (taskid,))
    photo = c.fetchone()[0]
    c.execute("select notice from %s where taskid=?" % (table_name), (taskid,))
    notice = c.fetchone()[0]
    c.close()
    task_list = {"taskid":taskid, "date":date, "task":task, "photo":photo, "notice":notice}
    return render_template("edit_tasklist_niwa.html", task_list = task_list, id = id)

@app.route("/edit/tasklist_niwa/<int:id>", methods = ["POST"])
def tasklist_niwa_update(id):
    taskid = request.form.get("taskid")
    taskid = int(taskid)
    date = request.form.get("date")
    task = request.form.get("task")
    photo = request.form.get("photo")
    notice = request.form.get("notice")
    conn = sqlite3.connect("maintenance.db")
    c =conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set date=? where taskid = ?" %(table_name), (date,taskid,))
    c.execute("update %s set task=? where taskid = ?" %(table_name), (task,taskid,))
    c.execute("update %s set photo=? where taskid = ?" %(table_name), (photo,taskid,))
    c.execute("update %s set notice=? where taskid = ?" %(table_name), (notice,taskid,))
    conn.commit()
    c.close()
    return redirect("/tasklist_niwa/%s" %(id)) 

# タスクリストから タスクの削除(うち/そと)
@app.route("/del/tasklist/<int:id>/<int:taskid>")
def del_tasklist(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from %s where taskid=?" % (table_name), (taskid,))
    c = conn.commit()
    conn.close()
    return redirect("/tasklist/%s" %(id)) 

# タスクリストから タスクの削除(にわ)
@app.route("/del/tasklist_niwa/<int:id>/<int:taskid>")
def del_tasklist_niwa(id,taskid):
    conn = sqlite3.connect("maintenance.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from %s where taskid=?" % (table_name), (taskid,))
    c = conn.commit()
    conn.close()
    return redirect("/tasklist_niwa/%s" %(id)) 

# 削除機能
# @app.route("/del/<int:id>")
# def del_task(id):
#     # DBに接続＿DB処理の準備＿SQL文の実行(taskテーブルのidがid（関数の引数)のもの
#     # のみ削除", (id,)
#     # 保存
#     # 接続終了
#     # /list でリダイレクト

#     conn = sqlite3.connect("maintenance.db")
#     c = conn.cursor()
#     c.execute("delete from %s where id=?" %(table_name), (id,))
#     c = conn.commit()
#     conn.close()
#     return redirect("/tasklist")
    

# 2021.6.15 ログイン機能など-----------------------------------------------------------
# 登録機能

# @app.route("/regist", methods = ["GET"])
#     # GETはHTMLを表示するだけ
# def regist_get():
#     return render_template("regist.html")

# @app.route("/regist", methods=["POST"])
# def regist_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
#     # requestでHTML側からデータを受け取る
    
#     conn = sqlite3.connect("maintenance.db")
#     c = conn.cursor()
#     c.execute("insert into users values(null,?,?)",(name,password))
#     conn.commit()
#     c.close()
#     return redirect("/login")

# log in ----------------------------------------------------------

# @app.route("/login",methods=["GET"])
# def login_get():
#     if "user_id" in session:
#         return redirect("/list")
#     else:
#         return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def login_post():
#     name = request.form.get("name")
#     password = request.form.get("password")
# #     # requestでHTML側からデータを受け取る
    
#     conn = sqlite3.connect("maintenance.db")
#     c = conn.cursor()
#     c.execute("select id from users where name = ? and password = ?", (name,password))
#     user_id = c.fetchone()
#     c.close()

# # id取れたかどうかで条件分岐

#     if user_id is None:
#         return render_template("login.html")
#     else:
#         session["user_id"] = user_id[0]
#     #     # クッキーをここで設定
    
    # return redirect("/list")

# ログアウト-----------------------------------------------------------------
# @app.route("/logout")
# def logout():
#     session.pop("user_id", None)
#     return redirect("/login")

# Winkel version

#リストの追加/コンドミニアム
@app.route("/add/room/condo",methods=["POST"])
def add_post_room_condo():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    room = request.form.get("room")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("w_error_condo.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,room,tablename))
        c.execute("create table %s (taskid INTEGER, item_id INTEGER, item TEXT, pro_date DATE, pro_number INTEGER, set_date DATE, t_date DATE, task TEXT, notice DATE, nt_id INTEGER, PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/condo")

#リストの追加/別荘
@app.route("/add/room/bessou",methods=["POST"])
def add_post_room_bessou():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    room = request.form.get("room")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("w_error_bessou.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,room,tablename))
        c.execute("create table %s (taskid INTEGER, item_id INTEGER, item TEXT, pro_date DATE, pro_number INTEGER, set_date DATE, t_date DATE, task TEXT, notice DATE, nt_id INTEGER, PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/bessou")

#リストの追加/キャンプ場
@app.route("/add/room/camp",methods=["POST"])
def add_post_room_camp():
    ios_id = request.form.get("ios_id")
    ios_id = int(ios_id)
    room = request.form.get("room")
    tablename = request.form.get("table_name")
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    # table_name 取得
    c.execute("select table_name from items")
    tb_list = []
    tb_list = c.fetchall()
    tbname_list = []
    for row in tb_list:
        tbname_list.append(row[0])
    if tablename in tbname_list:
        return render_template("w_error_camp.html")
    else:
        c.execute("insert into items values (null,?,?,?)", (ios_id,room,tablename))
        c.execute("create table %s (taskid INTEGER, item_id INTEGER, item TEXT, pro_date DATE, pro_number INTEGER, set_date DATE, t_date DATE, task TEXT, notice DATE, nt_id INTEGER, PRIMARY KEY(taskid AUTOINCREMENT))" %(tablename))
        conn.commit()
        c.close()
    return redirect("/list/camp")

# DBに保存されているものを表示してみよう
# コンドミニアム
@app.route("/list/condo")
def condo_list():
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select id, room from items where ios_id = 0")
    room_list=[]
    for row in c.fetchall():
        room_list.append({"id":row[0],"room":row[1]})
    c.close()
    return render_template("w_condo_list.html",condo_list = room_list)

# 別荘
@app.route("/list/bessou")
def bessou_list():
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select id, room from items where ios_id = 1")
    room_list=[]
    for row in c.fetchall():
        room_list.append({"id":row[0],"room":row[1]})
    c.close()
    return render_template("w_bessou_list.html",bessou_list = room_list)

# キャンプ場
@app.route("/list/camp")
def camp_list():
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select id, room from items where ios_id = 2")
    room_list=[]
    for row in c.fetchall():
        room_list.append({"id":row[0],"room":row[1]})
    c.close()
    return render_template("w_camp_list.html",camp_list = room_list)

# コンドミニアムの編集
@app.route("/edit/condo/<int:id>")
def edit_room_condo(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select room from items where id=?", (id,))
    room = c.fetchone()[0]
    print(room)
    c.close()
    room = {"id":id, "room":room}
    return render_template("w_edit_room_condo.html" , room = room)
    
# 変更したデータでコンドミニアムリスト更新
@app.route("/edit/condo", methods = ["POST"])
def update_room_condo():
    item_id = request.form.get("id")
    item_id = int(item_id)
    room = request.form.get("room")
    conn = sqlite3.connect("w_MN.db")
    c =conn.cursor()
    c.execute("update items set room=? where id = ?", (room,item_id))
    conn.commit()
    c.close()
    return redirect("/list/condo")
    
# 別荘リストの編集
@app.route("/edit/bessou/<int:id>")
def edit_room_bessou(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select room from items where id=?", (id,))
    room = c.fetchone()[0]
    c.close()
    room = {"id":id, "room":room}
    print(room)
    return render_template("w_edit_room_bessou.html" , room = room)
    
# 変更したデータで別荘リスト更新
@app.route("/edit/bessou", methods = ["POST"])
def update_room_bessou():
    item_id = request.form.get("id")
    item_id = int(item_id)
    room = request.form.get("room")
    conn = sqlite3.connect("w_MN.db")
    c =conn.cursor()
    c.execute("update items set room=? where id = ?", (room,item_id))
    conn.commit()
    c.close()
    return redirect("/list/bessou")

# キャンプ場リスト編集
@app.route("/edit/camp/<int:id>")
def edit_room_camp(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select room from items where id=?", (id,))
    room = c.fetchone()[0]
    c.close()
    room = {"id":id, "room":room}
    return render_template("w_edit_room_camp.html" , room = room)
    
# 変更したデータでキャンプ場リスト更新
@app.route("/edit/camp", methods = ["POST"])
def update_room_camp():
    item_id = request.form.get("id")
    item_id = int(item_id)
    room = request.form.get("room")
    conn = sqlite3.connect("w_MN.db")
    c =conn.cursor()
    c.execute("update items set room=? where id = ?", (room,item_id))
    conn.commit()
    c.close()
    return redirect("/list/camp")

# コンドミニアムストからアイテムの削除
@app.route("/del/condo/<int:id>")
def del_room_condo(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/condo")

# 別荘リストからアイテムの削除
@app.route("/del/bessou/<int:id>")
def del_room_bessou(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/bessou")

# キャンプ場リストからアイテムの削除
@app.route("/del/camp/<int:id>")
def del_room_camp(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id=?", (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from items where id=?", (id,))
    c.execute("drop table %s" % (table_name))
    c = conn.commit()
    conn.close()
    return redirect("/list/camp")

# 8/16 部屋ごとのアイテムをリストしてみよう
@app.route("/w_itemlist/<int:id>")
def w_itemlist(id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select id from items where id = ?" , (id,))
    id = c.fetchone()[0]
    c.execute("select room from items where id = ?" , (id,))
    room = c.fetchone()[0]
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select taskid, t_id, item, pro_date, pro_number, set_date from %s where pro_date is NOT NULL" % (table_name))
    itemlist = []
    item_list = []
    for row in c.fetchall():
        itemlist = dict({"taskid":row[0],"t_id":row[1], "item":row[2], "pro_date":row[3],"pro_number":row[4], "set_date":row[5]})
        item_list.append(itemlist) 
    c.close()
    return render_template("w_itemlist.html" , w_item_list = item_list, table_name = table_name, room = room, id = id)
    # return redirect("/login")

# 8/17 部屋ごとのアイテム追加の処理
@app.route("/add/w_itemlist/<int:id>",methods=["POST"])
def add_post_w_item(id):
    # user_id = session["user_id"]
    item = request.form.get("item")
    t_id = request.form.get("t_id")
    pro_date = request.form.get("pro_date")
    pro_number = request.form.get("pro_number")
    set_date = request.form.get("set_date")
    t_date = request.form.get("t_date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    # nt_id = int(nt_id)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
        #()はタプル型
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("insert into %s values (null,?,?,?,?,?,?,?,?,?,?)" % (table_name), (id,t_id,item,pro_date,pro_number,set_date,t_date,task,notice,nt_id))
    conn.commit()
    c.close()
    # return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    return redirect("/w_itemlist/%s" %(id))  

# 8/17 編集変更したデータで部屋ごとのアイテム更新
@app.route("/edit/w_itemlist/<int:id>/<int:taskid>")
def edit_w_itemlist_get(id,taskid):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select item from %s where taskid=?" % (table_name), (taskid,))
    item = c.fetchone()[0]
    c.execute("select pro_date from %s where taskid=?" % (table_name), (taskid,))
    pro_date = c.fetchone()[0]  
    c.execute("select pro_number from %s where taskid=?" % (table_name), (taskid,))
    pro_number = c.fetchone()[0] 
    c.execute("select set_date from %s where taskid=?" % (table_name), (taskid,))
    set_date = c.fetchone()[0]  
    c.execute("select t_date from %s where taskid=?" % (table_name), (taskid,))
    t_date = c.fetchone()[0]
    c.execute("select task from %s where taskid=?" % (table_name), (taskid,))
    task = c.fetchone()[0]
    c.execute("select notice from %s where taskid=?" % (table_name), (taskid,))
    notice = c.fetchone()[0]   
    c.execute("select nt_id from %s where taskid=?" % (table_name), (taskid,))
    nt_id = c.fetchone()[0] 
    c.close()
    task_list = {"taskid":taskid,"item":item, "pro_date":pro_date,"pro_number":pro_number,"set_date":set_date,"t_date":t_date, "task":task, "notice":notice, "nt_id":nt_id}
    return render_template("w_edit_itemlist.html", task_list = task_list, id = id)

@app.route("/edit/w_itemlist/<int:id>", methods = ["POST"])
def w_itemlist_update(id):
    taskid = request.form.get("taskid")
    taskid = int(taskid)
    item = request.form.get("item")
    pro_date = request.form.get("pro_date")
    pro_number = request.form.get("pro_number")
    set_date = request.form.get("set_date")
    t_date = request.form.get("t_date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    conn = sqlite3.connect("w_MN.db")
    c =conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set item=? where taskid = ?" %(table_name), (item,taskid,))
    c.execute("update %s set pro_date=? where taskid = ?" %(table_name), (pro_date,taskid,))
    c.execute("update %s set pro_number=? where taskid = ?" %(table_name), (pro_number,taskid,))
    c.execute("update %s set set_date=? where taskid = ?" %(table_name), (set_date,taskid,))
    c.execute("update %s set t_date=? where taskid = ?" %(table_name), (t_date,taskid,))
    c.execute("update %s set task=? where taskid = ?" %(table_name), (task,taskid,))
    c.execute("update %s set notice=? where taskid = ?" %(table_name), (notice,taskid,))
    c.execute("update %s set nt_id=? where taskid = ?" %(table_name), (nt_id,taskid,))
    conn.commit()
    c.close()
    return redirect("/w_itemlist/%s" %(id))  

# 8/17 部屋ごとのアイテムリストからアイテムの削除
@app.route("/del/w_itemlist/<int:id>/<int:taskid>")
def del_w_itemlist(id,taskid):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from %s where taskid=?" % (table_name), (taskid,))
    c = conn.commit()
    conn.close()
    return redirect("/w_itemlist/%s" %(id)) 

# 8/17 部屋ごとのアイテムのタスクをリストしてみよう
@app.route("/w_tasklist/<int:id>/<int:t_id>")
def w_tasklist(id,t_id):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select id from items where id = ?" , (id,))
    id = c.fetchone()[0]
    c.execute("select room from items where id = ?" , (id,))
    room = c.fetchone()[0]
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select item from %s where t_id = ?" % (table_name), (t_id,))
    item = c.fetchone()[0]
    c.execute("select taskid, item, pro_date, pro_number, set_date, t_date, task, notice, nt_id from %s where t_id = ?" % (table_name), (t_id,))
    tasklist = []
    task_list = []
    for row in c.fetchall():
        tasklist = dict({"taskid":row[0],"item":row[1], "pro_date":row[2],"pro_number":row[3], "set_date":row[4], "t_date":row[5],"task":row[6], "notice":row[7], "nt_id":row[8]})
        if tasklist["nt_id"] == 1:
            tasklist["nt_id"] = "done"
        else:
            tasklist["nt_id"] = "set"
        task_list.append(tasklist) 
    c.close()
    return render_template("w_tasklist.html" , w_task_list = task_list, table_name = table_name, room = room, id = id, item = item, t_id = t_id)
    # return redirect("/login")

# 8/17 部屋ごとのアイテムのタスク追加の処理
@app.route("/add/w_tasklist/<int:id>/<int:t_id>",methods=["POST"])
def add_post_w_task(id,t_id):
    # user_id = session["user_id"]
    t_id = request.form.get("t_id")
    item = request.form.get("item")
    pro_date = request.form.get("pro_date")
    pro_number = request.form.get("pro_number")
    set_date = request.form.get("set_date")
    t_date = request.form.get("t_date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
        #()はタプル型
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("insert into %s values (null,?,?,?,?,?,?,?,?,?,?)" % (table_name), (id,t_id,item,pro_date,pro_number,set_date,t_date,task,notice,nt_id))
    conn.commit()
    c.close()
    # return render_template("tasklist.html" , task_list = task_list, table_name = table_name, item = item, id = id)
    return redirect("/w_tasklist/%s/%s" %(id, t_id,))  

# 8/18 部屋ごとのアイテムのタスク編集変更したデータで更新
@app.route("/edit/w_tasklist/<int:id>/<int:taskid>")
def edit_w_tasklist_get(id,taskid):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("select t_id from %s where taskid=?" % (table_name), (taskid,))
    t_id = c.fetchone()[0]
    c.execute("select item from %s where taskid=?" % (table_name), (taskid,))
    item = c.fetchone()[0]
    c.execute("select pro_date from %s where taskid=?" % (table_name), (taskid,))
    pro_date = c.fetchone()[0]  
    c.execute("select pro_number from %s where taskid=?" % (table_name), (taskid,))
    pro_number = c.fetchone()[0] 
    c.execute("select set_date from %s where taskid=?" % (table_name), (taskid,))
    set_date = c.fetchone()[0]  
    c.execute("select t_date from %s where taskid=?" % (table_name), (taskid,))
    t_date = c.fetchone()[0]
    c.execute("select task from %s where taskid=?" % (table_name), (taskid,))
    task = c.fetchone()[0]
    c.execute("select notice from %s where taskid=?" % (table_name), (taskid,))
    notice = c.fetchone()[0]   
    c.execute("select nt_id from %s where taskid=?" % (table_name), (taskid,))
    nt_id = c.fetchone()[0] 
    c.close()
    task_list = {"taskid":taskid,"t_id":t_id, "item":item, "pro_date":pro_date,"pro_number":pro_number,"set_date":set_date,"t_date":t_date, "task":task, "notice":notice, "nt_id":nt_id}
    return render_template("w_edit_tasklist.html", task_list = task_list, id = id)

@app.route("/edit/w_tasklist/<int:id>", methods = ["POST"])
def w_tasklist_update(id):
    taskid = request.form.get("taskid")
    taskid = int(taskid)
    t_id = request.form.get("t_id")
    t_id = int(t_id)   
    item = request.form.get("item")
    pro_date = request.form.get("pro_date")
    pro_number = request.form.get("pro_number")
    set_date = request.form.get("set_date")
    t_date = request.form.get("t_date")
    task = request.form.get("task")
    notice = request.form.get("notice")
    nt_id = request.form.get("nt_id")
    conn = sqlite3.connect("w_MN.db")
    c =conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set t_id=? where taskid = ?" %(table_name), (t_id,taskid,))
    c.execute("update %s set item=? where taskid = ?" %(table_name), (item,taskid,))
    c.execute("update %s set pro_date=? where taskid = ?" %(table_name), (pro_date,taskid,))
    c.execute("update %s set pro_number=? where taskid = ?" %(table_name), (pro_number,taskid,))
    c.execute("update %s set set_date=? where taskid = ?" %(table_name), (set_date,taskid,))
    c.execute("update %s set t_date=? where taskid = ?" %(table_name), (t_date,taskid,))
    c.execute("update %s set task=? where taskid = ?" %(table_name), (task,taskid,))
    c.execute("update %s set notice=? where taskid = ?" %(table_name), (notice,taskid,))
    c.execute("update %s set nt_id=? where taskid = ?" %(table_name), (nt_id,taskid,))
    conn.commit()
    c.close()
    return redirect("/w_tasklist/%s/%s" %(id, t_id,))

#8/18 部屋ごとのアイテムのタスクリストから タスクの削除
@app.route("/del/w_tasklist/<int:id>/<int:t_id>/<int:taskid>")
def del_w_tasklist(id,t_id,taskid):
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("delete from %s where taskid=?" % (table_name), (taskid,))
    print(t_id)
    c = conn.commit()
    conn.close()
    return redirect("/w_tasklist/%s/%s" %(id, t_id,))

# 8/20 DBから通知を表示してみよう－今週の通知
@app.route("/notice/w_tasklist")
def notice_w_tasklist():
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
        c.execute("select items.room,  %s.item, %s.t_date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0],row[0]), (today,time7,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row3[0] is not None:
                nt_list.append({"room":row3[0],"item":row3[1],"t_date":row3[2],"task":row3[3],"notice":row3[4],"id":row3[5],"taskid":row3[6]})
    print(len(nt_list))
    c.close()
    return render_template("w_notice_list.html",nt_list = nt_list, today = today, time7 = time7)
    # return "該当する通知はありません"

# 今週の通知表示から実施済みタスクを表示しないようにする－今週の通知
@app.route("/notice/w_tasklist/nt/<int:id>/<int:taskid>",methods=["POST"])
def notice_w_tasklist_nt(id,taskid):
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
# まず実施済タスクのnt_idを1にupdateする
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect # noticeがtoday と一致するタスクをセレクト
        c.execute("select items.room, %s.item, %s.t_date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0],row[0]), (today,time7,))
        ntlist = []
        notice_list = c.fetchall()
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"room":row3[0],"item":row3[1],"t_date":row3[2],"task":row3[3],"notice":row3[4],"id":row3[5],"taskid":row3[6]})
    conn.commit()
    c.close()
    return render_template("w_notice_list.html",nt_list = nt_list, today = today, time7 = time7)

#8/20 DBから通知を表示してみよう－先週の通知
@app.route("/notice/w_tasklist/lw")
def notice_w_tasklist_lw():
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
        c.execute("select items.room,  %s.item, %s.t_date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0],row[0]), (time7,time14,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row3[0] is not None:
                nt_list.append({"room":row3[0],"item":row3[1],"t_date":row3[2],"task":row3[3],"notice":row3[4],"id":row3[5],"taskid":row3[6]})
    print(len(nt_list))
    c.close()
    return render_template("w_notice_list_lw.html",nt_list = nt_list, today = today, time7 = time7, time14 = time14)
    # return "該当する通知はありません"

# 先週の通知表示から実施済みタスクを表示しないようにする－先週の通知
@app.route("/notice/w_tasklist/nt_lw/<int:id>/<int:taskid>",methods=["POST"])
def notice_w_tasklist_nt_lw(id,taskid):
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
# まず実施済タスクのnt_idを1にupdateする
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect # noticeがtoday と一致するタスクをセレクト
        c.execute("select items.room, %s.item, %s.t_date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0],row[0]), (time7,time14,))
        ntlist = []
        notice_list = c.fetchall()
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"room":row3[0],"item":row3[1],"t_date":row3[2],"task":row3[3],"notice":row3[4],"id":row3[5],"taskid":row3[6]})
    conn.commit()
    c.close()
    return render_template("w_notice_list_lw.html",nt_list = nt_list, today = today, time7 = time7, time14 = time14)

#8/20 DBから通知を表示してみよう－来週の通知
@app.route("/notice/w_tasklist/nw")
def notice_w_tasklist_nw():
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
    time_p7 = today + dt.timedelta(days=7)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
        c.execute("select items.room,  %s.item, %s.t_date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0],row[0]), (time_p7,today,))
        ntlist = []
        notice_list = c.fetchall()
    #todayと一致する項目があったものだけをntlist に append
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
    #ntlistの中身をnt_list として連想配列化
        for row3 in ntlist:
            if row3[0] is not None:
                nt_list.append({"room":row3[0],"item":row3[1],"t_date":row3[2],"task":row3[3],"notice":row3[4],"id":row3[5],"taskid":row3[6]})
    print(len(nt_list))
    c.close()
    return render_template("w_notice_list_nw.html",nt_list = nt_list, today = today, time_p7 = time_p7)
    # return "該当する通知はありません"

#来週の通知表示から実施済みタスクを表示しないようにする－来週の通知
@app.route("/notice/w_tasklist/nt_nw/<int:id>/<int:taskid>",methods=["POST"])
def notice_w_tasklist_nt_nw(id,taskid):
    today = dt.date.today()
    time7 = today + dt.timedelta(days=-7)
    time14 = today + dt.timedelta(days=-14)
    time_p7 = today + dt.timedelta(days=7)
# まず実施済タスクのnt_idを1にupdateする
    nt_id = request.form.get("nt_id")
    nt_id = int(nt_id)
    conn = sqlite3.connect("w_MN.db")
    c = conn.cursor()
    c.execute("select table_name from items where id = ?" , (id,))
    table_name = c.fetchone()[0]
    c.execute("update %s set nt_id = 1 where taskid = ?" % (table_name), (taskid,))
    c.execute("select table_name from items")
    tbname_list = []
    ntlist = []
    nt_list = []
    for row in c.fetchall():
    # row[0]をtable_nameの変数としてselect # noticeがtoday と一致するタスクをセレクト
        c.execute("select items.room, %s.item, %s.t_date, %s.task, %s.notice, items.id, %s.taskid FROM items JOIN %s ON items.id = %s.item_id where notice <= ? and notice >= ? and nt_id =0" % (row[0],row[0],row[0],row[0],row[0],row[0],row[0]), (time_p7,today))
        ntlist = []
        notice_list = c.fetchall()
        for row2 in notice_list:
            if row2 is not None:
                ntlist.append(row2)
        for row3 in ntlist:
            if row[0] is not None:
                nt_list.append({"room":row3[0],"item":row3[1],"t_date":row3[2],"task":row3[3],"notice":row3[4],"id":row3[5],"taskid":row3[6]})
    conn.commit()
    c.close()
    return render_template("w_notice_list_nw.html",nt_list = nt_list, today = today, time7 = time7, time_p7 = time_p7)


#404ページ
@app.errorhandler(404)
def not_found(error):
    return "ページが見つかりません"

#おまじない
if __name__ == "__main__":
    # Flaskが持っている開発用サーバーを実行します。
    app.run(debug=True)