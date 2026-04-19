import http.server
import socketserver
import socket
import qrcode
import os
import threading

PORT = 8000
DIRECTORY = os.path.expanduser("C:\sarki_jpeg")  # Yayınlanacak klasör (burayı değiştir)
# Ör: DIRECTORY = r"C:\Users\hp\Pictures"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Sunucu çalışıyor: http://{get_local_ip()}:{PORT}")
        httpd.serve_forever()

def generate_qr():
    url = f"http://{get_local_ip()}:{PORT}"
    img = qrcode.make(url)
    qr_path = "server_qr_C_sarki_jpeg.png"
    img.save(qr_path)
    print(f"QR kod kaydedildi: {qr_path}")
    try:
        os.startfile(qr_path)  # Windows
    except AttributeError:
        pass  # Diğer sistemlerde otomatik açmayabilir

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    generate_qr()
    input("Sunucu çalışıyor... Çıkmak için Enter'a basın.\n")
