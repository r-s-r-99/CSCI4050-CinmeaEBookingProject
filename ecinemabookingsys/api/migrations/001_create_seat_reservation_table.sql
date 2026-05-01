-- Migration: Create SeatReservation table for temporary seat locks during booking

CREATE TABLE IF NOT EXISTS SeatReservation (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    showtime_id INT NOT NULL,
    seat_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (showtime_id) REFERENCES Showtime(showtime_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES Seat(seat_id) ON DELETE CASCADE,
    UNIQUE KEY unique_reservation (showtime_id, seat_id, user_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_showtime_user (showtime_id, user_id)
);

-- Optional: Create a scheduled event to clean up expired reservations every minute
-- (Requires EVENT privilege and scheduled_events enabled in MySQL)
-- DELIMITER $$
-- CREATE EVENT IF NOT EXISTS cleanup_expired_reservations
-- ON SCHEDULE EVERY 1 MINUTE
-- DO
--   DELETE FROM SeatReservation WHERE expires_at <= NOW();
-- DELIMITER ;
