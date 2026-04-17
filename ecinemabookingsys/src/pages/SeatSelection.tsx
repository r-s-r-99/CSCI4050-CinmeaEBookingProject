import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { Movie, Showtime, Seat } from '../types';
import { ArrowLeft, Monitor } from 'lucide-react';

type TicketCategory = 'adult' | 'senior' | 'child';

const TICKET_PRICES: Record<TicketCategory, number> = {
  adult: 12,
  senior: 8,
  child: 6,
};

interface SeatWithCategory extends Seat {
  category: TicketCategory;
}

export default function SeatSelection() {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [showtime, setShowtime] = useState<Showtime | null>(null);
  const [seats, setSeats] = useState<Seat[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<TicketCategory>('adult');
  const [seatCategories, setSeatCategories] = useState<Record<string, TicketCategory>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/showtimes/detail/${showtimeId}`)
      .then(res => res.json())
      .then(data => {
        const s = data.showtime;
        setShowtime({
          id: String(s.showtime_id),
          movieId: String(s.movie_id),
          date: new Date(s.show_date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }),
          time: s.show_time,
          theater: `Showroom ${s.room_id}`,
        });
        return fetch(`/api/movies/${s.movie_id}`);
      })
      .then(res => res.json())
      .then(data => {
        const m = data.movie;
        setMovie({
          id: m.movie_id,
          title: m.title,
          genre: m.genre,
          rating: m.rating,
          description: m.description,
          poster_url: m.poster_url,
          trailer_url: m.trailer_url,
          status: m.status,
        });
      })
      .catch(err => console.error('Error:', err))
      .finally(() => setLoading(false));
  }, [showtimeId]);

  useEffect(() => {
    const rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const seatsPerRow = 12;
    const newSeats: Seat[] = [];
    rows.forEach((row) => {
      for (let i = 1; i <= seatsPerRow; i++) {
        const isBooked = Math.random() < 0.3;
        newSeats.push({
          id: `${row}${i}`,
          row,
          number: i,
          status: isBooked ? 'booked' : 'available',
          type: 'regular',
        });
      }
    });
    setSeats(newSeats);
  }, []);

  const toggleSeat = (seatId: string) => {
    setSeats(prev => prev.map(seat => {
      if (seat.id === seatId && seat.status !== 'booked') {
        if (seat.status === 'selected') {
          setSeatCategories(prev => {
            const updated = { ...prev };
            delete updated[seatId];
            return updated;
          });
          return { ...seat, status: 'available' };
        } else {
          setSeatCategories(prev => ({ ...prev, [seatId]: selectedCategory }));
          return { ...seat, status: 'selected' };
        }
      }
      return seat;
    }));
  };

  const selectedSeats = seats.filter(s => s.status === 'selected');
  const totalPrice = selectedSeats.reduce((sum, seat) => {
    const category = seatCategories[seat.id] || 'adult';
    return sum + TICKET_PRICES[category];
  }, 0);

  const handleConfirmBooking = () => {
    if (selectedSeats.length === 0) return;
    const seatsWithCategory: SeatWithCategory[] = selectedSeats.map(seat => ({
      ...seat,
      category: seatCategories[seat.id] || 'adult',
    }));
    const booking = {
      showtime: showtime!,
      movie: movie!,
      seats: seatsWithCategory,
      totalPrice,
    };
    const existingBookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    existingBookings.push({
      ...booking,
      id: Date.now().toString(),
      bookingDate: new Date().toISOString(),
    });
    localStorage.setItem('bookings', JSON.stringify(existingBookings));
    navigate('/confirmation', { state: booking });
  };

  if (loading) {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Loading...</div>;
  }

  if (!showtime || !movie) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl mb-4">Showtime not found</h2>
          <button onClick={() => navigate('/')} className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
            Back to Home
          </button>
        </div>
      </div>
    );
  }
  
  const seatsByRow = seats.reduce((acc, seat) => {
    if (!acc[seat.row]) acc[seat.row] = [];
    acc[seat.row].push(seat);
    return acc;
  }, {} as Record<string, Seat[]>);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6">
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-8">
            <h1 className="text-3xl mb-2">{movie.title}</h1>
            <p className="text-gray-600">{showtime.theater} • {showtime.time} • {showtime.date}</p>
          </div>

          {/* Ticket Category Selector */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold mb-3">Select Ticket Type</h2>
            <div className="flex gap-3 flex-wrap">
              {(Object.entries(TICKET_PRICES) as [TicketCategory, number][]).map(([category, price]) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-5 py-3 rounded-lg border-2 transition-colors capitalize ${
                    selectedCategory === category
                      ? 'border-red-600 bg-red-50 text-red-600'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-semibold">{category}</div>
                  <div className="text-sm">${price}.00</div>
                </button>
              ))}
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Select a ticket type, then click seats to assign it.
            </p>
          </div>

          {/* Screen */}
          <div className="mb-12">
            <div className="flex justify-center mb-4">
              <div className="w-3/4 h-2 bg-gradient-to-b from-gray-400 to-gray-200 rounded-t-full"></div>
            </div>
            <div className="flex items-center justify-center gap-2 text-gray-600 text-sm">
              <Monitor className="w-4 h-4" />
              <span>SCREEN</span>
            </div>
          </div>

          {/* Seats */}
          <div className="mb-8 overflow-x-auto">
            <div className="inline-block min-w-full">
              {Object.entries(seatsByRow).map(([row, rowSeats]) => (
                <div key={row} className="flex items-center justify-center gap-2 mb-2">
                  <span className="w-8 text-center text-gray-600">{row}</span>
                  <div className="flex gap-2">
                    {rowSeats.map((seat, index) => {
                      const category = seatCategories[seat.id];
                      const isAisle = index === 5;

                      const seatColor =
                        seat.status === 'booked' ? 'bg-red-300 cursor-not-allowed' :
                        seat.status === 'selected' && category === 'adult' ? 'bg-blue-500 hover:bg-blue-600' :
                        seat.status === 'selected' && category === 'senior' ? 'bg-purple-500 hover:bg-purple-600' :
                        seat.status === 'selected' && category === 'child' ? 'bg-green-500 hover:bg-green-600' :
                        'bg-gray-200 hover:bg-gray-300';

                      return (
                        <div key={seat.id} className="flex gap-2">
                          {isAisle && <div className="w-4" />}
                          <button
                            onClick={() => toggleSeat(seat.id)}
                            disabled={seat.status === 'booked'}
                            className={`w-8 h-8 rounded-t-lg transition-colors ${seatColor}`}
                            title={seat.status === 'selected' ? `${seat.id} - ${category}` : seat.id}
                          />
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-6 justify-center mb-8 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-gray-200 rounded-t-lg"></div>
              <span>Available</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-500 rounded-t-lg"></div>
              <span>Adult (${TICKET_PRICES.adult})</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-purple-500 rounded-t-lg"></div>
              <span>Senior (${TICKET_PRICES.senior})</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-green-500 rounded-t-lg"></div>
              <span>Child (${TICKET_PRICES.child})</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-red-300 rounded-t-lg"></div>
              <span>Booked</span>
            </div>
          </div>

          {/* Booking Summary */}
          <div className="border-t pt-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-gray-600 mb-1">Selected Seats:</div>
                {selectedSeats.length > 0 ? (
                  <div className="space-y-1">
                    {selectedSeats.map(s => (
                      <div key={s.id} className="text-sm">
                        <span className="font-medium">{s.id}</span>
                        <span className="text-gray-500 capitalize"> — {seatCategories[s.id]} (${TICKET_PRICES[seatCategories[s.id]]})</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div>None</div>
                )}
              </div>
              <div className="text-right">
                <div className="text-gray-600">Total Price:</div>
                <div className="text-3xl text-red-600">${totalPrice.toFixed(2)}</div>
              </div>
            </div>
            <button
              onClick={handleConfirmBooking}
              disabled={selectedSeats.length === 0}
              className="w-full py-4 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors text-lg"
            >
              Confirm Booking
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}