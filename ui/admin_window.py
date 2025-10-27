from models.database import Database
from models.user import User
import customtkinter as ctk
from tkinter import ttk, messagebox

class AdminWindow:
    def __init__(self, user_name):
        self.user_name = user_name

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Base de datos y handler de usuarios
        self.db = Database(suppress_message=True)
        self.user_handler = User(self.db)

        self.root = ctk.CTk()
        self.root.title("Panel de Administrador")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self.root, height=60, corner_radius=0, fg_color="#1A5276")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"Panel de Administrador - {self.user_name}", font=("Consolas", 22, "bold")).pack(pady=10)

        # Sidebar
        sidebar = ctk.CTkFrame(self.root, width=100, corner_radius=0, fg_color="#154360")
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="Opciones", font=("Consolas", 17, "bold")).pack(pady=20)
        ctk.CTkButton(sidebar, text="Gestionar Usuarios", width=150, command=self.show_user_management).pack(pady=10)
        # Otros botones...
        ctk.CTkButton(sidebar, text="Cerrar Sessión", width=150, fg_color="#C0392B", command=self.close_session).pack(pady=40)

        # Content
        self.content = ctk.CTkFrame(self.root, fg_color="#1C2833", corner_radius=10)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ==================== Gestión de Usuarios ====================
    def show_user_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Usuarios", font=("Consolas", 20, "bold")).pack(pady=20)
        ctk.CTkButton(self.content, text="Agregar Usuario", width=200, command=self.add_user).pack(pady=10)

        # Treeview para usuarios
        columns = ("id", "name", "email", "role")
        self.tree = ttk.Treeview(self.content, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nombre")
        self.tree.heading("email", text="Correo")
        self.tree.heading("role", text="Rol")
        self.tree.pack(pady=10, fill="x", padx=20)

        btn_frame = ctk.CTkFrame(self.content, fg_color="#1C2833")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Editar Usuario", width=150, command=self.edit_user).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Usuario", width=150, command=self.delete_user).pack(side="left", padx=5)

        self.load_users()

    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        users = self.user_handler.get_all_user()
        for user in users:
            self.tree.insert("", "end", values=user)

    def add_user(self):
        popup = ctk.CTkToplevel(self.root)  
        popup.title("Agregar Usuario")
        popup.geometry("400x350")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text=f"Agregar Usuario", font=("Consolas", 22, "bold")).pack(pady=10)

        entry_name = ctk.CTkEntry(popup, placeholder_text="Nombre Completo", width=300)
        entry_name.pack(pady=10)
        entry_email = ctk.CTkEntry(popup, placeholder_text="Correo Electrónico", width=300)
        entry_email.pack(pady=10)
        entry_pass = ctk.CTkEntry(popup, placeholder_text="Contraseña", width=300)
        entry_pass.pack(pady=10)

        combo_type = ctk.CTkComboBox(popup, values=["Administrador", "Empleado", "Cliente"], width=300)
        combo_type.set("Cliente")
        combo_type.pack(pady=10)

        def save_user():
            name = entry_name.get()
            email = entry_email.get()
            password = entry_pass.get()
            role = combo_type.get()
            type_map = {"Administrador": 1, "Empleado": 2, "Cliente": 3}
            type_user = type_map.get(role, 3)

            self.user_handler.register(name, email, password, type_user)
            messagebox.showinfo("Éxito", f"Usuario {name} registrado como {role}")
            popup.destroy()
            self.load_users()

        ctk.CTkButton(popup, text="Guardar", width=200, command=save_user).pack(pady=15)

    # Placeholder para editar y eliminar
    def edit_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un usuario para editar")
            return
        user_data = self.tree.item(selected[0])["values"]

        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Usuario")
        popup.geometry("400x350")
        popup.resizable(False, False)

        entry_name = ctk.CTkEntry(popup, placeholder_text="Nombre Completo", width=300)
        entry_name.insert(0, user_data[1])
        entry_name.pack(pady=10)

        entry_email = ctk.CTkEntry(popup, placeholder_text="Correo Electrónico", width=300)
        entry_email.insert(0, user_data[2])
        entry_email.pack(pady=10)

        combo_type = ctk.CTkComboBox(popup, values=["Administrador", "Empleado", "Cliente"], width=300)
        combo_type.set(user_data[3])
        combo_type.pack(pady=10)

        def save_edit():
            name = entry_name.get()
            email = entry_email.get()
            role = combo_type.get()
            type_map = {"Administrador": 1, "Empleado": 2, "Cliente": 3}
            type_user = type_map.get(role, 3)
            self.user_handler.update_user(user_data[0], name, email, type_user)
            messagebox.showinfo("Éxito", f"Usuario {name} actualizado")
            popup.destroy()
            self.load_users()

        ctk.CTkButton(popup, text="Guardar Cambios", width=200, command=save_edit).pack(pady=15)

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un usuario para eliminar")
            return
        user_data = self.tree.item(selected[0])["values"]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar al usuario {user_data[1]}?")
        if confirm:
            self.user_handler.delete_user(user_data[0])
            self.load_users()



















    # Cerrar sesión
    def close_session(self):
        self.root.destroy()
        from ui.login_window import LoginWindow
        LoginWindow().run()

    def run(self):
        self.root.mainloop()
