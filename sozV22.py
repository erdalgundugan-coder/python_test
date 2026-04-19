import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
import unicodedata
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog

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
        self.root.title("Şarkı Sözü Arama-----Erdal GÜNDOĞAN")
        self.root.geometry("1200x700")

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

        tk.Button(folder_frame, text="Klasör Seç", command=self.select_folder).pack(side="left")
        self.file_count_label = tk.Label(folder_frame, text="Dosya: 0")
        self.file_count_label.pack(side="left", padx=10)

        search_frame = tk.Frame(top_frame)
        search_frame.pack(side="left", padx=5)

        #self.entry = tk.Entry(search_frame, width=50, font=self.font_textbox)
        self.entry = tk.Entry(search_frame, width=50, font=self.font_listbox)
        
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.search_in_all_files())

        tk.Button(search_frame, text="Ara", command=self.search_in_all_files).pack(side="left", padx=(0, 10))
        tk.Button(search_frame, text="Kaydet", command=self.save_file).pack(side="left")

        main_pane = tk.PanedWindow(self.root, orient="horizontal", sashrelief=tk.RAISED, sashwidth=5, showhandle=True)
        main_pane.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_pane)
        center_pane = tk.PanedWindow(main_pane, orient="vertical", sashrelief=tk.RAISED, sashwidth=5)
        right_frame = tk.Frame(main_pane)

        main_pane.add(left_frame, stretch="always")
        main_pane.add(center_pane, stretch="always")
        main_pane.add(right_frame, stretch="always")

        # Sol: Dosyalar ve arama sonucu dosyalar
        self.search_files_label = tk.Label(left_frame, text="Arama Sonucu Dosyaları:", font=self.font_listbox)
        self.search_files_label.grid(row=0, column=0, sticky="w")

        self.search_files_listbox = tk.Listbox(left_frame, height=5, font=self.font_listbox)
        self.search_files_listbox.grid(row=1, column=0, sticky="ew")
        self.search_files_listbox.bind("<<ListboxSelect>>", self.on_search_file_select)

        left_frame.grid_rowconfigure(2, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(left_frame, width=40, font=self.font_listbox)
        self.file_listbox.grid(row=2, column=0, sticky="nsew")
        scrollbar_files = tk.Scrollbar(left_frame, command=self.file_listbox.yview)
        scrollbar_files.grid(row=2, column=1, sticky="ns")
        self.file_listbox.config(yscrollcommand=scrollbar_files.set)
        self.file_listbox.bind("<<ListboxSelect>>", self.display_file_content)

        # Ortadaki paned: Üst: Arama sonuçları, Alt: Favoriler (aralarında kaydırılabilir)
        center_frame_top = tk.Frame(center_pane)
        center_frame_bottom = tk.Frame(center_pane)

        center_pane.add(center_frame_top, stretch="always")
        center_pane.add(center_frame_bottom, stretch="always")

        center_frame_top.grid_rowconfigure(1, weight=1)
        center_frame_top.grid_columnconfigure(0, weight=1)

        result_label = tk.Label(center_frame_top, text="Arama Sonuçları:", font=self.font_listbox)
        result_label.grid(row=0, column=0, sticky="w")

        self.result_listbox = tk.Listbox(center_frame_top, font=self.font_listbox, exportselection=False)
        self.result_listbox.grid(row=1, column=0, sticky="nsew")
        scrollbar_results = tk.Scrollbar(center_frame_top, command=self.result_listbox.yview)
        scrollbar_results.grid(row=1, column=1, sticky="ns")
        self.result_listbox.config(yscrollcommand=scrollbar_results.set)
        self.result_listbox.bind("<<ListboxSelect>>", self.show_line_file_content)

        btn_frame = tk.Frame(center_frame_top)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=5)

        self.btn_add_fav = tk.Button(btn_frame, text="Favorilere Ekle", command=self.add_selected_result_to_favorites)
        self.btn_add_fav.pack(side="left", padx=5)

        self.btn_remove_fav = tk.Button(btn_frame, text="Favoriden Çıkar", command=self.remove_selected_favorite)
        self.btn_remove_fav.pack(side="left", padx=5)

        self.btn_add_cursor_fav = tk.Button(btn_frame, text="İmleç Satırı Favori", command=self.add_current_line_to_favorites)
        self.btn_add_cursor_fav.pack(side="left", padx=5)


        center_frame_bottom.grid_rowconfigure(1, weight=1)
        center_frame_bottom.grid_columnconfigure(0, weight=1)

        
        self.fav_label = tk.Label(center_frame_bottom, text="Favoriler:", font=self.font_listbox)
        self.fav_label.grid(row=0, column=0, sticky="w")



        self.fav_listbox = tk.Listbox(center_frame_bottom, font=self.font_listbox, exportselection=False)
        self.fav_listbox.grid(row=1, column=0, sticky="nsew")
        scrollbar_fav = tk.Scrollbar(center_frame_bottom, command=self.fav_listbox.yview)
        scrollbar_fav.grid(row=1, column=1, sticky="ns")
        self.fav_listbox.config(yscrollcommand=scrollbar_fav.set)
        self.fav_listbox.bind("<<ListboxSelect>>", self.show_favorite_content)

        fav_btn_frame = tk.Frame(center_frame_bottom)
        fav_btn_frame.grid(row=2, column=0, sticky="ew", pady=5)

        tk.Button(fav_btn_frame, text="Favorileri Kaydet", command=self.save_favorites).pack(side="left", padx=5)
        tk.Button(fav_btn_frame, text="Favorileri Yükle", command=self.load_favorites).pack(side="left", padx=5)
        tk.Button(fav_btn_frame, text="Farklı Kaydet", command=self.save_favorites_as).pack(side="left", padx=5)   
        tk.Button(fav_btn_frame, text="Boş Favori Dosyası Oluştur", command=self.create_empty_favorites_file).pack(side="left", padx=5)
        



        # Sağdaki metin ve satır navigasyonu
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        line_nav_frame = tk.Frame(self.root)
        line_nav_frame.pack(fill="x", pady=2)

        tk.Label(line_nav_frame, text="Satır No:").pack(side="left")

        self.line_entry = tk.Entry(line_nav_frame, width=5)
        self.line_entry.pack(side="left", padx=5)
        self.line_entry.bind("<Return>", self.goto_line)

        tk.Button(line_nav_frame, text="Git", command=self.goto_line).pack(side="left")

        self.result_text = tk.Text(right_frame, wrap="word", font=self.font_textbox)
        self.result_text.grid(row=0, column=0, sticky="nsew")
        scrollbar_text = tk.Scrollbar(right_frame, command=self.result_text.yview)
        scrollbar_text.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar_text.set)

        self.cursor_line_label = tk.Label(right_frame, text="Satır No: -", font=self.font_listbox)
        self.cursor_line_label.grid(row=1, column=0, sticky="w", pady=2)

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
        self.load_files()
        self.update_file_list()

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
        self.file_count_label.config(text=f"Dosya: {len(self.file_contents)}")

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        #for filename in sorted(self.file_contents.keys()):
        for filename in sorted(self.file_contents.keys(), key=lambda x: x.lower()):

            self.file_listbox.insert(tk.END, filename)

    def normalize(self, text):
        text = text.casefold()
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        return text

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

        for filename, lines in self.file_contents.items():
            for lineno, line in enumerate(lines):
                norm_line = self.normalize(line)
                line_words = norm_line.split()

                if all(any(word.startswith(k) for word in line_words) for k in keywords):
                    display_line = f":{lineno}:{line.strip()}:...............................................................{filename}"
                    self.result_listbox.insert(tk.END, display_line)
                    self.search_results.append((filename, lineno, line.strip()))

        if not self.search_results:
            self.result_listbox.delete(0, tk.END)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Aranan kelime bulunamadı.")

        found_files = set(filename for filename, _, _ in self.search_results)
        self.search_files_listbox.delete(0, tk.END)
        #for f in sorted(found_files):
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

    def highlight_text_in_result(self, filename, highlight_line_no=None):
        self.result_text.delete("1.0", tk.END)

        # Tag temizliği
        for i in range(len(self.highlight_colors)):
            self.result_text.tag_delete(f"highlight{i}")
        self.result_text.tag_delete("highlight_line")

        # Tag ayarları
        self.result_text.tag_configure("highlight_line", background="lightyellow")
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
                display = f"{fav['file']}:{fav['line']} {fav['text']}"
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
            display = f"{fav['file']}:{fav['line']} {fav['text']}"
            
            filtered_favs.append(display)

        try:
            fav_index = filtered_favs.index(line_text)
        except ValueError:
            return

        if messagebox.askyesno("Onay", "Favoriden çıkarmak istediğinize emin misiniz?"):
            del self.favorites[fav_index]
            self.save_favorites()
            self.update_fav_list()

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
            display = f"{fav['file']}:{fav['line']} {fav['text']}"
            
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


    def save_favorites(self):
        """favorileri varsayılan favorites.json dosyasına kaydeder"""
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Bilgi", "Favoriler kaydedildi.")
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
        self.fav_label.config(text=f"Favoriler: ({file_name})")


    def create_empty_favorites_file(self):
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            self.favorites = []
            self.update_fav_list()
            messagebox.showinfo("Bilgi", f"Boş favori dosyası oluşturuldu:\n{FAVORITES_FILE}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya oluşturulamadı: {e}")





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
            messagebox.showinfo("Bilgi", "Bu favori zaten mevcut.")
            return

        self.favorites.append(fav_item)
        self.save_favorites()
        self.update_fav_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsSearcherApp(root)
    root.mainloop()
