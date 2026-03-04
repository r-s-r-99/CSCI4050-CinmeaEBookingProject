INSERT INTO Movie (title, genre, rating, description, poster_url, trailer_url, status)
VALUES 

('The Godfather', 'Crime', 'R', 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.', '', 'https://www.youtube.com/embed/sY1S34973zA', 'Currently Running'),
('Pulp Fiction', 'Crime', 'R', 'The lives of two mob hitmen, a boxer, and a gangster and his wife intertwine.', '', 'https://www.youtube.com/embed/s7EdQ4FqbhY', 'Currently Running'),
('The Shawshank Redemption', 'Drama', 'R', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption.', '', 'https://www.youtube.com/embed/6hB3S9bIaco', 'Currently Running'),
('Spirited Away', 'Animation', 'PG', 'A young girl wanders into a world ruled by gods, witches, and spirits.', '', 'https://www.youtube.com/embed/ByXuk9QqQmc', 'Currently Running'),
('Jurassic Park', 'Sci-Fi', 'PG-13', 'A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting kids.', '', 'https://www.youtube.com/embed/lc0UehYemQA', 'Currently Running'),
---
('2001: A Space Odyssey', 'Sci-Fi', 'G', 'After discovering a mysterious artifact, mankind sets off on a quest with a sentient computer.', '', 'https://www.youtube.com/embed/oR_e9y-bka0', 'Coming Soon'),
('Casablanca', 'Romance', 'PG', 'A cynical American expatriate struggles to decide whether or not to help his former lover.', '', 'https://www.youtube.com/embed/BkL9l7qovsE', 'Coming Soon'),
('The Shining', 'Horror', 'R', 'A family heads to an isolated hotel for the winter where a sinister presence influences the father.', '', 'https://www.youtube.com/embed/5Cb3ik6zP2I', 'Coming Soon'),
('Singin in the Rain', 'Musical', 'G', 'A silent film star falls for a chorus girl just as talkies are beginning to take over.', '', 'https://www.youtube.com/embed/5_EVHeNEIJY', 'Coming Soon'),
('Seven Samurai', 'Action', 'NR', 'A veteran samurai gathers six others to help a village of farmers fight off bandits.', '', 'https://www.youtube.com/embed/7mw6LyyoeGE', 'Coming Soon');

INSERT INTO Showtime (movie_id, show_date, show_time)
VALUES 
(1, '2026-03-05', '14:00:00'), (1, '2026-03-05', '17:00:00'), (1, '2026-03-05', '20:00:00'),
(2, '2026-03-05', '14:00:00'), (2, '2026-03-05', '20:00:00'),
(3, '2026-03-05', '13:00:00'), (3, '2026-03-05', '19:00:00'),
(4, '2026-03-05', '11:00:00'), (4, '2026-03-05', '15:00:00'),
(5, '2026-03-05', '12:00:00'), (5, '2026-03-05', '18:00:00');