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