import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Program bilgisi
PROGRAM_YAZARI = "Erdal GÜNDOĞAN 2025"

def hash_file(filepath):
    """Dosyanın içeriğinin hash değerini hesapla."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

class FileToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Dosya Bulma ve Kopyalama ({PROGRAM_YAZARI})")
        self.root.geometry("600x400")

        # Klasör seçim
        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Label(frame, text="Kaynak Klasör:").grid(row=0, column=0, sticky="e")
        self.src_entry = tk.Entry(frame, width=50)
        self.src_entry.grid(row=0, column=1)
        tk.Button(frame, text="Seç", command=self.select_source_folder).grid(row=0, column=2)

        tk.Label(frame, text="Hedef Klasör:").grid(row=1, column=0, sticky="e")
        self.dst_entry = tk.Entry(frame, width=50)
        self.dst_entry.grid(row=1, column=1)
        tk.Button(frame, text="Seç", command=self.select_dest_folder).grid(row=1, column=2)

        # Butonlar
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Önce Bul", command=self.find_files).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Sonra Kopyala", command=self.copy_files).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Aynı İçerikleri Tespit Et", command=self.find_duplicates).grid(row=0, column=2, padx=5)

        # Sonuç kutusu
        self.text_box = tk.Text(root, height=10)
        self.text_box.pack(fill="both", expand=True)

        # İşlem çubuğu
        self.progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=5)

        # Sayaçlar
        self.found_files = []
        self.duplicate_groups = []

    def select_source_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, folder)

    def select_dest_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dst_entry.delete(0, tk.END)
            self.dst_entry.insert(0, folder)

    def find_files(self):
        src = self.src_entry.get()
        if not os.path.isdir(src):
            messagebox.showerror("Hata", "Kaynak klasör geçersiz.")
            return

        self.found_files.clear()
        for root_dir, _, files in os.walk(src):
            for file in files:
                if file.lower().endswith(".txt"):
                    self.found_files.append(os.path.join(root_dir, file))

        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, f"Bulunan dosya sayısı: {len(self.found_files)}\n")
        for f in self.found_files:
            self.text_box.insert(tk.END, f"{f}\n")

    def copy_files(self):
        dst = self.dst_entry.get()
        if not os.path.isdir(dst):
            messagebox.showerror("Hata", "Hedef klasör geçersiz.")
            return

        if not self.found_files:
            messagebox.showwarning("Uyarı", "Önce dosyaları bulun.")
            return

        self.progress["maximum"] = len(self.found_files)
        copied_count = 0

        for i, file in enumerate(self.found_files, 1):
            shutil.copy2(file, dst)
            copied_count += 1
            self.progress["value"] = i
            self.root.update_idletasks()

        messagebox.showinfo("Tamamlandı", f"{copied_count} dosya kopyalandı.")

    def find_duplicates(self):
        src = self.src_entry.get()
        if not os.path.isdir(src):
            messagebox.showerror("Hata", "Kaynak klasör geçersiz.")
            return

        file_hashes = {}
        self.duplicate_groups.clear()
        all_txt_files = []

        for root_dir, _, files in os.walk(src):
            for file in files:
                if file.lower().endswith(".txt"):
                    all_txt_files.append(os.path.join(root_dir, file))

        self.progress["maximum"] = len(all_txt_files)
        self.progress["value"] = 0
        self.root.update_idletasks()

        for i, filepath in enumerate(all_txt_files, 1):
            file_hash = hash_file(filepath)
            file_hashes.setdefault(file_hash, []).append(filepath)
            self.progress["value"] = i
            self.root.update_idletasks()

        # Sadece 1'den fazla dosya olan grupları listele
        self.duplicate_groups = [files for files in file_hashes.values() if len(files) > 1]

        self.text_box.delete("1.0", tk.END)
        if not self.duplicate_groups:
            self.text_box.insert(tk.END, "Aynı içerikli dosya bulunamadı.\n")
            return

        self.text_box.insert(tk.END, f"Aynı içerikli dosya grupları ({len(self.duplicate_groups)} grup):\n\n")
        for group in self.duplicate_groups:
            self.text_box.insert(tk.END, "---\n")
            for f in group:
                self.text_box.insert(tk.END, f"{f}\n")

        if messagebox.askyesno("Silme Onayı", "Aynı içerikli dosyalardan bir kopya hariç hepsi silinsin mi?"):
            self.delete_duplicates()

    def delete_duplicates(self):
        deleted_count = 0
        for group in self.duplicate_groups:
            for file in group[1:]:  # İlk dosya kalsın
                try:
                    os.remove(file)
                    deleted_count += 1
                except Exception as e:
                    print(f"Silinemedi: {file} - {e}")

        messagebox.showinfo("Tamamlandı", f"{deleted_count} adet gereksiz kopya silindi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileToolApp(root)
    root.mainloop()
