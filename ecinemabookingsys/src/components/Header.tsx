import { Film, Ticket, User, LogIn, LogOut } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router';

export function Header() {
  const location = useLocation();
  const navigate = useNavigate();

  //Check if the user is currently logged in
  const userString = sessionStorage.getItem('user');
  //If the user exists in the current session, assign it to the user constant. It stays null if the user is not found.
  const user = userString ? JSON.parse(userString) : null;
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  //Handle the logout
  const handleLogout = () => {
    sessionStorage.clear();
    navigate('/');
    //Refresh the page upon logout (feels reassuring when it refreshes)
    window.location.reload();
  }; //handleLogout

  return (
    <header className="bg-gray-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-2xl">
            <Film className="w-8 h-8 text-red-500" />
            <span>Cinema E-Booking System</span>
          </Link>
          
          {/*the Movies tab is available regardless if a user is logged in or not*/}
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

            {user ? (
              <>
              {/*These only appear when the user is logged in: Movies, My Bookings, Profile, Logout*/}
              <Link
                to="/bookings"
                className={`flex items-center gap-2 hover:text-red-400 transition-colors ${
                  isActive('/bookings') ? 'text-red-400' : ''
                }`}
              >
                <Ticket className="w-5 h-5" />
                <span>My Bookings</span>
              </Link>

              <Link
                to="/editprofile"
                className={`flex items-center gap-2 hover:text-red-400 transition-colors ${
                  isActive('/editprofile') ? 'text-red-400' : ''
                }`}
              >
                <User className="w-5 h-5" />
                <span>Profile</span>
              </Link>

              <button onClick={handleLogout} 
                className={`flex items-center gap-2 hover:text-red-400 transition-colors ${
                  isActive('/editprofile') ? 'text-red-400' : ''
                  }`}
                >
                  <LogOut className="w-5 h-5"/>
                  <span>Log Out</span>
                </button>
              </>
            ) : (
            <>
            {/*These only appear when the user is logged out: Movies, Login*/}
            <Link
              to="/login"
              className={`flex items-center gap-2 hover:text-red-400 transition-colors ${
                isActive('/login') ? 'text-red-400' : ''
              }`}
            >
            <LogIn className="w-5 h-5" />
            <span>Log In</span>
          </Link>

          </>
        )}

          </nav>
        </div>
      </div>
    </header>
  );
}