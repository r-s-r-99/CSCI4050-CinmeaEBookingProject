INSERT INTO Movie (title, genre, rating, description, poster_url, trailer_url, status)
VALUES 

('The Godfather', 'Crime', 'R', 'mob life', '', 'https://www.youtube.com/embed/sY1S34973zA', 'Currently Running'),
('Pulp Fiction', 'Crime', 'R', 'pulp fiction life', '', 'https://www.youtube.com/embed/s7EdQ4FqbhY', 'Currently Running'),
('The Shawshank Redemption', 'Drama', 'R', 'prison life', '', 'https://www.youtube.com/embed/6hB3S9bIaco', 'Currently Running'),
('Spirited Away', 'Animation', 'PG', 'anime movie', '', 'https://www.youtube.com/embed/ByXuk9QqQmc', 'Currently Running'),
('Jurassic Park', 'Sci-Fi', 'PG-13', 'dinosaur rawr', '', 'https://www.youtube.com/embed/lc0UehYemQA', 'Currently Running'),
--
('2001: A Space Odyssey', 'Sci-Fi', 'G', 'flying through space', '', 'https://www.youtube.com/embed/oR_e9y-bka0', 'Coming Soon'),
('Casablanca', 'Romance', 'PG', 'love', '', 'https://www.youtube.com/embed/BkL9l7qovsE', 'Coming Soon'),
('The Shining', 'Horror', 'R', 'scary', '', 'https://www.youtube.com/embed/5Cb3ik6zP2I', 'Coming Soon'),
('Singin in the Rain', 'Musical', 'G', 'singing', '', 'https://www.youtube.com/embed/5_EVHeNEIJY', 'Coming Soon'),
('Seven Samurai', 'Action', 'NR', 'samurai movie', '', 'https://www.youtube.com/embed/7mw6LyyoeGE', 'Coming Soon');

INSERT INTO Showtime (movie_id, show_date, show_time)
VALUES 
(1, '2026-03-05', '14:00:00'), (1, '2026-03-05', '17:00:00'), (1, '2026-03-05', '20:00:00'),
(2, '2026-03-05', '14:00:00'), (2, '2026-03-05', '20:00:00'),
(3, '2026-03-05', '13:00:00'), (3, '2026-03-05', '19:00:00'),
(4, '2026-03-05', '11:00:00'), (4, '2026-03-05', '15:00:00'),
(5, '2026-03-05', '12:00:00'), (5, '2026-03-05', '18:00:00');
