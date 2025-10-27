UPDATE Rooms
SET room_key = ?, 
    name = ?, 
    capacity = ?, 
    schedule = ?, 
    availability = ?, 
    description = ?
WHERE id_room = ?;