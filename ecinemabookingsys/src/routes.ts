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
import AdminHome from './pages/AdminHome';
import Profile from './pages/Profile';
import MockEmailConfirm from './pages/MockEmailConfirm';


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
      { path: 'adminhome', Component: AdminHome },
      { path: 'profile', Component: Profile },
      { path: 'mockemailconfirm', Component: MockEmailConfirm },
    ],
  },
]);
