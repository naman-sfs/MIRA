html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Question Answering Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #5a5757;
            }

            .container {
                background-color: rgb(224, 212, 212);
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
                width: 80%;
                height: 80%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            #heading {
                color:#767579
            }

            input[type="text"] {
                width: 60%;
                padding: 15px;
                margin: 20px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }

            button {
                padding: 15px 30px;
                margin: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            .submit-btn {
                background-color: #4CAF50;
                color: white;
            }

            .clear-btn {
                background-color: #f44336;
                color: white;
            }

            .answer {
                margin-top: 20px;
                font-weight: bold;
                font-size: 18px;
                
            }

            .loader {
                border: 8px solid #f3f3f3;
                border-radius: 50%;
                border-top: 8px solid #3498db;
                width: 50px;
                height: 50px;
                animation: spin 2s linear infinite;
                display: none;
                margin: 20px auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 id="heading">MIRA</h1>
            <input type="text" id="question" placeholder="Ask your question here...">
            <button class="submit-btn" onclick="submitQuestion()">Submit</button>
            <button class="clear-btn" onclick="clearQuestion()">Ask a New Question</button>
            <div class="loader" id="loader"></div>
            <div class="answer" id="answer"></div>
        </div>

        <script>
            function submitQuestion() {
                const question = document.getElementById('question').value;
                if (question.trim() === '') {
                    alert('Please enter a question.');
                    return;
                }

                // Show loader
                document.getElementById('loader').style.display = 'block';
                document.getElementById('answer').innerText = '';

                // Mock API call
                fetchAnswerFromAPI(question);
            }

            function fetchAnswerFromAPI(question) {
                

                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");

                const raw = JSON.stringify({
                "question": question,
                "key": "1234"
                });

                const requestOptions = {
                method: "POST",
                headers: myHeaders,
                body: raw,
                redirect: "follow"
                };

                fetch("http://ec2-3-106-224-103.ap-southeast-2.compute.amazonaws.com:8000/api/mira/ask", requestOptions)
                .then((response) => response.json())
                .then((result) => {
                    const answer = result.data;
                    document.getElementById('answer').innerText = answer;
                    // Hide loader
                    document.getElementById('loader').style.display = 'none';
                })
                .catch((error) => {
                    console.error(error)
                    document.getElementById('answer').innerText = error;
                    document.getElementById('loader').style.display = 'none';
                });
            }

            function clearQuestion() {
                document.getElementById('question').value = '';
                document.getElementById('answer').innerText = '';
                document.getElementById('loader').style.display = 'none';
            }
        </script>
    </body>
    </html>

"""