import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

def save_text_as_jpeg():
    # Metin kutusundaki sözleri al
    text = result_text.get("1.0", tk.END).strip()
    if not text:
        return

    # Kaydetme yeri seçtir
    file_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG Files", "*.jpg"), ("All Files", "*.*")],
        title="Şarkı sözünü JPEG olarak kaydet"
    )
    if not file_path:
        return

    # Yazı tipi ayarı
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    # Satır bazlı ölçüm
    lines = text.split("\n")
    line_height = font.getbbox("A")[3] + 10
    width = 800
    height = line_height * len(lines) + 20

    # Görsel oluştur
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    y = 10
    for line in lines:
        draw.text((10, y), line, fill="black", font=font)
        y += line_height

    # Kaydet
    img.save(file_path, "JPEG")
    print(f"Kaydedildi: {file_path}")

# Tk örnek kullanım
root = tk.Tk()
root.title("Şarkı Sözü Görsel Kaydetme")

result_text = tk.Text(root, font=("Arial", 14), width=60, height=20)
result_text.pack(pady=10)

save_button = tk.Button(root, text="JPEG Olarak Kaydet", command=save_text_as_jpeg)
save_button.pack(pady=5)

root.mainloop()
