<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>University Assistant</title>
    <style>
        :root {
            --primary: #6200EE; /* Material Design purple */
            --primary-dark: #3700B3;
            --secondary: #03DAC6; /* Teal */
            --surface: #FFFFFF;
            --background: #F5F5F5;
            --on-primary: #FFFFFF;
            --on-surface: #212121;
            --on-background: #212121;
            --error: #B00020;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            background-color: var(--background);
            color: var(--on-background);
            height: 100vh;
            touch-action: manipulation;
        }
        
        /* Module 1: Chatbot FAB */
        .chatbot-fab {
            position: fixed;
            bottom: 24px;
            right: 16px;
            width: 56px;
            height: 56px;
            border-radius: 28px;
            background-color: var(--primary);
            color: var(--on-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 3px 5px rgba(0,0,0,0.2), 0 6px 10px rgba(0,0,0,0.14), 0 1px 18px rgba(0,0,0,0.12);
            z-index: 1000;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            outline: none;
        }
        
        .chatbot-fab:hover, .chatbot-fab:focus {
            background-color: var(--primary-dark);
            transform: scale(1.1);
        }
        
        .chatbot-fab img {
            width: 24px;
            height: 24px;
            filter: brightness(0) invert(1);
        }
        
        /* Module 2: Chat Interface */
        .chat-interface {
            position: fixed;
            bottom: 100px;
            right: 16px;
            width: calc(100% - 32px);
            max-width: 400px;
            height: 65vh;
            max-height: 600px;
            background-color: var(--surface);
            border-radius: 16px 16px 0 0;
            box-shadow: 0 8px 10px rgba(0,0,0,0.2), 0 16px 24px rgba(0,0,0,0.14), 0 6px 30px rgba(0,0,0,0.12);
            display: none;
            flex-direction: column;
            z-index: 999;
            overflow: hidden;
            transform-origin: bottom right;
        }
        
        .chat-interface.active {
            display: flex;
            animation: scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .chat-header {
            background-color: var(--primary);
            color: var(--on-primary);
            padding: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .chat-title {
            font-weight: 500;
            font-size: 1.25rem;
        }
        
        .close-btn {
            background: none;
            border: none;
            color: var(--on-primary);
            width: 24px;
            height: 24px;
            font-size: 1.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .chat-container {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background-color: var(--background);
            -webkit-overflow-scrolling: touch;
        }
        
        .message {
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.4;
            font-size: 0.95rem;
            animation: messageIn 0.2s ease;
            word-wrap: break-word;
        }
        
        @keyframes messageIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .bot-message {
            background-color: var(--surface);
            border-bottom-left-radius: 4px;
            align-self: flex-start;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            color: var(--on-surface);
        }
        
        .user-message {
            background-color: var(--primary);
            color: var(--on-primary);
            border-bottom-right-radius: 4px;
            align-self: flex-end;
        }
        
        .quick-replies {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }
        
        .quick-reply {
            background-color: var(--surface);
            border: 1px solid #E0E0E0;
            border-radius: 16px;
            padding: 8px 12px;
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .quick-reply:hover, .quick-reply:focus {
            background-color: #F5F5F5;
            border-color: var(--primary);
        }
        
        .typing-indicator {
            display: flex;
            gap: 6px;
            padding: 12px 16px;
            background-color: var(--surface);
            border-radius: 18px;
            width: fit-content;
            margin-bottom: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background-color: #757575;
            border-radius: 50%;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-4px); }
        }
        
        .input-area {
            padding: 8px 16px;
            background-color: var(--surface);
            border-top: 1px solid #E0E0E0;
            display: flex;
            gap: 8px;
            align-items: center;
        }
        
        #user-input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #E0E0E0;
            border-radius: 24px;
            outline: none;
            font-size: 0.95rem;
            background-color: var(--surface);
            color: var(--on-surface);
            transition: all 0.2s;
        }
        
        #user-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(98,0,238,0.2);
        }
        
        #send-btn {
            background-color: var(--primary);
            color: var(--on-primary);
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        #send-btn:hover, #send-btn:focus {
            background-color: var(--primary-dark);
        }
        
        /* Android-specific optimizations */
        @media (max-width: 600px) {
            .chat-interface {
                bottom: 0;
                right: 0;
                width: 100%;
                max-width: 100%;
                height: 75vh;
                border-radius: 16px 16px 0 0;
            }
            
            .message {
                max-width: 90%;
            }
            
            .chatbot-fab {
                bottom: 16px;
                right: 16px;
            }
        }
        
        /* Prevent text selection for better mobile UX */
        * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        input, textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }
    </style>
