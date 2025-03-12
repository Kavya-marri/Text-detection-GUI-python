import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import cv2
import os

# Configure pytesseract path if necessary
# Uncomment and set the path if Tesseract OCR is not in your PATH environment
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def select_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if file_path:
        try:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
            image_label.file_path = file_path
            output_text.delete(1.0, tk.END)  # Clear previous output
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

def detect_text():
    if hasattr(image_label, "file_path"):
        try:
            # Load image using OpenCV
            img_cv = cv2.imread(image_label.file_path)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

            # Perform text detection
            detected_text = pytesseract.image_to_string(img_rgb)

            # Display text in the output box
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, detected_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect text: {e}")
    else:
        messagebox.showwarning("Warning", "Please select an image first!")

# Create main GUI window
root = tk.Tk()
root.title("Text Detection GUI")
root.geometry("700x700")
root.resizable(False, False)

# UI components
title_label = tk.Label(root, text="Text Detection from Images", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

image_label = tk.Label(root, text="No Image Selected", width=50, height=20, bg="gray")
image_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

select_button = tk.Button(button_frame, text="Select Image", command=select_image, width=15)
select_button.grid(row=0, column=0, padx=5)

detect_button = tk.Button(button_frame, text="Detect Text", command=detect_text, width=15)
detect_button.grid(row=0, column=1, padx=5)

output_text = tk.Text(root, wrap=tk.WORD, height=15, width=80, font=("Arial", 12))
output_text.pack(pady=10)

# Run the application
root.mainloop()
