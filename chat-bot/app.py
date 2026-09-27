from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

GEMINI_KEY = os.environ.get("GEMINI_KEY", "")

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

    if not GEMINI_KEY:
        return jsonify({"reply": "❌ Chưa cài đặt khóa AI! Vui lòng liên hệ quản trị."})

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3.8-flash:generateContent?key={GEMINI_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Bạn là trợ lý thông minh, thân thiện, trả lời bằng tiếng Việt ngắn gọn tự nhiên. Câu hỏi: " + cau_hoi}]
        }]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        print(f"Trạng thái API: {res.status_code}")
        
        ket_qua = res.json()
        
        # Kiểm tra có lỗi từ API không
        if "error" in ket_qua:
            print(f"Lỗi API: {ket_qua['error']}")
            return jsonify({"reply": f"❌ Lỗi AI: {ket_qua['error'].get('message', 'Không xác định')}"})
        
        # Kiểm tra có kết quả không
        if "candidates" not in ket_qua or not ket_qua["candidates"]:
            print(f"Phản hồi không có candidates: {ket_qua}")
            return jsonify({"reply": "❌ AI không trả lời được, thử lại sau nhé!"})
        
        cau_tra_loi = ket_qua["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": cau_tra_loi})

    except Exception as e:
        print(f"Lỗi hệ thống: {str(e)}")
        return jsonify({"reply": f"❌ Lỗi: {str(e)}"})

if __name__ == "__main__":
    app.run(port=5000)
