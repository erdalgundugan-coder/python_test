import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import socket

httpd = None
server_thread = None
selected_dir = None

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
    # loglama fonksiyonunu override ederek Tkinter penceresine yazdıracağız
    def log_message(self, format, *args):
        msg = "%s - - [%s] %s\n" % (
            self.client_address[0],
            self.log_date_time_string(),
            format%args
        )
        # Konsola yazdır
        print(msg, end='')
        # Tkinter'daki log alanına yazdır
        if app and app.log_text:
            app.log_text.config(state=tk.NORMAL)
            app.log_text.insert(tk.END, msg)
            app.log_text.see(tk.END)
            app.log_text.config(state=tk.DISABLED)

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
        try:
            self.httpd.serve_forever()  # Sonsuz döngüde istekleri kabul eder
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
        self.title("Wi-Fi Dosya Paylaşımı - Erdal GÜNDOĞAN 2025")
        self.geometry("600x500")

        # Seçilen klasör etiketi
        self.label_dir = tk.Label(self, text="Henüz klasör seçilmedi.")
        self.label_dir.pack(pady=5)

        # Klasör seçme butonu
        self.btn_select = tk.Button(self, text="Klasör Seç", command=self.select_folder)
        self.btn_select.pack(pady=5)

        # Port girişi
        port_frame = tk.Frame(self)
        port_frame.pack(pady=5)
        tk.Label(port_frame, text="Port:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="8000")
        self.entry_port = tk.Entry(port_frame, textvariable=self.port_var, width=6)
        self.entry_port.pack(side=tk.LEFT)

        # Sunucu başlat / durdur butonları
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_start = tk.Button(btn_frame, text="Sunucuyu Başlat", bg="green", fg="white", command=self.start_server)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_stop = tk.Button(btn_frame, text="Sunucuyu Durdur", bg="red", fg="white", command=self.stop_server, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        # Log alanı (scrollable)
        self.log_text = scrolledtext.ScrolledText(self, height=15, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.server_thread = None
        self.selected_dir = None

    def append_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

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

        # Sunucu başlatılıyor
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

        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_select.config(state=tk.NORMAL)
        self.entry_port.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = App()
    app.mainloop()
#server