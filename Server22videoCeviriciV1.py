import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

VIDEO_EXTS = (".mp4", ".mov", ".avi", ".webm", ".mkv")

# --- FFmpeg yolu ---
FFMPEG_PATH = r"D:\sozler ve videolar materyal\ffmpeg-8.0\bin\ffmpeg.exe"

def convert_all_videos(log_widget):
    # Kaynak klasör
    src_dir = filedialog.askdirectory(title="Kaynak Klasörü Seç (Videolar)")
    if not src_dir:
        return

    # Hedef klasör
    dst_dir = filedialog.askdirectory(title="Hedef Klasörü Seç (Dönüştürülen Videolar)")
    if not dst_dir:
        return

    # Videoları tara
    videos = [f for f in os.listdir(src_dir) if f.lower().endswith(VIDEO_EXTS)]
    if not videos:
        messagebox.showinfo("Bilgi", "Seçilen klasörde video bulunamadı!")
        return

    log_widget.insert(tk.END, f"{len(videos)} video bulundu. Dönüştürülüyor...\n")
    log_widget.see(tk.END)

    for v in videos:
        input_path = os.path.abspath(os.path.join(src_dir, v))
        name, _ = os.path.splitext(v)
        output_path = os.path.abspath(os.path.join(dst_dir, f"{name}_converted.mp4"))

        try:
            cmd = [
                FFMPEG_PATH, "-y", "-i", input_path,
                "-vcodec", "libx264", "-crf", "23", "-preset", "fast",
                "-acodec", "aac", output_path
            ]
            subprocess.run(cmd, check=True)
            log_widget.insert(tk.END, f"Dönüştürüldü: {output_path}\n")
            log_widget.see(tk.END)
        except subprocess.CalledProcessError as e:
            log_widget.insert(tk.END, f"Hata (ffmpeg): {v} - {e}\n")
            log_widget.see(tk.END)
        except Exception as e:
            log_widget.insert(tk.END, f"Hata: {v} - {e}\n")
            log_widget.see(tk.END)

    messagebox.showinfo("Tamamlandı", f"Tüm videolar dönüştürüldü!\nHedef klasör: {dst_dir}")


# --- Tkinter Form ---
root = tk.Tk()
root.title("Kamp Keyfi - Tüm Videoları Dönüştür")
root.geometry("700x450")

btn_convert = tk.Button(
    root,
    text="Tüm Videoları Dönüştür",
    bg="#2563eb",
    fg="white",
    font=("Arial", 14),
    command=lambda: convert_all_videos(log_text)
)
btn_convert.pack(pady=10)

log_text = scrolledtext.ScrolledText(root, height=20, state=tk.NORMAL)
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
