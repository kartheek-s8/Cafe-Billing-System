-- Reset auto-increment counter
ALTER TABLE MenuItem AUTO_INCREMENT = 1;

-- Insert Italian cafe menu items
INSERT INTO MenuItem (name, price, category) VALUES
('Truffle Garlic Bread', 220.00, 'Appetizers'),
('Caprese Skewers', 240.00, 'Appetizers'),
('Rosemary Potato Bites', 200.00, 'Appetizers'),
('Stuffed Mushrooms', 260.00, 'Appetizers'),
('Mini Cheese Platter', 380.00, 'Appetizers'),

('Pomodoro Penne', 380.00, 'Pasta'),
('Creamy Alfredo Fettuccine', 420.00, 'Pasta'),
('Mushroom Truffle Tagliatelle', 480.00, 'Pasta'),
('Arrabbiata Spaghetti', 400.00, 'Pasta'),
('Four Cheese Gnocchi', 460.00, 'Pasta'),

('Classic Tiramisu', 280.00, 'Desserts'),
('Strawberry Panna Cotta', 260.00, 'Desserts'),
('Chocolate Hazelnut Bomb', 300.00, 'Desserts'),
('Lemon Ricotta Tart', 270.00, 'Desserts'),
('Gelato Trio', 250.00, 'Desserts');
