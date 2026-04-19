import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

ssid = "kamp_keyfi"
password = "12345678"
wifi_string = f"WIFI:T:WPA;S:{ssid};P:{password};;"

qr = qrcode.QRCode(box_size=10, border=4)
qr.add_data(wifi_string)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

try:
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
    font = ImageFont.truetype(font_path, 30)
except:
    font = ImageFont.load_default()

width, height = img.size
text = f"SSID: {ssid}\nPassword: {password}"
new_height = height + 70
new_img = Image.new("RGB", (width, new_height), "white")
new_img.paste(img, (0, 0))

draw = ImageDraw.Draw(new_img)
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_text = (width - text_width) // 2
y_text = height + 10

draw.text((x_text, y_text), text, fill="black", font=font)

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
output_path = os.path.join(desktop, "wifi_qr.jpeg")

new_img.save(output_path, "JPEG")
print(f"Wi-Fi QR kod resmi masaüstüne kaydedildi: {output_path}")
