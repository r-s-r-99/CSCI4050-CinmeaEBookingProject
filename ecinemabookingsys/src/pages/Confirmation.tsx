import { useLocation, useNavigate } from 'react-router';
import { CheckCircle2, Calendar, Clock, MapPin, Armchair, Ticket } from 'lucide-react';
import { useEffect } from 'react';

export default function Confirmation() {
  const location = useLocation();
  const navigate = useNavigate();
  const booking = location.state;

  useEffect(() => {
    if (!booking) {
      navigate('/');
    }
  }, [booking, navigate]);

  if (!booking) {
    return null;
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

              <div className="pt-4 border-t">
                <div className="flex items-center justify-between text-xl">
                  <span>Total Paid:</span>
                  <span className="text-red-600">${booking.totalPrice.toFixed(2)}</span>
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
