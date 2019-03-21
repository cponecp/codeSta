from flask import Blueprint, render_template, request, session, redirect
from codeStatic.utils.md5 import md5
from codeStatic.utils.helper import fetch_all, fetch_one

# account = Blueprint('account', __name__,template_folder="templates")
account = Blueprint('account', __name__)


@account.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":
        name = request.form.get('name')
        pwd = request.form.get('pwd')
        pwd = md5(pwd)

        data = fetch_one("select id, nickname from users where username=%s and pwd=%s", (name, pwd))

        if data is None:
            return "没有注册"
        session["user_info"] = data

        return redirect("/index")


@account.route('/logout')
def logout():
    if "user_info" in session:
        del session["user_info"]

    return redirect('/login')
