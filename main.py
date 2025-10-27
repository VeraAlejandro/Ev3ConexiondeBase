from ui.login_window import LoginWindow
from ui.admin_window import AdminWindow

def main():
    # Abrir ventana de login
    login = LoginWindow()
    role, user_name = login.run()  # Devuelve rol y nombre si login fue exitoso

    if role == "Administrador":
        admin = AdminWindow(user_name)
        admin.run()
    # Aquí puedes agregar más condicionales para Empleado, Cliente, etc.

if __name__ == "__main__":
    main()