import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class TxtExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Txt Dosya Arama ve Düzenleme")

        # --- Sol kısım: Dosya listesi ---
        left_frame = tk.Frame(root)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.folder_btn = tk.Button(left_frame, text="Klasör Seç", command=self.choose_folder)
        self.folder_btn.pack(pady=5)

        self.file_listbox = tk.Listbox(left_frame, width=40, height=25)
        self.file_listbox.pack(fill="y", expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.load_file_content)

        # --- Üst kısım: Arama kutusu + Yenile + Dörtlük Yap + Kaydet ---
        top_frame = tk.Frame(root)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)

        tk.Label(top_frame, text="Metin Ara:").pack(side="left")
        self.search_entry = tk.Entry(top_frame, width=40)
        self.search_entry.pack(side="left", padx=5)       
        self.search_entry.bind("<Return>", lambda event: self.search_text())  # Enter ile ara

        tk.Button(top_frame, text="Ara", command=self.search_text).pack(side="left", padx=5)

        # Yenile butonu
        self.refresh_btn = tk.Button(top_frame, text="Yenile", command=self.list_txt_files)
        self.refresh_btn.pack(side="left", padx=5)

        # Dörtlük Yap butonu
        self.quatrain_btn = tk.Button(top_frame, text="Dörtlük Yap", command=self.make_quatrains)
        self.quatrain_btn.pack(side="left", padx=5)

        # Kaydet butonu → sağ tarafa
        self.save_btn = tk.Button(top_frame, text="Kaydet", command=self.save_file)
        self.save_btn.pack(side="right", padx=5)

        # --- Sağ kısım: Dosya içeriği ---
        right_frame = tk.Frame(root)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.text_area = scrolledtext.ScrolledText(right_frame, wrap="word", undo=True)
        self.text_area.pack(fill="both", expand=True)

        # Sağ tıklama menüsü (kopyala, kes, yapıştır)
        self.popup_menu = tk.Menu(self.root, tearoff=0)
        self.popup_menu.add_command(label="Kes", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.popup_menu.add_command(label="Kopyala", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.popup_menu.add_command(label="Yapıştır", command=lambda: self.text_area.event_generate("<<Paste>>"))

        self.text_area.bind("<Button-3>", self.show_popup)

        self.current_file = None
        self.base_folder = None  


    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.base_folder = folder
            self.list_txt_files()

    def list_txt_files(self):
        if not self.base_folder:
            return
        self.file_listbox.delete(0, tk.END)
        for root, _, files in os.walk(self.base_folder):
            for file in files:
                if file.lower().endswith(".txt"):
                    full_path = os.path.join(root, file)
                    self.file_listbox.insert(tk.END, full_path)

    def load_file_content(self, event=None):
        try:
            selection = self.file_listbox.curselection()
            if not selection:
                return
            filepath = self.file_listbox.get(selection[0])
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)
            self.current_file = filepath

            # Eğer bir arama kelimesi varsa, yüklenen içerikte de vurgula
            query = self.search_entry.get().strip()
            if query:
                self.highlight_search(query)

        except Exception as e:
            messagebox.showerror("Hata", str(e))


    def search_text(self):
        query = self.search_entry.get().strip()
        if not query:
            self.list_txt_files()
            return

        self.file_listbox.delete(0, tk.END)
        for root, _, files in os.walk(self.base_folder):
            for file in files:
                if file.lower().endswith(".txt"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        if query.lower() in content.lower():
                            self.file_listbox.insert(tk.END, filepath)
                    except:
                        continue

        # Eğer içerik alanında açık dosya varsa, orada da kelimeyi vurgula
        self.highlight_search(query)

    def highlight_search(self, query):
        """Text alanında aranan kelimeyi vurgular"""
        self.text_area.tag_remove("highlight", "1.0", tk.END)  # Önceki vurguları temizle

        if not query:
            return

        start_pos = "1.0"
        while True:
            start_pos = self.text_area.search(query, start_pos, nocase=1, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(query)}c"
            self.text_area.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos

        # Vurgunun görünümü (sarı arkaplan, siyah yazı)
        self.text_area.tag_config("highlight", background="yellow", foreground="black")


    def save_file(self):
        if not self.current_file:
            messagebox.showwarning("Uyarı", "Kaydedilecek dosya seçili değil!")
            return
        try:
            content = self.text_area.get("1.0", tk.END).strip()
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Bilgi", "Dosya kaydedildi.")
            self.list_txt_files()  # listeyi yenile
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def make_quatrains(self):
        try:
            # Önce seçim var mı bak
            selection = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            start, end = self.text_area.index(tk.SEL_FIRST), self.text_area.index(tk.SEL_LAST)
        except tk.TclError:
            # Seçim yoksa tüm metni al
            selection = self.text_area.get("1.0", "end-1c").strip()
            start, end = "1.0", tk.END

        if not selection:
            return

        # Satır satır işle
        lines = [line.strip() for line in selection.splitlines() if line.strip()]

        # 4 satırlık gruplar halinde düzenle
        quatrains = []
        for i in range(0, len(lines), 4):
            quatrains.append("\n".join(lines[i:i+4]))

        new_content = "\n\n".join(quatrains)

        # Seçili kısmı veya tüm metni değiştir
        self.text_area.delete(start, end)
        self.text_area.insert(start, new_content)

    def show_popup(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = TxtExplorerApp(root)
    root.mainloop()
