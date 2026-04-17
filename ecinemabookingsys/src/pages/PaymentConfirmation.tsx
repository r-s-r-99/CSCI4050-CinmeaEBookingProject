import { useNavigate } from 'react-router';
import { Mail } from 'lucide-react';

export default function PaymentConfirmation() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-lg p-12 text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-6">
            <Mail className="w-12 h-12 text-blue-600" />
          </div>

          <h1 className="text-3xl font-bold mb-4">Payment Processed!</h1>
          <p className="text-xl text-gray-600 mb-6">Please check your email to confirm your booking.</p>

          <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded mb-8 text-left">
            <p className="text-gray-700">
              A confirmation link has been sent to your email address. <strong>Click the link in your email</strong> to complete and confirm your booking. The link will expire in 24 hours.
            </p>
          </div>

          <div className="space-y-3">
            <button
              onClick={() => navigate('/')}
              className="w-full px-6 py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
            >
              Continue Shopping
            </button>
            <button
              onClick={() => navigate('/bookings')}
              className="w-full px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
            >
              View My Bookings
            </button>
          </div>

          <p className="text-sm text-gray-500 mt-8">Didn't receive the email? Check your spam folder or contact support.</p>
        </div>
      </div>
    </div>
  );
}
