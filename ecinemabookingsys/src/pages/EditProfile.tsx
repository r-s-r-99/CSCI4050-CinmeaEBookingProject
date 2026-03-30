import { Home, Bell, Calendar, TrendingUp, User, Settings as SettingsIcon, ChevronLeft, Pen, Lock, HelpCircle, Palette, CreditCard, Check } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router';

const settingsMenuItems = [
  { id: 'edit-profile', label: 'Edit profile', icon: Pen },
  { id: 'edit-mailing-address', label: 'Edit Mailing Address', icon: Pen },
  { id: 'payment-cards', label: 'Payment Cards', icon: CreditCard},
  { id: 'security', label: 'Change Password', icon: Lock },
  { id: 'appearance', label: 'Preferences/Favorites', icon: Palette },
];

export default function EditProfile() {
  const [activeSection, setActiveSection] = useState('edit-profile');
  const [formData, setFormData] = useState({
    firstName: 'Allen',
    lastName: 'Chiu',
    email: 'asc73208@uga.edu',
    address: 'testing address',
    contactNumber: '678-862-6972',
    city: 'Athens',
    state: 'Georgia',
    password: 'need to be hidden',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
    alert('Profile updated successfully!');
  };

  const handleCancel = () => {
    // Reset form or navigate away
  };

  return (
    <div className="flex h-screen bg-white">

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto p-12">
          {/* Header */}
          <div className="flex items-center justify-between mb-12">
            <h1 className="text-4xl">Edit profile</h1>
            <div className="flex items-center gap-4">
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name Fields */}
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm mb-2">First Name</label>
                <input
                  type="text"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
              <div>
                <label className="block text-sm mb-2">Last Name</label>
                <input
                  type="text"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm mb-2">Email</label>
              <div className="relative">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
                <div className="absolute right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-red-500 rounded flex items-center justify-center">
                  <Lock className="w-4 h-4 text-white" />
                </div>
              </div>
            </div>

            {/* Contact Number */}
            <div>
              <label className="block text-sm mb-2">Phone Number</label>
              <input
                type="text"
                name="contactNumber"
                value={formData.contactNumber}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 pt-6">
              <button
                type="button"
                onClick={handleCancel}
                className="px-8 py-3 border-2 border-orange-500 text-orange-500 rounded-lg hover:bg-orange-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-12 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors"
              >
                Save
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}