from models.database import Database
from tkinter import messagebox
import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, timedelta

class Reservation:
    def __init__(self, db: Database):
        self.db = db

    # Registrar reservación
    def register(self, event_name, reservation_date, schedule, fkid_client, fkid_room):
        # Validar que sea mínimo 2 días antes
        fecha_reserva = datetime.strptime(reservation_date, "%Y-%m-%d")
        if fecha_reserva < datetime.now() + timedelta(days=2):
            raise ValueError("La reservación debe hacerse al menos 2 días antes")

        # Validar que no sea domingo
        if fecha_reserva.weekday() == 6:
            raise ValueError("No se pueden hacer reservaciones los domingos")

        # Validar que no exista otra reservación en la misma sala y turno
        query = "SELECT COUNT(*) FROM Reservations WHERE fkid_room=? AND reservation_date=? AND schedule=? AND status='Active'"
        count = self.db.query(query, (fkid_room, reservation_date, schedule))[0][0]
        if count > 0:
            raise ValueError("Ya existe una reservación para esta sala y horario")

        # Ejecutar creación
        self.db.execute(
            "create_reservation.sql",
            (event_name, reservation_date, schedule, 'Active', fkid_client, fkid_room)
        )

    # Consultar todas las reservaciones
    def get_all_reservations(self):
        return self.db.query("get_all_reservations.sql")

    # Actualizar solo la descripción o estado
    def update(self, id_reservation, event_name=None, status=None):
        self.db.execute("update_reservation.sql", (event_name, status, id_reservation))

    # Eliminar reservación
    def delete(self, id_reservation):
        self.db.execute("delete_reservation.sql", (id_reservation,))

    # Consultar disponibilidad de salas para una fecha
    def get_available_rooms(self, reservation_date):
        # Todas las salas
        all_rooms = self.db.query("get_all_rooms.sql")
        available_rooms = []

        for room in all_rooms:
            room_id = room[0]
            # Verificar si hay reservación activa en esta fecha y turno
            for turno in ["Morning", "Afternoon", "Evening"]:
                query = "SELECT COUNT(*) FROM Reservations WHERE fkid_room=? AND reservation_date=? AND schedule=? AND status='Active'"
                count = self.db.query(query, (room_id, reservation_date, turno))[0][0]
                if count == 0:
                    available_rooms.append((room[1], room[2], turno))  # clave, nombre, turno
        return available_rooms
