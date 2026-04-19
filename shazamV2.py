"""
TXT Dosya Kopyalama ve Yinelenen İçerik Temizleme
-------------------------------------------------
Bu program:
1. Seçilen klasördeki tüm .txt dosyalarını bulur ve hedef klasöre kopyalar.
2. Aynı isimli dosyaları _copy1, _copy2 ... şeklinde yeniden adlandırır.
3. 'Aynı İçerikleri Temizle' butonuyla içerikleri aynı olan dosyaları tespit eder
   ve kullanıcı onay verirse tek kopya bırakıp diğerlerini siler.

Programı yazan: Erdal GÜNDOĞAN
Yıl: 2025
"""

import os
import shutil
import time
import threading
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class TxtCopierApp:
    def __init__(self, master):
        self.master = master
        self.master.title("TXT Dosya Kopyalama - Erdal GÜNDOĞAN 2025")
        self.master.geometry("480x380")

        self.source_dir = ""
        self.target_dir = ""
        self.txt_files = []

        # Kaynak klasör seç
        tk.Button(master, text="Kaynak Klasörü Seç", command=self.select_source).pack(pady=5)
        self.source_label = tk.Label(master, text="Seçilmedi", fg="gray")
        self.source_label.pack()

        # Hedef klasör seç
        tk.Button(master, text="Hedef Klasörü Seç", command=self.select_target).pack(pady=5)
        self.target_label = tk.Label(master, text="Seçilmedi", fg="gray")
        self.target_label.pack()

        # Butonlar
        frame_btns = tk.Frame(master)
        frame_btns.pack(pady=10)
        self.find_btn = tk.Button(frame_btns, text="Bul", width=12, command=self.find_txt_files)
        self.find_btn.grid(row=0, column=0, padx=5)
        self.copy_btn = tk.Button(frame_btns, text="Kopyala", width=12, state="disabled", command=self.start_copy)
        self.copy_btn.grid(row=0, column=1, padx=5)
        self.clean_btn = tk.Button(frame_btns, text="Aynı İçerikleri Temizle", width=20, command=self.clean_duplicates)
        self.clean_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # İlerleme çubuğu
        self.progress = ttk.Progressbar(master, length=350, mode="determinate")
        self.progress.pack(pady=5)

        # Durum bilgileri
        self.count_label = tk.Label(master, text="Bulunan: 0 | Kopyalanan: 0", fg="green")
        self.count_label.pack()
        self.time_label = tk.Label(master, text="Süre: 0 sn", fg="blue")
        self.time_label.pack()

        # Alt bilgi
        tk.Label(master, text="Programı yazan: Erdal GÜNDOĞAN - 2025", fg="gray").pack(side="bottom", pady=5)

    def select_source(self):
        self.source_dir = filedialog.askdirectory(title="Kaynak klasörü seç")
        self.source_label.config(text=self.source_dir if self.source_dir else "Seçilmedi")

    def select_target(self):
        self.target_dir = filedialog.askdirectory(title="Hedef klasörü seç")
        self.target_label.config(text=self.target_dir if self.target_dir else "Seçilmedi")

    def find_txt_files(self):
        if not self.source_dir:
            messagebox.showwarning("Uyarı", "Lütfen kaynak klasörü seçin.")
            return

        self.txt_files.clear()
        for dirpath, _, filenames in os.walk(self.source_dir):
            for filename in filenames:
                if filename.lower().endswith(".txt"):
                    self.txt_files.append(os.path.join(dirpath, filename))

        self.count_label.config(text=f"Bulunan: {len(self.txt_files)} | Kopyalanan: 0")
        if self.txt_files:
            self.copy_btn.config(state="normal")
            messagebox.showinfo("Bulundu", f"{len(self.txt_files)} adet TXT dosyası bulundu.")
        else:
            self.copy_btn.config(state="disabled")
            messagebox.showinfo("Sonuç", "TXT dosyası bulunamadı.")

    def start_copy(self):
        if not self.target_dir:
            messagebox.showwarning("Uyarı", "Lütfen hedef klasörü seçin.")
            return
        if not self.txt_files:
            messagebox.showwarning("Uyarı", "Önce dosyaları bulmanız gerekiyor.")
            return

        self.copy_btn.config(state="disabled")
        threading.Thread(target=self.copy_txt_files).start()

    def copy_txt_files(self):
        total_files = len(self.txt_files)
        self.progress["maximum"] = total_files
        copied_files = 0
        start_time = time.time()

        for i, src_path in enumerate(self.txt_files, 1):
            base, ext = os.path.splitext(os.path.basename(src_path))
            dest_path = os.path.join(self.target_dir, base + ext)

            copy_index = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(self.target_dir, f"{base}_copy{copy_index}{ext}")
                copy_index += 1

            shutil.copy2(src_path, dest_path)
            copied_files += 1

            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = avg_time * (total_files - i)

            self.progress["value"] = i
            self.count_label.config(text=f"Bulunan: {total_files} | Kopyalanan: {copied_files}")
            self.time_label.config(text=f"Geçen: {int(elapsed)} sn | Kalan: {int(remaining)} sn")
            self.master.update_idletasks()

        messagebox.showinfo("Tamamlandı", f"{copied_files} adet TXT dosyası kopyalandı.")
        self.copy_btn.config(state="normal")

    def clean_duplicates(self):
        if not self.source_dir:
            messagebox.showwarning("Uyarı", "Lütfen kaynak klasörü seçin.")
            return

        duplicates = {}
        for dirpath, _, filenames in os.walk(self.source_dir):
            for filename in filenames:
                if filename.lower().endswith(".txt"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, "rb") as f:
                            content = f.read().strip()
                        file_hash = hashlib.md5(content).hexdigest()
                        duplicates.setdefault(file_hash, []).append(file_path)
                    except Exception as e:
                        print(f"Hata: {file_path} - {e}")

        # Yalnızca birden fazla kopyası olanlar
        same_content_groups = {h: files for h, files in duplicates.items() if len(files) > 1}

        if not same_content_groups:
            messagebox.showinfo("Sonuç", "Aynı içeriğe sahip dosya bulunamadı.")
            return

        # Listeleme
        report = "Aynı içerikli dosyalar:\n\n"
        for files in same_content_groups.values():
            report += "\n".join(files) + "\n\n"

        if messagebox.askyesno("Onay", f"{len(same_content_groups)} grup bulundu.\n\n"
                                       f"Aynı içeriğe sahip dosyalardan sadece bir kopya bırakmak istiyor musunuz?"):
            deleted_count = 0
            for files in same_content_groups.values():
                # İlkini bırak, diğerlerini sil
                for file_path in files[1:]:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except:
                        pass
            messagebox.showinfo("Tamamlandı", f"{deleted_count} dosya silindi.")
        else:
            messagebox.showinfo("İptal", "Silme işlemi yapılmadı.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TxtCopierApp(root)
    root.mainloop()
