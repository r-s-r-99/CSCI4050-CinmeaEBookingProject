export interface Movie {
  id: string;
  title: string;
  genre: string;
  duration: number;
  rating: string;
  description: string;
  image: string;
  nowShowing: boolean;
}

export interface Showtime {
  id: string;
  movieId: string;
  time: string;
  date: string;
  theater: string;
  price: number;
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