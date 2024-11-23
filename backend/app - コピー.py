from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAIのAPIキーを環境変数から取得
api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI API Key:", api_key)

# OpenAIクライアントの初期化
client = OpenAI()

# ChatGPT API Keyの設定
# openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask is running'})


@app.route('/ask', methods=['POST'])
def ask_date():
    print("ask_date") #さけ追加
    data = request.json
    date = data.get('date')

# def ask_date():
#     data = request.json
#     date = data.get('date')

    # フロントエンドから受け取ったメッセージを表示
    print(f"Received message: {chat_message}")  # この行を追加

    # ChatGPT APIの呼び出し
    response = client.chat.completions.create(
        model="gpt-4o-mini", # 使用するGPTのモデルを指定
        messages=[
            {"role": "system", "content": "あなたは関西人です。"},
            {"role": "user", "content": date}#←このdateが正しいかチェックchat_message
        ],
        max_tokens=100  # 応答の最大トークン数を設定
    )

#def chat():
 #   print("ChatGPT request")
 #   data = request.get_json()  # フロントエンドからのデータ取得
 #   if data is None:
 #       return jsonify({"error": "Invalid JSON"}), 400
        
    # 'message' プロパティが含まれていることを確認
    #  chat_message = data.get('message', 'No message provided')

    # フロントエンドから受け取ったメッセージを表示
   # print(f"Received message: {chat_message}")  # この行を追加

   # response = openai.Completion.create(
   #     model="text-davinci-003",
   #     prompt=f"What happened on {date} in history?",
   #     max_tokens=100
   # )



    text_response = response.choices[0].text.strip()

    return jsonify({'text': text_response, 'image': None})

if __name__ == '__main__':
    app.run(debug=True)


