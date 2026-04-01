import { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

interface PasswordForm {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}

interface ShowPasswords {
  currentPassword: boolean;
  newPassword: boolean;
  confirmPassword: boolean;
}

const PasswordInput = ({
  label,
  name,
  field,
  formData,
  showPasswords,
  handleChange,
  toggleShowPassword,
}: {
  label: string;
  name: keyof PasswordForm;
  field: keyof ShowPasswords;
  formData: PasswordForm;
  showPasswords: ShowPasswords;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  toggleShowPassword: (field: keyof ShowPasswords) => void;
}) => (
  <div className="mb-4">
    <label className="block text-sm text-gray-600 mb-1">{label}</label>
    <div className="relative">
      <input
        type={showPasswords[field] ? 'text' : 'password'}
        name={name}
        value={formData[name]}
        onChange={handleChange}
        className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm pr-10 focus:outline-none focus:ring-2 focus:ring-black"
      />
      <button
        type="button"
        onClick={() => toggleShowPassword(field)}
        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
      >
        {showPasswords[field] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
      </button>
    </div>
  </div>
);

export default function ChangePassword() {
  const [formData, setFormData] = useState<PasswordForm>({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [showPasswords, setShowPasswords] = useState<ShowPasswords>({
    currentPassword: false,
    newPassword: false,
    confirmPassword: false,
  });

  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [currentPasswordVerified, setCurrentPasswordVerified] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
    setSuccess(null);
  };

  const toggleShowPassword = (field: keyof ShowPasswords) => {
    setShowPasswords({ ...showPasswords, [field]: !showPasswords[field] });
  };

  const handleVerifyPassword = async () => {
    if (!formData.currentPassword) return;
    setIsVerifying(true);
    setError(null);

    try {
      const res = await fetch('/api/verify-password', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: formData.currentPassword }),
      });
      const data = await res.json();

      if (data.valid) {
        setCurrentPasswordVerified(true);
      } else {
        setError('Current password is incorrect.');
      }
    } catch {
      setError('Something went wrong.');
    } finally {
      setIsVerifying(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!currentPasswordVerified) {
      setError('Please verify your current password first.');
      return;
    }
    if (formData.newPassword !== formData.confirmPassword) {
      setError('New passwords do not match.');
      return;
    }
    if (formData.currentPassword === formData.newPassword) {
      setError('New password must be different from current password.');
      return;
    }
    if (formData.newPassword.length < 8) {
      setError('New password must be at least 8 characters.');
      return;
    }

    try {
      const res = await fetch('/api/change-password', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: formData.newPassword }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);

      setSuccess('Password changed successfully!');
      setFormData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setCurrentPasswordVerified(false);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-md">
      <h2 className="text-xl font-semibold mb-6">Change Password</h2>

      <form onSubmit={handleSubmit} className="border border-gray-200 rounded-xl p-6 bg-gray-50">

        <div className="mb-4">
          <label className="block text-sm text-gray-600 mb-1">Current Password</label>
          <div className="relative flex gap-2">
            <div className="relative flex-1">
              <input
                type={showPasswords.currentPassword ? 'text' : 'password'}
                name="currentPassword"
                value={formData.currentPassword}
                onChange={handleChange}
                disabled={currentPasswordVerified}
                className={`w-full border rounded-lg px-3 py-2 text-sm pr-10 focus:outline-none focus:ring-2 focus:ring-black ${currentPasswordVerified ? 'bg-green-50 border-green-400' : 'border-gray-300'
                  }`}
              />
              <button
                type="button"
                onClick={() => toggleShowPassword('currentPassword')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showPasswords.currentPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
            {!currentPasswordVerified && (
              <button
                type="button"
                onClick={handleVerifyPassword}
                disabled={isVerifying || !formData.currentPassword}
                className="px-3 py-2 bg-black text-white text-sm rounded-lg hover:bg-gray-800 disabled:opacity-50"
              >
                {isVerifying ? '...' : 'Verify'}
              </button>
            )}
            {currentPasswordVerified && (
              <span className="text-green-500 text-sm self-center">✓ Verified</span>
            )}
          </div>
        </div>

        <hr className="my-4 border-gray-200" />

        {/* New password fields — disabled until verified */}
        <div className={!currentPasswordVerified ? 'opacity-50 pointer-events-none' : ''}>
          <PasswordInput
            label="New Password"
            name="newPassword"
            field="newPassword"
            formData={formData}
            showPasswords={showPasswords}
            handleChange={handleChange}
            toggleShowPassword={toggleShowPassword}
          />
          <PasswordInput
            label="Confirm New Password"
            name="confirmPassword"
            field="confirmPassword"
            formData={formData}
            showPasswords={showPasswords}
            handleChange={handleChange}
            toggleShowPassword={toggleShowPassword}
          />
        </div>

        {/* Error message */}
        {error && (
          <p className="text-sm text-red-500 mb-4">{error}</p>
        )}

        {/* Success message */}
        {success && (
          <p className="text-sm text-green-500 mb-4">{success}</p>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
          >
            Change Password
          </button>
        </div>
      </form>
    </div>
  );
}