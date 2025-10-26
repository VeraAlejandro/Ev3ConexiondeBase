import customtkinter as ctk
from tkinter import messagebox
from models.database import Database
from models.user import User

#configuracion base 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#inicializar la base 
db = Database()
user_handler = User(db)

#ventana principal 
root = ctk.CTk()
root.title("Sistema de Ingreso")
root.geometry("450x420")
root.resizable(False,False)

#metodos
def login():
    email = entry_email.get()
    password = entry_pass.get()
    user = user_handler.login(email, password)
    if user:
        messagebox.showinfo("Ingreso", f"Bienvenido {user[1]}.\nTu rol es: {user[3]}")
    else:
        messagebox.showinfo("Error", "Correo o Contraseña Incorrectos.")

def open_register():
    reg = ctk.CTkTopLevel(root)
    reg.tittle("Registro de Usuario")
    reg.geometry("420x450")
    reg.resizable(False,False)

    ctk.CTkLabel(reg, text="Registro de Nuevo Usuario", font=("Consolas", 18, "bold")).pack(pady=15)

    entry_name = ctk.CTkEntry(reg, placeholder_text="Nombre Completo", width=300)
    entry_name.pack(pady=10)

