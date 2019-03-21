from flask import Blueprint, render_template, session, redirect, request, g
import os
import uuid
import json
from codeStatic.utils.helper import fetch_all, fetch_one, insert
from codeStatic.utils.file_count import count_row

home = Blueprint('home', __name__)


@home.before_request
def checklogin():
    if session.get("user_info") is None:
        return redirect('/login')
    g.id = session["user_info"]['id']


@home.route('/index', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@home.route('/userlist')
def userlist():
    sql = "select id, nickname from users"
    data = fetch_all(sql, ())
    return render_template('userlist.html', users=data)


@home.route('/upfile', methods=["GET", "POST"])
def upfile():
    """ 上传文件，并统计有效代码行数，写入数据库"""
    if request.method == 'GET':
        return render_template('push.html')

    # 获取上传文件
    file = request.files.get('code')
    if file is None:
        return 'none'
    total_num = 0
    # 检验文件后缀
    name_split = file.filename.rsplit('.', maxsplit=1)
    if name_split[1] == 'py':
        total_num = count_row(file.stream)
    elif name_split[1] == 'zip':
        import shutil
        target_path = os.path.join('upfiles', str(uuid.uuid4()))
        shutil._unpack_zipfile(file.stream, target_path)

        for base_path, folder_list, file_list in os.walk(target_path):
            for file_name in file_list:
                file_path = os.path.join(base_path, file_name)
                file_ext = file_path.rsplit('.', maxsplit=1)
                if len(file_ext) != 2:
                    continue
                if file_ext[1] != 'py':
                    continue
                file_num = count_row(file_path)
                total_num += file_num
    else:
        return render_template('push.html', err="您上传的文件格式不支持")
    # 获取当前时间
    import datetime
    ctime = datetime.date.today()
    sql = "insert into coderec(uid,rownum,push_date) values (%s,%s,%s)"

    data = fetch_one("select id from coderec where push_date=%s and uid=%s", (ctime, g.id))
    if data:
        return render_template('push.html', err="您今天已经上传过了")

    row = insert(sql, (g.id, total_num, ctime))

    return render_template('push.html', err="上传成功！")


@home.route('/detail/<int:uid>', methods=["GET"])
def detail(uid):
    """查看用户代码提交历史"""
    sql1 = "select nickname from users where id=%s"
    nickname = fetch_one(sql1, (uid,))
    sql2 = "select rownum,push_date from coderec  where uid=%s order by push_date desc "
    data = fetch_all(sql2, (uid,))

    # 拼接highcharts数据
    xAxis = {'categories': []}
    rownum = {"data": []}
    for i in data:
        ret = str(i['push_date'])
        xAxis['categories'].append(ret)
        rownum['data'].append(i['rownum'])
    xAxis = json.dumps(xAxis)
    rownum = json.dumps(rownum)
    return render_template("detail.html", name=nickname, data=data, xAxis=xAxis, rownum=rownum)
