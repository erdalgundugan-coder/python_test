import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import hashlib
from threading import Thread
import tkinter.ttk as ttk

class TxtCollectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TXT Dosya Toplayıcı")
        self.geometry("700x450")

        # Seçilen kaynak dosya ve klasör listeleri
        self.src_paths = []

        # Hedef klasör
        self.dst_folder = ""

        # Arayüz elemanları
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill="x")

        # Kaynak dosya/klasör seç
        btn_add_files = tk.Button(frame, text="Kaynak Dosya Ekle (.txt)", command=self.add_files)
        btn_add_files.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        btn_add_folder = tk.Button(frame, text="Kaynak Klasör Ekle (Alt Klasörler Dahil)", command=self.add_folder)
        btn_add_folder.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Seçilen kaynaklar listesi
        self.listbox_src = tk.Listbox(frame, height=8, selectmode=tk.EXTENDED)
        self.listbox_src.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Hedef klasör seç
        btn_select_dst = tk.Button(frame, text="Hedef Klasör Seç", command=self.select_dst_folder)
        btn_select_dst.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Seçilen hedef klasör etiketi
        self.label_dst = tk.Label(frame, text="Hedef klasör seçilmedi")
        self.label_dst.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # İşlem başlat butonu
        btn_start = tk.Button(frame, text="İşlemi Başlat", command=self.start_process)
        btn_start.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        # İşlem ilerleme çubuğu
        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progressbar.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # İşlem özeti metin kutusu
        self.text_summary = tk.Text(frame, height=10, state="disabled", wrap="word")
        self.text_summary.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Grid genişlik ayarı
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(5, weight=1)

    def add_files(self):
        files = filedialog.askopenfilenames(title="TXT Dosyaları Seçin", filetypes=[("Text Files", "*.txt")])
        if files:
            added = 0
            for f in files:
                if f not in self.src_paths:
                    self.src_paths.append(f)
                    added += 1
            self.update_src_list()
            self.append_summary(f"{added} dosya eklendi.")

    def add_folder(self):
        folder = filedialog.askdirectory(title="Kaynak Klasör Seçin")
        if folder:
            count_before = len(self.src_paths)
            for root, dirs, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(".txt"):
                        full_path = os.path.join(root, f)
                        if full_path not in self.src_paths:
                            self.src_paths.append(full_path)
            added = len(self.src_paths) - count_before
            self.update_src_list()
            self.append_summary(f"{added} dosya klasörden eklendi (alt klasörler dahil).")

    def update_src_list(self):
        self.listbox_src.delete(0, tk.END)
        for path in self.src_paths:
            self.listbox_src.insert(tk.END, path)

    def select_dst_folder(self):
        folder = filedialog.askdirectory(title="Hedef Klasör Seçin")
        if folder:
            self.dst_folder = folder
            self.label_dst.config(text=f"Hedef klasör: {self.dst_folder}")

    def start_process(self):
        if not self.src_paths:
            messagebox.showwarning("Uyarı", "Lütfen en az bir kaynak dosya veya klasör ekleyin.")
            return
        if not self.dst_folder:
            messagebox.showwarning("Uyarı", "Lütfen hedef klasörü seçin.")
            return
        self.text_summary.config(state="normal")
        self.text_summary.delete(1.0, tk.END)
        self.text_summary.config(state="disabled")
        self.progress_var.set(0)
        thread = Thread(target=self.process_files)
        thread.start()

    def process_files(self):
        def file_hash(path):
            hasher = hashlib.md5()
            try:
                with open(path, "rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        hasher.update(chunk)
            except Exception as e:
                self.append_summary(f"Hata: {path} okunamadı: {e}")
                return None
            return hasher.hexdigest()

        # Hedef klasörde var olan dosyaların hash ve isimleri
        existing_hashes = {}
        existing_names = set()

        for f in os.listdir(self.dst_folder):
            full_path = os.path.join(self.dst_folder, f)
            if os.path.isfile(full_path) and f.lower().endswith(".txt"):
                h = file_hash(full_path)
                if h:
                    existing_hashes[h] = full_path
                    existing_names.add(f)

        total = len(self.src_paths)
        copied = 0
        skipped = 0
        renamed = 0

        for i, src_path in enumerate(self.src_paths, 1):
            h = file_hash(src_path)
            if h is None:
                self.progress_var.set(i / total * 100)
                continue

            if h in existing_hashes:
                # Aynı içerik varsa kopyalamaya gerek yok
                skipped += 1
                self.append_summary(f"Atlandı (aynı içerik): {src_path}")
                self.progress_var.set(i / total * 100)
                continue

            fname = os.path.basename(src_path)
            dst_path = os.path.join(self.dst_folder, fname)

            if fname in existing_names:
                # Aynı isim farklı içerik, copy1, copy2 ekle
                base, ext = os.path.splitext(fname)
                copy_index = 1
                while True:
                    new_name = f"{base}_copy{copy_index}{ext}"
                    if new_name not in existing_names:
                        dst_path = os.path.join(self.dst_folder, new_name)
                        existing_names.add(new_name)
                        renamed += 1
                        break
                    copy_index += 1
            else:
                existing_names.add(fname)

            try:
                shutil.copy2(src_path, dst_path)
                existing_hashes[h] = dst_path
                copied += 1
                self.append_summary(f"Kopyalandı: {src_path} -> {dst_path}")
            except Exception as e:
                self.append_summary(f"Hata: {src_path} kopyalanamadı: {e}")

            self.progress_var.set(i / total * 100)

        self.append_summary("\nİşlem tamamlandı.")
        self.append_summary(f"Toplam dosya: {total}")
        self.append_summary(f"Kopyalanan: {copied}")
        self.append_summary(f"Atlanan (aynı içerik): {skipped}")
        self.append_summary(f"Yeniden adlandırılan: {renamed}")

    def append_summary(self, text):
        self.text_summary.config(state="normal")
        self.text_summary.insert(tk.END, text + "\n")
        self.text_summary.see(tk.END)
        self.text_summary.config(state="disabled")


if __name__ == "__main__":
    app = TxtCollectorApp()
    app.mainloop()
