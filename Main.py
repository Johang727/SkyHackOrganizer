#!/usr/bin/env python3

import tkinter as tk
import os, hashlib, subprocess, re
from tkinter import filedialog, messagebox

HACKS_DIR:str = "./hacks"
BASE_DIR:str = "./base"
PATCHED_DIR:str = "./patched"

US_CLEAN_HASH:str = "10af6a1a4d90ffb48bfb6c444324f7fd"
EU_CLEAN_HASH:str = "6735749e060e002efd88e61560e45567"

def select_clean_rom() -> None:
    directory = filedialog.askdirectory()
    if directory:
        auto_detect_roms()

def apply_patch() -> None:
    if not us_rom_path and not eu_rom_path:
        messagebox.showerror("Error", "Please select at least one clean base ROM first!")
        return
    
    subprocess.run(["xdelta3"]) # finish this command later

    messagebox.showinfo("Success", "This is where the magic happens. ROM Patched!")

def auto_detect_roms() -> None:
    global us_rom_path, eu_rom_path

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        messagebox.showwarning("Warning", "A base directory has been created in this folder, please place your base .nds files here!")
    else:
        # auto detect the base roms
        try:
            files:list[str] = [f for f in os.listdir(BASE_DIR) if f.endswith('.nds')]
            
            if not files:
                messagebox.showwarning("Warning", "Could not find any .nds files in ./base")

            for file in files:
                # check here for files
                file_path:str = f"./base/{file}"

                with open(file_path, "rb") as f:
                    digest = hashlib.file_digest(f, "md5")
                    md5_hash = digest.hexdigest()

                if US_CLEAN_HASH == md5_hash:
                    us_rom_path = file_path
                    us_label.config(text=f"US ROM: {file}")
                if EU_CLEAN_HASH == md5_hash:
                    eu_rom_path = file_path
                    eu_label.config(text=f"EU ROM: {file}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not read ./base folder: {e}")


# Create the main window
root = tk.Tk()
root.title("EoS Hack Manager")
root.geometry("500x500")

# Initialize global variables to store the paths
us_rom_path:str = ""
eu_rom_path:str = ""


# region init
region = tk.StringVar()
region.set("US")



browse_button = tk.Button(root, text="Select CLEAN ROMs folder.", command=select_clean_rom)
browse_button.pack(pady=(20, 2))

us_label = tk.Label(root, text="No US ROM selected", fg="gray")
us_label.pack(pady=(0, 0))

eu_label = tk.Label(root, text="No EU ROM selected", fg="gray")
eu_label.pack(pady=(0, 20))

auto_detect_roms()

def refresh_hack_list():
    """Scans the hacks/ folder and populates the Listbox."""

    if not os.path.exists(HACKS_DIR):
        os.makedirs(HACKS_DIR)
    if not os.path.exists(PATCHED_DIR):
        os.makedirs(PATCHED_DIR)

    hack_listbox.delete(0, tk.END)

    # Populate already patched files
    try:
        files = [f for f in os.listdir(PATCHED_DIR) if f.endswith('.nds')]

        for file in files:
            hack_listbox.insert(tk.END, f" ✅ {file}")

    except Exception as e:
        messagebox.showerror("Error", f"Could not read patched folder: {e}")

    # List all files ending in .xdelta
    try:
        files = [f for f in os.listdir(HACKS_DIR) if f.endswith('.xdelta')]
        
        if not files:
            hack_listbox.insert(tk.END, " No .xdelta files found in /hacks")
            return

        for file in files:
            hack_listbox.insert(tk.END, f" 📄 {file}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not read hacks folder: {e}")


def get_selected_hack():
    """Gets the file name currently highlighted by the user."""
    try:
        selected_index = hack_listbox.curselection()[0]
        selected_text = hack_listbox.get(selected_index)
        
        # Clean up the emoji prefix to get the raw filename
        filename = selected_text.replace(" 📄 ", "")
        
        if re.match(".*nds", filename):
            messagebox.showinfo("Info", f"Launching MelonDS!")
        else:
            messagebox.showinfo("Info", f"Launching xdelta!")

    except IndexError:
        messagebox.showwarning("Warning", "Please select a hack from the list first.")

# Label for the list

region_switcher = tk.Frame(root)
region_switcher.pack(side="right", padx=(0, 20))


us_btn = tk.Radiobutton(region_switcher, text="US", variable=region, value="US")
us_btn.pack(side="top")
eu_btn = tk.Radiobutton(region_switcher, text="EU", variable=region, value="EU")
eu_btn.pack(side="top")

list_label = tk.Label(root, text="Available Patches in /hacks:", font=("Arial", 10, "bold"))
list_label.pack(pady=(10, 2), anchor="w", padx=10)

# We use a sub-frame to bundle the listbox and scrollbar tightly together
list_frame = tk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

# Create Scrollbar
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create Listbox and link it to Scrollbar
# exportselection=False prevents losing selection when clicking other elements
hack_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Courier", 10), exportselection=False)
hack_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure scrollbar to scroll the listbox
scrollbar.config(command=hack_listbox.yview)

# Button to check selection
select_button = tk.Button(root, text="Play Hack", command=get_selected_hack)
select_button.pack(pady=10)

# Run the scan automatically when the app opens
refresh_hack_list()

root.mainloop()
