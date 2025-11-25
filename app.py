from flask import Flask, request, render_template_string
import urllib.parse
import requests
import base64

app = Flask(__name__)

# Secrets
FACTORY_WHATSAPP = "+8615808103712"
YOUR_REFERRAL_CODE = "REF_GROK2025"

def generate_image(prompt):
    # Using Pollinations AI - free text-to-image API no key required
    encoded_prompt = urllib.parse.quote(f"{prompt}, fashion product photo, white background, studio lighting, ultra detailed, 8k")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?model=flux&width=1024&height=1024"
    r = requests.get(url, timeout=60)
    r.raise_for_status()  # Raise error if not 200
    return base64.b64encode(r.content).decode()

def upload_to_imgbb(b64_image):
    try:
        r = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": "10b08c5be2b4f6c9a2f1d2e8f7c3e4a5", "image": b64_image},
            timeout=15
        )
        return r.json()["data"]["url"]
    except:
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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No One Else Has This</title>
    <style>
        body {font-family:Arial;background:#000;color:#fff;text-align:center;padding:30px;}
        h1 {font-size:2.8em;background:linear-gradient(90deg,#ff00aa,#00ffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
        input[type=text],select {width:90%;max-width:600px;padding:18px;margin:10px;font-size:1.4em;border:3px solid #ff00aa;border-radius:15px;background:#111;color:white;}
        input[type=submit] {padding:18px 60px;font-size:1.6em;background:#ff00aa;border:none;border-radius:50px;cursor:pointer;}
        .result {margin:60px auto;max-width:600px;}
        img {width:100%;border-radius:20px;margin:20px 0;box-shadow:0 0 40px #ff00aa88;}
        button {margin:15px 0;padding:16px;width:100%;font-size:1.3em;border:none;border-radius:40px;cursor:pointer;}
        .produce {background:#25d366;color:white;font-weight:bold;}
    </style>
</head>
<body>
    <h1>No One Else Has This</h1>
    <p>Describe your dream clothing — China makes it real</p>
    <form method="post">
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
        <input type="submit" value="Generate">
    </form>
    {% if img_b64 %}
    <div class="result">
        <img src="data:image/png;base64,{{ img_b64 }}" alt="Generated Image">
        <button class="produce" onclick="window.open('{{ wa_link }}')"> Produce in China — $32–48 </button>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    img_b64 = None
    wa_link = None
    if request.method == 'POST':
        prompt = request.form['prompt'].strip()
        size = request.form.get('size', 'M')
        qty = request.form.get('qty', '1')
        img_b64 = generate_image(prompt)
        img_url = upload_to_imgbb(img_b64)
        wa_link = generate_whatsapp_link(prompt, img_url, size, qty)
    return render_template_string(HTML, img_b64=img_b64, wa_link=wa_link)

if __name__ == '__main__':
    print("LIVE → http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
