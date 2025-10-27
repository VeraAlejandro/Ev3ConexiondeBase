SELECT u.id_user, u.name, u.email, t.name_type
FROM Users u
LEFT JOIN Type_Users t ON u.fkid_type_user = t.id_type_user;