</head>
<body>
    <!-- Module 1: Floating Action Button (Android-style) -->
    <button class="chatbot-fab" id="chatbot-fab" aria-label="Open chat">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Chat">
    </button>
    
    <!-- Module 2: Chat Interface -->
    <div class="chat-interface" id="chat-interface">
        <div class="chat-header">
            <div class="chat-title">University Assistant</div>
            <button class="close-btn" id="close-btn" aria-label="Close chat">×</button>
        </div>
        
        <div class="chat-container" id="chat-container">
            <!-- Messages will appear here -->
        </div>
        
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Type your question..." autocomplete="off" enterkeyhint="send">
            <button id="send-btn" aria-label="Send message">➤</button>
        </div>
    </div>

    <script>
        // Comprehensive FAQ Database (Android-optimized)
        const faqDatabase = {
            // [Previous FAQ entries remain the same]
            // ...
            
            // Added Android-specific questions
            "app download": "Download the official university app from the Google Play Store. Search for '[Your University] Mobile'.",
            "android issues": "For app issues on Android, try clearing cache in Settings > Apps. If problems persist, contact IT support.",
            "mobile login": "Use your university credentials to log in to mobile services. Enable biometric login in app settings for faster access.",
            "notifications": "Manage app notifications in Android Settings > Apps > [University App] > Notifications.",
            "offline access": "Some app features work offline. Download course materials while on WiFi for offline access.",
            "tablet support": "The university app is optimized for both phones and tablets. Landscape mode available on larger screens.",
            "android requirements": "App requires Android 8.0 or later. Update your OS for best performance and security.",
            "sync issues": "If data isn't syncing, pull down to refresh or check your internet connection in Android Settings.",
            
            // [Rest of the FAQ database]
            // ...
        };

        // Quick reply suggestions (Android-optimized)
        const quickReplies = [
            "App download",
            "Mobile login help",
            "Class schedule",
            "Library hours",
            "Campus map",
            "IT support",
            "Bus schedule",
            "Student services"
        ];

        // DOM elements
        const fab = document.getElementById('chatbot-fab');
        const chatInterface = document.getElementById('chat-interface');
        const closeBtn = document.getElementById('close-btn');
        const chatContainer = document.getElementById('chat-container');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');

        // Toggle chat interface
        fab.addEventListener('click', () => {
            chatInterface.classList.add('active');
            userInput.focus();
        });
        
        closeBtn.addEventListener('click', () => {
            chatInterface.classList.remove('active');
        });

        // Close when clicking outside (for Android UX)
        document.addEventListener('click', (e) => {
            if (!chatInterface.contains(e.target) && e.target !== fab) {
                chatInterface.classList.remove('active');
            }
        });

        // Initial bot message
        setTimeout(() => {
            addBotMessage("Hello! I'm your university assistant. I can help with registration, campus services, app support, and more!");
            showQuickReplies();
        }, 1000);

        // Send message functions
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        // Android back button support
        document.addEventListener('backbutton', handleBackButton, false);
        function handleBackButton() {
            if (chatInterface.classList.contains('active')) {
                chatInterface.classList.remove('active');
            } else {
                // Default back button behavior
                navigator.app.exitApp();
            }
        }

        // Touch-optimized functions
        function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;

            addUserMessage(message);
            userInput.value = '';
            showTyping();
            
            setTimeout(() => {
                const response = getBotResponse(message);
                addBotMessage(response);
                showQuickReplies();
            }, 600 + Math.random() * 800); // Faster response for mobile
        }

        function addUserMessage(text) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            messageDiv.textContent = text;
            chatContainer.appendChild(messageDiv);
            scrollToBottom();
        }

        function addBotMessage(text) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message bot-message';
            messageDiv.innerHTML = text;
            chatContainer.appendChild(messageDiv);
            scrollToBottom();
        }

        function scrollToBottom() {
            chatContainer.scrollTop = chatContainer.scrollHeight;
            // Smooth scrolling for Android
            chatContainer.style.scrollBehavior = 'smooth';
            setTimeout(() => {
                chatContainer.style.scrollBehavior = 'auto';
            }, 500);
        }

        function showTyping() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator';
            typingDiv.innerHTML = `
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            `;
            chatContainer.appendChild(typingDiv);
            scrollToBottom();
            
            setTimeout(() => {
                if (typingDiv.parentNode) typingDiv.remove();
            }, 1500);
        }

        function showQuickReplies() {
            document.querySelectorAll('.quick-replies').forEach(el => el.remove());
            
            const container = document.createElement('div');
            container.className = 'quick-replies';
            
            quickReplies.forEach(reply => {
                const btn = document.createElement('div');
                btn.className = 'quick-reply';
                btn.textContent = reply;
                btn.addEventListener('click', () => {
                    userInput.value = reply;
                    sendMessage();
                });
                container.appendChild(btn);
            });
            
            chatContainer.appendChild(container);
            scrollToBottom();
        }

        function getBotResponse(userMessage) {
            userMessage = userMessage.toLowerCase();
            
            // Check for direct matches
            for (const [keyword, response] of Object.entries(faqDatabase)) {
                const regex = new RegExp(`\\b${keyword}\\b`, 'i');
                if (regex.test(userMessage)) {
                    return response;
                }
            }
            
            // Check for similar questions
            if (/hi|hello|hey/.test(userMessage)) return faqDatabase['hello'];
            if (/app|download|android/.test(userMessage)) return faqDatabase['app download'];
            if (/register|enroll/.test(userMessage)) return faqDatabase['register for classes'];
            if (/login|sign in/.test(userMessage)) return faqDatabase['mobile login'];
            if (/map|location/.test(userMessage)) return faqDatabase['campus map'];
            if (/bus|transport/.test(userMessage)) return faqDatabase['bus schedule'];
            
            return faqDatabase['default'];
        }

        // Android vibration feedback
        function vibrate() {
            if (navigator.vibrate) {
                navigator.vibrate(50);
            }
        }

        // Add vibration to interactions
        fab.addEventListener('click', vibrate);
        sendBtn.addEventListener('click', vibrate);
        closeBtn.addEventListener('click', vibrate);
    </script>
</body>
</html>
