INSERT INTO Reservations (
    event_name,
    reservation_date,
    schedule,
    status,
    fkid_client,
    fkid_room
) VALUES (?, ?, ?, ?, ?, ?);
