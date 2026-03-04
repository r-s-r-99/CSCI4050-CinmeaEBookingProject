export interface Movie {
  id: number;
  title: string;
  genre: string;
  rating: string;
  description: string;
  poster_url: string;
  trailer_url: string;
  status: string;
}

export interface Showtime {
  id: string;
  movieId: string;
  time: string;
  date: string;
  theater: string;
}

export interface Seat {
  id: string;
  row: string;
  number: number;
  status: 'available' | 'selected' | 'booked';
  type: 'regular' | 'vip';
}

export interface Booking {
  id: string;
  movie: Movie;
  showtime: Showtime;
  seats: Seat[];
  totalPrice: number;
  bookingDate: string;
}