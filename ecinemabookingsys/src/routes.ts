import { createBrowserRouter } from 'react-router';
import { Layout } from './components/layout';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import SeatSelection from './pages/SeatSelection';
import Confirmation from './pages/Confirmation';
import BookingPage from './pages/BookingPage';
import { Bookings } from './pages/Bookings';
import Login from './pages/Login';
import Register from './pages/Register';
<<<<<<< HEAD
import AdminHome from './pages/AdminHome';
=======
>>>>>>> 8be98aec0653c67effbcb9c085b185255649a10d

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
      { path: 'login', Component: Login },
      { path: 'register', Component: Register },
<<<<<<< HEAD
      { path: 'adminhome', Component: AdminHome },
    ],
  },
]);
=======
    ],
  },
]);
>>>>>>> 8be98aec0653c67effbcb9c085b185255649a10d
