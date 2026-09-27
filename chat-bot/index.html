<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trợ Lý Thông Minh</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Segoe UI, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .chat-container { width: 100%; max-width: 450px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); overflow: hidden; display: flex; flex-direction: column; height: 85vh; max-height: 700px; }
        .chat-header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; text-align: center; font-size: 18px; font-weight: 600; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; background: #f8f9fa; }
        .message { margin-bottom: 15px; display: flex; max-width: 90%; }
        .user { margin-left: auto; flex-direction: row-reverse; }
        .ai { margin-right: auto; }
        .bubble { padding: 12px 18px; border-radius: 18px; line-height: 1.5; }
        .user .bubble { background: #667eea; color: white; border-bottom-right-radius: 4px; }
        .ai .bubble { background: white; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.08); border-bottom-left-radius: 4px; }
        .chat-input { display: flex; padding: 20px; background: white; border-top: 1px solid #eee; }
        #message-input { flex: 1; padding: 14px 20px; border: 2px solid #e0e0e0; border-radius: 30px; outline: none; font-size: 15px; transition: border 0.3s; }
        #message-input:focus { border-color: #667eea; }
        #send-btn { margin-left: 10px; padding: 14px 25px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 30px; cursor: pointer; font-size: 15px; font-weight: 600; transition: transform 0.2s; }
        #send-btn:hover { transform: scale(1.05); }
        .typing .bubble { color: #888; }
        .dot { animation: blink 1.4s infinite; }
        .dot:nth-child(2) { animation-delay: 0.2s; }
        .dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">🤖 Trợ Lý Thông Minh</div>
        <div class="chat-messages" id="messages">
            <div class="message ai">
                <div class="bubble">Xin chào! Tôi là trợ lý AI. Bạn cần hỗ trợ gì hôm nay? 😊</div>
            </div>
        </div>
        <div class="chat-input">
            <input type="text" id="message-input" placeholder="Nhập câu hỏi của bạn...">
            <button id="send-btn">Gửi</button>
        </div>
    </div>

    <script>
        const input = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        const messagesDiv = document.getElementById('messages');

        async function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            // Hiển thị tin nhắn người dùng
            addMessage(text, 'user');
            input.value = '';

            // Hiệu ứng đang gõ
            const typingId = addTyping();

            try {
                // Gọi API backend
                const response = await fetch('/chat-bot/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();
                removeTyping(typingId);
                
                if (data.reply) {
                    addMessage(data.reply, 'ai');
                } else {
                    addMessage('Xin lỗi, có lỗi xảy ra!', 'ai');
                }
            } catch (err) {
                removeTyping(typingId);
                addMessage('Lỗi kết nối, vui lòng thử lại!', 'ai');
            }
        }

        function addMessage(text, sender) {
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            div.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
            messagesDiv.appendChild(div);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function addTyping() {
            const id = 'typing-' + Date.now();
            const div = document.createElement('div');
            div.id = id;
            div.className = 'message ai typing';
            div.innerHTML = `<div class="bubble"><span class="dot">●</span> <span class="dot">●</span> <span class="dot">●</span></div>`;
            messagesDiv.appendChild(div);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            return id;
        }

        function removeTyping(id) {
            document.getElementById(id)?.remove();
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', e => e.key === 'Enter' && sendMessage());
    </script>
</body>
</html>
