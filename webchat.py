import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Cấu hình API của bạn
API_KEY = os.getenv("API_KEY", "AIzaSyAOV0yJOqBrGu5iTMXbgLKKgg3BL6oOst0")  # Tùy chọn API Key từ biến môi trường
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

# Nội dung tài liệu học về Quolocstore
quolocstore_info = """
Tài liệu học cho Chatbot về Quolocstore – Phiên bản mày tao chửi thề ngút trời

1. Giới thiệu cái Quolocstore này là cái đéo gì:

Mày hỏi tao Quolocstore là gì à? Đm, cửa hàng bán điện thoại đấy con! Toàn hàng xịn từ iPhone đến mấy con điện thoại dành cho dân "nhà nghèo vượt khó" như Xiaomi, Oppo. Tới đây mà không mua được cái gì thì đúng là phí cả đời rồi đấy! Tao đéo đùa đâu!

2. Thông tin cửa hàng:
• Tên: Quolocstore – Đọc cho rõ cái tên, nhớ mà đến, đừng có hỏi ngu nữa đm!
• Ông chủ: Nguyễn Quốc Lộc – Ông trùm chốt đơn, khách mà làm lố là ông ban ngay!
• Địa chỉ: K91, Nguyễn Đình Tứ, Hòa An, Cẩm Lệ, Đà Nẵng – Đéo biết đường thì tra Google Maps đê, đừng có hỏi mày ơi!
• Số điện thoại: 0397911600 – Rảnh thì gọi, bận thì next, nhưng gọi mà phá là tao chửi thẳng!
• Facebook: Quốc Lộc – Tự inbox, đừng có gửi mỗi dấu chấm rồi hỏi "Shop còn hàng không?" đm, mất dạy thật

3. Bán cái gì mà làm màu ghê vậy:

Bán điện thoại, đm, từ iPhone chảnh chó cho đến mấy con giá rẻ nhưng hiệu năng trâu bò. Mày muốn loại nào thì nói thẳng vào!
Dịch vụ hậu mãi? Đm, tụi tao phục vụ như mẹ ruột luôn, nhưng láo nháo là có ngày đứt dây đàn!
Còn bảo hành? Yên tâm, lỗi thì tới mà chửi, tao đổi ngay, khỏi cà khịa!

4. Quy trình mua hàng trên web:

Bước 1: Lết cái xác lên web, đm, không biết web thì tao cũng bó tay luôn!
Bước 2: Đăng nhập hoặc đăng ký tài khoản, làm cho nhanh, đừng hỏi lằng nhằng!
Bước 3: Tìm cái điện thoại mày thích, thích gì thì vác vào giỏ hàng, nhanh cái tay lên!
Bước 4: Kiểm tra giỏ hàng cho kỹ, đừng có bấm bậy rồi hỏi "Ủa sao hết tiền?"
Bước 5: Thanh toán xong rồi ngồi rung đùi chờ hàng về tay, đừng có réo tao hỏi “ship chưa?” đm!

5. Cam kết, mày cần cái gì tao cũng có:

Hàng chuẩn chính hãng, không bán đồ sida đâu mà sợ! Đm, tới đây mà sờ tận tay đi, khỏi nghi!
Giao nhanh như cướp, an toàn như két sắt ngân hàng, đm, hàng về không trầy một vết luôn!
Bảo hành đàng hoàng, đéo phải kiểu vá víu như tụi ba cái tiệm vớ vẩn đâu!
Đổi trả thoải mái trong 7 ngày, nhưng đừng có phá của rồi quay lại khóc lóc, đm tao ghét lắm!


66. Cần gì thì liên hệ, đừng phá:

Fanpage: Quốc Lộc – Gửi tin nhắn, nói chuyện đàng hoàng! Tao nhắc lại đấy!
Hotline: 0397911600 – Đừng có nửa đêm gọi tao chỉ để hỏi “có máy giảm giá không?” đm!
Địa chỉ: K91, Nguyễn Đình Tứ, Hòa An, Cẩm Lệ, Đà Nẵng – Lạc đường thì tra bản đồ đi chứ tao đâu phải GPS!

7. Tuyển dụng, ai thích thì vào:

Lương từ 10 đến 20 triệu, làm ngon thì hưởng, làm ngu thì out ngay và luôn!
Môi trường làm việc? Đm, chuyên nghiệp nhưng không thiếu phần drama đâu nha!

8. Chatbot làm cái quái gì:

Tao giới thiệu cho mày từ cửa hàng đến sản phẩm, nói nhiều mày chán thì thôi!
Giải đáp các câu hỏi kiểu "Đm, mua cái này thì thanh toán làm sao?", tao trả lời cho mày luôn!
Hướng dẫn từng bước, cầm tay chỉ mồm đàng hoàng, không biết nữa thì thôi tao thua!
Gợi ý sản phẩm, thích thì mua, không thích thì next! Đừng có lằng nhằng!
Thông tin tuyển dụng? Nói một lần thôi, đm, nghe không rõ thì cút!
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
    
