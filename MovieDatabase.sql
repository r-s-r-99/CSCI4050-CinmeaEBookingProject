CREATE DATABASE IF NOT EXISTS CinemaEBooking;
USE CinemaEBooking;

CREATE TABLE IF NOT EXISTS Movie (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,          
    genre VARCHAR(100) NOT NULL,       
    rating VARCHAR(10),                
    description TEXT,                     
    poster_url VARCHAR(500),          
    trailer_url VARCHAR(500),             
    status ENUM('In Theaters Now', 'Coming Soon') NOT NULL 
);

CREATE TABLE IF NOT EXISTS Showtime (
    showtime_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    show_date DATE,                     
    show_time TIME,                         
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);