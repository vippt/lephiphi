from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

# === GEMINI 2.5 CHÍNH THỨC ===
MODEL_LIST = [
    "gemini-3.8-flash",
]

@app.route('/chat-bot/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat-bot/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def goi_ai(cau_hoi, model_ten):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_ten}:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": "Bạn là trợ lý thân thiện, trả lời tiếng Việt ngắn gọn tự nhiên. Câu hỏi: " + cau_hoi}]
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
        return jsonify({"reply": "❌ Chưa cài đặt GEMINI_KEY trên Render!"})

    for model in MODEL_LIST:
        try:
            ket_qua = goi_ai(cau_hoi, model)
            print(f"[{model}] → {str(ket_qua)[:200]}")
            
            if "error" in ket_qua:
                msg = ket_qua["error"]["message"]
                if "high demand" in msg.lower() or "quota" in msg.lower():
                    continue
                return jsonify({"reply": f"❌ {msg}"})
            
            if "candidates" in ket_qua and ket_qua["candidates"]:
                cau_tra_loi = ket_qua["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"reply": cau_tra_loi})

        except Exception as e:
            print(f"Lỗi {model}: {str(e)}")
            continue

    return jsonify({"reply": "⏳ AI tạm thời bận, vui lòng gửi lại sau 1-2 phút nhé!"})

if __name__ == "__main__":
    app.run(port=5000)
