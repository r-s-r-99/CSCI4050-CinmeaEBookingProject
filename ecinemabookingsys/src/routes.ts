import { createBrowserRouter } from 'react-router';
import { Layout } from './components/layout';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AdminRoute } from './components/AdminRoute';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import TicketSelection from './pages/TicketSelection';
import SeatSelection from './pages/SeatSelection';
import Checkout from './pages/Checkout';
import Payment from './pages/Payment';
import PaymentConfirmation from './pages/PaymentConfirmation';
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
import EditMovie from './pages/EditMovie';
import Recommended from './pages/Recommended';


export const router = createBrowserRouter([
  {
    path: '/',
    Component: Layout,
    children: [
      { index: true, Component: Home },
      { path: 'movie/:id', Component: MovieDetail },
      { path: 'booking/:showtimeId/tickets', Component: TicketSelection },
      { path: 'booking/:showtimeId', Component: SeatSelection },
      { path: 'checkout', Component: Checkout },
      { path: 'payment', Component: Payment },
      { path: 'payment-confirmation', Component: PaymentConfirmation },
      { path: 'confirmation', Component: Confirmation },
      { path: 'bookings', Component: Bookings },
      { path: 'login', Component: Login },
      { path: 'register', Component: Register },


      {
        path: 'admin',
        Component: ProtectedRoute,
        children: [
          { index: true, Component: AdminHome },
          { path: 'manage-movies', Component: ManageMovies },
          { path: 'manage-movies/admin-movie/:id', Component: AdminMovieDetail },
          { path: 'manage-movies/edit-movie/:id', Component: EditMovie },
          { path: 'manage-movies/add-movies', Component: AddMovies },
          { path: 'manage-movies/manage-showtimes', Component: ManageShowtimes }
        ],
      },


      { path: 'forgot-password', Component: ForgotPassword },
      { path: 'reset-password', Component: ResetPassword },


      {
        path: 'manage-movies',
        Component: AdminRoute,
        children: [{ index: true, Component: ManageMovies }],
      },
      {
        path: 'add-movies',
        Component: AdminRoute,
        children: [{ index: true, Component: AddMovies }],
      },

      {
        path: 'manage-showtimes',
        Component: AdminRoute,
        children: [{ index: true, Component: ManageShowtimes }],
      },
      {
        path: 'edit-movies/:id',
        Component: AdminRoute,
        children: [{ index: true, Component: EditMovie }],
      },
      {
        path: 'bookings',
        Component: ProtectedRoute,
        children: [{ index: true, Component: Bookings }],
      },
      {
        path: 'settings',
        Component: ProtectedRoute,
        children: [
          {
            Component: SettingsLayout,
            children: [
              { path: 'edit-profile', Component: EditProfile },
              { path: 'edit-mailing-address', Component: EditMailingAddress },
              { path: 'payment-cards', Component: PaymentCards },
              { path: 'security', Component: ChangePassword },
              { path: 'appearance', Component: Preferences },
              { path: 'recommended', Component: Recommended }
            ],
          },
        ],
      },


    ],
  },
]);