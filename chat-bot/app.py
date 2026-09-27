from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# === THÔNG TIN TỪ CV.LEPHIPHI.COM — BOT SẼ DỰA VÀO ĐÂY ĐỂ TRẢ LỜI ===
THONG_TIN_CV = """
THÔNG TIN VỀ LÊ PHI PHI:

- Tên: Lê Phi Phi
- Lĩnh vực: Công nghệ, Tự động hóa, Lập trình, Thiết kế web
- Kỹ năng chính:
  • Lập trình: Python, HTML/CSS/JavaScript, Google Apps Script
  • Tự động hóa điều khiển thiết bị điện, hệ thống thông minh
  • Thiết kế trang web, cổng liên hệ, công cụ tổ chức sự kiện
  • Quản trị tài chính, quy trình làm việc hiệu quả
- Dự án đã thực hiện:
  • Trang giới thiệu cá nhân cv.lephiphi.com
  • Hệ thống tự động hóa, điều khiển từ xa
  • Công cụ hỗ trợ tổ chức đám cưới, quản lý thông tin
  • Mẫu giao diện hiện đại, tương thích di động
- Đặc điểm: Làm việc thực tế, giải pháp đơn giản hiệu quả, hỗ trợ tận tình
- Liên hệ: Thông qua biểu mẫu tại lephiphi.com hoặc cv.lephiphi.com
"""

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

    # Xây dựng nội dung gửi AI: thông tin CV + câu hỏi
    prompt = f"""Dưới đây là thông tin về Lê Phi Phi:

{THONG_TIN_CV}

Hãy trả lời câu hỏi dựa trên thông tin trên. Nếu không có thông tin, trả lời lịch sự và nói bạn không biết hoặc hướng dẫn liên hệ.
Nếu câu hỏi không liên quan đến thông tin trên, trả lời một cách hữu ích và thân thiện.

Câu hỏi: {cau_hoi}
Trả lời bằng tiếng Việt ngắn gọn, tự nhiên, dễ hiểu.
"""

    # === Dùng Pollinations — MIỄN PHÍ, KHÔNG CẦN KHÓA ===
    try:
        res = requests.post(
            "https://text.pollinations.ai/",
            json={
                "model": "mistral",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "seed": 42
            },
            timeout=35
        )

        if res.ok:
            ket_qua = res.json()
            cau_tra_loi = ket_qua.get("choices", [{}])[0].get("message", {}).get("content", "")
            if cau_tra_loi:
                return jsonify({"reply": cau_tra_loi.strip()})

        # Dự phòng: mô hình khác
        res2 = requests.post(
            "https://text.pollinations.ai/",
            json={
                "model": "openai",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=35
        )
        if res2.ok:
            kq2 = res2.json()
            tl2 = kq2.get("choices", [{}])[0].get("message", {}).get("content", "")
            if tl2:
                return jsonify({"reply": tl2.strip()})

        return jsonify({"reply": "⏳ Hệ thống đang bận, vui lòng gửi lại sau vài giây nhé!"})

    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return jsonify({"reply": f"❌ Lỗi: {str(e)} — vui lòng thử lại"})

if __name__ == "__main__":
    app.run(port=5000)
