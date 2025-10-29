-- Parámetros: ? = fkid_room, ? = reservation_date, ? = schedule
SELECT COUNT(*) 
FROM Reservations 
WHERE fkid_room = ? 
  AND reservation_date = ? 
  AND schedule = ? 
  AND status = 'Active';
