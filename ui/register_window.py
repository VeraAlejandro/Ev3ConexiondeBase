import customtkinter as ctk
from tkinter import messagebox
from models.user import User
from models.database import Database

class RegisterWindow:
    def __init__(self, master=None):
        self.master = master  # Guardamos la ventana de login
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.db = Database()
        self.user_handler = User(self.db)

        # Si se llama desde login, master es la ventana principal
        self.root = ctk.CTkToplevel(master) if master else ctk.CTk()
        self.root.title("Registro de Usuario")
        self.root.geometry("420x450")
        self.root.resizable(False, False)

        # Título
        ctk.CTkLabel(self.root, text="Registro de Nuevo Usuario", font=("Consolas", 18, "bold")).pack(pady=15)

        # Entradas
        self.entry_name = ctk.CTkEntry(self.root, placeholder_text="Nombre Completo", width=300)
        self.entry_name.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self.root, placeholder_text="Correo Electrónico", width=300)
        self.entry_email.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self.root, placeholder_text="Contraseña", width=300)
        self.entry_pass.pack(pady=10)

        # Combo box para tipo de usuario
        self.combo_type = ctk.CTkComboBox(self.root, values=["Administrador", "Empleado", "Cliente"], width=300)
        self.combo_type.set("Cliente")
        self.combo_type.pack(pady=10)

        # Botón registrar
        ctk.CTkButton(self.root, text="Registrar", width=200, command=self.register_user).pack(pady=20)

    def register_user(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_pass.get()
        type_str = self.combo_type.get()

        type_map = {"Administrador": 1, "Empleado": 2, "Cliente": 3}
        type_user = type_map.get(type_str, 3)

        try:
            self.user_handler.register(name, email, password, type_user)
            messagebox.showinfo("Éxito", f"Usuario {name} registrado como {type_str}")
            self.root.destroy()  # Cierra la ventana de registro
            if self.master:      # Si se pasó master, lo mostramos de nuevo
                self.master.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {str(e)}")

    def run(self):
        self.root.mainloop()
