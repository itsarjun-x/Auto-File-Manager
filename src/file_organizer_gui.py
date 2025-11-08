import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sys
import os

EXT_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Video": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".rar"]
}

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        
        # Set window icon
        try:
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'Logo.ico')
            else:
                icon_path = 'Logo.ico'
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="📁 File Organizer", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle = ttk.Label(main_frame, text="Automatically organize your files into categorized folders", 
                           foreground="gray")
        subtitle.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # File types info
        info_frame = ttk.LabelFrame(main_frame, text="Supported File Types", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        types_text = (
            "🖼️ Images: .jpg, .jpeg, .png, .gif, .bmp\n"
            "📄 Documents: .pdf, .docx, .doc, .txt, .pptx\n"
            "🎵 Audio: .mp3, .wav, .flac\n"
            "🎬 Video: .mp4, .mov, .avi\n"
            "📦 Archives: .zip, .tar, .gz, .rar\n"
            "📂 Others: All other file types"
        )
        types_label = ttk.Label(info_frame, text=types_text, justify=tk.LEFT)
        types_label.grid(row=0, column=0)
        
        # Path selection
        path_label = ttk.Label(main_frame, text="Folder Path:")
        path_label.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=40)
        path_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 10))
        
        browse_btn = ttk.Button(main_frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=3, column=2, pady=(0, 10))
        
        # Organize button
        organize_btn = ttk.Button(main_frame, text="🚀 Organize Files", command=self.organize_files)
        organize_btn.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to organize files")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=5, column=0, columnspan=3)
        
        # Configure column weights
        main_frame.columnconfigure(1, weight=1)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if folder:
            self.path_var.set(folder)
    
    def organize_files(self):
        folder_path = self.path_var.get().strip()
        
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder path")
            return
        
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            messagebox.showerror("Error", "Invalid folder path")
            return
        
        try:
            file_count = 0
            for p in folder.iterdir():
                if p.is_dir():
                    continue
                
                ext = p.suffix.lower()
                moved = False
                
                for foldername, exts in EXT_MAP.items():
                    if ext in exts:
                        dest = folder / foldername
                        dest.mkdir(exist_ok=True)
                        shutil.move(str(p), str(dest / p.name))
                        moved = True
                        file_count += 1
                        break
                
                if not moved:
                    other = folder / "Others"
                    other.mkdir(exist_ok=True)
                    shutil.move(str(p), str(other / p.name))
                    file_count += 1
            
            self.status_var.set(f"✅ Success! Organized {file_count} files")
            messagebox.showinfo("Success", 
                              f"Organization complete!\n\n{file_count} files organized into folders:\n"
                              "Images, Documents, Audio, Video, Archives, and Others")
        
        except Exception as e:
            self.status_var.set("❌ Error occurred")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()