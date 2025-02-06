import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Cấu hình API của bạn
API_KEY = os.getenv("API_KEY", "AIzaSyAOV0yJOqBrGu5iTMXbgLKKgg3BL6oOst00")  # Tùy chọn API Key từ biến môi trường
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

# Nội dung tài liệu học về Quolocstore
quolocstore_info = """
Tài liệu học cho Chatbot về Quolocstore

1. Giới thiệu chung về Quolocstore
   Quolocstore là một cửa hàng chuyên kinh doanh các dòng điện thoại di động của nhiều hãng khác nhau, mang đến sự lựa chọn phong phú và đa dạng cho khách hàng. Cửa hàng cung cấp các dịch vụ tận tâm, nhấn mạnh đến sự hài lòng và trải nghiệm mua sắm tuyệt vời.

2. Thông tin cửa hàng
   • Tên cửa hàng: Quolocstore
   • Chủ sử hữu: Nguyễn Quốc Lộc
   • Địa chỉ: K91, Nguyễn Đình Tứ, Hòa An, Cẩm Lệ, Đà Nẵng
   • Số điện thoại: 0397911600
   • Facebook: Quốc Lộc

3. Dịch vụ chính
   Cung cấp các sản phẩm điện thoại của các hãng nổi tiếng như: Apple (iPhone), Samsung, Xiaomi, Oppo, Vivo,... và các dịch vụ hậu mãi như bảo hành toàn quốc, tư vấn lựa chọn điện thoại phù hợp, thanh toán linh hoạt.

4. Quy trình mua hàng trên website
   - Truy cập website chính thức của Quolocstore.
   - Đăng nhập/đăng ký tài khoản.
   - Tìm kiếm sản phẩm, thêm vào giỏ hàng.
   - Kiểm tra giỏ hàng và thanh toán.
   - Xác nhận hoàn tất và nhận thông báo giao hàng.

5. Cam kết
   - Sản phẩm chính hãng, chất lượng cao.
   - Giao hàng nhanh chóng và an toàn.
   - Bảo hành chính hãng, hỗ trợ sửa chữa nhanh.
   - Đổi trả hàng trong vòng 7 ngày nếu có lỗi từ nhà sản xuất.

6. Thông tin liên hệ
   - Fanpage: Quốc Lộc
   - Hotline: 0397911600
   - Địa chỉ: K91, Nguyễn Đình Tứ, Hòa An, Cẩm Lệ, Đà Nẵng

7. Tuyển dụng nhân viên
   - Mức lương từ 10 triệu đến 20 triệu đồng.
   - Môi trường làm việc chuyên nghiệp.

8. Tính năng của Chatbot
   - Giới thiệu cửa hàng và sản phẩm.
   - Giải đáp các câu hỏi về mua hàng, điều kiện thanh toán.
   - Hướng dẫn quy trình mua sắm.
   - Gợi ý sản phẩm theo nhu cầu khách hàng.
   - Cung cấp thông tin tuyển dụng.
"""

# Lịch sử hội thoại
conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    user_message = request.json.get("message", "")

    # Kết hợp thông tin nền với câu hỏi của khách hàng
    combined_text = quolocstore_info + "\n\nCâu hỏi của khách hàng: " + user_message

    # Thêm tin nhắn của khách hàng vào lịch sử hội thoại
    conversation_history.append({
        "role": "user",
        "parts": [{"text": combined_text}]
    })

    payload = {
        "contents": conversation_history
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            # Thêm câu trả lời của chatbot vào lịch sử
            conversation_history.append({
                "role": "model",
                "parts": [{"text": answer}]
            })
            return jsonify({"reply": answer.strip()})
        else:
            return jsonify({"reply": "Chatbot không có câu trả lời."})
    else:
        return jsonify({"reply": f"Lỗi: {response.status_code}"}), response.status_code

if __name__ == "__main__":
    # Lấy cổng từ biến môi trường hoặc mặc định là 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
