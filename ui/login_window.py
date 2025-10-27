import customtkinter as ctk
from tkinter import messagebox
from models.user import User
from models.database import Database
from ui.register_window import RegisterWindow

class LoginWindow:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.db = Database(suppress_message=True)  # Evita mostrar mensaje de base cargada
        self.user_handler = User(self.db)

        self.root = ctk.CTk()
        self.root.title("Login System")
        self.root.geometry("450x420")
        self.root.resizable(False, False)

        # Frame
        frame = ctk.CTkFrame(self.root, corner_radius=15)
        frame.pack(pady=30, padx=30, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Inicio de Sesión", font=("Consolas", 28, "bold")).pack(pady=20)

        self.entry_email = ctk.CTkEntry(frame, placeholder_text="Correo Electronico", width=300)
        self.entry_email.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(frame, placeholder_text="Contraseña", show="*", width=300)
        self.entry_pass.pack(pady=10)

        btn_login = ctk.CTkButton(frame, text="Ingresar", width=200, command=self.login)
        btn_login.pack(pady=15)

        ctk.CTkLabel(frame, text="¿No tienes una cuenta?", font=("Segoe UI", 11)).pack(pady=5)
        btn_register = ctk.CTkButton(frame, text="Crear cuenta", width=200, fg_color="#16A085",
                                     hover_color="#1ABC9C", command=self.open_register)
        btn_register.pack(pady=5)

        self.role = None
        self.user_name = None

        self.login_successful = False  # Para controlar si login fue exitoso

    def login(self):
        email = self.entry_email.get()
        password = self.entry_pass.get()
        user = self.user_handler.login(email, password)
        if user:
            self.role = user[3]
            self.user_name = user[1]
            self.login_successful = True
            messagebox.showinfo("Ingreso", f"Bienvenido {self.user_name}.\nTu rol es: {self.role}")
            self.root.destroy()  # Cierra ventana login
        else:
            messagebox.showerror("Error", "Correo o Contraseña Incorrectos.")

    def open_register(self):
        self.root.withdraw()  # Oculta login
        reg = RegisterWindow(master=self.root)
        reg.run()
        self.root.deiconify()  # Muestra login nuevamente después de cerrar registro

    def run(self):
        self.root.mainloop()
        if self.login_successful:
            return self.role, self.user_name
        return None, None
