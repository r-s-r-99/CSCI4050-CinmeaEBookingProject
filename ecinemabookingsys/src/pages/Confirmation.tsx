import { useLocation, useNavigate, useSearchParams } from 'react-router';
import { CheckCircle2, Calendar, Clock, MapPin, Armchair, Ticket, Mail } from 'lucide-react';
import { useEffect, useState } from 'react';

interface BookingData {
  booking_id: number;
  movie: any;
  showtime: any;
  seats: any[];
  totalPrice: number;
  bookingDate?: string;
  verified?: boolean;
}

export default function Confirmation() {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [booking, setBooking] = useState<BookingData | null>(location.state);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isEmailVerified, setIsEmailVerified] = useState(false);

  const bookingId = searchParams.get('booking_id');

  useEffect(() => {
    // If booking_id is in URL, fetch from API (email verified)
    if (bookingId) {
      setLoading(true);
      fetch(`/api/bookings/${bookingId}`, { credentials: 'include' })
        .then(res => res.json())
        .then(data => {
          if (data.booking) {
            setBooking(data.booking);
            setIsEmailVerified(true);
          } else {
            setError('Booking not found');
          }
        })
        .catch(err => {
          console.error('Error fetching booking:', err);
          setError('Failed to load booking');
        })
        .finally(() => setLoading(false));
    } else if (!booking) {
      // No booking in state and no booking_id in URL
      navigate('/');
    }
  }, [bookingId, booking, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Loading your booking...</p>
        </div>
      </div>
    );
  }

  if (error || !booking) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">{error || 'Booking not found'}</p>
          <button onClick={() => navigate('/')} className="px-4 py-2 bg-red-600 text-white rounded">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const bookingNumber = `BK${Date.now().toString().slice(-8)}`;

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Success Icon */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-4">
              <CheckCircle2 className="w-12 h-12 text-green-600" />
            </div>
            <h1 className="text-3xl mb-2">Booking Confirmed!</h1>
            <p className="text-gray-600">Your tickets have been successfully booked</p>
            {isEmailVerified && (
              <div className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-green-50 border border-green-200 rounded-lg">
                <Mail className="w-4 h-4 text-green-600" />
                <span className="text-sm text-green-700 font-medium">✓ Email Verified</span>
              </div>
            )}
          </div>

          {/* Booking Details */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 mb-6">
            <div className="flex items-center justify-between mb-6 pb-6 border-b">
              <div>
                <div className="text-sm text-gray-600 mb-1">Booking Number</div>
                <div className="text-2xl font-mono">{bookingNumber}</div>
              </div>
              <Ticket className="w-12 h-12 text-red-600" />
            </div>

            <div className="space-y-4">
              <div>
                <h2 className="text-2xl mb-1">{booking.movie.title}</h2>
                <div className="text-gray-600">{booking.movie.genre} • {booking.movie.rating}</div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-gray-600 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-600">Date</div>
                    <div>{booking.showtime.date}</div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Clock className="w-5 h-5 text-gray-600 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-600">Time</div>
                    <div>{booking.showtime.time}</div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <MapPin className="w-5 h-5 text-gray-600 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-600">Theater</div>
                    <div>{booking.showtime.theater}</div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Armchair className="w-5 h-5 text-gray-600 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-600">Seats</div>
                    <div>{booking.seats.map((s: any) => s.id).join(', ')}</div>
                  </div>
                </div>
              </div>

              {/* Order Summary - Ticket Breakdown */}
              <div className="pt-4 border-t">
                <h3 className="font-semibold text-lg mb-3">Order Summary</h3>

                {/* Seats with Details */}
                <div className="space-y-2 mb-4 bg-gray-50 p-3 rounded">
                  {booking.seats.map((seat: any, idx: number) => (
                    <div key={idx} className="flex items-center justify-between text-sm">
                      <div>
                        <span className="font-medium">{seat.id}</span>
                        <span className="text-gray-600 capitalize"> — {seat.category}</span>
                      </div>
                      <span className="font-medium">${[12, 8, 6][['adult', 'senior', 'child'].indexOf(seat.category)]}</span>
                    </div>
                  ))}
                </div>

                {/* Ticket Count Breakdown */}
                <div className="space-y-1 mb-4 pb-4 border-b text-sm">
                  {(() => {
                    const counts: Record<string, number> = {};
                    const prices: Record<string, number> = { adult: 12, senior: 8, child: 6 };
                    booking.seats.forEach((s: any) => {
                      counts[s.category] = (counts[s.category] || 0) + 1;
                    });
                    return Object.entries(counts).map(([category, count]) => (
                      <div key={category} className="flex justify-between">
                        <span className="capitalize">{count}x {category} ticket{count > 1 ? 's' : ''}</span>
                        <span>${(count * prices[category as keyof typeof prices]).toFixed(2)}</span>
                      </div>
                    ));
                  })()}
                </div>

                <div className="flex items-center justify-between text-xl">
                  <span className="font-semibold">Total Price (Before Tax):</span>
                  <span className="text-red-600 font-bold">${booking.totalPrice.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-3">
            <button
              onClick={() => navigate('/bookings')}
              className="w-full py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              View My Bookings
            </button>
            <button
              onClick={() => navigate('/')}
              className="w-full py-3 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Book Another Movie
            </button>
          </div>

          {/* Info */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Note:</strong> Please arrive at least 15 minutes before showtime. 
              Show this booking number at the counter to collect your tickets.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
