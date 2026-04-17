import { createBrowserRouter } from 'react-router';
import { Layout } from './components/layout';
import { ProtectedRoute } from './components/ProtectedRoute';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import SeatSelection from './pages/SeatSelection';
import Confirmation from './pages/Confirmation';
import { Bookings } from './pages/Bookings';
import SettingsLayout from './pages/SettingsLayout';
import EditProfile from './pages/EditProfile';
import EditMailingAddress from './pages/EditMailingAddress';
import PaymentCards from './pages/PaymentCards';
import ChangePassword from './pages/ChangePassword';
import Preferences from './pages/Preferences';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminHome from './pages/AdminHome';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import ManageMovies from './pages/ManageMovies';
import ManageShowtimes from './pages/ManageShowtimes';
import AddMovies from './pages/AddMovies';
import AdminMovieDetail from './pages/AdminMovieDetail';


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


      { path: 'admin',
        Component: ProtectedRoute,
        children: [
          { index: true,                      Component: AdminHome },
          { path: 'manage-movies',            Component: ManageMovies },
          { path: 'manage-movies/admin-movie/:id',          Component: AdminMovieDetail },
          { path: 'manage-movies/add-movies',  Component: AddMovies },
          { path: 'manage-movies/manage-showtimes',  Component: ManageShowtimes },
        ],
      },


      { path: 'forgot-password', Component: ForgotPassword },
      { path: 'reset-password', Component: ResetPassword },


      {
        path: 'settings',
        Component: ProtectedRoute,   
        children: [
          {
            Component: SettingsLayout,
            children: [
              { path: 'edit-profile',         Component: EditProfile },
              { path: 'edit-mailing-address', Component: EditMailingAddress },
              { path: 'payment-cards',        Component: PaymentCards },
              { path: 'security',             Component: ChangePassword },
              { path: 'appearance',           Component: Preferences},
            ],
          },
        ],
      },


    ],
  },
]);