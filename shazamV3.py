import os
import hashlib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Dosya içeriğinden MD5 hash üret
def file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(8192)
        while buf:
            hasher.update(buf)
            buf = f.read(8192)
    return hasher.hexdigest()

# TXT dosyalarını tara ve hash ile grupla
def find_duplicate_files():
    folder = filedialog.askdirectory(title="Klasör Seç")
    if not folder:
        return

    txt_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".txt"):
                txt_files.append(os.path.join(root, file))

    if not txt_files:
        messagebox.showinfo("Bilgi", "Hiç TXT dosyası bulunamadı.")
        return

    progress["maximum"] = len(txt_files)
    progress["value"] = 0
    window.update()

    hashes = {}
    duplicates = {}

    for i, filepath in enumerate(txt_files, 1):
        try:
            h = file_hash(filepath)
            if h in hashes:
                duplicates.setdefault(h, []).append(filepath)
            else:
                hashes[h] = filepath
        except Exception as e:
            print(f"Hata: {filepath} - {e}")

        progress["value"] = i
        window.update_idletasks()

    show_duplicates(duplicates)

# Bulunan kopyaları göster
def show_duplicates(duplicates):
    text_output.delete(1.0, tk.END)
    if not duplicates:
        text_output.insert(tk.END, "Aynı içeriğe sahip dosya bulunamadı.\n")
        return

    text_output.insert(tk.END, f"Aynı içeriğe sahip grup sayısı: {len(duplicates)}\n\n")

    example_count = 0
    for hash_value, files in duplicates.items():
        if example_count < 10:  # İlk 10 örnek göster
            text_output.insert(tk.END, "🔹 Grup:\n")
            text_output.insert(tk.END, f"  Orijinal: {files[0]}\n")
            for f in files[1:]:
                text_output.insert(tk.END, f"  Kopya: {f}\n")
            text_output.insert(tk.END, "\n")
            example_count += 1
    text_output.insert(tk.END, "Silme işlemi için 'Kopyaları Sil' butonuna basabilirsiniz.\n")

    global duplicate_data
    duplicate_data = duplicates

# Kopyaları sil
def delete_duplicates():
    if not duplicate_data:
        messagebox.showwarning("Uyarı", "Silinecek kopya bulunamadı.")
        return

    cevap = messagebox.askyesno("Onay", "Tüm kopyaları silmek istediğinizden emin misiniz?")
    if not cevap:
        return

    deleted_count = 0
    for files in duplicate_data.values():
        for f in files[1:]:  # İlk dosya kalır, diğerleri silinir
            try:
                os.remove(f)
                deleted_count += 1
            except Exception as e:
                print(f"Silme hatası: {f} - {e}")

    messagebox.showinfo("Tamamlandı", f"{deleted_count} kopya dosya silindi.")
    text_output.insert(tk.END, f"\n✅ {deleted_count} kopya dosya silindi.\n")

# Ana pencere
window = tk.Tk()
window.title("TXT İçerik Karşılaştırma - Erdal GÜNDOĞAN 2025")
window.geometry("800x600")

frame_buttons = tk.Frame(window)
frame_buttons.pack(pady=10)

btn_find = tk.Button(frame_buttons, text="TXT Kopyaları Bul", command=find_duplicate_files)
btn_find.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(frame_buttons, text="Kopyaları Sil", command=delete_duplicates)
btn_delete.pack(side=tk.LEFT, padx=5)

progress = ttk.Progressbar(window, length=600, mode="determinate")
progress.pack(pady=10)

text_output = tk.Text(window, height=25, wrap="word")
text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

duplicate_data = {}

window.mainloop()
