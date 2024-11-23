import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, jsonify, request
from flask_cors import CORS

# .envファイルを読み込む
load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI APIクライアントを初期化
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/multiply/<int:num>', methods=['GET'])
def multiply(num):
    result = num * 2
    return jsonify({"doubled_value": result})

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({"message": f"You said: {message}"})

@app.route('/api/chatgpt', methods=['POST'])
def chatgpt_request():
    print("ChatGPTリクエスト受信")
    data = request.get_json()
    selected_date = data.get('date')
    print(f"受信した日付: {selected_date}")
    
    if not selected_date:
        print("日付が提供されていません")
        return jsonify({"error": "日付が提供されていません"}), 400
    
    try:
        print("OpenAI APIリクエスト送信")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは優秀なアシスタントです。"},
                {"role": "user", "content": f"{selected_date}は何の日ですか？簡潔に説明してください。"}
            ]
        )
        answer = response.choices[0].message.content
        print("OpenAI APIレスポンス受信")

        # 画像生成リクエスト
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=f"{selected_date}の日を表す画像",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = image_response.data[0].url
        print("画像URL:", image_url)

        return jsonify({"response": answer, "image_url": image_url})
    except Exception as e:
        print(f"エラー発生: \n{str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
