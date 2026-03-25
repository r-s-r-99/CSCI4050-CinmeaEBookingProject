import { Movie, Showtime } from '../types';

export const movies: Movie[] = [
  {
    id: '1',
    title: 'Velocity Rush',
    genre: 'Action',
    duration: 142,
    rating: 'PG-13',
    description: 'An adrenaline-pumping action thriller that follows an elite team on a mission to stop a global threat. Packed with explosive sequences and heart-stopping stunts.',
    image: 'https://images.unsplash.com/photo-1765510296004-614b6cc204da?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhY3Rpb24lMjBtb3ZpZSUyMHBvc3RlcnxlbnwxfHx8fDE3NzE2NzUwNDd8MA&ixlib=rb-4.1.0&q=80&w=1080',
    nowShowing: true,
  },
  {
    id: '2',
    title: 'Cosmic Horizon',
    genre: 'Sci-Fi',
    duration: 156,
    rating: 'PG-13',
    description: 'Journey to the edge of the universe in this visually stunning sci-fi epic. A crew of explorers discovers a mysterious signal that could change humanity forever.',
    image: 'https://images.unsplash.com/photo-1751823886813-0cfc86cb9478?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzY2llbmNlJTIwZmljdGlvbiUyMGNpbmVtYXxlbnwxfHx8fDE3NzE3MDU2NTh8MA&ixlib=rb-4.1.0&q=80&w=1080',
    nowShowing: true,
  },
  {
    id: '3',
    title: 'The Haunting',
    genre: 'Horror',
    duration: 98,
    rating: 'R',
    description: 'Terror lurks in every shadow in this spine-chilling horror experience. A family moves into their dream home, only to discover they are not alone.',
    image: 'https://images.unsplash.com/photo-1636337897543-83b55150608f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxob3Jyb3IlMjBtb3ZpZSUyMHRoZWF0ZXJ8ZW58MXx8fHwxNzcxNzA1NjU5fDA&ixlib=rb-4.1.0&q=80&w=1080',
    nowShowing: true,
  },
  {
    id: '4',
    title: 'Love in Paris',
    genre: 'Romance',
    duration: 112,
    rating: 'PG',
    description: 'A heartwarming romantic comedy about two strangers who meet by chance in the city of love. Sometimes the best things in life are unexpected.',
    image: 'https://images.unsplash.com/photo-1602837761734-dc0936210748?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyb21hbnRpYyUyMGNvbWVkeSUyMGNvdXBsZXxlbnwxfHx8fDE3NzE2MjM5Njd8MA&ixlib=rb-4.1.0&q=80&w=1080',
    nowShowing: true,
  },
  {
    id: '5',
    title: 'Adventure Kingdom',
    genre: 'Animation',
    duration: 95,
    rating: 'G',
    description: 'Join a brave young hero on an enchanting animated adventure through a magical kingdom. Perfect for the whole family!',
    image: 'https://images.unsplash.com/photo-1655532391070-ef6c6e922e39?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhbmltYXRlZCUyMGNoaWxkcmVuJTIwbW92aWV8ZW58MXx8fHwxNzcxNzA1NjYwfDA&ixlib=rb-4.1.0&q=80&w=1080',
    nowShowing: true,
  },
  {
    id: '6',
    title: 'Shadow Protocol',
    genre: 'Thriller',
    duration: 128,
    rating: 'R',
    description: 'A mind-bending thriller that keeps you guessing until the final frame. Nothing is as it seems in this game of deception and intrigue.',
    image: 'https://images.unsplash.com/photo-1563905463861-7d77975b3a44?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0aHJpbGxlciUyMHN1c3BlbnNlJTIwZGFya3xlbnwxfHx8fDE3NzE2MjYxOTR8MA&ixlib=rb-4.1.0&q=80&w=1080',
    nowShowing: false,
  },
];

export const showtimes: Showtime[] = [
  // Velocity Rush
  { id: 's1', movieId: '1', time: '10:00 AM', date: '2026-02-22', theater: 'Screen 1'},
  { id: 's2', movieId: '1', time: '1:30 PM', date: '2026-02-22', theater: 'Screen 1'},
  { id: 's3', movieId: '1', time: '5:00 PM', date: '2026-02-22', theater: 'Screen 2'},
  { id: 's4', movieId: '1', time: '8:30 PM', date: '2026-02-22', theater: 'Screen 1'},
  
  // Cosmic Horizon
  { id: 's5', movieId: '2', time: '11:00 AM', date: '2026-02-22', theater: 'Screen 3'},
  { id: 's6', movieId: '2', time: '2:30 PM', date: '2026-02-22', theater: 'Screen 3'},
  { id: 's7', movieId: '2', time: '6:00 PM', date: '2026-02-22', theater: 'Screen 3'},
  { id: 's8', movieId: '2', time: '9:30 PM', date: '2026-02-22', theater: 'Screen 3'},
  
  // The Haunting
  { id: 's9', movieId: '3', time: '12:00 PM', date: '2026-02-22', theater: 'Screen 4'},
  { id: 's10', movieId: '3', time: '3:00 PM', date: '2026-02-22', theater: 'Screen 4'},
  { id: 's11', movieId: '3', time: '7:00 PM', date: '2026-02-22', theater: 'Screen 4'},
  { id: 's12', movieId: '3', time: '10:00 PM', date: '2026-02-22', theater: 'Screen 4'},
  
  // Love in Paris
  { id: 's13', movieId: '4', time: '11:30 AM', date: '2026-02-22', theater: 'Screen 5'},
  { id: 's14', movieId: '4', time: '2:00 PM', date: '2026-02-22', theater: 'Screen 5'},
  { id: 's15', movieId: '4', time: '5:30 PM', date: '2026-02-22', theater: 'Screen 5'},
  { id: 's16', movieId: '4', time: '8:00 PM', date: '2026-02-22', theater: 'Screen 5'},
  
  // Adventure Kingdom
  { id: 's17', movieId: '5', time: '10:30 AM', date: '2026-02-22', theater: 'Screen 6'},
  { id: 's18', movieId: '5', time: '1:00 PM', date: '2026-02-22', theater: 'Screen 6'},
  { id: 's19', movieId: '5', time: '3:30 PM', date: '2026-02-22', theater: 'Screen 6'},
  { id: 's20', movieId: '5', time: '6:00 PM', date: '2026-02-22', theater: 'Screen 6'},
];

export function getMovieById(id: string): Movie | undefined {
  return movies.find(movie => movie.id === id);
}

export function getShowtimesByMovieId(movieId: string): Showtime[] {
  return showtimes.filter(showtime => showtime.movieId === movieId);
}

export function getShowtimeById(id: string): Showtime | undefined {
  return showtimes.find(showtime => showtime.id === id);
}