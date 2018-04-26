# 以下為宣告 ################################## (1)
# 導入 os 模組, 主要用來判斷是否在 OpenShift 上執行
import os
from flask import Flask, request, redirect, render_template, session
import random

# 以下為全域變數宣告 ############################# (2)
# 確定程式檔案所在目錄, 在 Windows 有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))

# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
    template_root_dir = os.environ['OPENSHIFT_REPO_DIR']+"/static"
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"
    template_root_dir = _curdir + "/static"

# 啟動 app
app = Flask(__name__)

# 使用 session 必須要設定 secret_key
app.secret_key = 'A0Zr9@8j/3yX R~XHH!jmN]LWX/,?R@T'

# 以下為相關各方法的定義 ########################### (3)
@app.route("/")
def index():
    #這是猜數字遊戲的起始表單, 主要在產生答案, 並且將 count 歸零
    # 將標準答案存入 answer session 對應區
    theanswer = random.randint(1, 100)
    thecount = 0
    # 將答案與計算次數變數存進 session 對應變數
    session['answer'] = theanswer
    session['count'] = thecount

    return render_template("index.html", answer=theanswer, count=thecount)
@app.route('/guessform')
def guessform():
    session["count"] += 1
    guess = session.get("guess")
    theanswer = session.get("answer")
    count = session.get("count")
    
    return render_template("guessform.html", guess=guess, answer=theanswer, count=count)
@app.route('/docheck', methods=['POST'])
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
# http://2014c2-mdenfu.rhcloud.com/c2g30/flag
# 直接送出 html 版本
@app.route("/drawflag")
def drawflag():
    '''
    原始程式來源: http://blog.roodo.com/esabear/archives/19215194.html
    改寫為 Brython 程式
    '''
    outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/Brython3.2.3-20151122-082712/brython.js"></script>
</head>
<body onload="brython({debug:1, cache:'version'})">
<canvas id="plotarea" width="300" height="200"></canvas>
<script type="text/python">
# 導入 doc
from browser import document as doc
import math

# 準備繪圖畫布
canvas = doc["plotarea"]
ctx = canvas.getContext("2d")
# 進行座標轉換, x 軸不變, y 軸反向且移動 canvas.height 單位光點
# ctx.setTransform(1, 0, 0, -1, 0, canvas.height)
# 以下採用 canvas 原始座標繪圖
flag_w = canvas.width
flag_h = canvas.height
circle_x = flag_w/4
circle_y = flag_h/4
# 先畫滿地紅
ctx.fillStyle='rgb(255, 0, 0)'
ctx.fillRect(0,0,flag_w,flag_h)
# 再畫青天
ctx.fillStyle='rgb(0, 0, 150)'
ctx.fillRect(0,0,flag_w/2,flag_h/2)
# 畫十二道光芒白日
ctx.beginPath()
star_radius = flag_w/8
angle = 0
for i in range(24):
    angle += 5*math.pi*2/12
    toX = circle_x + math.cos(angle)*star_radius
    toY = circle_y + math.sin(angle)*star_radius
    # 只有 i 為 0 時移動到 toX, toY, 其餘都進行 lineTo
    if (i):
        ctx.lineTo(toX, toY)
    else:
        ctx.moveTo(toX, toY)
ctx.closePath()
# 將填色設為白色
ctx.fillStyle = '#fff'
ctx.fill()
# 白日:藍圈
ctx.beginPath()
ctx.arc(circle_x, circle_y, flag_w*17/240, 0, math.pi*2, True)
ctx.closePath()
# 填色設為藍色
ctx.fillStyle = 'rgb(0, 0, 149)'
ctx.fill()
# 白日:白心
ctx.beginPath()
ctx.arc(circle_x, circle_y, flag_w/16, 0, math.pi*2, True)
ctx.closePath()
# 填色設為白色
ctx.fillStyle = '#fff'
ctx.fill()
</script>
</body>
</html>
'''
    return outstring
# 直接送出 html 版本
@app.route("/drawstar")
def drawstar():
    outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/Brython3.2.3-20151122-082712/brython.js"></script>
</head>
<body onload="brython({debug:1, cache:'version'})">
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
# 導入 doc
from browser import document as doc
import math

# 準備繪圖畫布
canvas = doc["plotarea"]
ctx = canvas.getContext("2d")
# 進行座標轉換, x 軸不變, y 軸反向且移動 800 光點
ctx.setTransform(1, 0, 0, -1, 0, 800)

# 定義畫線函式
def draw_line(x1, y1, x2, y2, linethick = 3, color = "black"):
    ctx.beginPath()
    ctx.lineWidth = linethick
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.strokeStyle = color
    ctx.stroke()

# x, y 為中心,  r 為半徑, angle 旋轉角,  solid 空心或實心,  color 顏色
def star(x, y, r, angle=0, solid=False, color="#f00"):
    # 以 x, y 為圓心, 計算五個外點
    deg = math.pi/180
    # 圓心到水平線距離
    a = r*math.cos(72*deg)
    # a 頂點向右到內點距離
    b = (r*math.cos(72*deg)/math.cos(36*deg))*math.sin(36*deg)
    # 利用畢氏定理求內點半徑
    rin = math.sqrt(a**2 + b**2)
    # 查驗 a, b 與 rin
    #print(a, b, rin)
    if(solid):
        ctx.beginPath()
    for i in range(5):
        xout = (x + r*math.sin((360/5)*deg*i+angle*deg))
        yout = (y + r*math.cos((360/5)*deg*i+angle*deg))
        # 外點增量 + 1
        xout2 = x + r*math.sin((360/5)*deg*(i+1)+angle*deg)
        yout2 = y + r*math.cos((360/5)*deg*(i+1)+angle*deg)
        xin = x + rin*math.sin((360/5)*deg*i+36*deg+angle*deg)
        yin = y + rin*math.cos((360/5)*deg*i+36*deg+angle*deg)
        # 查驗外點與內點座標
        #print(xout, yout, xin, yin)
        if(solid):
            # 填色
            if(i==0):
                ctx.moveTo(xout, yout)
                ctx.lineTo(xin, yin)
                ctx.lineTo(xout2, yout2)
            else:
                ctx.lineTo(xin, yin)
                ctx.lineTo(xout2, yout2)
        else:
            # 空心
            draw_line(xout, yout, xin, yin, color)
            # 畫空心五芒星, 無關畫線次序, 若實心則與畫線次序有關
            draw_line(xout2, yout2, xin, yin, color)
    if(solid):
        ctx.fillStyle = color
        ctx.fill()
star(600, 600, 100, 30, True, "#00f")
star(100, 100, 30, 0, True, "#f00")
#star(300, 300, 50, 0, False, "#000")
for i in range(5):
    for j in range(5):
        star(200+65*i, 200+65*j, 30, 0, False, "#000")
</script>
</body>
</html>
'''
    return outstring
