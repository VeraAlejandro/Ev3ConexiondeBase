UPDATE Reservations
SET
    event_name = ?,
    reservation_date = ?,
    schedule = ?,
    status = ?,
    fkid_client = ?,
    fkid_room = ?
WHERE id_reservation = ?;
