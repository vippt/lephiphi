from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

GROQ_KEY = os.environ.get("GROQ_KEY", "")

# === TÊN MÔ HÌNH CHÍNH XÁC TRÊN GROQ ===
MODEL_LIST = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "gemma2-9b-it"
]

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
        return jsonify({"reply": "❌ Chưa cài đặt GROQ_KEY trên Render!"})

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    for model in MODEL_LIST:
        try:
            res = requests.post(
                url,
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "Bạn là trợ lý thông minh, thân thiện, trả lời bằng tiếng Việt ngắn gọn tự nhiên."},
                        {"role": "user", "content": cau_hoi}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                },
                timeout=30
            )

            ket_qua = res.json()
            
            if "error" in ket_qua:
                print(f"[{model}] Lỗi: {ket_qua['error']}")
                continue
            
            if "choices" in ket_qua and ket_qua["choices"]:
                cau_tra_loi = ket_qua["choices"][0]["message"]["content"]
                return jsonify({"reply": cau_tra_loi})

        except Exception as e:
            print(f"Lỗi {model}: {str(e)}")
            continue

    return jsonify({"reply": "⚠️ Tất cả mô hình đều bận, thử lại sau nhé!"})

if __name__ == "__main__":
    app.run(port=5000)
