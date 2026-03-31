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

INSERT INTO Movie (title, genre, rating, description, poster_url, trailer_url, status)
VALUES 

('The Godfather', 'Crime', 'R', 'mob life', 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg', 'https://www.youtube.com/embed/sY1S34973zA', 'Currently Running'),
('Pulp Fiction', 'Crime', 'R', 'pulp fiction life', 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg', 'https://www.youtube.com/embed/s7EdQ4FqbhY', 'Currently Running'),
('The Shawshank Redemption', 'Drama', 'R', 'prison life', 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg', 'https://www.youtube.com/embed/6hB3S9bIaco', 'Currently Running'),
('Spirited Away', 'Animation', 'PG', 'anime movie', 'https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg', 'https://www.youtube.com/embed/ByXuk9QqQmc', 'Currently Running'),
('Jurassic Park', 'Sci-Fi', 'PG-13', 'dinosaur rawr', 'https://image.tmdb.org/t/p/w500/9i3plLl89DHMz7mahksDaAo7HIS.jpg', 'https://www.youtube.com/embed/lc0UehYemQA', 'Currently Running'),
--
('2001: A Space Odyssey', 'Sci-Fi', 'G', 'flying through space', 'https://image.tmdb.org/t/p/w500/ve72VxNqjGM69Uky4WToA3q0uRf.jpg', 'https://www.youtube.com/embed/oR_e9y-bka0', 'Coming Soon'),
('Casablanca', 'Romance', 'PG', 'love', 'https://image.tmdb.org/t/p/w500/5K7cOHoay2mZusSLezBOY0Qxh8a.jpg', 'https://www.youtube.com/embed/BkL9l7qovsE', 'Coming Soon'),
('The Shining', 'Horror', 'R', 'scary', 'https://image.tmdb.org/t/p/w500/9fgh3Ns1iRzlQNYuJyK0ARQZU7w.jpg', 'https://www.youtube.com/embed/5Cb3ik6zP2I', 'Coming Soon'),
('Singin in the Rain', 'Musical', 'G', 'singing', 'https://image.tmdb.org/t/p/w500/w03EiJVHP8Un77boQeE7hg9DVdU.jpg', 'https://www.youtube.com/embed/5_EVHeNEIJY', 'Coming Soon'),
('Seven Samurai', 'Action', 'NR', 'samurai movie', 'https://image.tmdb.org/t/p/w500/8OKmBV5BUFzmozIC3pPWKHy17kx.jpg', 'https://www.youtube.com/embed/7mw6LyyoeGE', 'Coming Soon');

INSERT INTO Showtime (movie_id, show_date, show_time)
VALUES 
(1, '2026-03-05', '14:00:00'), (1, '2026-03-05', '17:00:00'), (1, '2026-03-05', '20:00:00'),
(2, '2026-03-05', '14:00:00'), (2, '2026-03-05', '20:00:00'),
(3, '2026-03-05', '13:00:00'), (3, '2026-03-05', '19:00:00'),
(4, '2026-03-05', '11:00:00'), (4, '2026-03-05', '15:00:00'),
(5, '2026-03-05', '12:00:00'), (5, '2026-03-05', '18:00:00');