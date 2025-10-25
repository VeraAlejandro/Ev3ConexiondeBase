import tkinter as tk 
from tkinter import messagebox, ttk 
from models.database import Database
from models.user import User 


db = Database()
user_handler = User(db)

root = tk.Tk()
root.title("Bienvenido a Reservaciones AVV")
root.geometry("300x250")

def login():
    email = entry_email.get()
    password = entry_pass.get()
    user = user_handler.login(email,password)
    if user:
        messagebox.showinfo("Login", f"Welcome, {user[1]}! Your role is {user[3]}")
    else:
        messagebox.showerror("Login", "Invalid email or password.")
