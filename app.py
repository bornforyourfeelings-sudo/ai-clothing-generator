from flask import Flask, render_template_string
import os

app = Flask(__name__)

FACTORY_WHATSAPP = "8615808103712"
YOUR_REFERRAL_CODE = "REF_GROK2025"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No One Else Has This</title>
    <style>
        body {font-family:Arial;background:#000;color:#fff;text-align:center;padding:30px;}
        h1 {font-size:2.8em;background:linear-gradient(90deg,#ff00aa,#00ffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
        input[type=text],select {width:90%;max-width:600px;padding:18px;margin:10px;font-size:1.4em;border:3px solid #ff00aa;border-radius:15px;background:#111;color:white;}
        input[type=submit] {padding:18px 60px;font-size:1.6em;background:#ff00aa;border:none;border-radius:50px;cursor:pointer;color:white;font-weight:bold;}
        input[type=submit]:disabled {opacity:0.5;cursor:not-allowed;}
        .result {margin:60px auto;max-width:600px;display:none;}
        img {width:100%;border-radius:20px;margin:20px 0;box-shadow:0 0 40px #ff00aa88;}
        button {margin:15px 0;padding:16px;width:100%;font-size:1.3em;border:none;border-radius:40px;cursor:pointer;}
        .produce {background:#25d366;color:white;font-weight:bold;}
        .error {color:#ff00aa;margin:20px;padding:15px;background:#330011;border-radius:10px;}
        .loader {display:none;border:5px solid #333;border-top:5px solid #ff00aa;border-radius:50%;width:50px;height:50px;animation:spin 1s linear infinite;margin:30px auto;}
        @keyframes spin {0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
        .status {color:#00ffff;margin:15px;font-size:0.9em;}
    </style>
</head>
<body>
    <h1>No One Else Has This</h1>
    <p>Describe your dream clothing — China makes it real</p>
    
    <form id="appForm">
        <input type="text" id="prompt" placeholder="Describe your dream clothing..." required>
        <select id="size">
            <option>XS</option><option>S</option><option selected>M</option>
            <option>L</option><option>XL</option><option>XXL</option>
        </select>
        <input type="text" id="qty" placeholder="Quantity" value="1">
        <input type="submit" id="btn" value="Generate">
    </form>
    
    <div class="loader" id="loader"></div>
    <div class="status" id="status"></div>
    <div class="error" id="error" style="display:none;"></div>
    
    <div class="result" id="resultBlock">
        <img id="resultImg" src="" alt="Generated Image">
        <button class="produce" id="waButton">Produce in China — $32–48</button>
    </div>

    <script>
        const FACTORY_WHATSAPP = "{{ whatsapp }}";
        const YOUR_REFERRAL_CODE = "{{ referral }}";

        document.getElementById('appForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const promptVal = document.getElementById('prompt').value.trim();
            const sizeVal = document.getElementById('size').value;
            const qtyVal = document.getElementById('qty').value;
            const imgElement = document.getElementById('resultImg');
            const resultDiv = document.getElementById('resultBlock');
            const loader = document.getElementById('loader');
            const btn = document.getElementById('btn');
            const status = document.getElementById('status');
            const errorDiv = document.getElementById('error');

            btn.value = "Dreaming...";
            btn.disabled = true;
            loader.style.display = "block";
            resultDiv.style.display = "none";
            errorDiv.style.display = "none";
            status.textContent = "Generating image... This may take 30-60 seconds";

            const enhancedPrompt = `${promptVal}, fashion product photo, white background, studio lighting, high quality`;
            const seed = Date.now();
            
            // Multiple API attempts
            const apis = [
                `https://image.pollinations.ai/prompt/${encodeURIComponent(enhancedPrompt)}?width=1024&height=1024&seed=${seed}&nologo=true`,
                `https://pollinations.ai/p/${encodeURIComponent(enhancedPrompt)}?width=1024&height=1024&seed=${seed}`,
                `https://image.pollinations.ai/prompt/${encodeURIComponent(enhancedPrompt)}?seed=${seed}`,
            ];

            let currentApiIndex = 0;
            let imageUrl = '';
            let attempts = 0;
            const maxAttempts = 3;

            async function tryGenerate() {
                if (currentApiIndex >= apis.length) {
                    attempts++;
                    if (attempts < maxAttempts) {
                        status.textContent = `Attempt ${attempts + 1}/${maxAttempts}... Servers are busy, retrying...`;
                        currentApiIndex = 0;
                        setTimeout(tryGenerate, 2000);
                        return;
                    }
                    
                    loader.style.display = "none";
                    btn.value = "Generate";
                    btn.disabled = false;
                    status.textContent = "";
                    errorDiv.textContent = "⚠️ Image generation temporarily unavailable. API servers are overloaded. Please try again in 1-2 minutes, or describe your design directly in WhatsApp - the factory can help visualize it!";
                    errorDiv.style.display = "block";
                    return;
                }

                const apiUrl = apis[currentApiIndex];
                console.log(`Trying API ${currentApiIndex + 1}: ${apiUrl}`);
                status.textContent = `Trying generation method ${currentApiIndex + 1}/${apis.length}...`;

                imageUrl = apiUrl;
                imgElement.src = apiUrl;
            }

            imgElement.onload = function() {
                console.log("Image loaded successfully!");
                loader.style.display = "none";
                resultDiv.style.display = "block";
                btn.value = "Generate";
                btn.disabled = false;
                status.textContent = "";

                const message = `Hello MMS Clothing!
Fully custom clothing — cut & sew
Referral: ${YOUR_REFERRAL_CODE} → 25% cashback
Design: ${imageUrl}
Description: ${promptVal}
Size: ${sizeVal} | Quantity: ${qtyVal} pc(s)
Please send quote + sample cost + lead time.
Thank you!`;

                const waLink = `https://api.whatsapp.com/send?phone=${FACTORY_WHATSAPP}&text=${encodeURIComponent(message)}`;
                document.getElementById('waButton').onclick = () => window.open(waLink, '_blank');
            };

            imgElement.onerror = function() {
                console.log(`API ${currentApiIndex + 1} failed, trying next...`);
                currentApiIndex++;
                setTimeout(tryGenerate, 1000);
            };

            tryGenerate();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, whatsapp=FACTORY_WHATSAPP, referral=YOUR_REFERRAL_CODE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
