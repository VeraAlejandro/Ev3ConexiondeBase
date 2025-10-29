from models.database import Database
from datetime import datetime, timedelta

class Reservation:
    def __init__(self, db: Database):
        self.db = db

    # Registrar reservación
    def register(self, event_name, reservation_date, schedule, fkid_client, fkid_room):
        # Validar formato de fecha
        try:
            fecha_reserva = datetime.strptime(reservation_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Formato de fecha inválido. Usa YYYY-MM-DD")

        # Validar que sea al menos 2 días antes
        if fecha_reserva < datetime.now() + timedelta(days=2):
            raise ValueError("La reservación debe hacerse al menos 2 días antes")

        # Validar que no sea domingo
        if fecha_reserva.weekday() == 6:
            raise ValueError("No se pueden hacer reservaciones los domingos")

        # Validar que no exista otra reservación activa en esa sala y horario
        count = self.db.query("get_available_rooms.sql", (fkid_room, reservation_date, schedule))[0][0]
        if count > 0:
            raise ValueError("Ya existe una reservación activa para esta sala y horario")

        # Registrar usando archivo SQL
        self.db.execute(
            "create_reservation.sql",
            (event_name, reservation_date, schedule, 'Active', fkid_client, fkid_room)
        )

    # Obtener todas las reservaciones
    def get_all_reservations(self):
        return self.db.query("get_all_reservations.sql")

    # Actualizar reservación (solo nombre y estado)
    def update(self, id_reservation, event_name=None, status=None):
        self.db.query("update_reservation.sql", (event_name, status, id_reservation))

    # Eliminar reservación
    def delete(self, id_reservation):
        self.db.execute("delete_reservation.sql", (id_reservation,))

    # Consultar disponibilidad de salas
    def get_available_rooms_list(self, reservation_date):
        """Esta es la función que debes llamar desde admin_window.py"""
        all_rooms = self.db.query("get_all_rooms.sql")  # id_room, room_key, name
        available_rooms = []

        for room in all_rooms:
            room_id = room[0]
            room_key = room[1]
            room_name = room[2]

            for turno in ["Morning", "Afternoon", "Evening"]:
                count = self.db.query("get_available_rooms.sql", (room_id, reservation_date, turno))[0][0]
                if count == 0:
                    available_rooms.append((room_key, room_name, turno))
        return available_rooms
