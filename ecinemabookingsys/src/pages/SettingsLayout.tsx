import { useNavigate, useLocation, Outlet } from 'react-router';
import { Pen, CreditCard, Lock, Palette } from 'lucide-react';

const settingsMenuItems = [
  { id: 'edit-profile',         label: 'Edit Profile',          icon: Pen,        path: '/settings/edit-profile' },
  { id: 'edit-mailing-address', label: 'Edit Mailing Address',  icon: Pen,        path: '/settings/edit-mailing-address' },
  { id: 'payment-cards',        label: 'Payment Cards',         icon: CreditCard, path: '/settings/payment-cards' },
  { id: 'security',             label: 'Change Password',       icon: Lock,       path: '/settings/security' },
  { id: 'appearance',           label: 'Preferences/Favorites', icon: Palette,    path: '/settings/appearance' },
];

export default function SettingsLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="flex h-screen bg-white">
      {/* Sidebar */}
      <div className="w-72 bg-gray-50 border-r border-gray-200 p-6">
        <nav className="space-y-1">
          {settingsMenuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <button
                key={item.id}
                onClick={() => navigate(item.path)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive ? 'bg-white shadow-sm' : 'text-gray-600 hover:bg-white hover:text-gray-900'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Child route renders here */}
      <div className="flex-1 p-8">
        <Outlet />
      </div>
    </div>
  );
}