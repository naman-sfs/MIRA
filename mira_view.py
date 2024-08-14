import os

html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MIRA</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #181818;
            }}

            .container {{
                background-color: #f3f3f3;
                padding: 40px;
                border-radius: 15px;
                /* box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px; */
                width: 83%;
                height: 80%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                box-shadow: #6f6a69 0px 45px 90px -18px inset, #6f6a69 0px 27px 54px -27px inset;
            }}

            #heading {{
                color: #060606;
                font-family: cursive;
                background: linear-gradient(to right, #121FCF 0%, #CF1512 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;

            }}

            input[type="text"] {{
                width: 60%;
                padding: 15px;
                margin: 20px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }}

            button {{
                padding: 15px 30px;
                margin: 10px;
                border: 2px solid white;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
            }}
            
            button:hover{{
                background-color:lightslategrey;
            }}

            .submit-btn {{
                background-color: #060606;
                color: white;
            }}

            .clear-btn {{
                background-color: #6f6a69;
                color: white;
            }}

            .answer {{
                margin-top: 20px;
                font-weight: 500;
                font-size: 18px;
                text-align: left;
                color: #060606;
                
            }}

            .loader {{
                border: 8px solid #f3f3f3;
                border-radius: 50%;
                border-top: 8px solid black;
                width: 50px;
                height: 50px;
                animation: spin 0.5s linear infinite;
                display: none;
                margin: 20px auto;
                position:relative;
            }}
            
            .copy-btn {{
                background-color: #080808;
                color: white;
                margin-top:20px;
            }}
            
            .counter {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 16px;
                font-weight: bold;
                color: #060606;
            }}

            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 id="heading">MIRA</h1>
            <input type="text" id="question" placeholder="Ask your question here...">
            <div class="button-container" style="display:flex;">
                <button class="submit-btn" onclick="submitQuestion()">Submit</button>
                <button class="clear-btn" onclick="clearQuestion()" style="display:none;">Ask a New Question</button>
            </div>
            <div class="loader" id="loader">
                <div class="counter" id="counter">0</div>
            </div>
            <div class="answer" id="answer"></div>
            <button class="copy-btn" onclick="copyToClipboard()" style="display:none;">Copy Response</button>
        </div>

        <script>
            function submitQuestion() {{
                const question = document.getElementById('question').value;
                if (question.trim() === '') {{
                    alert('Please enter a question.');
                    return;
                }}

                // Show loader
                document.getElementById('loader').style.display = 'block';
                document.getElementById('answer').innerText = '';
                document.querySelector('.copy-btn').style.display = 'none';
                startCounter();
                // API call
                fetchAnswerFromAPI(question);
            }}

            function fetchAnswerFromAPI(question) {{
                

                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");

                const raw = JSON.stringify({{
                "question": question,
                "key": "1234"
                }});

                const requestOptions = {{
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
                }};

                fetch("{os.getenv('MY_DOMAIN')}/api/mira/ask", requestOptions)
                .then((response) => response.json())
                .then((result) => {{
                    const answer = result.data;
                    document.getElementById('answer').innerText = answer;
                    // Hide loader
                    document.getElementById('loader').style.display = 'none';
                    document.querySelector('.copy-btn').style.display = 'block';
                    document.querySelector('.clear-btn').style.display = 'block';
                    stopCounter();
                }})
                .catch((error) => {{
                    console.error(error)
                    document.getElementById('answer').innerText = error;
                    document.getElementById('loader').style.display = 'none';
                    document.querySelector('.clear-btn').style.display = 'block';
                    stopCounter();           
                }});
            }}

            function clearQuestion() {{
                document.getElementById('question').value = '';
                document.getElementById('answer').innerText = '';
                document.getElementById('loader').style.display = 'none';
                document.querySelector('.copy-btn').style.display = 'none';
                document.querySelector('.clear-btn').style.display = 'none';
                stopCounter();
            }}
            
            function copyToClipboard() {{
                const answer = document.getElementById('answer').innerText;
                const textarea = document.createElement('textarea');
                textarea.value = answer;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('Answer copied to clipboard!');
            }}
            
            function startCounter() {{
                let count = 0;
                document.getElementById('counter').innerText = count;
                counterInterval = setInterval(() => {{
                    count++;
                    document.getElementById('counter').innerText = count;
                }}, 1000);
            }}

            function stopCounter() {{
                clearInterval(counterInterval);
                document.getElementById('counter').innerText = '0';
            }}
            
        </script>
    </body>
    </html>

