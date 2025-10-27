SELECT 
    u.id_user,
    u.name,
    u.email,
    t.name_type AS role
FROM 
    Users u
JOIN 
    Type_Users t ON u.fkid_type_user = t.id_type_user
WHERE 
    u.email = ? AND u.pass = ?;