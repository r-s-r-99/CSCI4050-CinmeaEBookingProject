import { Home, Bell, Calendar, TrendingUp, User, Settings as SettingsIcon, ChevronLeft, Pen, Lock, HelpCircle, Palette, Check } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router';

const settingsMenuItems = [
  { id: 'edit-profile', label: 'Edit profile', icon: Pen },
  { id: 'notification', label: 'Notification', icon: Bell },
  { id: 'security', label: 'Security', icon: Lock },
  { id: 'appearance', label: 'Appearance', icon: Palette },
  { id: 'help', label: 'Help', icon: HelpCircle },
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
    aptNumber: '101',
    houseNumber: '123',
    zipCode: '30601',
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
            <h1 className="text-4xl">Mailing Address</h1>
            <div className="flex items-center gap-4">
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">

            {/* Address */}
            <div>
              <label className="block text-sm mb-2">Street Address</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>

            <div>
              <label className="block text-sm mb-2">Zip Code</label>
              <input
                type="text"
                name="zipCode"
                value={formData.zipCode}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm mb-2">House Number</label>
                <input
                  type="text"
                  name="houseNumber"
                  value={formData.houseNumber}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
              <div>
                <label className="block text-sm mb-2">Apartment Number</label>
                <input
                  type="text"
                  name="aptNumber"
                  value={formData.aptNumber}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
            </div>

            {/* City and State */}
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm mb-2">City</label>
                <input
                  type="text"
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
              <div>
                <label className="block text-sm mb-2">State</label>
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
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