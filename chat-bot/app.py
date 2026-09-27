from flask import Flask, request, jsonify, send_from_directory
import requests
import json

app = Flask(__name__)

# === THÔNG TIN CV ===
THONG_TIN_CV = """
THÔNG TIN VỀ LÊ PHI PHI:
- Tên: Lê Phi Phi
- Lĩnh vực: Công nghệ, Tự động hóa, Lập trình, Thiết kế web
- Kỹ năng: Python, HTML/CSS/JS, Google Apps Script, Tự động hóa, Thiết kế giao diện
- Dự án: cv.lephiphi.com, hệ thống tự động hóa, công cụ tổ chức sự kiện
- Liên hệ: qua trang lephiphi.com hoặc cv.lephiphi.com 0922332243
- Số điện thoại: 0922332243
"""

@app.route('/chat-bot/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat-bot/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def goi_pollinations(prompt, model_ten):
    """Gọi Pollinations với kiểm tra lỗi đầy đủ"""
    url = "https://text.pollinations.ai/"
    try:
        res = requests.post(
            url,
            json={
                "model": model_ten,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=40
        )
        
        # Kiểm tra mã trạng thái
        if res.status_code != 200:
            print(f"[{model_ten}] Mã lỗi: {res.status_code}")
            return None
        
        # Kiểm tra nội dung trống
        if not res.text or res.text.strip() == "":
            print(f"[{model_ten}] Phản hồi trống")
            return None
        
        # Kiểm tra JSON hợp lệ
        try:
            du_lieu = res.json()
        except json.JSONDecodeError as e:
            print(f"[{model_ten}] JSON không hợp lệ: {str(e)}")
            print(f"Nội dung: {res.text[:200]}")
            return None
        
        # Trích xuất câu trả lời
        return du_lieu.get("choices", [{}])[0].get("message", {}).get("content", "")
        
    except Exception as e:
        print(f"[{model_ten}] Lỗi kết nối: {str(e)}")
        return None

@app.route('/chat-bot/ask', methods=['POST'])
def ask():
    data = request.get_json()
    cau_hoi = data.get('message', '').strip()

    if not cau_hoi:
        return jsonify({"reply": "Bạn chưa nhập câu hỏi ạ!"})

    prompt = f"""Dựa trên thông tin sau đây, trả lời câu hỏi một cách tự nhiên bằng tiếng Việt:

{THONG_TIN_CV}

Nếu không có thông tin, trả lời lịch sự. Nếu câu hỏi không liên quan, trả lời hữu ích.
Câu hỏi: {cau_hoi}"""

    # Thử lần lượt từng mô hình
    for mo_hinh in ["mistral", "openai", "llama"]:
        cau_tra_loi = goi_pollinations(prompt, mo_hinh)
        if cau_tra_loi and len(cau_tra_loi.strip()) > 3:
            return jsonify({"reply": cau_tra_loi.strip()})

    # Nếu tất cả đều lỗi
    return jsonify({
        "reply": "⏳ Hệ thống AI đang bận nhẹ. Bạn vui lòng gửi lại sau vài giây nhé! Hoặc hỏi lại với nội dung đơn giản hơn."
    })

if __name__ == "__main__":
    app.run(port=5000)
