import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import socket
from PIL import Image, ImageTk
import qrcode
import io

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

        thumb_dir = os.path.join(path, ".thumbnails")
        os.makedirs(thumb_dir, exist_ok=True)

        # Desteklenen dosya türleri
        image_ext = (".jpg", ".jpeg", ".png", ".gif")
        video_ext = (".mp4", ".mov", ".avi", ".mkv")
        heic_ext = (".heic",)

        current_files = [f for f in file_list if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(image_ext + video_ext + heic_ext)]

        # Thumbnail klasöründeki dosyalar sil (olmayanları)
        thumbs = os.listdir(thumb_dir)
        for thumb_file in thumbs:
            if thumb_file not in current_files:
                try:
                    os.remove(os.path.join(thumb_dir, thumb_file))
                    print(f"Thumbnail silindi: {thumb_file}")
                except Exception as e:
                    print(f"Thumbnail silinirken hata: {thumb_file} -> {e}")

        # Thumbnail oluşturma sadece resimler için
        for name in current_files:
            ext = os.path.splitext(name)[1].lower()
            full_path = os.path.join(path, name)
            thumb_path = os.path.join(thumb_dir, name)

            if ext in image_ext:
                if not os.path.exists(thumb_path):
                    try:
                        with Image.open(full_path) as img:
                            img.thumbnail((150, 150))
                            img.save(thumb_path, "JPEG")
                    except Exception as e:
                        print(f"Thumbnail oluşturulamadı: {name} -> {e}")
                        continue
            else:
                # Video veya HEIC için thumbnail oluşturulmaz
                pass

        # 📌 ÖNCE resimler, sonra videolar, sonra HEIC
        def sort_key(filename):
            ext = os.path.splitext(filename)[1].lower()
            full_path = os.path.join(path, filename)
            mtime = os.path.getmtime(full_path)

            if ext in video_ext:
                # Videoları en yeni tarih ilk olacak şekilde sıralamak için negatif zaman
                return (0, -mtime)
            elif ext in image_ext:
                return (1, filename.lower())
            elif ext in heic_ext:
                return (2, filename.lower())
            else:
                return (3, filename.lower())

        current_files.sort(key=sort_key)


    # HTML oluşturma (kalan kısım aynı)   


        html = [
            "<html><head>",
            "<meta charset='utf-8'>",
            "<title>Medya Galerisi</title>",
            "<style>",
            """
            body { font-family: Arial; text-align:center; background:#f0f0f0; margin:0; }
            .gallery {
                display: flex;
                flex-direction: column; /* Tek sütun */
                align-items: center;
                padding: 10px;
                gap: 20px;
            }
            .gallery-item {
                width: 90%; /* Maksimum genişlik, resim büyük olacak */
            }
            .gallery-item img, .gallery-item video {
                width: 100%;
                height: auto;
                border-radius: 8px;
            }

            .gallery-item:hover img, .gallery-item:hover video, .gallery-item:hover .icon { transform: scale(1.05); }

            /* Modal Styles */
            #modal { display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9); align-items: center; justify-content: center; }
            #modal img, #modal video { max-width: 90%; max-height: 90%; border-radius: 8px; }
            #modal .close, #modal .prev, #modal .next {
                position: absolute; top: 50%; color: white; font-size: 2em; user-select: none; cursor: pointer; padding: 10px;
                background: rgba(0,0,0,0.3); border-radius: 50%;
                transform: translateY(-50%);
            }
            #modal .close { top: 10%; right: 5%; font-size: 2.5em; }
            #modal .prev { left: 2%; }
            #modal .next { right: 2%; }
            """,
            "</style>",
            "</head><body>",
            "<h2>📷 Medya Galerisi</h2>",
            "<div class='gallery'>"
        ]

        for idx, name in enumerate(current_files):
            ext = os.path.splitext(name)[1].lower()
            full_url = name
            if ext in image_ext:
                thumb_url = f".thumbnails/{name}"
                html.append(f'<div class="gallery-item" data-index="{idx}" data-type="image" data-full="{full_url}">')
                html.append(f'<img src="{thumb_url}" alt="{name}">')
                html.append("</div>")
            elif ext in video_ext:
                # Video küçük gösterim için video tag kullan
                html.append(f'<div class="gallery-item" data-index="{idx}" data-type="video" data-full="{full_url}">')
                html.append(f'<video src="{full_url}" muted preload="metadata" style="width:100%; height:auto; border-radius:8px;"></video>')
                html.append("</div>")
            elif ext in heic_ext:
                # HEIC için ikon placeholder
                html.append(f'<div class="gallery-item" data-index="{idx}" data-type="heic" data-full="{full_url}">')
                html.append(f'<div class="icon" style="width:100%; height:100%; line-height:100%; background:#ccc; color:#555; font-weight:bold; border-radius:8px;">HEIC</div>')
                html.append("</div>")

        html.append("</div>")

        # Modal HTML
        html.append("""
        <div id="modal">
            <span class="close" title="Kapat">&times;</span>
            <span class="prev" title="Önceki">&#10094;</span>
            <span class="next" title="Sonraki">&#10095;</span>
            <img id="modal-img" src="" alt="Resim" style="display:none;">
            <video id="modal-video" controls style="display:none;"></video>
        </div>
        """)

        # Modal JS
        html.append("""
        <script>
        const modal = document.getElementById('modal');
        const modalImg = document.getElementById('modal-img');
        const modalVideo = document.getElementById('modal-video');
        const closeBtn = modal.querySelector('.close');
        const prevBtn = modal.querySelector('.prev');
        const nextBtn = modal.querySelector('.next');
        const galleryItems = document.querySelectorAll('.gallery-item');
        let currentIndex = 0;

        function showModal(index) {
            currentIndex = index;
            const item = galleryItems[currentIndex];
            const type = item.getAttribute('data-type');
            const fullSrc = item.getAttribute('data-full');

            if (type === 'image') {
                modalImg.src = fullSrc;
                modalImg.style.display = 'block';
                modalVideo.style.display = 'none';
                modalVideo.pause();
                modalVideo.src = "";
            } else if (type === 'video') {
                modalVideo.src = fullSrc;
                modalVideo.style.display = 'block';
                modalVideo.play();
                modalImg.style.display = 'none';
                modalImg.src = "";
            } else {
                // HEIC veya desteklenmeyen türler için basit mesaj
                modalImg.style.display = 'none';
                modalVideo.style.display = 'none';
                modalImg.src = "";
                modalVideo.pause();
                modalVideo.src = "";
                alert('Bu medya türü tam ekran görüntülenemiyor.');
                return;
            }
            modal.style.display = 'flex';
        }

        function closeModal() {
            modal.style.display = 'none';
            modalImg.src = '';
            modalVideo.pause();
            modalVideo.src = '';
        }

        function showNext() {
            currentIndex = (currentIndex + 1) % galleryItems.length;
            showModal(currentIndex);
        }

        function showPrev() {
            currentIndex = (currentIndex - 1 + galleryItems.length) % galleryItems.length;
            showModal(currentIndex);
        }

        galleryItems.forEach((item, idx) => {
            item.addEventListener('click', () => showModal(idx));
        });

        closeBtn.addEventListener('click', closeModal);
        nextBtn.addEventListener('click', showNext);
        prevBtn.addEventListener('click', showPrev);

        document.addEventListener('keydown', function(event) {
            if (modal.style.display === 'flex') {
                if (event.key === 'ArrowRight') showNext();
                else if (event.key === 'ArrowLeft') showPrev();
                else if (event.key === 'Escape') closeModal();
            }
        });

        let touchStartX = null;
        modal.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        });
        modal.addEventListener('touchend', function(e) {
            if (!touchStartX) return;
            let touchEndX = e.changedTouches[0].screenX;
            let diff = touchStartX - touchEndX;
            if (Math.abs(diff) > 50) {
                if (diff > 0) showNext();
                else showPrev();
            }
            touchStartX = null;
        });
        </script>
        """)

        html.append("</body></html>")

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
        except OSError:
            app.after(0, lambda: messagebox.showerror("Hata", f"Port {self.port} zaten kullanılıyor!"))
            app.after(0, app.stop_server)
            return
        app.after(0, lambda: app.append_log(f"Sunucu başladı: http://{get_local_ip()}:{self.port}/\n"))
        app.after(0, lambda: app.show_qr_code(f"http://{get_local_ip()}:{self.port}/"))
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
        self.title("Wi-Fi QR Medya Paylaşımı v1.5 - Erdal GÜNDOĞAN 2025")
        self.geometry("600x600")

        self.label_dir = tk.Label(self, text="Henüz klasör seçilmedi.")
        self.label_dir.pack(pady=5)

        self.btn_select = tk.Button(self, text="Klasör Seç\nMedya-Video Paylaşımı", command=self.select_folder)
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

        self.log_text = scrolledtext.ScrolledText(self, height=15, state=tk.DISABLED)
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
