from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# Lấy khóa từ biến môi trường (an toàn)
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

# Phục giao diện tại thư mục gốc /chat-bot/
@app.route('/chat-bot/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat-bot/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Nhận câu hỏi & trả lời
@app.route('/chat-bot/ask', methods=['POST'])
def ask():
    data = request.get_json()
    cau_hoi = data.get('message', '').strip()
    
    if not cau_hoi:
        return jsonify({"reply": "Bạn chưa nhập câu hỏi ạ!"})

    # Gọi AI Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": "Bạn là trợ lý thông minh, thân thiện, trả lời bằng tiếng Việt ngắn gọn tự nhiên. Câu hỏi: " + cau_hoi}]
        }]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        ket_qua = res.json()
        cau_tra_loi = ket_qua["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": cau_tra_loi})
    except Exception as e:
        print(f"Lỗi: {e}")
        return jsonify({"reply": "Xin lỗi, tôi chưa trả lời được ngay, thử lại sau nhé!"})

if __name__ == "__main__":
    app.run(port=5000)
