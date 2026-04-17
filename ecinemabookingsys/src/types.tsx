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
  id: string | number;
  bookingId: string | number;
  movie: Movie;
  showtime: {
    showtimeId: string;
    movieId: string;
    roomId: string;
    showDate: string;
    showTime: string;
  };
  tickets: any[];
  totalPrice: number;
  bookingDate: string;
  userId: string | number;
}