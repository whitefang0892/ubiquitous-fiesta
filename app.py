from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# --- ユーティリティ関数: ファイル読み込み ---
def load_scripture_text(filename, default="(漢字版がありません)") -> str:
    try:
        with open(filename, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"ファイル読み込みエラー: {filename}, {e}")
        text = default
    return text

# --- 初期設定 ---
# 初期のお経ファイルは「方便品」
current_scripture = "houben.txt"
current_kanji = "houben_kanji.txt"

scripture_text = load_scripture_text(current_scripture, "ここにお経を記載してください。")
kanji_text = load_scripture_text(current_kanji, "(漢字版がありません)")
lines = scripture_text.splitlines()
kanji_lines = kanji_text.splitlines()

# グローバルな現在行のインデックス（0始まり）
current_index = 0

# --- ルート: メイン画面 ---
@app.route('/')
def index():
    # テンプレートにテキスト群と現在インデックス、漢字版の配列を渡す
    return render_template(
        'index.html',
        lines=lines,
        kanji_lines=kanji_lines,
        current_index=current_index
    )

# --- APIエンドポイント ---
@app.route('/get_current', methods=["GET"])
def get_current():
    global current_index
    return jsonify({
        "current_index": current_index,
        "current_line": lines[current_index] if current_index < len(lines) else "",
        "current_kanji": kanji_lines[current_index] if current_index < len(kanji_lines) else ""
    })

@app.route('/next', methods=["POST"])
def next_line():
    global current_index
    if current_index < len(lines) - 1:
        current_index += 1
    return jsonify({"current_index": current_index})

@app.route('/back', methods=["POST"])
def back_line():
    global current_index
    if current_index > 0:
        current_index -= 1
    return jsonify({"current_index": current_index})

@app.route('/reset', methods=["POST"])
def reset_line():
    global current_index
    current_index = 0
    return jsonify({"current_index": current_index})

# ※ お経の切り替え機能は、ファイル名を受け取って再読み込みするように拡張可能です。

if __name__ == '__main__':
    # デバッグモードで起動（本番時は必要に応じて設定変更）
    app.run(debug=True)
