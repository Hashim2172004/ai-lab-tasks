import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")

tasks = []

# Functions
def add_task():
    task = entry.get()
    if task != "":
        tasks.append(task)
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_task():
    try:
        selected = listbox.curselection()[0]
        listbox.delete(selected)
        tasks.pop(selected)
    except:
        messagebox.showwarning("Warning", "Please select a task to delete!")

def clear_tasks():
    listbox.delete(0, tk.END)
    tasks.clear()

# UI Elements
title = tk.Label(root, text="My To-Do List", font=("Arial", 18))
title.pack(pady=10)

entry = tk.Entry(root, width=25, font=("Arial", 14))
entry.pack(pady=10)

add_btn = tk.Button(root, text="Add Task", width=15, command=add_task)
add_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", width=15, command=delete_task)
delete_btn.pack(pady=5)

clear_btn = tk.Button(root, text="Clear All", width=15, command=clear_tasks)
clear_btn.pack(pady=5)

listbox = tk.Listbox(root, width=35, height=10, font=("Arial", 12))
listbox.pack(pady=20)

root.mainloop()