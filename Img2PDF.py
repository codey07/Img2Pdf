import tkinter as tk
from tkinter import filedialog
from PIL import Image

def convert():
    file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if not file_path:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return
    image = Image.open(file_path)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(output_path, "PDF", resolution=100.0)
    print(f"Saved PDF: {output_path}")

root = tk.Tk()
root.title("JPEG to PDF Converter")

# Make the window bigger
root.geometry("500x300")  # width x height

# Center the button and make it larger
button = tk.Button(root, text="Select JPEG and Convert", command=convert, padx=40, pady=20)
button.pack(pady=80, expand=True)

root.mainloop()
