SELECT
    r.id_reservation,
    r.event_name,
    r.reservation_date,
    r.schedule,
    c.name AS client_name,
    rm.name AS room_name,
    r.status
FROM Reservations r
JOIN Clients c ON r.fkid_client = c.id_client
JOIN Rooms rm ON r.fkid_room = rm.id_room
ORDER BY r.id_reservation ASC;
