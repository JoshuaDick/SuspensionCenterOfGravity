import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import ctypes as ct
import platform

def dark_title_bar(window):
    if (platform.platform() == 'Windows'):
        window.update()
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, 20, ct.byref(value), 4)

def calculate():
    try:
        Front_Right = float(entry_FR.get())
        Front_Left = float(entry_FL.get())
        Rear_Right = float(entry_RR.get())
        Rear_Left = float(entry_RL.get())
        
        total_weight = Front_Right + Front_Left + Rear_Right + Rear_Left
        percentFront = (Front_Right + Front_Left) / total_weight * 100
        percentBack = (Rear_Right + Rear_Left) / total_weight * 100
        
        WB = float(entry_WB.get())
        Rf = float(entry_Rf.get())
        Rr = float(entry_Rr.get())
        theta = float(entry_theta.get())
        Wr = float(entry_Wr.get()) + float(entry_Wr2.get())

        a = percentFront * WB / 100
        h = (Wr - total_weight * (a / WB)) / (total_weight / WB * math.tan(theta * math.pi / 180)) + Wr * (Rr - Rf) / total_weight + Rf
        
        result_text = f'{percentFront:.2f}% Front\n{percentBack:.2f}% Back\n\n'
        result_text += f'{((Front_Right+Rear_Right)/total_weight)*100:.2f}% Right\n{((Front_Left+Rear_Left)/total_weight)*100:.2f}% Left\n\n'
        result_text += f'Center of Gravity: ({a:.2f} inches from front wheel, {h:.2f} inches from ground)'
        
        messagebox.showinfo("Results", result_text)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create the main window
root = tk.Tk()
root.title("Center of Gravity Calculator")
root.configure(bg='black')
dark_title_bar(root)

# Load and display the image
img = Image.open("car.png")  # Replace with your image path
img = img.resize((400, 100), Image.LANCZOS)  # Resize the image
photo = ImageTk.PhotoImage(img)

label_image = tk.Label(root, image=photo, bg='black')
label_image.pack(pady=(10, 0))  # Place the image at the top

# Create and place labels and entry fields
labels = [
    "Front Right Weight (LBS):", "Front Left Weight (LBS):",
    "Rear Right Weight (LBS):", "Rear Left Weight (LBS):",
    "Length from wheel center to wheel center (inches):",
    "Radius of front wheels (inches):", "Radius of rear wheels (inches):",
    "Elevation Angle (Degrees):", "Elevated Rear Left Weight (LBS):",
    "Elevated Rear Right Weight (LBS):"
]

entries = []
for text in labels:
    frame = tk.Frame(root, bg='black')  # Create a frame for each label-entry pair
    frame.pack(pady=5, fill=tk.X)  # Pack the frame and make it fill the width

    label = tk.Label(frame, text=text, bg='black', fg='white')
    label.pack(side=tk.LEFT)  # Pack the label to the left
    
    entry = tk.Entry(frame, bg='darkgrey', fg='black', width=20)  # Set a fixed width for the entry
    entry.pack(side=tk.RIGHT)  # Pack the entry to the right without expand and fill
    entries.append(entry)

# Assign entries to variables
entry_FR, entry_FL, entry_RR, entry_RL, entry_WB, entry_Rf, entry_Rr, entry_theta, entry_Wr, entry_Wr2 = entries

# Create a calculate button
calc_button = tk.Button(root, text="Calculate", command=calculate, bg='darkgrey', fg='black')
calc_button.pack(pady=10)

# Run the application
root.mainloop()
