import { Pen, Lock, Bell, HelpCircle, Palette } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function EditMailingAddress() {
  const [formData, setFormData] = useState({
    street: '',
    zipCode: '',
    houseNumber: '',
    apt: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch('/api/retrieve-mailing-address', { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error('Failed to load address');
        return res.json();
      })
      .then(data => {
        setFormData({
          street:      data.street ?? '',
          zipCode:     data.zip ?? '',
          houseNumber: data.houseNumber ?? '',
          apt:         data.apt ?? '',
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
    const res = await fetch('/api/update-mailing-address', {
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
    setLoading(true);
    fetch('/api/retrieve-mailing-address', { credentials: 'include' })
      .then(res => res.json())
      .then(data => {
        setFormData({
          street:      data.street ?? '',
          zipCode:     data.zip ?? '',
          houseNumber: data.houseNumber ?? '',
          apt:         data.apt ?? '',
        });
        setLoading(false);
      });
  };

  if (loading) return (
    <div className="flex items-center justify-center h-full text-gray-500">
      Loading address...
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
            <h1 className="text-4xl">Mailing Address</h1>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm mb-2">Street Address</label>
              <input
                type="text"
                name="street"
                value={formData.street}
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
                  name="apt"
                  value={formData.apt}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
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