import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import socket
from PIL import Image, ImageTk, ImageOps, ImageFilter
import qrcode
import io

# --- HEIC desteği (varsa otomatik) ---
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_OK = True
except Exception:
    HEIF_OK = False

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".heic", ".heif", ".webp")
VIDEO_EXTS = (".mp4", ".mov", ".avi", ".webm", ".mkv")
DOC_EXTS   = (".txt", ".pdf")

def make_thumb(in_path, out_path, max_size=1200):
    """
    Yüksek kaliteli thumbnail üretimi:
    - EXIF yönü düzeltilir
    - RGB'ye çevrilir
    - LANCZOS ile yeniden boyutlandırılır
    - Hafif UnsharpMask ile keskinleştirilir
    - JPEG (quality=95, subsampling=0) olarak kaydedilir
    """
    with Image.open(in_path) as im:
        # HEIC/WebP vs. sorunlarını azaltmak için güvenli dönüşümler
        im = ImageOps.exif_transpose(im)  # kameradan gelen EXIF yönünü düzelt
        im = im.convert("RGB")
        w, h = im.size
        if w > max_size or h > max_size:
            ratio = min(max_size / w, max_size / h)
            new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
            im = im.resize(new_size, Image.LANCZOS)
        # Metin okunurluğunu artırmak için çok hafif keskinleştirme
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
        # Yüksek kalite JPEG olarak kaydet
        im.save(out_path, "JPEG", quality=95, optimize=True, subsampling=0)

class TkinterHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        msg = "%s - - [%s] %s\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        )
        print(msg, end='')
        if app and app.log_text:
            app.log_text.config(state=tk.NORMAL)
            app.log_text.insert(tk.END, msg)
            app.log_text.see(tk.END)
            app.log_text.config(state=tk.DISABLED)

    def list_directory(self, path):
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "Klasör bulunamadı")
            return None
        # Burada klasör adını alıyoruz
        folder_name = os.path.basename(os.path.abspath(path))

        thumb_dir = os.path.join(path, ".thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)
        # Klasörleri bul
                # Klasörleri bul (.thumbnails hariç)
        dir_list = [
            f for f in file_list
            if os.path.isdir(os.path.join(path, f)) and f != ".thumbnails"
        ]

        # Dosyaları filtreden geçir
        all_files = [
            f for f in file_list
            if os.path.isfile(os.path.join(path, f))
        ]

        # Sıralama: En yeni en üstte
        all_files.sort(key=lambda a: os.path.getmtime(os.path.join(path, a)), reverse=True)

        image_files = [f for f in all_files if f.lower().endswith(IMAGE_EXTS)]
        video_files = [f for f in all_files if f.lower().endswith(VIDEO_EXTS)]
        doc_files   = [f for f in all_files if f.lower().endswith(DOC_EXTS)]

        # Thumbnail temizlik (sadece resimlerin .jpg thumbnail'larını tut)
        desired_thumbs = {os.path.splitext(f)[0] + ".jpg" for f in image_files}
        for t in os.listdir(thumb_dir):
            if t not in desired_thumbs:
                try:
                    os.remove(os.path.join(thumb_dir, t))
                    print(f"Thumbnail silindi: {t}")
                except Exception as e:
                    print(f"Thumbnail silinirken hata: {t} -> {e}")

        # HTML
        html = [
                "<html><head>",
                "<meta charset='utf-8'>",
                "<meta name='viewport' content='width=device-width, initial-scale=1'>",
                "<title>Paylaşım Galerisi</title>",
                "<style>",
                "body { font-family: Arial, Helvetica, sans-serif; background:#f3f4f6; margin:0; }",
                "h2 { margin:16px; }",
                ".wrap { max-width: 1200px; margin: 0 auto; padding: 8px 12px 32px; }",
                ".item { margin:16px auto; background:white; padding:12px; border-radius:12px; ",
                "        box-shadow:0 2px 8px rgba(0,0,0,0.08); max-width: 95%; }",
                ".name { font-size:14px; color:#374151; margin-top:8px; word-break: break-all; }",
                "img, video { width:100%; height:auto; display:block; border-radius:10px;",
                "             max-width: 90vw; max-height: 80vh; object-fit: contain; }",
                "a { color:#2563eb; text-decoration:none; }",
                "a:hover { text-decoration:underline; }",
                ".section { margin-top:24px; }",
                "</style>",
                "</head><body>",
                "<div class='wrap'>",
                "<h2><a href='/'>📂 Kamp Keyfi Ana Sayfa</a></h2>"   # <-- burası eklendi
                f"<h3>📁 {folder_name}</h3>"  # <-- burası eklendi
        ]

        # --- Klasörler ---
        if dir_list:
            html.append("")#<div class='section'><h4>📁 Seçim Klasörler</h4>")
            for d in sorted(dir_list):
                html.append(
                    f"<div class='item'>"
                    f"<div class='name'><a href='{d}/'>{d}</a></div>"
                    f"</div>"
                )
            html.append("</div>")

                # --- Görseller ---
        if image_files:
            html.append("<div class='section'><h3>🖼️ Kamp Keyfi Resimler</h3>")
            for name in image_files:
                full_path = os.path.join(path, name)
                # Thumbnail adı: <dosya_adi>.jpg
                thumb_name = os.path.splitext(name)[0] + ".jpg"
                thumb_path = os.path.join(thumb_dir, thumb_name)

                if not os.path.exists(thumb_path):
                    try:
                        make_thumb(full_path, thumb_path, max_size=1200)  # daha büyük ve net
                    except Exception as e:
                        print(f"Thumbnail oluşturulamadı: {name} -> {e}")
                        continue

                html.append(
                    f"<div class='item'>"
                    f"<a href='{name}' target='_blank'>"
                    f"<img src='.thumbnails/{thumb_name}' alt='{name}' loading='lazy'></a>"
                    f"<div class='name'>{name}</div>"
                    f"</div>"
                )
            html.append("</div>")

        # --- Videolar ---
        if video_files:
            html.append("<div class='section'><h3>🎬 Kamp Keyfi Videolar</h3>")
            for name in video_files:
                # Basit video oynatıcı (poster üretmiyoruz; istenirse ffmpeg ile eklenebilir)
                html.append(
                    f"<div class='item'>"
                    f"<video src='{name}' controls preload='metadata' playsinline "
                    f"muted style='outline:none' loading='lazy'></video>"
                    f"<div class='name'><a href='{name}' target='_blank'>{name}</a></div>"
                    f"</div>"
                )
            html.append("</div>")

        # --- Belgeler ---
        if doc_files:
            html.append("<div class='section'><h3>📄 Kamp Keyfi Belgeler</h3>")
            for name in doc_files:
                html.append(
                    f"<div class='item'>"
                    f"<div class='name'><a href='{name}' target='_blank'>{name}</a></div>"
                    f"</div>"
                )
            html.append("</div>")

        if not (image_files or video_files or doc_files):
            html.append("")#"<p>Bu klasörde gösterilecek desteklenen dosya bulunamadı.</p>")

        html.append("</div></body></html>")
        encoded = "\n".join(html).encode("utf-8", "surrogateescape")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()

        return io.BytesIO(encoded)

class ServerThread(threading.Thread):
    def __init__(self, directory, port):
        super().__init__(daemon=True)
        self.directory = directory
        self.port = port
        self.httpd = None

    def run(self):
        handler = lambda *args, **kwargs: TkinterHTTPHandler(*args, directory=self.directory, **kwargs)
        try:
            self.httpd = socketserver.ThreadingTCPServer(("", self.port), handler)
            self.httpd.daemon_threads = True
            # Yeniden kullanıma izin: server hızlı yeniden başlatılırsa iş görür
            self.httpd.allow_reuse_address = True
        except OSError:
            app.after(0, lambda: messagebox.showerror("Hata", f"Port {self.port} zaten kullanılıyor!"))
            app.after(0, app.stop_server)
            return
        url = f"http://{get_local_ip()}:{self.port}/"
        app.after(0, lambda: app.append_log(f"Sunucu başladı: {url}\n"))
        app.after(0, lambda: app.show_qr_code(url))
        try:
            self.httpd.serve_forever()
        except Exception as e:
            app.after(0, lambda: app.append_log(f"Sunucu hata ile durdu: {e}\n"))

    def shutdown(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wi-Fi Medya(Kamp Keyfi Resim-Video) Paylaşımı V11.0 - Erdal GÜNDOĞAN 2025")
        self.geometry("640x720")

        self.label_dir = tk.Label(self, text="Henüz klasör seçilmedi.")
        self.label_dir.pack(pady=5)

        self.btn_select = tk.Button(self, text="Kamp Keyfi\nKlasör Seç\nWi-Fi Paylaşım", command=self.select_folder)
        self.btn_select.pack(pady=5)

        port_frame = tk.Frame(self)
        port_frame.pack(pady=5)
        tk.Label(port_frame, text="Port:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="8000")
        self.entry_port = tk.Entry(port_frame, textvariable=self.port_var, width=6)
        self.entry_port.pack(side=tk.LEFT)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_start = tk.Button(btn_frame, text="Sunucuyu Başlat", bg="green", fg="white", command=self.start_server)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(btn_frame, text="Sunucuyu Durdur", bg="red", fg="white", command=self.stop_server, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        self.qr_label = None  # QR kod alanı

        self.log_text = scrolledtext.ScrolledText(self, height=18, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.server_thread = None
        self.selected_dir = None

    def append_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def show_qr_code(self, link):
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_img = ImageTk.PhotoImage(img)
        if self.qr_label:
            self.qr_label.destroy()
        self.qr_label = tk.Label(self, image=qr_img)
        self.qr_label.image = qr_img
        self.qr_label.pack(pady=10)
        self.append_log(f"QR Kod oluşturuldu: {link}\n")

    def select_folder(self):
        dir_path = filedialog.askdirectory(title="Klasör Seç")
        if dir_path:
            self.selected_dir = dir_path
            self.label_dir.config(text=f"Seçilen klasör: {dir_path}")
            self.append_log(f"Klasör seçildi: {dir_path}\n")

    def start_server(self):
        if not self.selected_dir:
            messagebox.showwarning("Uyarı", "Lütfen önce bir klasör seçin!")
            return
        try:
            port = int(self.port_var.get())
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir port numarası girin (1-65535).")
            return

        self.server_thread = ServerThread(self.selected_dir, port)
        self.server_thread.start()

        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_select.config(state=tk.DISABLED)
        self.entry_port.config(state=tk.DISABLED)
        self.append_log("Sunucu başlatılıyor...\n")

    def stop_server(self):
        if self.server_thread:
            self.append_log("Sunucu durduruluyor...\n")
            self.server_thread.shutdown()
            self.server_thread = None
            self.append_log("Sunucu durduruldu.\n")

        if self.qr_label:
            self.qr_label.destroy()
            self.qr_label = None

        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_select.config(state=tk.NORMAL)
        self.entry_port.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = App()
    app.mainloop()
