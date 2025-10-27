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
    reg = ctk.CTkToplevel(root)
    reg.title("Registro de Usuario")
    reg.geometry("420x450")
    reg.resizable(False,False)

    ctk.CTkLabel(reg, text="Registro de Nuevo Usuario", font=("Consolas", 18, "bold")).pack(pady=15)

    entry_name = ctk.CTkEntry(reg, placeholder_text="Nombre Completo", width=300)
    entry_name.pack(pady=10)

    entry_email = ctk.CTkEntry(reg, placeholder_text="Correo Electronico", width=300)
    entry_email.pack(pady=10)

    entry_pass = ctk.CTkEntry(reg, placeholder_text="Contraseña", width=300)
    entry_pass.pack(pady=10)

    combo_type = ctk.CTkComboBox(reg, values=["Administrador", "Empleado", "Cliente"], width=300)
    combo_type.set("Cliente")#por default cliente
    combo_type.pack(pady=10)

    def register_user():
        #con metodo get obtenemos el valor del objeto 
        name = entry_name.get()
        email = entry_email.get()
        password = entry_pass.get()
        type_str = combo_type.get()#obtenemos el valor del combobox
        type_map = {"Administrador": 1, "Empleado": 2, "Cliente": 3}#diccionario para validar el tipo de usuario 
        type_user = type_map.get(type_str, 3)#si ocurre un error que por defecto sea cliente 
        user_handler.register(name, email, password, type_user)#envio de parametros hacia la clase register
        messagebox.showinfo("Exito", f"Usuario {name} registrado como {type_str}")
        reg.destroy()

    btn_register = ctk.CTkButton(reg, text = "Registrar", command=register_user, width=200)
    btn_register.pack(pady=20)

#Interfaz de Login 
frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(pady=30, padx=30, fill="both", expand=True)

ctk.CTkLabel(frame, text="Inicio de Sesión", font=("Consolas", 28, "bold")).pack(pady=20)

entry_email = ctk.CTkEntry(frame, placeholder_text="Correo Electronico", width=300)
entry_email.pack(pady=10)

entry_pass = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", width=300)
entry_pass.pack(pady=10)

btn_Login = ctk.CTkButton(frame, text="Ingresar", width=200, command=login)
btn_Login.pack(pady=15)

ctk.CTkLabel(frame, text="¿No tienes una cuenta?", font=("Segoe UI", 11)).pack(pady=5)
btn_register = ctk.CTkButton(frame, text="Crear cuenta", width=200, fg_color="#16A085", hover_color="#1ABC9C", command=open_register)
btn_register.pack(pady=5)

root.mainloop()
