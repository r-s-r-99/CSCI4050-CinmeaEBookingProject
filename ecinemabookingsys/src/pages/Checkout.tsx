import { useLocation, useNavigate } from 'react-router';
import { ArrowLeft, Mail, AlertCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

const TICKET_PRICES: Record<string, number> = {
  adult: 12,
  senior: 8,
  child: 6,
};

export default function Checkout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isValidEmail, setIsValidEmail] = useState(true);

  const booking = location.state?.booking;

  useEffect(() => {
    if (!booking) {
      navigate('/');
      return;
    }

    // Fetch current user's email from profile
    fetch('/api/retrieve-edit-profile', { credentials: 'include' })
      .then(res => res.json())
      .then(data => {
        if (data.email) {
          setEmail(data.email);
        }
      })
      .catch(err => console.error('Error fetching user profile:', err));
  }, [booking, navigate]);

  const validateEmail = (emailValue: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    setIsValidEmail(emailRegex.test(emailValue));
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newEmail = e.target.value;
    setEmail(newEmail);
    validateEmail(newEmail);
  };

  const handleContinue = async () => {
    if (!isValidEmail || !email) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/bookings/create-temporary', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          showtime_id: booking.showtime.id,
          seats: booking.seats.map((s: any) => ({
            seat_id: s.id, // Seat identifier (e.g., "A1", "B5")
            ticket_type: s.category,
            ticket_price: TICKET_PRICES[s.category],
          })),
          email,
          total_price: booking.totalPrice,
          movie_details: {
            title: booking.movie.title,
            showtime: `${booking.showtime.date} at ${booking.showtime.time}`,
          },
        }),
      });

      if (!response.ok) {
        const error_data = await response.json();
        throw new Error(error_data.error || 'Failed to process booking');
      }

      const data = await response.json();
      navigate('/payment', { state: { temp_booking_token: data.temp_booking_token, booking } });
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      setLoading(false);
    }
  };

  if (!booking) {
    return null;
  }

  const selectedSeatsCount = booking.seats.length;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        <div className="bg-white rounded-lg shadow-lg p-12">
          <h1 className="text-4xl font-bold mb-10">Order Summary & Confirmation</h1>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Left Column: Order Summary */}
            <div>
              {/* Movie Details */}
              <div className="mb-8 pb-8 border-b">
                <div className="flex gap-6">
                  <img src={booking.movie.poster_url} alt={booking.movie.title} className="w-24 h-32 rounded object-cover" />
                  <div>
                    <h2 className="text-2xl font-bold mb-2">{booking.movie.title}</h2>
                    <p className="text-gray-600 mb-2">{booking.movie.genre} • {booking.movie.rating}</p>
                    <div className="space-y-1 text-sm">
                      <p><span className="font-semibold">Showtime:</span> {booking.showtime.date} at {booking.showtime.time}</p>
                      <p><span className="font-semibold">Theater:</span> {booking.showtime.theater}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Seats & Pricing Breakdown */}
              <div>
                <h3 className="font-semibold text-lg mb-4">Selected Seats</h3>
                <div className="bg-gray-50 p-4 rounded mb-4 space-y-2">
                  {booking.seats.map((seat: any, idx: number) => (
                    <div key={idx} className="flex justify-between text-sm">
                      <div>
                        <span className="font-medium">{seat.id}</span>
                        <span className="text-gray-600 capitalize"> — {seat.category}</span>
                      </div>
                      <span className="font-medium">${TICKET_PRICES[seat.category]}</span>
                    </div>
                  ))}
                </div>

                {/* Price Breakdown */}
                <div className="space-y-2 mb-6 pb-6 border-b">
                  {(() => {
                    const counts: Record<string, number> = {};
                    booking.seats.forEach((s: any) => {
                      counts[s.category] = (counts[s.category] || 0) + 1;
                    });
                    return Object.entries(counts).map(([category, count]) => (
                      <div key={category} className="flex justify-between text-sm">
                        <span className="capitalize">{count}x {category} ticket{count > 1 ? 's' : ''}</span>
                        <span>${(count * TICKET_PRICES[category]).toFixed(2)}</span>
                      </div>
                    ));
                  })()}
                </div>

                <div className="flex justify-between text-lg font-bold">
                  <span>Total:</span>
                  <span className="text-red-600">${booking.totalPrice.toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* Right Column: Email Confirmation */}
            <div className="bg-gray-50 p-8 rounded-lg">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                <Mail className="w-5 h-5 text-red-600" />
                Email Confirmation
              </h3>

              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 flex items-start gap-2">
                  <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                  <p>{error}</p>
                </div>
              )}

              <div className="mb-6">
                <label className="block text-sm font-semibold mb-3">Email Address</label>
                <input
                  type="email"
                  value={email}
                  onChange={handleEmailChange}
                  className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none transition ${
                    isValidEmail ? 'border-gray-300 focus:border-red-600' : 'border-red-300 focus:border-red-600'
                  }`}
                  placeholder="your@email.com"
                />
                {!isValidEmail && email && <p className="text-red-600 text-sm mt-2">Please enter a valid email</p>}
              </div>

              <div className="space-y-3 mb-8">
                <p className="text-sm text-gray-700">
                  <strong>✓</strong> Verification link will be sent to your email
                </p>
                <p className="text-sm text-gray-700">
                  <strong>✓</strong> Click link in email to confirm booking
                </p>
                <p className="text-sm text-gray-700">
                  <strong>✓</strong> Booking expires in 24 hours
                </p>
              </div>

              <button
                onClick={handleContinue}
                disabled={loading || !isValidEmail || !email}
                className="w-full bg-red-600 text-white py-4 rounded-lg font-semibold hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors text-lg"
              >
                {loading ? 'Processing...' : 'Continue to Payment'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
