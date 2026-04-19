import os
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def clean_filename(s):
    # Küçük harfe çevir, boşlukları alt çizgi yap, özel karakterleri kaldır
    s = s.strip().lower()
    s = s.replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]", "", s)
    return s[:30]  # maksimum 30 karakter

def save_selected_text_as_jpeg():
    save_dir = r"C:\sarki_jpeg"
    os.makedirs(save_dir, exist_ok=True)

    try:
        selected_text = result_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
    except tk.TclError:
        print("Seçili metin yok!")
        return

    if not selected_text:
        print("Metin boş!")
        return

    first_line = selected_text.split("\n")[0]
    filename_base = clean_filename(first_line)
    if not filename_base:
        filename_base = "sozler"

    # Dosya adı tarih ile
    filename = f"{filename_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(save_dir, filename)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    lines = selected_text.split("\n")
    line_height = font.getbbox("A")[3] + 10
    width = 800
    height = line_height * len(lines) + 20

    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    y = 10
    for line in lines:
        draw.text((10, y), line, fill="black", font=font)
        y += line_height

    img.save(filepath, "JPEG")
    print(f"JPEG kaydedildi: {filepath}")

# Örnek Tkinter buton ekleme
save_jpeg_button = tk.Button(root, text="Seçili Metni JPEG Kaydet", command=save_selected_text_as_jpeg)
save_jpeg_button.pack(pady=5)
