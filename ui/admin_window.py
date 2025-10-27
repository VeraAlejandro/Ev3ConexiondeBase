import customtkinter as ctk

class AdminWindow:
    def __init__(self, user_name):
        self.user_name = user_name
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Panel de Administrador")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        #HEADER
        header = ctk.CTkFrame(self.root, height=60, corner_radius=0, fg_color="#1A5276")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"Panel de Administrador - {self.user_name}", font=("Consolas", 22, "bold")).pack(pady=10)

        #barra
        sidebar = ctk.CTkFrame(self.root, width=100, corner_radius=0, fg_color="#154360")
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="Opciones", font=("Consolas", 17, "bold")).pack(pady=20)

        #botones del slidebar
        ctk.CTkButton(sidebar, text="Gestionar Usuarios", width=150, command=self.show_user_management).pack(pady=10)
        ctk.CTkButton(sidebar, text="Gestionar Clientes", width=150, command=self.show_client_management).pack(pady=10)
        ctk.CTkButton(sidebar, text="Gestionar Salas", width=150, command=self.show_room_management).pack(pady=10)
        ctk.CTkButton(sidebar, text="Reservaciones", width=150, command=self.show_reservation).pack(pady=10)
        ctk.CTkButton(sidebar, text="Ver Reportes", width=150, command=self.show_reports).pack(pady=10)
        ctk.CTkButton(sidebar, text="Cerrar Sessión", width=150, fg_color="#C0392B", command=self.close_session).pack(pady=40)

        self.content = ctk.CTkFrame(self.root, fg_color="#1C2833", corner_radius=10)
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.content, text="Bienvenido al Panel del Administrador", font=("Consolas", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self.content, text="Aquí podrás gestionar usuarios, ver reportes y configurar el sistema.", font=("Consolas", 13)).pack(pady=10)

    #metodo para limpiar el content 
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()
    
    #secciones del panel 
    def show_user_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Usuarios", font=("Consolas", 20, "bold")).pack(pady=20)
    
    def show_client_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Clientes", font=("Consolas", 20, "bold")).pack(pady=20)

    def show_room_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Salas", font=("Consolas", 20, "bold")).pack(pady=20)
    
    def show_reservation(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Reservaciones", font=("Consolas", 20, "bold")).pack(pady=20)
    
    def show_reports(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Reportes", font=("Consolas", 20, "bold")).pack(pady=20)




    # Cerrar sesión y volver a login
    def close_session(self):
        self.root.destroy()
        from ui.login_window import LoginWindow
        LoginWindow().run()

    # Ejecutar ventana
    def run(self):
        self.root.mainloop()
