
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
import os

# Main application
root = tk.Tk()
root.title("Python Notepad")
root.geometry("800x550")
root.minsize(500, 350)

# Variables
current_file = None
dark_mode = False

# Text font
text_font = font.Font(family="Arial", size=12)

# Main text area
text_area = tk.Text(
    root,
    wrap="word",
    undo=True,
    font=text_font,
    padx=10,
    pady=10,
    borderwidth=0
)
text_area.pack(fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(text_area)
scrollbar.pack(side="right", fill="y")
scrollbar.config(command=text_area.yview)
text_area.config(yscrollcommand=scrollbar.set)


# Update window title
def update_title():
    name = os.path.basename(current_file) if current_file else "Untitled"
    root.title(f"{name} - Python Notepad")


# New File
def new_file():
    global current_file

    if not confirm_save():
        return

    text_area.delete("1.0", "end")
    current_file = None
    update_title()


# Open File
def open_file():
    global current_file

    if not confirm_save():
        return

    path = filedialog.askopenfilename(
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if path:
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            text_area.delete("1.0", "end")
            text_area.insert("1.0", content)

            current_file = path
            update_title()

        except (OSError, UnicodeError) as error:
            messagebox.showerror("Error", str(error))


# Save File
def save_file():
    global current_file

    if current_file is None:
        save_as()
        return

    try:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", "end-1c"))

        update_title()
        return True

    except OSError as error:
        messagebox.showerror("Error", str(error))
        return False


# Save As
def save_as():
    global current_file

    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if path:
        old_file = current_file
        current_file = path

        if save_file():
            return True

        current_file = old_file
        return False

    return False


# Confirm before discarding text
def confirm_save():
    if not text_area.edit_modified():
        return True

    answer = messagebox.askyesnocancel(
        "Unsaved Changes",
        "Do you want to save your changes?"
    )

    if answer is None:
        return False

    if answer:
        result = save_file()
        return result is True

    return True


# Cut, Copy, Paste
def cut_text():
    text_area.event_generate("<<Cut>>")


def copy_text():
    text_area.event_generate("<<Copy>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def select_all():
    text_area.tag_add("sel", "1.0", "end-1c")
    return "break"


# Find Text
def find_text():
    word = simpledialog.askstring("Find", "Enter text to find:")

    if not word:
        return

    text_area.tag_remove("found", "1.0", "end")

    start = "1.0"
    count = 0

    while True:
        position = text_area.search(
            word, start, stopindex="end", nocase=True
        )

        if not position:
            break

        end = f"{position}+{len(word)}c"
        text_area.tag_add("found", position, end)

        start = end
        count += 1

    text_area.tag_config(
        "found",
        background="yellow",
        foreground="black"
    )

    if count == 0:
        messagebox.showinfo("Find", "Text not found.")
    else:
        messagebox.showinfo("Find", f"Found {count} match(es).")


# Change Font Size
def change_font_size():
    size = simpledialog.askinteger(
        "Font Size",
        "Enter font size (8-40):",
        minvalue=8,
        maxvalue=40
    )

    if size:
        text_font.configure(size=size)


# Word Count
def word_count():
    content = text_area.get("1.0", "end-1c")

    words = len(content.split())
    characters = len(content)
    lines = int(text_area.index("end-1c").split(".")[0])

    messagebox.showinfo(
        "Document Statistics",
        f"Words: {words}\n"
        f"Characters: {characters}\n"
        f"Lines: {lines}"
    )


# Dark Mode
def toggle_dark_mode():
    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:
        text_area.config(
            bg="#1e1e1e",
            fg="white",
            insertbackground="white"
        )
        root.config(bg="#333333")
    else:
        text_area.config(
            bg="white",
            fg="black",
            insertbackground="black"
        )
        root.config(bg="SystemButtonFace")


# Word Wrap
def toggle_wrap():
    if text_area.cget("wrap") == "word":
        text_area.config(wrap="none")
    else:
        text_area.config(wrap="word")


# Exit Application
def exit_app():
    if confirm_save():
        root.destroy()


# Menu Bar
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)

file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_as)

file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)

edit_menu.add_command(label="Undo", command=lambda: text_area.event_generate("<<Undo>>"))
edit_menu.add_command(label="Redo", command=lambda: text_area.event_generate("<<Redo>>"))

edit_menu.add_separator()

edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_command(label="Select All", command=select_all)
edit_menu.add_command(label="Find", command=find_text)

menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Format Menu
format_menu = tk.Menu(menu_bar, tearoff=0)

format_menu.add_command(label="Font Size", command=change_font_size)
format_menu.add_command(label="Word Wrap", command=toggle_wrap)
format_menu.add_command(label="Dark Mode", command=toggle_dark_mode)

menu_bar.add_cascade(label="Format", menu=format_menu)

# Tools Menu
tools_menu = tk.Menu(menu_bar, tearoff=0)
tools_menu.add_command(label="Word Count", command=word_count)

menu_bar.add_cascade(label="Tools", menu=tools_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)

help_menu.add_command(
    label="About",
    command=lambda: messagebox.showinfo(
        "About",
        "Python Notepad\nDeveloped using Python and Tkinter."
    )
)

menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Keyboard Shortcuts
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-f>", lambda event: find_text())
root.bind("<Control-a>", lambda event: select_all())

# Track modifications
text_area.edit_modified(False)
text_area.bind(
    "<<Modified>>",
    lambda event: text_area.edit_modified(False)
)

# Closing event
root.protocol("WM_DELETE_WINDOW", exit_app)

# Start application
update_title()
root.mainloop()
