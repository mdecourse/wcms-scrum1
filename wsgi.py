import os
import guess
# 導入 gear.py
import gear
# 假如 View 採用 class Guess() 架構, 則必須利用 appadd_url_rule 進行 routing, 而不可在 class 物件中使用 @app.route
# 等同 app.view_functions['index'] = Guess().index
#app.add_url_rule('/', 'index', Guess().index)
# 等同 app.view_functions['docheck'] = Guess().docheck, 而且允許使用 POST 方法
#app.add_url_rule('/docheck', 'docheck', Guess().docheck, methods=['POST'])
# 等同 app.view_functions['guessform'] = Guess().guessform
#app.add_url_rule('/guessform', 'guessform', Guess().guessform)
ap = guess.app
ap.add_url_rule('/gear_index', 'gear_index', gear.Gear().index)
ap.add_url_rule('/gear_width', 'gear_width', gear.Gear().gear_width, methods=['POST'])

if __name__ == "__main__":
    ap.run(debug=True)
