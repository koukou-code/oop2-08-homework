from flask import Flask, request, render_template
import random # ランダムデータ作成のためのライブラリ

app = Flask(__name__)

# 1. プロジェクトのトップ（じゃんけんアプリや、課題のアプリへのリンクを配置するだけ）
@app.route('/')
def index():
    return render_template('index.html')


# 2. じゃんけんアプリの入力フォーム
@app.route('/janken')
def janken():
    # じゃんけんの入力画面のテンプレートを呼び出し
    return render_template('janken_form.html')


# 3. じゃんけんデータ送信先とじゃんけん結果表示画面
@app.route('/janken/play', methods=["POST"])
def janken_play():

    # <input type="text" id="your_name" name="name">
    name = request.form.get("name")
    if not name:
        name = "名無しさん"
    
    # <input type="radio" id="hand_rock" value="rock" name="hand">
    # <input type="radio" id="hand_scissor" value="scissor" name="hand">
    # <input type="radio" id="hand_paper" value="paper" name="hand">
    hand = request.form.get("hand", None)

    # プレイヤーが勝ったかどうか（勝ったときだけTrueにする）
    is_win = False

    # リストの中からランダムに選ぶ
    cpu = random.choice(["rock", "scissor", "paper"])
    if request.form.get("is_settai") == "on":
        if not hand:
            hand = "rock"  # デフォルトはグー
        # 接待モードではCPUは常に負ける手をだす。
        if hand == "rock":
            cpu = "scissor"
        elif hand == "scissor":
            cpu = "paper"
        elif hand == "paper":
            cpu = "rock"

    # じゃんけん処理
    if hand == cpu:
        result_message = "あいこ"
    else:
        if hand == "rock":
            if cpu == "scissor":
                result_message = "{}の勝ち".format(name)
                is_win = True
            else:
                result_message = "{}の負け".format(name)
        elif hand == "scissor":
            if cpu == "paper":
                result_message = "{}の勝ち".format(name)
                is_win = True
            else:
                result_message = "{}の負け".format(name)
        elif hand == "paper":
            if cpu == "rock":
                result_message = "{}の勝ち".format(name)
                is_win = True
            else:
                result_message = "{}の負け".format(name)
        else:
            result_message = "後出しはダメです。"

    # 渡したいデータを先に定義しておいてもいいし、テンプレートを先に作っておいても良い
    return render_template('janken_play.html',
                           result_message=result_message,
                           name=name,
                           hand=hand,
                           cpu=cpu,
                           is_win=is_win)
    
    


# 4. 占いアプリの入力フォーム
@app.route('/uranai')
def uranai():
    return render_template('uranai_form.html')


# 5. 占いデータ送信先と占い結果表示画面
@app.route('/uranai/play', methods=["POST"])
def uranai_play():
    # <input type="text" id="your_name" name="name">
    name = request.form.get("name", "")

    # <input type="date" id="your_birthdate" name="birthdate">
    birthdate = request.form.get("birthdate", "")

    return render_template('uranai_play.html',
                           name=name,
                           birthdate=birthdate)

if __name__ == '__main__':
    # portは適宜書き換えてください
    app.run(host="0.0.0.0", port=8888, debug=True)