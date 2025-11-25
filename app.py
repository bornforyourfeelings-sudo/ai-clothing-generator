from flask import Flask, render_template_string
import os

app = Flask(__name__)

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
        <img id="resultImg" src="" alt="Generated Image" crossorigin="anonymous">
        <button class="produce" id="waButton">Produce in China — $32–48</button>
    </div>

    <script>
        const FACTORY_WHATSAPP = "8615808103712";
        const REFERRAL = "REF_GROK2025";

        document.getElementById('appForm').onsubmit = async (e) => {
            e.preventDefault();
            
            const prompt = document.getElementById('prompt').value.trim();
            const size = document.getElementById('size').value;
            const qty = document.getElementById('qty').value;
            const img = document.getElementById('resultImg');
            const result = document.getElementById('resultBlock');
            const loader = document.getElementById('loader');
            const btn = document.getElementById('btn');
            const status = document.getElementById('status');
            const error = document.getElementById('error');

            btn.value = "Dreaming...";
            btn.disabled = true;
            loader.style.display = "block";
            result.style.display = "none";
            error.style.display = "none";
            status.textContent = "Generating image... 30-60 seconds";

            const enhanced = encodeURIComponent(`${prompt}, fashion product photo, white background, studio lighting, professional`);
            const seed = Date.now();
            
            const urls = [
                `https://image.pollinations.ai/prompt/${enhanced}?width=1024&height=1024&seed=${seed}&nologo=true`,
                `https://image.pollinations.ai/prompt/${enhanced}?seed=${seed}`,
                `https://pollinations.ai/p/${enhanced}`,
            ];

            let i = 0;
            let imageUrl = '';

            function tryLoad() {
                if (i >= urls.length) {
                    loader.style.display = "none";
                    btn.value = "Generate";
                    btn.disabled = false;
                    status.textContent = "";
                    error.textContent = "⚠️ AI image generation is temporarily unavailable (free API overloaded). You can still order - just describe your design in WhatsApp and the factory will help visualize it!";
                    error.style.display = "block";
                    return;
                }
                
                imageUrl = urls[i];
                status.textContent = `Trying method ${i+1}/${urls.length}...`;
                console.log('Trying:', imageUrl);
                img.src = imageUrl;
            }

            img.onload = () => {
                loader.style.display = "none";
                result.style.display = "block";
                btn.value = "Generate";
                btn.disabled = false;
                status.textContent = "";

                const msg = `Hello MMS Clothing!
Fully custom clothing — cut & sew
Referral: ${REFERRAL} → 25% cashback
Design: ${imageUrl}
Description: ${prompt}
Size: ${size} | Quantity: ${qty} pc(s)
Please send quote + sample cost + lead time.
Thank you!`;

                document.getElementById('waButton').onclick = () => 
                    window.open(`https://api.whatsapp.com/send?phone=${FACTORY_WHATSAPP}&text=${encodeURIComponent(msg)}`, '_blank');
            };

            img.onerror = () => {
                console.log(`Method ${i+1} failed`);
                i++;
                setTimeout(tryLoad, 1500);
            };

            tryLoad();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
