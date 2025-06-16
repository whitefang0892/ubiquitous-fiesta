from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 表示用テキストを読み込む
    with open('houben.txt', encoding='utf-8') as f:
        lines = f.readlines()
    return render_template('index.html', lines=lines)

if __name__ == '__main__':
    app.run()