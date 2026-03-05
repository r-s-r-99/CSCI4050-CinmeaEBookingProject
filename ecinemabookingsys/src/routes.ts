import { createBrowserRouter } from 'react-router';
import { Layout } from './components/layout';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import SeatSelection from './pages/SeatSelection';
import Confirmation from './pages/Confirmation';
import BookingPage from './pages/BookingPage';
import { Bookings } from './pages/Bookings';

export const router = createBrowserRouter([
  {
    path: '/',
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: 'movie/:id', Component: MovieDetail },
      { path: 'booking/:showtimeId', Component: SeatSelection },
      { path: 'confirmation', Component: Confirmation },
      { path: 'bookings', Component: Bookings },
    ],
  },
]);
