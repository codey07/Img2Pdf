import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import subprocess

# Make sure to install windnd: pip install windnd
import windnd  

last_dir = os.path.expanduser("~")
jpeg_list = []

# ---------------- Helper Functions ----------------
def open_folder_with_files(file_paths):
    """Open folder containing files and select them (Windows only)"""
    for file_path in file_paths:
        subprocess.run(["explorer", "/select,", file_path])

def add_jpegs(files):
    """Add JPEG files from selection or drag-and-drop"""
    global jpeg_list
    for file_path in files:
        if isinstance(file_path, bytes):
            file_path = file_path.decode('utf-8')
        if file_path.lower().endswith((".jpg", ".jpeg")) and file_path not in jpeg_list:
            jpeg_list.append(file_path)
            listbox.insert(tk.END, os.path.basename(file_path))

def select_jpegs():
    global last_dir
    files = filedialog.askopenfilenames(
        initialdir=last_dir,
        filetypes=[("JPEG files", "*.jpg;*.jpeg")],
        title="Select JPEG files"
    )
    if files:
        last_dir = os.path.dirname(files[0])
        add_jpegs(files)

def convert_all():
    global jpeg_list, last_dir
    if not jpeg_list:
        messagebox.showwarning("No JPEGs", "No JPEG files in the list to convert!")
        return

    last_dir = os.path.dirname(jpeg_list[0])
    new_pdfs = []

    for file_path in jpeg_list:
        try:
            image = Image.open(file_path)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(last_dir, base_name + ".pdf")
            image.save(output_path, "PDF", resolution=100.0)
            new_pdfs.append(output_path)
        except Exception as e:
            print(f"Error converting {file_path}: {e}")

    if new_pdfs:
        open_folder_with_files(new_pdfs)
        messagebox.showinfo("Conversion Complete", f"Converted {len(new_pdfs)} JPEGs to PDFs!")

def remove_selected():
    global jpeg_list
    selected_indices = listbox.curselection()
    for i in reversed(selected_indices):
        listbox.delete(i)
        del jpeg_list[i]

def clear_list():
    global jpeg_list
    listbox.delete(0, tk.END)
    jpeg_list.clear()

# ---------------- Tkinter UI ----------------
root = tk.Tk()
root.title("JPEG to PDF Converter")
root.geometry("600x450")

# Listbox
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 12))
listbox.pack(fill="both", expand=True, padx=20, pady=(10, 0))

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Convert All to PDFs", command=convert_all, font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove Selected", command=remove_selected, font=("Arial", 12)).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Clear List", command=clear_list, font=("Arial", 12)).grid(row=0, column=2, padx=5)

# Menu
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Select JPEG(s)", command=select_jpegs)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# ---------------- Windnd Drag & Drop ----------------
windnd.hook_dropfiles(listbox, func=add_jpegs)

root.mainloop()
