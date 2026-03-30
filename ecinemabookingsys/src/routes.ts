import { createBrowserRouter } from 'react-router';
import { Layout } from './components/layout';
import { ProtectedRoute } from './components/ProtectedRoute';
import Home from './pages/Home';
import MovieDetail from './pages/MovieDetail';
import SeatSelection from './pages/SeatSelection';
import Confirmation from './pages/Confirmation';
import BookingPage from './pages/BookingPage';
import { Bookings } from './pages/Bookings';
import SettingsLayout from './pages/SettingsLayout';
import EditProfile from './pages/EditProfile';
import EditMailingAddress from './pages/EditMailingAddress';
import PaymentCards from './pages/PaymentCards';
import ChangePassword from './pages/ChangePassword';
import Preferences from './pages/Preferences';
import Login from './pages/Login';
import Register from './pages/Register';

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
              { path: 'appearance',           Component: Preferences },
            ],
          },
        ],
      },
    ],
  },
]);