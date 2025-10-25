SELECT id_user, name, email,fkid_type_user
FROM Users 
WHERE email = ? AND pass = ?;