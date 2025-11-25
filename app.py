from flask import Flask, request, render_template_string
import urllib.parse
import requests
import base64
import time
import os

app = Flask(__name__)

# Secrets
FACTORY_WHATSAPP = "+8615808103712"
YOUR_REFERRAL_CODE = "REF_GROK2025"

def generate_image(prompt):
    """Generate image using multiple APIs with retry logic"""
    seed = int(time.time())
    encoded_prompt = urllib.parse.quote(f"{prompt}, fashion product photo, white background, studio lighting, detailed")
    
    # Multiple API endpoints to try
    apis = [
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true",
        f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}",
    ]
    
    last_error = None
    
    for i, url in enumerate(apis):
        try:
            print(f"Trying API {i+1}: {url}")
            r = requests.get(url, timeout=45, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # Check if response is valid image
            if r.status_code == 200 and len(r.content) > 1000:
                print(f"Success with API {i+1}")
                return base64.b64encode(r.content).decode()
            else:
                print(f"API {i+1} failed: status {r.status_code}, size {len(r.content)}")
                
        except Exception as e:
            print(f"API {i+1} error: {e}")
            last_error = str(e)
            time.sleep(1)  # Wait before next attempt
            continue
    
    # If all APIs failed, raise error
    raise Exception(f"All image generation attempts failed. Last error: {last_error}")

def upload_to_imgbb(b64_image):
    """Upload to ImgBB with fallback"""
    try:
        r = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": "10b08c5be2b4f6c9a2f1d2e8f7c3e4a5", "image": b64_image},
            timeout=15
        )
        if r.status_code == 200:
            return r.json()["data"]["url"]
    except Exception as e:
        print(f"ImgBB upload failed: {e}")
    
    return f"data:image/png;base64,{b64_image}"

def generate_whatsapp_link(prompt, img_url, size, qty):
    message = f"""Hello MMS Clothing!
Fully custom clothing — cut & sew
Referral: {YOUR_REFERRAL_CODE} → 25% cashback
Design:
{img_url}
Description: {prompt}
Size: {size} | Quantity: {qty} pc(s)
Please send quote + sample cost + lead time.
Thank you!"""
    phone = FACTORY_WHATSAPP.replace('+', '')
    encoded_message = urllib.parse.quote(message)
    return f"https://api.whatsapp.com/send?phone={phone}&text={encoded_message}"

HTML = """
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
        input[type=submit]:disabled {opacity:0.5;cursor:not-allowed;}
        .result {margin:60px auto;max-width:600px;}
        img {width:100%;border-radius:20px;margin:20px 0;box-shadow:0 0 40px #ff00aa88;}
        button {margin:15px 0;padding:16px;width:100%;font-size:1.3em;border:none;border-radius:40px;cursor:pointer;}
        .produce {background:#25d366;color:white;font-weight:bold;}
        .error {color:#ff00aa;margin:20px;padding:15px;background:#330011;border-radius:10px;}
        .loader {display:none;border:5px solid #333;border-top:5px solid #ff00aa;border-radius:50%;width:50px;height:50px;animation:spin 1s linear infinite;margin:30px auto;}
        @keyframes spin {0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
    </style>
</head>
<body>
    <h1>No One Else Has This</h1>
    <p>Describe your dream clothing — China makes it real</p>
    <form method="post" id="mainForm">
        <input type="text" name="prompt" placeholder="Describe your dream clothing..." required>
        <select name="size">
            <option>XS</option>
            <option>S</option>
            <option selected>M</option>
            <option>L</option>
            <option>XL</option>
            <option>XXL</option>
        </select>
        <input type="text" name="qty" placeholder="Quantity" value="1">
        <input type="submit" value="Generate" id="submitBtn">
    </form>
    <div class="loader" id="loader"></div>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
    {% if img_b64 %}
    <div class="result">
        <img src="data:image/png;base64,{{ img_b64 }}" alt="Generated Image">
        <button class="produce" onclick="window.open('{{ wa_link }}')"> Produce in China — $32–48 </button>
    </div>
    {% endif %}
    <script>
        document.getElementById('mainForm').onsubmit = function() {
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').value = 'Dreaming... (30-60s)';
            document.getElementById('loader').style.display = 'block';
        };
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    img_b64 = None
    wa_link = None
    error = None
    
    if request.method == 'POST':
        try:
            prompt = request.form['prompt'].strip()
            size = request.form.get('size', 'M')
            qty = request.form.get('qty', '1')
            
            print(f"Generating image for: {prompt}")
            img_b64 = generate_image(prompt)
            img_url = upload_to_imgbb(img_b64)
            wa_link = generate_whatsapp_link(prompt, img_url, size, qty)
            print("Image generated successfully!")
            
        except Exception as e:
            error = f"Generation failed: {str(e)}. Please try again or simplify your description."
            print(f"Error: {e}")
    
    return render_template_string(HTML, img_b64=img_b64, wa_link=wa_link, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
