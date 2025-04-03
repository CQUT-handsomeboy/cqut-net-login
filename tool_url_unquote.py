"""
该工具用于将URL解码
"""

from urllib.parse import unquote


def parse(raw):
    return unquote(raw)


import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("URL解码")

text_box = tk.Text(root, height=20, width=100, wrap="word")
text_box.pack(padx=10, pady=10)


def command():
    content = text_box.get("1.0", tk.END)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, parse(content))


submit_button = ttk.Button(root, text="URL解码", command=command)
submit_button.pack(padx=10, pady=10)

root.mainloop()
