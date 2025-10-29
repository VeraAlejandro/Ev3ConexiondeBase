from models.database import Database
from models.user import User
import customtkinter as ctk
from tkinter import ttk, messagebox
from models.client import Client
from models.room import Room
from models.reservation import Reservation
from datetime import datetime


class AdminWindow:
    def __init__(self, user_name):
        self.user_name = user_name

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Base de datos y handler 
        self.db = Database(suppress_message=True)
        self.user_handler = User(self.db)
        self.client_handler = Client(self.db)
        self.room_handler = Room(self.db)
        self.reservation_handler = Reservation(self.db)


        self.root = ctk.CTk()
        self.root.title("Panel de Administrador")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        # Header
        header = ctk.CTkFrame(self.root, height=60, corner_radius=0, fg_color="#1A5276")
        header.pack(fill="x")
        ctk.CTkLabel(header, text=f"Panel de Administrador - {self.user_name}", font=("Consolas", 22, "bold")).pack(pady=10)

        # Sidebar
        sidebar = ctk.CTkFrame(self.root, width=100, corner_radius=0, fg_color="#153560")
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="Opciones", font=("Consolas", 17, "bold")).pack(pady=20)
        ctk.CTkButton(sidebar, text="Gestionar Usuarios", width=150, command=self.show_user_management).pack(pady=10)
        ctk.CTkButton(sidebar, text="Gestionar Clientes", width=150, command=self.show_client_management).pack(pady=10)
        ctk.CTkButton(sidebar, text="Gestionar Salas", width=150, command=self.show_room_management).pack(pady=10)
        ctk.CTkButton(sidebar, text="Reservaciones", width=150, command=self.show_reservation_management).pack(pady=10)
        #ctk.CTkButton(sidebar, text="Ver Reportes", width=150, command=self.show_reports).pack(pady=10)
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

        combo_type = ctk.CTkComboBox(popup, values=["Administrador", "Empleado"], width=300)
        combo_type.set("Empleado")
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

    # ==================== Gestión de Clientes ====================
    def show_client_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Clientes", font=("Consolas", 20, "bold")).pack(pady=20)
        ctk.CTkButton(self.content, text="Agregar Cliente", width=200, command=self.add_client).pack(pady=10)

        # Tabla (Treeview)
        columns = ("id", "client_key", "name", "email", "phone")
        self.client_tree = ttk.Treeview(self.content, columns=columns, show="headings", height=10)
        self.client_tree.heading("id", text="ID")
        self.client_tree.heading("client_key", text="Clave Única")
        self.client_tree.heading("name", text="Nombre")
        self.client_tree.heading("email", text="Correo")
        self.client_tree.heading("phone", text="Teléfono")
        self.client_tree.pack(pady=10, fill="x", padx=20)

        # Botones Editar / Eliminar
        btn_frame = ctk.CTkFrame(self.content, fg_color="#1C2833")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Editar Cliente", width=150, command=self.edit_client).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Cliente", width=150, command=self.delete_client).pack(side="left", padx=5)

        self.load_clients()

    def load_clients(self):
        # Limpiar tabla
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)

        # Cargar clientes desde la base
        clients = self.client_handler.get_all_clients()
        for client in clients:
            self.client_tree.insert("", "end", values=client)

    def add_client(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Agregar Cliente")
        popup.geometry("400x400")
        popup.resizable(False, False)

        entry_key = ctk.CTkEntry(popup, placeholder_text="Clave Única", width=300)
        entry_key.pack(pady=10)
        entry_name = ctk.CTkEntry(popup, placeholder_text="Nombre Completo", width=300)
        entry_name.pack(pady=10)
        entry_email = ctk.CTkEntry(popup, placeholder_text="Correo Electrónico", width=300)
        entry_email.pack(pady=10)
        entry_phone = ctk.CTkEntry(popup, placeholder_text="Teléfono", width=300)
        entry_phone.pack(pady=10)
        entry_pass = ctk.CTkEntry(popup, placeholder_text="Contraseña", show="*", width=300)
        entry_pass.pack(pady=10)

        def save_client():
            client_key = entry_key.get()
            name = entry_name.get()
            email = entry_email.get()
            phone = entry_phone.get()
            password = entry_pass.get()

            if not all([client_key, name, email, phone, password]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            self.client_handler.register(client_key, name, email, phone, password)
            messagebox.showinfo("Éxito", f"Cliente {name} registrado correctamente")
            popup.destroy()
            self.load_clients()

        ctk.CTkButton(popup, text="Guardar", width=200, command=save_client).pack(pady=15)

    def edit_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un cliente para editar")
            return
        client_data = self.client_tree.item(selected[0])["values"]

        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Cliente")
        popup.geometry("400x400")
        popup.resizable(False, False)

        entry_key = ctk.CTkEntry(popup, placeholder_text="Clave Única", width=300)
        entry_key.insert(0, client_data[1])
        entry_key.pack(pady=10)
        entry_name = ctk.CTkEntry(popup, placeholder_text="Nombre Completo", width=300)
        entry_name.insert(0, client_data[2])
        entry_name.pack(pady=10)
        entry_email = ctk.CTkEntry(popup, placeholder_text="Correo Electrónico", width=300)
        entry_email.insert(0, client_data[3])
        entry_email.pack(pady=10)
        entry_phone = ctk.CTkEntry(popup, placeholder_text="Teléfono", width=300)
        entry_phone.insert(0, client_data[4])
        entry_phone.pack(pady=10)

        def save_edit():
            client_key = entry_key.get()
            name = entry_name.get()
            email = entry_email.get()
            phone = entry_phone.get()
            if not all([client_key, name, email, phone]):
                messagebox.showerror("Error", "Ningún campo puede estar vacío")
                return
            self.client_handler.update(client_data[0], client_key, name, email, phone)
            messagebox.showinfo("Éxito", f"Cliente {name} actualizado correctamente")
            popup.destroy()
            self.load_clients()

        ctk.CTkButton(popup, text="Guardar Cambios", width=200, command=save_edit).pack(pady=15)

    def delete_client(self):
        selected = self.client_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona un cliente para eliminar")
            return
        client_data = self.client_tree.item(selected[0])["values"]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar al cliente {client_data[2]}?")
        if confirm:
            self.client_handler.delete(client_data[0])
            self.load_clients()


    # ==================== Gestión de salas  ====================
    def show_room_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Salas", font=("Consolas", 20, "bold")).pack(pady=20)
        ctk.CTkButton(self.content, text="Agregar Sala", width=200, command=self.add_room).pack(pady=10)

        # Tabla de salas
        columns = ("id_room", "room_key", "name", "capacity", "schedule", "availability", "description")
        self.room_tree = ttk.Treeview(self.content, columns=columns, show="headings", height=10)
        for col in columns:
            self.room_tree.heading(col, text=col.capitalize())
        self.room_tree.pack(pady=10, fill="x", padx=20)

        # Botones
        btn_frame = ctk.CTkFrame(self.content, fg_color="#1C2833")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Editar Sala", width=150, command=self.edit_room).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Sala", width=150, command=self.delete_room).pack(side="left", padx=5)

        self.load_rooms()

    def load_rooms(self):
        # Limpiar tabla
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)

        # Obtener salas
        rooms = self.room_handler.get_all_rooms()
        for room in rooms:
            self.room_tree.insert("", "end", values=room)

    def add_room(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Agregar Sala")
        popup.geometry("400x500")
        popup.resizable(False, False)

        entry_key = ctk.CTkEntry(popup, placeholder_text="Clave de Sala", width=300)
        entry_key.pack(pady=10)

        entry_name = ctk.CTkEntry(popup, placeholder_text="Nombre de Sala", width=300)
        entry_name.pack(pady=10)

        entry_capacity = ctk.CTkEntry(popup, placeholder_text="Capacidad", width=300)
        entry_capacity.pack(pady=10)

        combo_schedule = ctk.CTkComboBox(popup, values=["Morning", "Afternoon", "Evening"], width=300)
        combo_schedule.set("Morning")
        combo_schedule.pack(pady=10)

        combo_availability = ctk.CTkComboBox(popup, values=["Disponible", "No disponible"], width=300)
        combo_availability.set("Disponible")
        combo_availability.pack(pady=10)

        entry_description = ctk.CTkEntry(popup, placeholder_text="Descripción", width=300)
        entry_description.pack(pady=10)

        def save_room():
            room_key = entry_key.get()
            name = entry_name.get()
            capacity = entry_capacity.get()
            schedule = combo_schedule.get()
            availability = 1 if combo_availability.get() == "Disponible" else 0
            description = entry_description.get()

            self.room_handler.register(room_key, name, capacity, schedule, availability, description)
            messagebox.showinfo("Éxito", f"Sala {name} registrada correctamente")
            popup.destroy()
            self.load_rooms()

        ctk.CTkButton(popup, text="Guardar", width=200, command=save_room).pack(pady=15)

    def edit_room(self):
        selected = self.room_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una sala para editar")
            return

        room_data = self.room_tree.item(selected[0])["values"]
        print("Datos de la sala:", room_data)  # Solo para debug

        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Sala")
        popup.geometry("400x500")
        popup.resizable(False, False)

        # Entradas
        entry_key = ctk.CTkEntry(popup, width=300, placeholder_text="Clave de Sala")
        entry_key.insert(0, room_data[1] if len(room_data) > 1 else "")
        entry_key.pack(pady=10)

        entry_name = ctk.CTkEntry(popup, width=300, placeholder_text="Nombre de Sala")
        entry_name.insert(0, room_data[2] if len(room_data) > 2 else "")
        entry_name.pack(pady=10)

        entry_capacity = ctk.CTkEntry(popup, width=300, placeholder_text="Capacidad")
        entry_capacity.insert(0, room_data[3] if len(room_data) > 3 else "")
        entry_capacity.pack(pady=10)

        # Validación de valores de schedule
        schedule_value = room_data[4] if len(room_data) > 4 and room_data[4] in ["Morning", "Afternoon", "Evening"] else "Morning"
        combo_schedule = ctk.CTkComboBox(popup, values=["Morning", "Afternoon", "Evening"], width=300)
        combo_schedule.set(schedule_value)
        combo_schedule.pack(pady=10)

        # Validación de valores de availability
        availability_value = "Disponible" if len(room_data) > 5 and room_data[5] == 1 else "No disponible"
        combo_availability = ctk.CTkComboBox(popup, values=["Disponible", "No disponible"], width=300)
        combo_availability.set(availability_value)
        combo_availability.pack(pady=10)

        entry_description = ctk.CTkEntry(popup, width=300, placeholder_text="Descripción")
        entry_description.insert(0, room_data[6] if len(room_data) > 6 else "")
        entry_description.pack(pady=10)

        # Guardar cambios
        def save_edit():
            room_key = entry_key.get()
            name = entry_name.get()
            capacity = entry_capacity.get()
            schedule = combo_schedule.get()
            availability = 1 if combo_availability.get() == "Disponible" else 0
            description = entry_description.get()

            # Validación de campos
            if not all([room_key, name, capacity, schedule]):
                messagebox.showerror("Error", "Los campos clave, nombre, capacidad y horario son obligatorios")
                return

            self.room_handler.update(room_data[0], room_key, name, capacity, schedule, availability, description)
            messagebox.showinfo("Éxito", f"Sala {name} actualizada correctamente")
            popup.destroy()
            self.load_rooms()

        # Botón Guardar Cambios
        ctk.CTkButton(popup, text="Guardar Cambios", width=200, command=save_edit).pack(pady=15)


    def delete_room(self):
        selected = self.room_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Selecciona una sala para eliminar")
            return

        room_data = self.room_tree.item(selected[0])["values"]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar la sala {room_data[2]}?")
        if confirm:
            self.room_handler.delete(room_data[0])
            self.load_rooms()


# ==================== Gestión de Reservaciones ====================
    def show_reservation_management(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestión de Reservaciones", font=("Consolas", 20, "bold")).pack(pady=20)
        ctk.CTkButton(self.content, text="Agregar Reservación", width=200, command=self.add_reservation).pack(pady=10)
        ctk.CTkButton(self.content, text="Consultar Disponibilidad", width=200, command=self.check_availability).pack(pady=10)

        # Tabla (Treeview)
        columns = ("ID", "Evento", "Fecha", "Horario", "Estado", "Cliente", "Sala")
        self.reservation_tree = ttk.Treeview(self.content, columns=columns, show="headings", height=10)

        for col in columns:
            self.reservation_tree.heading(col, text=col)
            self.reservation_tree.column(col, width=120, anchor="center")

        self.reservation_tree.pack(pady=10, fill="x", padx=20)

        # Botones de acción
        btn_frame = ctk.CTkFrame(self.content, fg_color="#1C2833")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Editar Reservación", width=150, command=self.edit_reservation).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Reservación", width=150, command=self.delete_reservation).pack(side="left", padx=5)

        self.load_reservations()


    def load_reservations(self):
        for item in self.reservation_tree.get_children():
            self.reservation_tree.delete(item)

        try:
            reservations = self.reservation_handler.get_all_reservations()
            for res in reservations:
                self.reservation_tree.insert("", "end", values=res)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las reservaciones.\n{e}")


    def add_reservation(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Agregar Reservación")
        popup.geometry("400x520")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Nueva Reservación", font=("Consolas", 22, "bold")).pack(pady=10)

        # Campos de entrada
        entry_event = ctk.CTkEntry(popup, placeholder_text="Nombre del Evento", width=300)
        entry_event.pack(pady=10)

        entry_date = ctk.CTkEntry(popup, placeholder_text="Fecha (YYYY-MM-DD)", width=300)
        entry_date.pack(pady=10)

        combo_schedule = ctk.CTkComboBox(popup, values=["Morning", "Afternoon", "Evening"], width=300)
        combo_schedule.set("Morning")
        combo_schedule.pack(pady=10)

        # Clientes
        clients = self.client_handler.get_all_clients()
        client_options = [f"{c[0]} - {c[2]}" for c in clients]
        combo_client = ctk.CTkComboBox(popup, values=client_options, width=300)
        if client_options:
            combo_client.set(client_options[0])
        combo_client.pack(pady=10)

        # Salas
        rooms = self.room_handler.get_all_rooms()
        room_options = [f"{r[0]} - {r[2]}" for r in rooms]
        combo_room = ctk.CTkComboBox(popup, values=room_options, width=300)
        if room_options:
            combo_room.set(room_options[0])
        combo_room.pack(pady=10)

        def save_reservation():
            event_name = entry_event.get().strip()
            date_str = entry_date.get().strip()
            schedule = combo_schedule.get().strip()

            if not all([event_name, date_str, schedule]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Validar formato de fecha
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD.")
                return

            try:
                client_id = int(combo_client.get().split(" - ")[0])
                room_id = int(combo_room.get().split(" - ")[0])
                self.reservation_handler.register(
                    event_name=event_name,
                    reservation_date=date_str,
                    schedule=schedule,
                    fkid_client=client_id,
                    fkid_room=room_id
                )
                messagebox.showinfo("Éxito", f"Reservación para '{event_name}' registrada correctamente.")
                popup.destroy()
                self.load_reservations()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="Guardar Reservación", width=200, command=save_reservation).pack(pady=15)


    def edit_reservation(self):
        selected = self.reservation_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reservación para editar.")
            return

        res_data = self.reservation_tree.item(selected[0])["values"]

        popup = ctk.CTkToplevel(self.root)
        popup.title("Editar Reservación")
        popup.geometry("400x350")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text=f"Editar: {res_data[1]}", font=("Consolas", 18, "bold")).pack(pady=10)

        entry_event = ctk.CTkEntry(popup, width=300)
        entry_event.insert(0, res_data[1])
        entry_event.pack(pady=10)

        combo_status = ctk.CTkComboBox(popup, values=["Active", "Canceled"], width=300)
        combo_status.set(res_data[4])
        combo_status.pack(pady=10)

        def save_edit():
            event_name = entry_event.get().strip()
            status = combo_status.get().strip()

            if not event_name:
                messagebox.showerror("Error", "El nombre del evento no puede estar vacío.")
                return

            try:
                self.reservation_handler.update(
                    reservation_id=res_data[0],
                    event_name=event_name,
                    status=status
                )
                messagebox.showinfo("Éxito", f"Reservación '{event_name}' actualizada correctamente.")
                popup.destroy()
                self.load_reservations()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="Guardar Cambios", width=200, command=save_edit).pack(pady=15)


    def delete_reservation(self):
        selected = self.reservation_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona una reservación para eliminar.")
            return

        res_data = self.reservation_tree.item(selected[0])["values"]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar la reservación '{res_data[1]}'?")

        if confirm:
            try:
                self.reservation_handler.delete(res_data[0])
                self.load_reservations()
                messagebox.showinfo("Éxito", "Reservación eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))


    def check_availability(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Disponibilidad de Salas")
        popup.geometry("420x450")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text="Consultar Disponibilidad", font=("Consolas", 18, "bold")).pack(pady=10)

        entry_date = ctk.CTkEntry(popup, placeholder_text="Fecha (YYYY-MM-DD)", width=300)
        entry_date.pack(pady=10)

        tree = ttk.Treeview(popup, columns=("ID", "Sala", "Horario"), show="headings", height=10)
        for col in ("ID", "Sala", "Horario"):
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        tree.pack(pady=10, fill="x", padx=20)

        def load_availability():
            date_str = entry_date.get().strip()
            for item in tree.get_children():
                tree.delete(item)

            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD.")
                return

            try:
                available = self.reservation_handler.get_available_rooms_list(date_str)
                if not available:
                    messagebox.showinfo("Sin resultados", "No hay salas disponibles para esa fecha.")
                    return
                for room in available:
                    tree.insert("", "end", values=room)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(popup, text="Consultar", width=200, command=load_availability).pack(pady=10)


    # Cerrar sesión
    def close_session(self):
        self.root.destroy()
        from ui.login_window import LoginWindow
        LoginWindow().run()

    def run(self):
        self.root.mainloop()
