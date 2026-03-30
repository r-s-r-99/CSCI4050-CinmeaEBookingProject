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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError(null);
    setSuccess(null);
  };

  const toggleShowPassword = (field: keyof ShowPasswords) => {
    setShowPasswords({ ...showPasswords, [field]: !showPasswords[field] });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    // Validate new password matches confirm password
    if (formData.newPassword !== formData.confirmPassword) {
      setError('New passwords do not match.');
      return;
    }

    // Validate new password is different from current
    if (formData.currentPassword === formData.newPassword) {
      setError('New password must be different from current password.');
      return;
    }

    // Validate password length
    if (formData.newPassword.length < 8) {
      setError('New password must be at least 8 characters.');
      return;
    }

    try {
      // Make API call here
      // const response = await fetch('/api/change-password', {
      //   method: 'POST',
      //   body: JSON.stringify(formData),
      // });
      // if (!response.ok) throw new Error('Current password is incorrect.');

      setSuccess('Password changed successfully!');
      setFormData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err: any) {
      setError(err.message);
    }
  };

  const PasswordInput = ({
    label,
    name,
    field,
  }: {
    label: string;
    name: keyof PasswordForm;
    field: keyof ShowPasswords;
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

  return (
    <div className="max-w-md">
      <h2 className="text-xl font-semibold mb-6">Change Password</h2>

      <form onSubmit={handleSubmit} className="border border-gray-200 rounded-xl p-6 bg-gray-50">

        <PasswordInput
          label="Current Password"
          name="currentPassword"
          field="currentPassword"
        />

        <hr className="my-4 border-gray-200" />

        <PasswordInput
          label="New Password"
          name="newPassword"
          field="newPassword"
        />

        <PasswordInput
          label="Confirm New Password"
          name="confirmPassword"
          field="confirmPassword"
        />

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