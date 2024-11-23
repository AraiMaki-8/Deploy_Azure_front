import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# CORS設定を強化
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # CORS設定を更新

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


@app.route('/api/ask-date', methods=['POST'])
def ask_date():
    print("ask_date") #さけ追加
    data = request.get_json()
    date = data.get('date') # フロントエンドから送られた日付を取得

# def ask_date():
#     data = request.json
#     date = data.get('date')

    # フロントエンドから受け取ったメッセージを表示
    print(f"Received date: {date}")  # この行を追加

    try:

        # ChatGPT APIの呼び出し
        response = client.chat.completions.create(
            model="gpt-4o", # 使用するGPTのモデルを指定
            messages=[
                {"role": "system", "content": "あなたは歴史の専門家です。"},
                {"role": "user", "content":  f" {date} は何の日かを100文字以内にまとめて教えてください。それに合わせた画像も生成してください"} # ユーザーのメッセージ
            ],
            #max_tokens=100  # 応答の最大トークン数を設定
        )

        # ChatGPTからの応答
        chatgpt_reply = response.choices[0].message.content
        print(f"ChatGPTからの応答: {chatgpt_reply}")

        # 応答をもとに画像生成プロンプトを作成
        image_prompt = f"{chatgpt_reply}に関連する画像を生成してください。"

        # DALL·E APIを使って画像を生成
        response_image = client.Image.create(
            model="dall-e-3",
            prompt=image_prompt,  # ChatGPTの応答に基づくプロンプト
            n=1, # 生成する画像の数
            size="1024x1024"  # 画像のサイズ
        )
        
        # 生成された画像のURLを取得
        image_url = response_image['data'][0]['url']
        print(f"生成された画像のURL: {image_url}")

        # 応答と画像URLを返す
        return jsonify({"text": chatgpt_reply, "image_url": image_url})




        # # 応答のメッセージを抽出
        # chatgpt_reply = response.choices[0].message.content
        # print(f"ChatGPTからの応答: {chatgpt_reply}")
        # return jsonify({"text": chatgpt_reply})

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}") # エラーハンドリング
        return jsonify({"error": "Failed to get response from OpenAI"}), 500

if __name__ == '__main__':
    app.run(debug=True)

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
   
    # text_response = response.choices[0].text.strip()

    # return jsonify({'text': text_response, 'image': None})