# 直接送出 html 版本
@app.route("/drawcango")
def drawcango():
    outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/Cango-7v13.js"></script>
<script type="text/javascript" src="/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="/static/Brython3.2.3-20151122-082712/brython.js"></script>
</head>
<body onload="brython({debug:1, cache:'version'})">
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
from javascript import JSConstructor
from browser import window
import math

cango = JSConstructor(window.Cango)
cgo = cango("plotarea")
cgo.setGridboxRHC()
cgo.setWorldCoords(-1, -25, 2, 50) 
cgo.drawText("使用 Cango 繪圖程式庫!", 0, 0, {"fontSize":60, "fontWeight": 1200, "lorg":5 })

# Cango2D example
cango2d = JSConstructor(window.Cango2D)
tweener = JSConstructor(window.Tweener)
g = cango2d("plotarea")
g.setWorldCoords(-10, -10, 20)
hello = g.drawText("加油!加油!", 0, 0, {
"fillColor":"blue",
"fontSize":16,
"lorg":5 })
sclTwn = tweener([1, 2, 1], 1000, 5000, 'loopAll')
rotTwn = tweener([0, 360, -360], 1000, 5000, 'loopAll')
hello.transform.scale(sclTwn)
hello.transform.rotate(rotTwn)
g.animate(hello)
g.playAnimation()
</script>
</body>
</html>
'''
    return outstring
# 直接送出 html 版本
@app.route("/drag")
def drag():
    outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/Cango2D-6v13.js"></script>
<script type="text/javascript" src="/static/Brython3.2.3-20151122-082712/brython.js"></script>
</head>
<body onload="brython({debug:1, cache:'version'})">
<canvas id="plotarea" width="800" height="800"></canvas>
<script type="text/python">
from browser import window
from javascript import JSConstructor
  
cango = JSConstructor(window.Cango2D)
shapedefs = window.shapeDefs
obj2d = JSConstructor(window.Obj2D)
cgo = cango("plotarea")
x1, y1 = 40, 20
cx1, cy1 = 90, 120
x2, y2 = 120, 100
cx2, cy2 = 130, 20
cx3, cy3 = 150, 120
x3, y3 = 180, 60

def dragC1(mousePos):
    global cx1, cy1
    cx1 = mousePos.x
    cy1 = mousePos.y
    drawCurve()
 
def dragC2(mousePos):
    global cx2, cy2
    cx2 = mousePos.x
    cy2 = mousePos.y
    drawCurve()
 
def dragC3(mousePos):
    global cx3, cy3
    cx3 = mousePos.x
    cy3 = mousePos.y
    drawCurve()
 
def drawCurve():
    # curve change shape so it must be re-draw each time
    # draw a quadratic bezier from x1,y2 to x2,y2
    qbez = obj2d(['M', x1, y1, 'Q', cx1, cy1, x2, y2], "PATH",  {
          "strokeColor":'blue'})
    cbez = obj2d(['M', x2, y2, 'C', cx2, cy2, cx3, cy3, x3, y3], "PATH",  {
          "strokeColor":'green'})
    # show lines to control point
    L1 = obj2d(['M', x1, y1, 'L', cx1, cy1, x2, y2], "PATH", {
      "strokeColor":"rgba(0, 0, 0, 0.2)",
      "dashed":[4]})  # semi-transparent gray
    L2 = obj2d(['M', x2, y2, 'L', cx2, cy2], "PATH", {
      "strokeColor":"rgba(0, 0, 0, 0.2)",
      "dashed":[4]})
    L3 = obj2d(['M', x3, y3, 'L', cx3, cy3], "PATH", {
      "strokeColor":"rgba(0, 0, 0, 0.2)",
      "dashed":[4]})
    # draw draggable control points
    c1.transform.reset()
    c1.transform.translate(cx1, cy1)
    c2.transform.reset()
    c2.transform.translate(cx2, cy2)
    c3.transform.reset()
    c3.transform.translate(cx3, cy3)
    grp = cgo.createGroup2D(qbez, cbez, L1, L2, L3, c1, c2, c3)
    cgo.renderFrame(grp)
 
cgo.clearCanvas("lightyellow")
cgo.setWorldCoords(0, 0, 200)
 
# draggable control points
c1 = obj2d(shapedefs.circle(4), "SHAPE", {"fillColor":'red'})
c1.enableDrag(None, dragC1, None)
c2 = c1.dup()
c2.enableDrag(None, dragC2, None)
c3 = c1.dup()
c3.enableDrag(None, dragC3, None)
drawCurve();
</script>
</body>
</html>
'''
    return outstring


