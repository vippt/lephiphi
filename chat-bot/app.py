from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import os

app = Flask(__name__)

GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

# Danh sách mô hình dự phòng
MODEL_LIST = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-2.0-flash"
]

@app.route('/chat-bot/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat-bot/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def goi_ai(cau_hoi, model_ten):
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_ten}:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": "Bạn là trợ lý thông minh, thân thiện, trả lời tiếng Việt ngắn gọn tự nhiên. Câu hỏi: " + cau_hoi}]
        }]
    }
    res = requests.post(url, json=payload, timeout=30)
    return res.json()

@app.route('/chat-bot/ask', methods=['POST'])
def ask():
    data = request.get_json()
    cau_hoi = data.get('message', '').strip()

    if not cau_hoi:
        return jsonify({"reply": "Bạn chưa nhập câu hỏi ạ!"})
    if not GEMINI_KEY:
        return jsonify({"reply": "❌ Chưa cài đặt khóa AI!"})

    # Thử lần lượt từng mô hình, tối đa 2 lần mỗi mô hình
    for model in MODEL_LIST:
        for thu in range(2):
            try:
                ket_qua = goi_ai(cau_hoi, model)
                
                if "error" in ket_qua:
                    msg = ket_qua["error"].get("message", "")
                    print(f"[{model}] Lỗi: {msg}")
                    # Nếu quá tải → thử ngay mô hình khác
                    if "high demand" in msg or "quota" in msg:
                        time.sleep(1)
                        continue
                    return jsonify({"reply": f"❌ {msg}"})
                
                if "candidates" in ket_qua and ket_qua["candidates"]:
                    cau_tra_loi = ket_qua["candidates"][0]["content"]["parts"][0]["text"]
                    return jsonify({"reply": cau_tra_loi})

            except Exception as e:
                print(f"Lỗi gọi AI: {str(e)}")
                time.sleep(1)

    return jsonify({"reply": "⏳ AI đang bận, vui lòng gửi lại sau ít phút nhé!"})

if __name__ == "__main__":
    app.run(port=5000)
