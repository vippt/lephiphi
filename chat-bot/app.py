from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# === KHÔNG CẦN KHÓA GÌ CẢ ===

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

    # Gọi Pollinations AI — MIỄN PHÍ, không cần khóa
    prompt = f"Bạn là trợ lý thông minh, thân thiện, trả lời bằng tiếng Việt ngắn gọn tự nhiên. Câu hỏi: {cau_hoi}"
    
    try:
        import requests
        url = "https://text.pollinations.ai/"
        res = requests.post(url, json={
            "model": "mistral",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }, timeout=30)

        if res.ok:
            ket_qua = res.json()
            cau_tra_loi = ket_qua.get("choices", [{}])[0].get("message", {}).get("content", "")
            if cau_tra_loi:
                return jsonify({"reply": cau_tra_loi})

        return jsonify({"reply": "Xin lỗi, đang xử lý, thử lại nhé!"})

    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return jsonify({"reply": f"❌ Lỗi: {str(e)}"})

if __name__ == "__main__":
    app.run(port=5000)
