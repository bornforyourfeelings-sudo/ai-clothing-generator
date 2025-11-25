from flask import Flask, render_template_string

app = Flask(__name__)

# Вся логика перенесена в JavaScript, чтобы обойти блокировку IP Render
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No One Else Has This</title>
    <style>
        body {font-family:Arial;background:#000;color:#fff;text-align:center;padding:30px;}
        h1 {font-size:2.8em;background:linear-gradient(90deg,#ff00aa,#00ffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
        input[type=text],select {width:90%;max-width:600px;padding:18px;margin:10px;font-size:1.4em;border:3px solid #ff00aa;border-radius:15px;background:#111;color:white;}
        input[type=submit] {padding:18px 60px;font-size:1.6em;background:#ff00aa;border:none;border-radius:50px;cursor:pointer;color:white;font-weight:bold;}
        input[type=submit]:disabled {background:#555;cursor:wait;}
        
        .result {margin:60px auto;max-width:600px; display: none;} 
        img {width:100%;border-radius:20px;margin:20px 0;box-shadow:0 0 40px #ff00aa88;}
        button {margin:15px 0;padding:16px;width:100%;font-size:1.3em;border:none;border-radius:40px;cursor:pointer;}
        .produce {background:#25d366;color:white;font-weight:bold;}
        
        .loader {display:none; border: 5px solid #222; border-top: 5px solid #ff00aa; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 30px auto;}
        @keyframes spin {0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); }}
        .error-msg {color: #ff3333; display: none; margin-top: 20px;}
    </style>
</head>
<body>

    <h1>No One Else Has This</h1>
    <p>Describe your dream clothing — China makes it real</p>

    <form id="appForm">
        <input type="text" id="prompt" placeholder="Describe your dream clothing..." required>
        <select id="size">
            <option>XS</option>
            <option>S</option>
            <option selected>M</option>
            <option>L</option>
            <option>XL</option>
            <option>XXL</option>
        </select>
        <input type="text" id="qty" placeholder="Quantity" value="1">
        <input type="submit" id="submitBtn" value="Generate">
    </form>
    
    <div class="loader" id="loader"></div>
    <p class="error-msg" id="errorMsg">Generation failed. Please try again.</p>

    <div class="result" id="resultBlock">
        <img id="resultImg" src="" alt="Generated Image" referrerpolicy="no-referrer">
        <button class="produce" id="waButton"> Produce in China — $32–48 </button>
    </div>

    <script>
        const FACTORY_WHATSAPP = "8613980632981"; 
        const YOUR_REFERRAL_CODE = "REF_GROK2025";

        document.getElementById('appForm').addEventListener('submit', function(e) {
            e.preventDefault(); 
            
            const promptVal = document.getElementById('prompt').value;
            const sizeVal = document.getElementById('size').value;
            const qtyVal = document.getElementById('qty').value;
            
            const imgElement = document.getElementById('resultImg');
            const resultDiv = document.getElementById('resultBlock');
            const loader = document.getElementById('loader');
            const btn = document.getElementById('submitBtn');
            const errorMsg = document.getElementById('errorMsg');

            // Сброс UI
            btn.value = "Dreaming...";
            btn.disabled = true;
            loader.style.display = "block";
            resultDiv.style.display = "none";
            errorMsg.style.display = "none";

            // Генерация ссылки (Seed делает её уникальной)
            const seed = Math.floor(Math.random() * 1000000);
            const fullPrompt = encodeURIComponent(promptVal + ", fashion product photo, white background, studio lighting, 8k");
            // Добавляем nologo=true
            const imageUrl = "https://image.pollinations.ai/prompt/" + fullPrompt + "?model=flux&width=1024&height=1024&seed=" + seed + "&nologo=true";

            // Устанавливаем источник картинки
            imgElement.src = imageUrl;

            // Если картинка загрузилась
            imgElement.onload = function() {
                loader.style.display = "none";
                resultDiv.style.display = "block";
                btn.value = "Generate";
                btn.disabled = false;

                // Ссылка WhatsApp с тем же URL картинки
                const message = "Hello MMS Clothing!\\nFully custom clothing — cut & sew\\nReferral: " + YOUR_REFERRAL_CODE + " → 25% cashback\\nDesign:\\n" + imageUrl + "\\nDescription: " + promptVal + "\\nSize: " + sizeVal + " | Quantity: " + qtyVal + " pc(s)\\nPlease send quote + sample cost + lead time.\\nThank you!";

                const waLink = "https://wa.me/" + FACTORY_WHATSAPP + "?text=" + encodeURIComponent(message);
                
                document.getElementById('waButton').onclick = () => window.open(waLink, '_blank');
            };

            // Если ошибка загрузки
            imgElement.onerror = function() {
                loader.style.display = "none";
                errorMsg.style.display = "block";
                btn.value = "Try Again";
                btn.disabled = false;
            };
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    # Просто отдаем HTML. Python здесь "отдыхает".
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    # Порт для локального запуска, на Render он игнорируется (используется gunicorn)
    app.run(debug=True)
