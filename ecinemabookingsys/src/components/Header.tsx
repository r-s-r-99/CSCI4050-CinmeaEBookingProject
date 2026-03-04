import { Film, Ticket, User } from 'lucide-react';
import { Link, useLocation } from 'react-router';

export function Header() {
  const location = useLocation();
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-gray-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-2xl">
            <Film className="w-8 h-8 text-red-500" />
            <span>CineBook</span>
          </Link>
          
          <nav className="flex items-center gap-6">
            <Link
              to="/"
              className={`flex items-center gap-2 hover:text-red-400 transition-colors ${
                isActive('/') ? 'text-red-400' : ''
              }`}
            >
              <Film className="w-5 h-5" />
              <span>Movies</span>
            </Link>
            <Link
              to="/bookings"
              className={`flex items-center gap-2 hover:text-red-400 transition-colors ${
                isActive('/bookings') ? 'text-red-400' : ''
              }`}
            >
              <Ticket className="w-5 h-5" />
              <span>My Bookings</span>
            </Link>
            <button className="flex items-center gap-2 hover:text-red-400 transition-colors">
              <User className="w-5 h-5" />
              <span>Account</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}
