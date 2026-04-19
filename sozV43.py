import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
import unicodedata
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog
import re
# EXE veya script konumuna göre klasör ayarı
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
FAVORITES_FILE = os.path.join(APP_DIR, "favorites.json")
class GroupSelectDialog(Dialog):
    def __init__(self, parent, groups):
        self.groups = groups
        self.selected_group = None
        super().__init__(parent, title="Favori Grubu Seç veya Yeni Gir")
    def body(self, master):
        tk.Label(master, text="Mevcut Gruplar:").grid(row=0, column=0, sticky="w")
        self.combo = ttk.Combobox(master, values=self.groups, state="readonly")
        self.combo.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        if self.groups:
            self.combo.current(0)
        tk.Label(master, text="Ya da Yeni Grup:").grid(row=2, column=0, sticky="w")
        self.entry_new = tk.Entry(master)
        self.entry_new.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        return self.combo  # focus burada başlasın
    def apply(self):
        new_group = self.entry_new.get().strip()
        if new_group:
            self.selected_group = new_group
        else:
            self.selected_group = self.combo.get() if self.combo.get() else "Genel"
class LyricsSearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Şarkı Sözü Arama-----Erdal GÜNDOĞAN--2025")
        self.root.geometry("1200x700")
        self.root.state('zoomed')
        self.base_font_size_listbox = 12
        self.base_font_size_textbox = 12
        self.font_listbox = tkfont.Font(family="Arial", size=self.base_font_size_listbox)
        self.font_textbox = tkfont.Font(family="Arial", size=self.base_font_size_textbox)
        self.folder_path = APP_DIR  # Başlangıç klasörü exe/script klasörü
        self.file_contents = {}
        self.search_results = []
        self.current_selection = ""
        self.favorites = []
        self.current_favorites_file = FAVORITES_FILE
        # Vurgulama renkleri
        self.highlight_colors = ["red", "blue", "green", "purple", "orange", "brown", "magenta"]
        self.setup_ui()
        self.setup_bindings()
        self.load_files()  # Başlangıçta dosyaları yükle
        self.update_file_list()
        self.load_favorites()
    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5, fill="x")
        folder_frame = tk.Frame(top_frame)
        folder_frame.pack(side="left", padx=5)
        tk.Button(folder_frame, text="Klasör\nSeç", command=self.select_folder).pack(side="left")
        tk.Button(folder_frame, text="Yenile", command=self.refresh_file_list).pack(side="left", padx=5)
        self.file_count_label = tk.Label(folder_frame, text="Dosya: 0")
        self.file_count_label.pack(side="left", padx=10)
        self.folder_path_label = tk.Label(folder_frame, text=f"Klasör:\n{self.folder_path}", font=("Arial", 9))
        self.folder_path_label.pack(side="left", padx=10)
        search_frame = tk.Frame(top_frame)
        search_frame.pack(side="left", padx=5) 
        #self.entry = tk.Entry(search_frame, width=50, font=self.font_textbox)
        self.entry = tk.Entry(search_frame, width=50, font=self.font_listbox)        
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.search_in_all_files())
        # Entry için sağ tık menüsü
        self.entry_menu = tk.Menu(self.root, tearoff=0)
        self.entry_menu.add_command(label="Kes", command=lambda: self.entry.event_generate("<<Cut>>"))
        self.entry_menu.add_command(label="Kopyala", command=lambda: self.entry.event_generate("<<Copy>>"))
        self.entry_menu.add_command(label="Yapıştır", command=lambda: self.entry.event_generate("<<Paste>>"))
        self.entry.bind("<Button-3>", self.show_entry_menu)
        tk.Button(search_frame, text="Ara", command=self.search_in_all_files).pack(side="left", padx=(0, 10))
        tk.Button(search_frame, text="Kaydet\nŞarkı Metni Üzende\n Değişikliğini Kaydet", command=self.save_file).pack(side="left")
        self.btn_new_txt = tk.Button(search_frame, text="Farklı Kaydet Şarkı\nEkrani Sil Düzenle,\nilk Satır Başlık Olur", command=self.new_txt_toggle)
        self.btn_new_txt.pack(side="left", padx=5)

        main_pane = tk.PanedWindow(self.root, orient="horizontal", sashrelief=tk.RAISED, sashwidth=5, showhandle=True)
        main_pane.pack(fill="both", expand=True)
        left_frame = tk.Frame(main_pane)
        center_pane = tk.PanedWindow(main_pane, orient="vertical", sashrelief=tk.RAISED, sashwidth=5)
        right_frame = tk.Frame(main_pane)
        main_pane.add(left_frame, stretch="always")
        main_pane.add(center_pane, stretch="always")
        main_pane.add(right_frame, stretch="always")
        # Sol: Dosyalar ve arama sonucu dosyalar
        self.search_files_label = tk.Label(left_frame, text="Bulunan Dosyalar (.txt):", font=self.font_listbox)
        self.search_files_label.grid(row=2, column=0, sticky="w")
        tk.Label(left_frame, text="Ara (Dosya.txt):", font=self.font_listbox).grid(row=0, column=0, sticky="w", pady=(5,0))
        self.file_search_entry = tk.Entry(left_frame, font=self.font_listbox)
        self.file_search_entry.grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(0, 5))
        self.file_search_entry.bind("<KeyRelease>", self.filter_file_list)
        self.search_files_listbox = tk.Listbox(left_frame, height=5, font=self.font_listbox)
        self.search_files_listbox.grid(row=3, column=0, sticky="ew")

        scrollbar_filesz = tk.Scrollbar(left_frame, command=self.search_files_listbox.yview)
        scrollbar_filesz.grid(row=3, column=1, sticky="ns")
        self.search_files_listbox.config(yscrollcommand=scrollbar_filesz.set)

        self.search_files_listbox.bind("<<ListboxSelect>>", self.on_search_file_select)
        left_frame.grid_rowconfigure(4, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        self.file_listbox = tk.Listbox(left_frame, width=40, font=self.font_listbox)
        self.file_listbox.grid(row=4, column=0, sticky="nsew")
        scrollbar_files = tk.Scrollbar(left_frame, command=self.file_listbox.yview)
        scrollbar_files.grid(row=4, column=1, sticky="ns")
        self.file_listbox.config(yscrollcommand=scrollbar_files.set)
        self.file_listbox.bind("<<ListboxSelect>>", self.display_file_content)
        # Ortadaki paned: Üst: Arama sonuçları, Alt: Favoriler (aralarında kaydırılabilir)
        center_frame_top = tk.Frame(center_pane)
        center_frame_bottom = tk.Frame(center_pane)
        center_pane.add(center_frame_top, stretch="always")
        center_pane.add(center_frame_bottom, stretch="always")
        center_frame_top.grid_rowconfigure(1, weight=1)
        center_frame_top.grid_columnconfigure(0, weight=1)
        result_label = tk.Label(center_frame_top, text="Arama Sonuçları (Önce Favorilerden Başlar):", font=self.font_listbox)
        result_label.grid(row=0, column=0, sticky="w")
        self.result_listbox = tk.Listbox(center_frame_top, font=self.font_listbox, exportselection=False)
        self.result_listbox.grid(row=1, column=0, sticky="nsew")
        scrollbar_results = tk.Scrollbar(center_frame_top, command=self.result_listbox.yview)
        scrollbar_results.grid(row=1, column=1, sticky="ns")
        self.result_listbox.config(yscrollcommand=scrollbar_results.set)
        self.result_listbox.bind("<<ListboxSelect>>", self.show_line_file_content)
        btn_frame = tk.Frame(center_frame_top)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=5)
        self.btn_add_fav = tk.Button(btn_frame, text="Favori Ekle\nArama Sonucundan\nÜst Kutudan", command=self.add_selected_result_to_favorites)
        self.btn_add_fav.pack(side="left", padx=5)
        self.btn_remove_fav = tk.Button(btn_frame, text="Favori Çıkar\nFavori Listesinden\nAlt Kutudan", command=self.remove_selected_favorite)
        self.btn_remove_fav.pack(side="left", padx=5)
        self.btn_add_cursor_fav = tk.Button(btn_frame, text="Favori Ekle\nMetin İmleç Satırı\nSağ Kutudan", command=self.add_current_line_to_favorites)
        self.btn_add_cursor_fav.pack(side="left", padx=5)
        center_frame_bottom.grid_rowconfigure(1, weight=1)
        center_frame_bottom.grid_columnconfigure(0, weight=1)        
        self.fav_label = tk.Label(center_frame_bottom, text="Favori Listesi:", font=self.font_listbox)
        self.fav_label.grid(row=0, column=0, sticky="w")
        self.fav_listbox = tk.Listbox(center_frame_bottom, font=self.font_listbox, exportselection=False)
        self.fav_listbox.grid(row=1, column=0, sticky="nsew")
        scrollbar_fav = tk.Scrollbar(center_frame_bottom, command=self.fav_listbox.yview)
        scrollbar_fav.grid(row=1, column=1, sticky="ns")
        self.fav_listbox.config(yscrollcommand=scrollbar_fav.set)
        self.fav_listbox.bind("<<ListboxSelect>>", self.show_favorite_content)
        fav_btn_frame = tk.Frame(center_frame_bottom)
        fav_btn_frame.grid(row=2, column=0, sticky="ew", pady=5)
        #tk.Button(fav_btn_frame, text="Favorileri Kaydet", command=self.save_favorites).pack(side="left", padx=5)
        tk.Button(fav_btn_frame, text="Favori liste Yükle", command=self.load_favorites).pack(side="left", padx=5)
        #tk.Button(fav_btn_frame, text="Fav Farklı Kaydet", command=self.save_favorites_as).pack(side="left", padx=5)   
        tk.Button(fav_btn_frame, text="Fav liste Kaydet /Yeni Oluştur", command=self.create_empty_favorites_file).pack(side="left", padx=5) 
        # Sağdaki metin ve satır navigasyonu
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        line_nav_frame = tk.Frame(self.root)
        line_nav_frame.pack(fill="x", pady=2)
        copy_btn = tk.Button(right_frame, text="→ Yeni Pencerede Göster", command=self.open_floating_copy)
        copy_btn.grid(row=0, column=10, pady=5, padx=5, sticky="ne")
        copy_btn_sec = tk.Button(right_frame, text="→ Seçimi Yeni Pencerede\nGöster", command=self.open_floating_copy_sec)
        copy_btn_sec.grid(row=1, column=10, pady=5, padx=5, sticky="ne")
        copy_btn_sil = tk.Button(right_frame, text="→ SeçimiN Boşluklarını Sil", command=self.open_floating_copy_sec)
        self.clean_spaces_button = tk.Button(right_frame, text="Boşlukları Temizle", command=self.fazla_bosluklari_temizle)
        self.clean_spaces_button.grid(row=2, column=10, pady=5, padx=5, sticky="ne")


        #tk.Label(line_nav_frame, text="Satır No:").pack(side="left")
        #self.line_entry = tk.Entry(line_nav_frame, width=5)
        #self.line_entry.pack(side="left", padx=5)
        #self.line_entry.bind("<Return>", self.goto_line)
        #tk.Button(line_nav_frame, text="Git", command=self.goto_line).pack(side="left")
        self.result_text = tk.Text(right_frame, wrap="word", font=self.font_textbox)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar_text = tk.Scrollbar(right_frame, command=self.result_text.yview)
        scrollbar_text.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar_text.set)
        
        # Text için sağ tık menüsü (Kes, Kopyala, Yapıştır)
        self.text_menu = tk.Menu(self.root, tearoff=0)
        self.text_menu.add_command(label="Kes", command=lambda: self.result_text.event_generate("<<Cut>>"))
        self.text_menu.add_command(label="Kopyala", command=lambda: self.result_text.event_generate("<<Copy>>"))
        self.text_menu.add_command(label="Yapıştır", command=lambda: self.result_text.event_generate("<<Paste>>"))
        self.result_text.bind("<Button-3>", self.show_text_menu)
        
        # Sağ tık kopyala menüsü
        #self.text_menu = tk.Menu(self.root, tearoff=0)
        #self.text_menu.add_command(label="Kopyala", command=lambda: self.result_text.event_generate("<<Copy>>"))
        #self.result_text.bind("<Button-3>", self.show_text_menu)
        self.cursor_line_label = tk.Label(right_frame, text="Satır No: -", font=self.font_listbox)
        self.cursor_line_label.grid(row=1, column=0, sticky="w", pady=2)
        self.dosya_label = tk.Label(right_frame, text="Dosya Adı :- ", font=self.font_listbox)
        self.dosya_label.grid(row=1, column=0, sticky="n", pady=2)#erdal

        # Sağ tık menüsü
        self.file_menu = tk.Menu(self.root, tearoff=0)
        self.file_menu.add_command(label="Yenile", command=self.refresh_file_list)
        self.file_menu.add_command(label="Yeni .txt Dosyası Oluştur", command=self.create_new_txt_file)
        self.file_menu.add_command(label="Yeniden Adlandır", command=self.rename_selected_file)
        self.file_menu.add_command(label="BOŞ GEÇ", command=None)
        self.file_menu.add_command(label="Sil", command=self.delete_selected_file)
        self.file_listbox.bind("<Button-3>", self.show_file_menu)  
        self.file_listbox.bind("<Delete>", self.delete_selected_file)  
        self.dark_mode_enabled = False  # Başlangıçta açık mod
        # Dark mode butonu
        self.dark_button = tk.Button(top_frame, text="🌙\nDark Mode", command=self.toggle_dark_mode)
        self.dark_button.pack(side=tk.RIGHT, padx=5)
        


    def goto_line(self, event=None):
        line_str = self.line_entry.get()
        if not line_str.isdigit():
            messagebox.showerror("Hata", "Geçerli bir satır numarası girin.")
            return
        line_num = int(line_str) + 1
        self.result_text.see(f"{line_num}.0")
        self.result_text.mark_set("insert", f"{line_num}.0")
        self.result_text.focus()
    def scroll_to_line(self, line_no):
        def do_scroll():
            self.result_text.see(f"{line_no+1}.0")
            self.result_text.mark_set("insert", f"{line_no+1}.0")
            self.result_text.tag_add("highlight_line", f"{line_no+1}.0", f"{line_no+1}.end")
        self.root.after_idle(do_scroll)
    def setup_bindings(self):
        self.root.bind("<Control-plus>", lambda e: self.adjust_textbox_font(1))
        self.root.bind("<Control-minus>", lambda e: self.adjust_textbox_font(-1))
        self.root.bind("<Control-=>", lambda e: self.adjust_textbox_font(1))
        self.root.bind("<Control-f>", lambda e: self.entry.focus_set())
        self.result_text.bind("<KeyRelease>", self.update_cursor_line)
        self.result_text.bind("<ButtonRelease>", self.update_cursor_line)
    def update_cursor_line(self, event=None):
        cursor_index = self.result_text.index("insert")
        line_num = cursor_index.split('.')[0]
        self.cursor_line_label.config(text=f"Satır No: {int(line_num) - 1}")
    def adjust_textbox_font(self, delta):
        self.base_font_size_textbox += delta
        if self.base_font_size_textbox < 6:
            self.base_font_size_textbox = 6
        self.font_textbox.configure(size=self.base_font_size_textbox)
    def select_folder(self):
        self.entry.focus_set()
        folder = filedialog.askdirectory(initialdir=APP_DIR)
        if not folder:
            return
        self.folder_path = folder
        self.folder_path_label.config(text=f"Klasör: {self.folder_path}")  # Buraya ekledik
        self.load_files()
        self.update_file_list()
    def refresh_file_list(self):
        self.load_files()
        self.update_file_list()
        self.result_text.delete("1.0", tk.END)
    def load_files(self):
        self.file_contents = {}
        for root_dir, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(".txt"):
                    rel_path = os.path.relpath(os.path.join(root_dir, file), self.folder_path)
                    try:
                        with open(os.path.join(root_dir, file), "r", encoding="utf-8") as f:
                            lines = f.readlines()
                            self.file_contents[rel_path] = lines
                    except UnicodeDecodeError:
                        try:
                            with open(os.path.join(root_dir, file), "r", encoding="ISO-8859-9") as f:
                                lines = f.readlines()
                                self.file_contents[rel_path] = lines
                        except Exception as e:
                            print(f"{rel_path} okunamadı: {e}")
        self.file_count_label.config(text=f"Dosya Sayısı: {len(self.file_contents)}")
    def update_file_list(self):
        if hasattr(self, "file_search_entry") and self.file_search_entry.get().strip():
            self.filter_file_list()
            return
        self.file_listbox.delete(0, tk.END)      
        #for filename in sorted(self.file_contents.keys()):
        for filename in sorted(self.file_contents.keys(), key=lambda x: x.lower()):
            self.file_listbox.insert(tk.END, filename)
    def normalize(self, text):
        text = text.casefold()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        return text
    def filter_file_list(self, event=None):
        query = self.file_search_entry.get().strip().lower()
        self.file_listbox.delete(0, tk.END)
        for filename in sorted(self.file_contents.keys(), key=lambda x: x.lower()):
            if query in filename.lower():
                self.file_listbox.insert(tk.END, filename)
    def find_original_index_and_length(self, original, target_norm, norm_index):
        original_index = 0
        normalized_accum = ''
        for i, char in enumerate(original):
            normalized_char = self.normalize(char)
            normalized_accum += normalized_char
            if len(normalized_accum) > norm_index:
                return original_index, len(target_norm)
            original_index += 1
        return original_index, len(target_norm)
    def search_in_all_files(self):
        raw_input = self.entry.get().strip()
        if not raw_input:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Lütfen arama kelimesi girin.")
            self.result_listbox.delete(0, tk.END)
            self.search_results = []
            return

        keywords = [self.normalize(w) for w in raw_input.split()]
        self.result_text.delete("1.0", tk.END)
        self.result_listbox.delete(0, tk.END)
        self.search_results = []

        # 1. Favori dosyalar öne alınır
        favorite_files = list({fav["file"] for fav in self.favorites})
        all_files = list(self.file_contents.keys())

        # Önce favori dosyalar
        priority_files = [f for f in favorite_files if f in self.file_contents]
        # Sonra kalanlar
        remaining_files = [f for f in all_files if f not in favorite_files]

        search_order = priority_files + remaining_files

        for filename in search_order:
            lines = self.file_contents[filename]
            y = 0
            for lineno, line in enumerate(lines):
                if lineno >= y:
                    norm_line = self.normalize(line)
                    line_words = norm_line.split()
                    if all(any(word.startswith(k) for word in line_words) for k in keywords):
                        is_fav = filename in favorite_files
                        prefix = "[FAV] " if is_fav else ""
                        display_line = f"{prefix}:{lineno}:{line.strip()}:...............................................................{filename}"
                        self.result_listbox.insert(tk.END, display_line)
                        self.search_results.append((filename, lineno, line.strip()))
                        y = lineno + 40

        if not self.search_results:
            self.result_listbox.delete(0, tk.END)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Aranan kelime bulunamadı.")

        found_files = set(filename for filename, _, _ in self.search_results)
        self.search_files_listbox.delete(0, tk.END)
        for f in sorted(found_files, key=lambda x: x.lower()):
            self.search_files_listbox.insert(tk.END, f)

    def on_search_file_select(self, event):
        sel = self.search_files_listbox.curselection()
        if not sel:
            return
        selected_file = self.search_files_listbox.get(sel[0])
        try:
            idx = self.file_listbox.get(0, tk.END).index(selected_file)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(idx)
            self.file_listbox.see(idx)
            self.display_file_content()
        except ValueError:
            pass
    def show_line_file_content(self, event=None):        
        selected = self.result_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        if index >= len(self.search_results):
            return
        filename, lineno, line = self.search_results[index]
        try:
            idx = self.file_listbox.get(0, tk.END).index(filename)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(idx)
            self.file_listbox.see(idx)
        except ValueError:
            pass
        self.highlight_text_in_result(filename, lineno)
    def display_file_content(self, event=None):
        selected = self.file_listbox.curselection()
        if not selected:
            return
        filename = self.file_listbox.get(selected[0])
        self.highlight_text_in_result(filename, None)
        self.current_selection = filename
    def create_new_txt_file(self):
        new_name = tk.simpledialog.askstring("Yeni Dosya", "Yeni dosya adı (örnek: yenidosya.txt):", initialvalue="yeni_dosya.txt")
        if not new_name:
            return
        if not new_name.endswith(".txt"):
            new_name += ".txt"
        full_path = os.path.join(self.folder_path, new_name)
        if os.path.exists(full_path):
            messagebox.showerror("Hata", "Bu isimde bir dosya zaten var.")
            return
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write("")  # boş içerik
            self.load_files()
            self.update_file_list()
            messagebox.showinfo("Başarılı", f"'{new_name}' oluşturuldu.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya oluşturulamadı:\n{e}")
    def highlight_text_in_result(self, filename, highlight_line_no=None):
        self.result_text.delete("1.0", tk.END)
        # Kullanıcı metni seçebilsin diye eski seçim tagini temizle
        self.result_text.tag_remove("sel", "1.0", tk.END)
        self.result_text.tag_remove("sel", "1.0", tk.END)
        # Tag temizliği
        for i in range(len(self.highlight_colors)):
            self.result_text.tag_delete(f"highlight{i}")
        self.result_text.tag_delete("highlight_line")
        # Tag ayarları
        self.result_text.tag_configure("highlight_line", background="lightblue")
        for idx, color in enumerate(self.highlight_colors):
            #self.result_text.tag_configure(f"highlight{idx}", foreground=color, font=("Arial", self.base_font_size_textbox, "bold"))
            self.result_text.tag_configure(f"highlight{idx}", foreground=color, underline=0)
        keywords = [self.normalize(w) for w in self.entry.get().strip().split()]
        lines = self.file_contents.get(filename, [])
        for i, line in enumerate(lines):
            self.result_text.insert(tk.END, line)
            norm_line = self.normalize(line)
            matched_line = False
            for idx, keyword in enumerate(keywords):
                start = 0
                while True:
                    found_idx = norm_line.find(keyword, start)
                    if found_idx == -1:
                        break
                    real_start, length = self.find_original_index_and_length(line, keyword, found_idx)
                    real_end = real_start + length
                    tag_name = f"highlight{idx}"
                    self.result_text.tag_add(tag_name, f"{i+1}.{real_start}", f"{i+1}.{real_end}")
                    matched_line = True
                    start = found_idx + length
            if matched_line:
                self.result_text.tag_add("highlight_line", f"{i+1}.0", f"{i+1}.end")
        if highlight_line_no is not None:
            self.scroll_to_line(highlight_line_no)
        self.dosya_label.config(text=os.path.basename(filename))  # Dosya adını göster

    def save_file(self):
        if not self.current_selection:
            tk.messagebox.showwarning("Uyarı", "Önce dosya seçin.")
            return
        content = self.result_text.get("1.0", "end-1c")
        file_path = os.path.join(self.folder_path, self.current_selection)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Bilgi", "Dosya kaydedildi.")            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata: {e}")
    def add_selected_result_to_favorites(self):
        sel = self.result_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self.search_results):
            return
        filename, lineno, line = self.search_results[idx]
        # Mevcut gruplar
        groups = list(set(fav.get("group", "Genel") for fav in self.favorites))
        if not groups:
            groups = ["Genel"]
        dialog = GroupSelectDialog(self.root, groups)
        group = dialog.selected_group if dialog.selected_group else "Genel"
        fav_item = {"file": filename, "line": lineno, "text": line, "group": group}
        if fav_item in self.favorites:
            messagebox.showinfo("Bilgi", "Bu favori zaten mevcut.")
            return
        self.favorites.append(fav_item)
        self.save_favorites()
        self.update_fav_list()
    def update_fav_list(self):
        self.fav_listbox.delete(0, tk.END)
        grouped = {}
        for fav in self.favorites:
            grp = fav.get("group", "Genel")
            grouped.setdefault(grp, []).append(fav)
        for group, favs in grouped.items():
            self.fav_listbox.insert(tk.END, f"--- {group} ---")
            for fav in favs:
                #display = f"{fav['file']}:{fav['line']} {fav['text']}"
                display =f" {fav['text']}...............................................{fav['file']}:{fav['line']}"
                self.fav_listbox.insert(tk.END, display)
            self.fav_listbox.insert(tk.END, "")  # boşluk
    def remove_selected_favorite(self):
        sel = self.fav_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        line_text = self.fav_listbox.get(idx)
        if line_text.startswith("---") or line_text.strip() == "":
            return  # Grup başlığı veya boşluk seçiliyse işlem yapma
        # Grup başlıkları ve boş satırlar listeye dahil, o yüzden doğru favori bulmak için filtreleyelim
        filtered_favs = []
        for fav in self.favorites:
            display =f" {fav['text']}...............................................{fav['file']}:{fav['line']}"            
            filtered_favs.append(display)
        try:
            fav_index = filtered_favs.index(line_text)
        except ValueError:
            return
        #if messagebox.askyesno("Onay", "Favoriden çıkarmak istediğinize emin misiniz?"):
        del self.favorites[fav_index]
        self.update_fav_list()
        self.save_favorites_to_current_file()   # <-- eklenen satır (JSON güncelle)

    def show_favorite_content(self, event=None):
        sel = self.fav_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        line_text = self.fav_listbox.get(idx)
        if line_text.startswith("---") or line_text.strip() == "":
            return  # Grup başlığı veya boşluk seçiliyse işlem yapma
        # Grup başlıkları ve boş satırlar listeye dahil, o yüzden doğru favori bulmak için filtreleyelim
        filtered_favs = []
        for fav in self.favorites:
            display =f" {fav['text']}...............................................{fav['file']}:{fav['line']}"            
            filtered_favs.append(display)
        try:
            fav_index = filtered_favs.index(line_text)
        except ValueError:
            return
        fav = self.favorites[fav_index]
        filename = fav['file']
        lineno = fav['line']
        # Dosyayı seç
        try:
            idx_file = self.file_listbox.get(0, tk.END).index(filename)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(idx_file)
            self.file_listbox.see(idx_file)
        except ValueError:
            pass
        self.highlight_text_in_result(filename, lineno)
    def get_current_favorites_filename(self):
        import os
        return os.path.basename(self.favorites)  
    def show_entry_menu(self, event):
        try:
            self.entry_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.entry_menu.grab_release()        
    def show_text_menu(self, event):
        try:
            self.text_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.text_menu.grab_release()
    def save_favorites(self):
        """favorileri varsayılan favorites.json dosyasına kaydeder"""
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
            #messagebox.showinfo("Bilgi", "Favoriler kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Favoriler kaydedilemedi: {e}")
    def save_favorites_as(self):
        """favorileri kullanıcı tarafından seçilen farklı bir dosyaya kaydeder"""
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON Dosyası", "*.json"), ("Tüm Dosyalar", "*.*")])
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Bilgi", "Favoriler farklı dosyaya kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")
    def load_favorites(self):
        """Seçilen JSON dosyasından favorileri yükler ve başlığa dosya adını ekler"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Dosyası", "*.json"), ("Tüm Dosyalar", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.favorites = data
                else:
                    self.favorites = []
        except Exception as e:
            messagebox.showerror("Hata", f"Favoriler yüklenemedi: {e}")
            return
        # Güncel kullanılan dosya adı kaydedilir
        self.current_favorites_file = file_path
        self.update_favorites_label()
        self.update_fav_list()
    def update_favorites_label(self):
        file_name = os.path.basename(self.current_favorites_file)
        self.fav_label.config(text=f"Favori Listesi: ({file_name})")
    def delete_selected_file(self,event=None):
        sel = self.file_listbox.curselection()
        if not sel:
            return
        filename = self.file_listbox.get(sel[0])
        full_path = os.path.join(self.folder_path, filename)
        if not messagebox.askyesno("Sil", f"{filename} dosyasını silmek istiyor musunuz?"):
            return
        try:
            os.remove(full_path)
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya silinemedi:\n{e}")
            return
        # Listeyi güncelle
        self.load_files()
        self.update_file_list()
        self.result_text.delete("1.0", tk.END)
    def create_empty_favorites_file(self):
        self.save_favorites_as()
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            self.favorites = []
            self.update_fav_list()
            
            messagebox.showinfo("Bilgi", f"Boş favori dosyası oluşturuldu:\n{FAVORITES_FILE}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya oluşturulamadı: {e}")
    def show_file_menu(self, event):
        # Sağ klik yapılan dosyayı seç
        try:
            index = self.file_listbox.nearest(event.y)
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(index)
            self.file_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.file_menu.grab_release()
    def rename_selected_file(self):
        sel = self.file_listbox.curselection()
        if not sel:
            return
        old_name = self.file_listbox.get(sel[0])
        new_name = tk.simpledialog.askstring("Yeniden Adlandır", f"Yeni ad (.txt uzantısıyla):", initialvalue=old_name)
        if not new_name or new_name == old_name:
            return
        old_path = os.path.join(self.folder_path, old_name)
        new_path = os.path.join(self.folder_path, new_name)
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            messagebox.showerror("Hata", f"Yeniden adlandırılamadı:\n{e}")
            return
        # Liste ve içerikleri güncelle
        self.load_files()
        self.update_file_list()
    def add_current_line_to_favorites(self):
        cursor_index = self.result_text.index("insert")
        line_num = int(cursor_index.split('.')[0]) - 1  # 0 tabanlı
        line_text = self.result_text.get(f"{line_num+1}.0", f"{line_num+1}.end").strip()
        filename = self.current_selection
        if not filename:
            messagebox.showwarning("Uyarı", "Bir dosya seçili değil.")
            return
        # Mevcut gruplar
        groups = list(set(fav.get("group", "Genel") for fav in self.favorites))
        if not groups:
            groups = ["Genel"]
        dialog = GroupSelectDialog(self.root, groups)
        group = dialog.selected_group if dialog.selected_group else "Genel"
        fav_item = {"file": filename, "line": line_num, "text": line_text, "group": group}
        if fav_item in self.favorites:
            #messagebox.showinfo("Bilgi", "Bu favori zaten mevcut.")
            return
        self.favorites.append(fav_item)
        self.save_favorites()
        self.update_fav_list()

    def save_favorites_to_current_file(self):
        """Favorileri o anda kullanılan JSON dosyasına yazar"""
        try:
            with open(self.current_favorites_file, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Hata", f"Favori dosyasına yazılamadı:\n{e}")


    def open_floating_copy(self):
        """Metni ayrı pencereye gönderir. Pencere zaten varsa, yeniden oluşturmaz."""
        content = self.result_text.get("1.0", "end-1c")

        # Eğer pencere daha önce açılmışsa, sadece içerik güncelle
        if hasattr(self, "floating_win") and self.floating_win.winfo_exists():
            self.copy_text_area.delete("1.0", tk.END)
            self.copy_text_area.insert("1.0", content)

            # önce seçim var mı kontrol et
            if self.result_text.tag_ranges("sel"):
                sel_start = self.result_text.index("sel.first")
                line_num = int(sel_start.split('.')[0])
            else:
                cursor_index = self.result_text.index("insert")
                line_num = int(cursor_index.split('.')[0])

            total_lines = int(self.copy_text_area.index("end-1c").split('.')[0])
            fraction = (line_num - 1) / max(total_lines, 1)
            self.copy_text_area.yview_moveto(fraction)

            # vurgulama
            self.copy_text_area.tag_delete("cursor_line")
            self.copy_text_area.tag_add("cursor_line", f"{line_num}.0", f"{line_num}.end")
            self.copy_text_area.tag_config("cursor_line", background="lightblue")

            self.floating_win.lift()
            return

        # Yeni pencere oluştur
        self.floating_win = tk.Toplevel(self.root)
        self.floating_win.title("Metin Kopyası")
        self.floating_win.geometry("700x700")

        if not hasattr(self, "copy_font_size"):
            self.copy_font_size = 30
        copy_font = tkfont.Font(family="Arial", size=self.copy_font_size)

        # Font artır/azalt fonksiyonları
        def inc_font(event=None):
            self.copy_font_size += 2
            copy_font.configure(size=self.copy_font_size)
            scale.set(self.copy_font_size)

        def dec_font(event=None):
            self.copy_font_size -= 1
            if self.copy_font_size < 6: 
                self.copy_font_size = 6
            copy_font.configure(size=self.copy_font_size)
            scale.set(self.copy_font_size)

        self.floating_win.bind("+", lambda e: inc_font())
        self.floating_win.bind("=", lambda e: inc_font())
        self.floating_win.bind("-", lambda e: dec_font())

        # Üstte scale
        scale = tk.Scale(self.floating_win, from_=8, to=30, orient="horizontal",
                        label="Yazı Boyutu", command=lambda val: copy_font.configure(size=int(val)))
        scale.set(self.copy_font_size)
        scale.pack(fill="x", pady=5)

        # Metin alanı + scrollbar
        frame = tk.Frame(self.floating_win)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.copy_text_area = tk.Text(frame, wrap="word", font=copy_font, yscrollcommand=scrollbar.set)
        self.copy_text_area.pack(fill="both", expand=True)
        scrollbar.config(command=self.copy_text_area.yview)

        # İlk içeriği yükle
        self.copy_text_area.insert("1.0", content)

        # önce seçim var mı kontrol et
        if self.result_text.tag_ranges("sel"):
            sel_start = self.result_text.index("sel.first")
            line_num = int(sel_start.split('.')[0])
        else:
            cursor_index = self.result_text.index("insert")
            line_num = int(cursor_index.split('.')[0])

        # satırı en üste al
        total_lines = int(self.copy_text_area.index("end-1c").split('.')[0])
        fraction = (line_num - 1) / max(total_lines, 1)
        self.copy_text_area.yview_moveto(fraction)

        # vurgulama
        self.copy_text_area.tag_delete("cursor_line")
        self.copy_text_area.tag_add("cursor_line", f"{line_num}.0", f"{line_num}.end")
        self.copy_text_area.tag_config("cursor_line", background="lightblue")


    def new_txt_toggle(self):
        """
        İlk basış → metin kutusunu temizler.
        Sonraki basış → metnin ilk satırını önerip dosya olarak kaydeder.
        """
        current_text = self.result_text.get("1.0", "end-1c").strip()

        # Eğer kutu boşsa, sadece temizleyip kullanıcıya yazması için bırak
        if current_text == "":
            self.result_text.delete("1.0", tk.END)
            messagebox.showinfo("Bilgi", "Yeni şarkı sözünü yaz ve bitirince yine bu butona bas.")
            return

        # Eğer kutuda yazı varsa → kaydetme moduna geç
        first_line = current_text.splitlines()[0] if current_text.splitlines() else "yeni_dosya"
        # Temiz dosya adı önerisi üretelim
        suggested_name = self.normalize(first_line).replace(" ", " ")[:30]

        answer = tk.simpledialog.askstring("Dosya Adı", "Kaydedilecek dosya adı (uzantısız):",
                                        initialvalue=suggested_name)
        if not answer:
            return

        if not answer.endswith(".txt"):
            filename = answer + ".txt"
        else:
            filename = answer

        full_path = os.path.join(self.folder_path, filename)
        if os.path.exists(full_path):
            messagebox.showerror("Hata", "Bu isimde bir dosya zaten var.")
            return

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(current_text)
            self.load_files()
            self.update_file_list()
            messagebox.showinfo("Başarılı", f"{filename} kaydedildi.")
            self.result_text.delete("1.0", tk.END)  # yeni satır için temizle
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi:\n{e}")

    def toggle_dark_mode(self):
        self.dark_mode_enabled = not self.dark_mode_enabled
        if self.dark_mode_enabled:
            self.copy_text_area.configure(bg="#2E2E2E", fg="#FFFFFF", insertbackground="white")
            self.dark_button.configure(text="☀️\nLight Mode")
        else:
            self.copy_text_area.configure(bg="white", fg="black", insertbackground="lightblue")
            self.dark_button.configure(text="🌙\nDark Mode")

    def open_floating_copy_sec(self, event=None):        
        """Metni ayrı pencereye gönderir. Pencere zaten varsa, yeniden oluşturmaz."""
        content = self.result_text.get(tk.SEL_FIRST, tk.SEL_LAST)

        # Eğer pencere daha önce açılmışsa, sadece içerik güncelle
        if hasattr(self, "floating_win") and self.floating_win.winfo_exists():
            self.copy_text_area.delete("1.0", tk.END)
            self.copy_text_area.insert("1.0", content)

            # önce seçim var mı kontrol et
            if self.result_text.tag_ranges("sel"):
                sel_start = self.result_text.index("sel.first")
                line_num = int(sel_start.split('.')[0])
            else:
                cursor_index = self.result_text.index("insert")
                line_num = int(cursor_index.split('.')[0])

            total_lines = int(self.copy_text_area.index("end-1c").split('.')[0])
            fraction = (line_num - 1) / max(total_lines, 1)
            self.copy_text_area.yview_moveto(fraction)

            # vurgulama
            self.copy_text_area.tag_delete("cursor_line")
            self.copy_text_area.tag_add("cursor_line", f"{line_num}.0", f"{line_num}.end")
            self.copy_text_area.tag_config("cursor_line", background="lightblue")

            self.floating_win.lift()
            return

        # Yeni pencere oluştur
        self.floating_win = tk.Toplevel(self.root)
        self.floating_win.title("Metin Kopyası")
        self.floating_win.geometry("700x700")

        if not hasattr(self, "copy_font_size"):
            self.copy_font_size = 30
        copy_font = tkfont.Font(family="Arial", size=self.copy_font_size)

        # Font artır/azalt fonksiyonları
        def inc_font(event=None):
            self.copy_font_size += 2
            copy_font.configure(size=self.copy_font_size)
            scale.set(self.copy_font_size)

        def dec_font(event=None):
            self.copy_font_size -= 1
            if self.copy_font_size < 6: 
                self.copy_font_size = 6
            copy_font.configure(size=self.copy_font_size)
            scale.set(self.copy_font_size)

        self.floating_win.bind("+", lambda e: inc_font())
        self.floating_win.bind("=", lambda e: inc_font())
        self.floating_win.bind("-", lambda e: dec_font())

        # Üstte scale
        scale = tk.Scale(self.floating_win, from_=8, to=30, orient="horizontal",
                        label="Yazı Boyutu", command=lambda val: copy_font.configure(size=int(val)))
        scale.set(self.copy_font_size)
        scale.pack(fill="x", pady=5)

        # Metin alanı + scrollbar
        frame = tk.Frame(self.floating_win)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.copy_text_area = tk.Text(frame, wrap="word", font=copy_font, yscrollcommand=scrollbar.set)
        self.copy_text_area.pack(fill="both", expand=True)
        scrollbar.config(command=self.copy_text_area.yview)

        # İlk içeriği yükle
        self.copy_text_area.insert("1.0", content)

        # önce seçim var mı kontrol et
        if self.result_text.tag_ranges("sel"):
            sel_start = self.result_text.index("sel.first")
            line_num = int(sel_start.split('.')[0])
        else:
            cursor_index = self.result_text.index("insert")
            line_num = int(cursor_index.split('.')[0])

        # satırı en üste al
        total_lines = int(self.copy_text_area.index("end-1c").split('.')[0])
        fraction = (line_num - 1) / max(total_lines, 1)
        self.copy_text_area.yview_moveto(fraction)

        # vurgulama
        self.copy_text_area.tag_delete("cursor_line")
        self.copy_text_area.tag_add("cursor_line", f"{line_num}.0", f"{line_num}.end")
        self.copy_text_area.tag_config("cursor_line", background="lightblue")

    

    def fazla_bosluklari_temizle(self):
        content = self.result_text.get("1.0", "end-1c")

        # Satır satır işle → strip + çoklu boşlukları sadeleştir
        lines = content.splitlines()
        cleaned_lines = [re.sub(r"[ \t]+", " ", line.strip()) for line in lines]

        cleaned = "\n".join(cleaned_lines)

        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", cleaned)


    def on_closing(self):
        
        if self.favorites:  # Favori varsa sorsun
            
            yanit = messagebox.askyesnocancel("Çıkış", "Favori listesini kaydetmek ister misiniz?\nFavori Listesi Üzerine Kaydet.")
            if yanit is None:
                return  # Cancel tuşuna basıldı, çıkış iptal
            elif yanit:
                self.save_favorites_as()
                self.save_favorites()

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsSearcherApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Çarpıya basınca
    root.mainloop()
# favorileri en önce aramaya dahil etti oldu.
#FAV işaretli en önde raıyor
#del eklendi, fav sil ot gülcelleme yapıldı
#ekran yansıtıldı, exe yaparken arkada siyah terminal oen çıkmaması için pyinstaller --onefile --windowed sozV40.py yap.
