CREATE DATABASE IF NOT EXISTS cinemaebooking;
USE cinemaebooking;

CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    role ENUM('customer', 'admin') NOT NULL DEFAULT 'customer',
    account_status ENUM('Active', 'Inactive', 'Suspended') NOT NULL DEFAULT 'Inactive',
    promo_subscribed BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS MailingAddress (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    house_number VARCHAR(20),
    street VARCHAR(255),
    apt VARCHAR(50),
    zip VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PaymentCard (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    card_number VARCHAR(255) NOT NULL,
    expiration_date DATE NOT NULL,
    billing_house VARCHAR(20),
    billing_street VARCHAR(255),
    billing_apt VARCHAR(50),
    billing_zip VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PasswordResetToken (
    token_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movie (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    rating VARCHAR(10),
    description TEXT,
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    status ENUM('Currently Running', 'Coming Soon') NOT NULL
);

CREATE TABLE IF NOT EXISTS Showroom (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number INT NOT NULL UNIQUE,
    number_of_seats INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Seat (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    seat_number VARCHAR(10) NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Showroom(room_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Showtime (
    showtime_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT NOT NULL,
    room_id INT,
    show_date DATE NOT NULL,
    show_time TIME NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES Showroom(room_id)
);

CREATE TABLE IF NOT EXISTS Promotion (
    promotion_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percentage DOUBLE NOT NULL,
    start_date DATE,
    end_date DATE,
    tickets_available INT
);

CREATE TABLE IF NOT EXISTS Booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    showtime_id INT NOT NULL,
    card_id INT,
    promotion_id INT,
    total_price DOUBLE NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (showtime_id) REFERENCES Showtime(showtime_id),
    FOREIGN KEY (card_id) REFERENCES PaymentCard(card_id),
    FOREIGN KEY (promotion_id) REFERENCES Promotion(promotion_id)
);

CREATE TABLE IF NOT EXISTS Ticket (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    seat_id INT NOT NULL,
    ticket_type ENUM('Child', 'Adult', 'Senior') NOT NULL,
    show_date DATE,
    ticket_price DOUBLE NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES Seat(seat_id)
);

CREATE TABLE IF NOT EXISTS Favorite (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    date_added DATE DEFAULT (CURRENT_DATE),
    UNIQUE KEY unique_fav (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Preference (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    date_added DATE,
    preference_score INT,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Recommendation (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    recommendation_date DATE,
    score DOUBLE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
);

INSERT INTO Showroom (room_number, number_of_seats) VALUES
(1, 96),
(2, 96),
(3, 96),
(4, 96);

INSERT INTO Seat (seat_number, room_id) VALUES
('A1',1),('A2',1),('A3',1),('A4',1),('A5',1),('A6',1),('A7',1),('A8',1),('A9',1),('A10',1),('A11',1),('A12',1),
('B1',1),('B2',1),('B3',1),('B4',1),('B5',1),('B6',1),('B7',1),('B8',1),('B9',1),('B10',1),('B11',1),('B12',1),
('C1',1),('C2',1),('C3',1),('C4',1),('C5',1),('C6',1),('C7',1),('C8',1),('C9',1),('C10',1),('C11',1),('C12',1),
('D1',1),('D2',1),('D3',1),('D4',1),('D5',1),('D6',1),('D7',1),('D8',1),('D9',1),('D10',1),('D11',1),('D12',1),
('E1',1),('E2',1),('E3',1),('E4',1),('E5',1),('E6',1),('E7',1),('E8',1),('E9',1),('E10',1),('E11',1),('E12',1),
('F1',1),('F2',1),('F3',1),('F4',1),('F5',1),('F6',1),('F7',1),('F8',1),('F9',1),('F10',1),('F11',1),('F12',1),
('G1',1),('G2',1),('G3',1),('G4',1),('G5',1),('G6',1),('G7',1),('G8',1),('G9',1),('G10',1),('G11',1),('G12',1),
('H1',1),('H2',1),('H3',1),('H4',1),('H5',1),('H6',1),('H7',1),('H8',1),('H9',1),('H10',1),('H11',1),('H12',1);

INSERT INTO Promotion (code, discount_percentage, start_date, end_date, tickets_available) VALUES
('WELCOME10', 10.0, '2026-04-01', '2026-04-30', 100),
('SUMMER20', 20.0, '2026-06-01', '2026-08-31', 500);

INSERT INTO User (email, password, first_name, last_name, role, account_status)
VALUES (
    'admin@cinemabooking.com',
    '$2b$12$KIXn7rHQL5L0Eup3vMnVeeSBCMQb4Y7JxHFCGvHzSl6VTT0FBJlwu',
    'Admin',
    'User',
    'admin',
    'Active'
);