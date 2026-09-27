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
        return jsonify({"reply": "❌ Chưa cài đặt GEMINI_KEY trên Render!"})

    # === THEO TÀI LIỆU CHÍNH THỨC GOOGLE ===
    url = "https://generativelanguage.googleapis.com/v1beta/interactions"
    
    headers = {
        "x-goog-api-key": GEMINI_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gemini-3.8-flash",
        "input": f"Bạn là trợ lý thông minh, thân thiện, trả lời bằng tiếng Việt ngắn gọn tự nhiên. Câu hỏi: {cau_hoi}"
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Mã trạng thái: {res.status_code}")
        
        ket_qua = res.json()
        
        if "error" in ket_qua:
            loi = ket_qua["error"]
            return jsonify({"reply": f"❌ {loi.get('message', 'Lỗi không xác định')}"})
        
        cau_tra_loi = ket_qua.get("output_text", "")
        if not cau_tra_loi:
            return jsonify({"reply": "❌ Không nhận được câu trả lời từ AI"})
        
        return jsonify({"reply": cau_tra_loi})

    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return jsonify({"reply": f"❌ Lỗi kết nối: {str(e)}"})

if __name__ == "__main__":
    app.run(port=5000)