"""



html_content_convo = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIRA Chat</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: row;
            height: 100vh;
            margin: 0;
            width:60vw;
            position:fixed;
            left:20vw;
            background-color: #3d3d3d;
            

        }}
        #chat-container {{
            flex: 1;
            padding: 10px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            background-color: #181818;
        }}
        .chat-message {{
            max-width: 60%;
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
            clear: both;
        }}
        .user-message {{
            background-color: #dcf8c6;
            align-self: flex-end;
            text-align: right;
        }}
        .assistant-message {{
            background-color: #f1f0f0;
            align-self: flex-start;
            ont-family: system-ui;
        }}
        #input-container {{
            display: flex;
            padding: 0px 0px;
            
        }}
        #input-container input {{
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }}
        #input-container button {{
            padding: 10px;
            margin-left: 0px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            width: 10%;
        }}
        .typing {{
            font-style: italic;
            color: #888;
        }}
        #header {{
            display: flex;
            align-items: center;
            padding: 5px;
            background-color: #f1f0f0;
            color: white;
            padding-left:10px;
        }}
        #header div {{
            width: 25px;
            height: 25px;
            border-radius: 50%;
            margin-right: 10px;
            background-color: black;
            border: 2px solid #007bff;
        }}
        #header h1 {{
            font-size: 1.5em;
            margin: 0;
            font-family: cursive;
            background: linear-gradient(to right, #121FCF 0%, #CF1512 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        
        #sidebar {{
            width: 240px;
            background-color: #f4f4f4;
            padding: 0px;
            height: 100vh;
            overflow-y: auto;
        }}

        #sidebar-heading{{
            background-color: #007bff;
            font-size: 1.5em;
            padding: 8px;
            font-family: sans-serif;
            font-weight: 700;
            color:#f1f0f0
        }}
        #chat {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        
        .conversation {{
            cursor: pointer;
            padding: 10px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .conversation:hover {{
            background-color: #007bff;
            color: #f1f0f0;
        }}
    </style>
</head>
<body>
    <div id="sidebar">
        <div id="sidebar-heading">Conversations</div>
        <div id="conversation-list">
            <div class="conversation">FastAPI CRUD operations in python and mongo</div>
            <div class="conversation">How to build a robot</div>
            <div class="conversation">What is Bipolar Disorder?</div>
        </div>
    </div>
    <div id="chat">
        <div id="header">
            <div></div>
            <h1>MIRA</h1>
        </div>
        <div id="chat-container"></div>
        <div id="input-container">
            <input type="text" id="message-input" placeholder="Type a message...">
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        let chatHistory = [];

        document.getElementById('send-button').addEventListener('click', sendMessage);
        document.getElementById('message-input').addEventListener('keypress', function (e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});

        function sendMessage() {{
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            if (message === '') return;

            // Add user message to chat
            addMessageToChat('user', message);
            input.value = '';

            // Show typing animation
            showTypingAnimation();

            // Send message to the assistant
            fetch('{os.getenv('MY_DOMAIN')}/api/mira/ask', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    question: message,
                    key: "1234"
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                // Remove typing animation
                removeTypingAnimation();

                // Add assistant's reply to chat
                addMessageToChat('assistant', data.data);
            }})
            .catch(error => {{
                console.error('Error:', error);
            }});
        }}

        function addMessageToChat(sender, message) {{
            const chatContainer = document.getElementById('chat-container');
            const messageElement = document.createElement('div');
            messageElement.classList.add('chat-message');
            if (sender === 'user') {{
                messageElement.classList.add('user-message');
            }} else {{
                messageElement.classList.add('assistant-message');
            }}
            messageElement.innerText = message;

            // Add message to chat history
            chatHistory.push({{ sender: sender, message: message }});

            chatContainer.appendChild(messageElement);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}

        function showTypingAnimation() {{
            const chatContainer = document.getElementById('chat-container');
            const typingElement = document.createElement('div');
            typingElement.classList.add('chat-message', 'assistant-message', 'typing');
            typingElement.textContent = 'Assistant is typing...';
            typingElement.id = 'typing-animation';

            chatContainer.appendChild(typingElement);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}

        function removeTypingAnimation() {{
            const typingElement = document.getElementById('typing-animation');
            if (typingElement) {{
                typingElement.remove();
            }}
        }}
    </script>
</body>
</html>

"""
