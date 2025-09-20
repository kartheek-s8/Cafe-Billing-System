CREATE TABLE MenuItem (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(item_id) REFERENCES MenuItem(id)
);
