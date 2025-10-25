CREATE TABLE IF NOT EXISTS Type_Users(
    id_type_user INTEGER PRIMARY KEY AUTOINCREMENT,
    name_type TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Users(
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    pass TEXT NOT NULL,
    fkid_type_user INTEGER,
    registration_date TEXT DEFAULT (DATE('now')),
    FOREIGN KEY (fkid_type_user) REFERENCES Type_Users(id_type_user)
);

CREATE TABLE IF NOT EXISTS Clients(
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    client_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    pass TEXT NOT NULL,
    registration_date TEXT DEFAULT (DATE('now'))
);

CREATE TABLE IF NOT EXISTS Rooms(
    id_room INTEGER PRIMARY KEY AUTOINCREMENT,
    room_key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    schedule TEXT CHECK (schedule IN ('Morning','Afternoon','Evening')) NOT NULL,
    availability INTEGER DEFAULT 1,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Reservations(
    id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    reservation_date TEXT NOT NULL,
    schedule TEXT CHECK (schedule IN ('Morning','Afternoon','Evening')) NOT NULL,
    create_at TEXT DEFAULT (DATE('now')),
    status TEXT CHECK (status IN ('Active','Canceled')) DEFAULT 'Active',
    fkid_client INTEGER NOT NULL,
    fkid_room INTEGER NOT NULL,
    FOREIGN KEY (fkid_client) REFERENCES Clients(id_client),
    FOREIGN KEY (fkid_room) REFERENCES Rooms(id_room)
);