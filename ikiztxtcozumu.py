import os
import hashlib
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def dosya_hashi(dosya_yolu):
    """Dosya içeriğini MD5 hash ile özetler"""
    import hashlib
    hash_md5 = hashlib.md5()
    with open(dosya_yolu, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def klasor_sec():
    yol = filedialog.askdirectory()
    if yol:
        klasor_yolu.set(yol)
        log_ekle(f"Seçilen klasör: {yol}\n")

def ikizleri_ayikla():
    ana_klasor = klasor_yolu.get()
    if not ana_klasor:
        messagebox.showwarning("Uyarı", "Lütfen önce bir klasör seçin!")
        return
    
    ikiz_klasor = os.path.join(ana_klasor, "ikizler")
    os.makedirs(ikiz_klasor, exist_ok=True)

    hash_map = {}
    ikiz_sayisi = 0

    for root, dirs, files in os.walk(ana_klasor):
        for dosya in files:
            if dosya.lower().endswith(".txt"):
                yol = os.path.join(root, dosya)
                # "ikizler" klasörünü atla
                if ikiz_klasor in yol:
                    continue

                h = dosya_hashi(yol)
                if h in hash_map:
                    # İkiz bulundu, ikizler klasörüne taşı
                    yeni_yol = os.path.join(ikiz_klasor, dosya)
                    
                    # Aynı isim varsa çakışmayı önle
                    sayac = 1
                    while os.path.exists(yeni_yol):
                        yeni_yol = os.path.join(
                            ikiz_klasor, f"{os.path.splitext(dosya)[0]}_{sayac}.txt"
                        )
                        sayac += 1
                    
                    shutil.move(yol, yeni_yol)
                    log_ekle(f"İkiz bulundu ve taşındı: {yol} -> {yeni_yol}\n")
                    ikiz_sayisi += 1
                else:
                    hash_map[h] = yol

    log_ekle(f"\n✅ İşlem tamamlandı. {ikiz_sayisi} ikiz dosya bulundu ve taşındı.\n")
    messagebox.showinfo("Bitti", f"İşlem tamamlandı.\nToplam {ikiz_sayisi} ikiz dosya bulundu.")

def log_ekle(mesaj):
    log_alani.insert(tk.END, mesaj)
    log_alani.see(tk.END)

# --- Tkinter Arayüzü ---
pencere = tk.Tk()
pencere.title("Txt İkiz Ayıklayıcı")
pencere.geometry("700x500")

klasor_yolu = tk.StringVar()

frame = tk.Frame(pencere)
frame.pack(pady=10)

btn_klasor = tk.Button(frame, text="Klasör Seç", command=klasor_sec)
btn_klasor.pack(side="left", padx=5)

lbl_klasor = tk.Label(frame, textvariable=klasor_yolu, width=60, anchor="w")
lbl_klasor.pack(side="left", padx=5)

btn_basla = tk.Button(pencere, text="İkizleri Ayıkla", command=ikizleri_ayikla, bg="lightgreen")
btn_basla.pack(pady=10)

log_alani = scrolledtext.ScrolledText(pencere, width=80, height=20)
log_alani.pack(pady=10)

pencere.mainloop()
