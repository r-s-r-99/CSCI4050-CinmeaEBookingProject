import { Film, Ticket, User, LogOut, ShieldCheck } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router';
import { useEffect, useState } from 'react';

interface AuthState {
  isLoggedIn: boolean;
  role?: string;
}

export function Header() {
  const location = useLocation();
  const navigate = useNavigate();
  const [auth, setAuth] = useState<AuthState>({ isLoggedIn: false });

  const isActive = (path: string) => location.pathname === path;

  // Check session on mount and route changes
  useEffect(() => {
    fetch('/api/me', { credentials: 'include' })
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data?.user_id) {
          setAuth({ isLoggedIn: true, role: data.role });
        } else {
          setAuth({ isLoggedIn: false });
        }
      })
      .catch(() => setAuth({ isLoggedIn: false }));
  }, [location.pathname]);

  const handleLogout = async () => {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' });
    setAuth({ isLoggedIn: false });
    navigate('/login');
  };

  return (
    <header className="bg-gray-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-2xl">
            <Film className="w-8 h-8 text-red-500" />
            <span>Cinema E-Booking System</span>
          </Link>

          <nav className="flex items-center gap-6">
            <Link
              to="/"
              className={`flex items-center gap-2 hover:text-red-400 transition-colors ${isActive('/') ? 'text-red-400' : ''
                }`}
            >
              <Film className="w-5 h-5" />
              <span>Movies</span>
            </Link>
            {auth.isLoggedIn && (
              <Link
                to="/bookings"
                className={`flex items-center gap-2 hover:text-red-400 transition-colors ${isActive('/bookings') ? 'text-red-400' : ''}`}
              >
                <Ticket className="w-5 h-5" />
                <span>My Order History</span>
              </Link>
            )}

            {auth.isLoggedIn && auth.role === 'admin' && (
              <Link
                to="/admin"
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border transition-colors ${isActive('/admin')
                    ? 'bg-purple-600 border-purple-500 text-white'
                    : 'border-purple-500 text-purple-400 hover:bg-purple-600 hover:text-white'
                  }`}
              >
                <ShieldCheck className="w-4 h-4" />
                <span>Admin Panel</span>
              </Link>
            )}

            {auth.isLoggedIn && (
              <Link
                to="/settings/edit-profile"
                className={`flex items-center gap-2 hover:text-red-400 transition-colors ${isActive('/settings/edit-profile') ? 'text-red-400' : ''
                  }`}
              >
                <User className="w-5 h-5" />
                <span>Profile</span>
              </Link>
            )}

            {auth.isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            ) : (
              <Link
                to="/login"
                className="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
              >
                Sign In
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}