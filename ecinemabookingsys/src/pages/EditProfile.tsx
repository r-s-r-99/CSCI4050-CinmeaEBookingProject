import { Lock, Pen, CreditCard, Palette } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function EditProfile() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phoneNumber: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch('/api/retrieve-edit-profile', { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error('Failed to load profile');
        return res.json();
      })
      .then(data => {
        setFormData({
          firstName: data.firstName ?? '',
          lastName: data.lastName ?? '',
          email: data.email ?? '',
          phoneNumber: data.phoneNumber ?? '',
        });
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/update-profile', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    }
  };

  const handleCancel = () => {
    // re-fetch to reset form to DB values
    setLoading(true);
    fetch('/api/retrieve-edit-profile', { credentials: 'include' })
      .then(res => res.json())
      .then(data => {
        setFormData({
          firstName: data.firstName ?? '',
          lastName: data.lastName ?? '',
          email: data.email ?? '',
          phoneNumber: data.phoneNumber ?? '',
        });
        setLoading(false);
      });
  };

  if (loading) return (
    <div className="flex items-center justify-center h-full text-gray-500">
      Loading profile...
    </div>
  );

  if (error) return (
    <div className="flex items-center justify-center h-full text-red-500">
      {error}
    </div>
  );

  return (
    <div className="flex h-screen bg-white">
      <div className="flex-1 overflow-auto">
        <div className="max-w-4xl mx-auto p-12">
          <div className="flex items-center justify-between mb-12">
            <h1 className="text-4xl">Edit profile</h1>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
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

            <div>
              <label className="block text-sm mb-2">Email</label>
              <div className="relative">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  disabled
                  className="w-full px-4 py-3 pr-12 border border-gray-200 rounded-lg bg-gray-50 text-gray-500 cursor-not-allowed"
                />
                <div className="absolute right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-red-500 rounded flex items-center justify-center">
                  <Lock className="w-4 h-4 text-white" />
                </div>
              </div>
              <p className="text-xs text-gray-400 mt-1">Email cannot be changed</p>
            </div>

            <div>
              <label className="block text-sm mb-2">Phone Number</label>
              <input
                type="text"
                name="phoneNumber"
                value={formData.phoneNumber}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>

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
                {saved ? 'Saved ✓' : 'Save'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}