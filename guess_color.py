
from flask import Flask, request, redirect, render_template, session
import os
import sys

# 確定程式檔案所在目錄, 在 Windows 有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 將所在目錄設為系統搜尋目錄
sys.path.append(_curdir)
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # while program is executed in OpenShift
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # while program is executed in localhost
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"
class Guesscolor(object):
    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(download_root_dir+"downloads"):
            try:
                os.makedirs(download_root_dir+"downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"images"):
            try:
                os.makedirs(download_root_dir+"images")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"tmp"):
            try:
                os.makedirs(download_root_dir+"tmp")
            except:
                print("mkdir error")
    def index():
        #這是猜數字遊戲的起始表單, 主要在產生答案, 並且將 count 歸零
        # 將標準答案存入 answer session 對應區
        colors = ["R", "W", "Y", "G", "B", "P"]
        theanswer = random.sample(colors, 4)  
        thecount = 0
        # 將答案與計算次數變數存進 session 對應變數
        session['answer'] = theanswer
        session['count'] = thecount

        return render_template("index.html", answer=theanswer, count=thecount)
    def guessform():
        session["count"] += 1
        guess = session.get("guess")
        theanswer = session.get("answer")
        count = session.get("count")
        
        return render_template("guessform.html", guess=guess, answer=theanswer, count=count)
    def docheck():
        # session[] 存資料
        # session.get() 取 session 資料
        # 利用 request.form[] 取得表單欄位資料, 然後送到 template
        guess = request.form["guess"]
        session["guess"] = guess
        # 假如使用者直接執行 doCheck, 則設法轉回根方法
        if guess is None:
            redirect("/")
        # 從 session 取出 answer 對應資料, 且處理直接執行 docheck 時無法取 session 值情況
        try:
            theanswer = int(session.get('answer'))
        except:
            redirect("/")
        # 經由表單所取得的 guess 資料型別為 string
        try:
            theguess = int(guess)
        except:
            return redirect("/guessform")
        # 每執行 doCheck 一次,次數增量一次
        session["count"] += 1
        count = session.get("count")
        # 答案與所猜數字進行比對
        if theanswer < theguess:
            return render_template("toobig.html", guess=guess, answer=theanswer, count=count)
        elif theanswer > theguess:
            return render_template("toosmall.html", guess=guess, answer=theanswer, count=count)
        else:
            # 已經猜對, 從 session 取出累計猜測次數
            thecount = session.get('count')
            return "猜了 "+str(thecount)+" 次, 終於猜對了, 正確答案為 "+str(theanswer)+": <a href='/'>再猜</a>"
        # 應該不會執行下列一行
        return render_template("docheck.html", guess=guess)
