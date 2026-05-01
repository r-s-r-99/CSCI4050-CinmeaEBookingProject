-- Seat Reservations table for temporary seat locking
-- This table stores temporary seat reservations during the booking process

CREATE TABLE IF NOT EXISTS seat_reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    showtime_id INT NOT NULL,
    seat_id VARCHAR(10) NOT NULL,
    session_token VARCHAR(64) NOT NULL,
    reserved_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    INDEX idx_showtime_expires (showtime_id, expires_at),
    INDEX idx_session_token (session_token),
    UNIQUE KEY unique_seat_showtime (showtime_id, seat_id)
);

-- Note: The unique key ensures a seat can only be reserved once per showtime
-- Expired reservations can be cleaned up periodically or on-demand