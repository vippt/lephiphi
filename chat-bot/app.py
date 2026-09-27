from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_KEY", "")

@app.route('/chat-bot/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat-bot/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/chat-bot/ask', methods=['POST'])
def ask():
    data = request.get_json()
    cau_hoi = data.get('message', '').strip()

    if not cau_hoi:
        return jsonify({"reply": "Bạn chưa nhập câu hỏi ạ!"})
    if not GROQ_KEY:
        return jsonify({"reply": "❌ Chưa cài đặt GROQ_KEY!"})

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Bạn là trợ lý thông minh, thân thiện, trả lời tiếng Việt ngắn gọn tự nhiên."},
                    {"role": "user", "content": cau_hoi}
                ],
                "temperature": 0.7
            },
            timeout=30
        )

        ket_qua = res.json()
        if "choices" in ket_qua:
            cau_tra_loi = ket_qua["choices"][0]["message"]["content"]
            return jsonify({"reply": cau_tra_loi})
        
        return jsonify({"reply": "❌ " + str(ket_qua)})

    except Exception as e:
        return jsonify({"reply": f"❌ Lỗi: {str(e)}"})

if __name__ == "__main__":
    app.run(port=5000)
