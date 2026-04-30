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
    card_name varchar(255) NOT NULL,
    card_number VARCHAR(255) NOT NULL,
    cvv VARCHAR(255) NOT NULL, 
    expiration_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PasswordResetToken (
    token_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(255),
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
