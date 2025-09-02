from flask import Flask, send_file, render_template
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<int:width>/<int:height>')
def generate_image(width, height):
    if width <= 0 or height <= 0:
        return "Invalid dimensions", 400

    # Create a gray image
    img = Image.new('RGB', (width, height), color=(211, 211, 211))  # Light gray background

    draw = ImageDraw.Draw(img)
    text = f"{width}X{height}"

    # Use a default font; try to load a system font or fallback
    try:
        # Assuming the font file is copied to the container (e.g., via Dockerfile)
        font_path = "ARIALNB.TTF"  # Adjust path based on where you copy the font
        font_size = (min(width, height) // 2) # Start with a smaller fraction for better scaling

        while font_size > 0:
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            if text_width <= width * 0.8 and text_height <= height * 0.8:  # Allow 80% of image size
                break
            font_size -= 1
        if font_size <= 0:
            font = ImageFont.load_default()
    except IOError:
        # Fallback to default font if truetype font not found
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

    # Calculate position to center the text
    x = (width - text_width) / 2
    y = (height - text_height) / 2 - bbox[1]  # Adjust for baseline

    # Draw the text in black
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # Save to in-memory buffer
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))