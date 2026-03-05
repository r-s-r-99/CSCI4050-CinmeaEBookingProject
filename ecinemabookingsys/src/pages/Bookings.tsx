import { useEffect, useState } from 'react';
import { Calendar, Clock, MapPin, Armchair, Trash2 } from 'lucide-react';
import { Booking } from '../types';

export function Bookings() {
  const [bookings, setBookings] = useState<Booking[]>([]);

  useEffect(() => {
    const storedBookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    setBookings(storedBookings);
  }, []);

  const handleDelete = (bookingId: string) => {
    const updatedBookings = bookings.filter(b => b.id !== bookingId);
    setBookings(updatedBookings);
    localStorage.setItem('bookings', JSON.stringify(updatedBookings));
  };

  if (bookings.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-32">
        <div className="text-center">
          <div className="text-6xl mb-4">🎬</div>
          <h2 className="text-2xl mb-2">No Bookings Yet</h2>
          <p className="text-gray-600 mb-6">Start by booking your favorite movies!</p>
          <a
            href="/"
            className="inline-block px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Browse Movies
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl mb-8">My Bookings</h1>

        <div className="space-y-6">
          {bookings.map(booking => (
            <div key={booking.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="md:flex">
                <div className="md:w-48 h-64 md:h-auto">
                  <img
                    src={booking.movie.image}
                    alt={booking.movie.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex-1 p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h2 className="text-2xl mb-1">{booking.movie.title}</h2>
                      <div className="text-gray-600">
                        {booking.movie.genre} • {booking.movie.rating}
                      </div>
                    </div>
                    <button
                      onClick={() => handleDelete(booking.id)}
                      className="text-red-600 hover:text-red-700 p-2 hover:bg-red-50 rounded-lg transition-colors"
                      title="Cancel Booking"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="grid sm:grid-cols-2 gap-4 mb-4">
                    <div className="flex items-center gap-3">
                      <Calendar className="w-5 h-5 text-gray-600" />
                      <div>
                        <div className="text-sm text-gray-600">Date</div>
                        <div>{booking.showtime.date}</div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <Clock className="w-5 h-5 text-gray-600" />
                      <div>
                        <div className="text-sm text-gray-600">Time</div>
                        <div>{booking.showtime.time}</div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <MapPin className="w-5 h-5 text-gray-600" />
                      <div>
                        <div className="text-sm text-gray-600">Theater</div>
                        <div>{booking.showtime.theater}</div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <Armchair className="w-5 h-5 text-gray-600" />
                      <div>
                        <div className="text-sm text-gray-600">Seats</div>
                        <div>{booking.seats.map(s => s.id).join(', ')}</div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t">
                    <div className="text-sm text-gray-600">
                      Booked on {new Date(booking.bookingDate).toLocaleDateString()}
                    </div>
                    <div className="text-2xl text-red-600">
                      ${booking.totalPrice.toFixed(2)}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}