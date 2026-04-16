import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router';
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
  const location = useLocation();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [showtime, setShowtime] = useState<Showtime | null>(null);
  const [seats, setSeats] = useState<Seat[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<TicketCategory>('adult');
  const [seatCategories, setSeatCategories] = useState<Record<string, TicketCategory>>({});
  const [loading, setLoading] = useState(true);

  // Ticket selection state
  const [requiredTickets, setRequiredTickets] = useState<TicketCategory[]>([]);
  const [validationError, setValidationError] = useState<string>('');

  useEffect(() => {
    // Extract ticket selection data if provided
    const state = location.state as any;
    if (state?.ticketSelection) {
      setRequiredTickets(state.ticketSelection.categories);
      // Pre-set first category
      if (state.ticketSelection.categories.length > 0) {
        setSelectedCategory(state.ticketSelection.categories[0]);
      }
    }

    fetch(`/api/showtimes/detail/${showtimeId}`)
      .then(res => res.json())
      .then(data => {
        const s = data.showtime;
        setShowtime({
          id: String(s.showtime_id),
          movieId: String(s.movie_id),
          date: new Date(s.show_date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }),
          time: s.show_time,
          theater: 'Main Theater',
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
  }, [showtimeId, location.state]);

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
          setValidationError('');
          return { ...seat, status: 'available' };
        } else {
          // Determine which category to assign
          let categoryToAssign = selectedCategory;

          if (requiredTickets.length > 0) {
            // Count already assigned seats
            const selectedSeatsCount = Object.keys(seatCategories).length;
            if (selectedSeatsCount < requiredTickets.length) {
              // Auto-assign the next required category
              categoryToAssign = requiredTickets[selectedSeatsCount];
            }
          }

          setSeatCategories(prev => ({ ...prev, [seatId]: categoryToAssign }));

          // Check if we now have the correct number of seats
          if (requiredTickets.length > 0) {
            const willHaveCount = Object.keys(seatCategories).length + 1;
            if (willHaveCount === requiredTickets.length) {
              setValidationError('');
            } else if (willHaveCount > requiredTickets.length) {
              setValidationError(`You've selected too many seats. You need ${requiredTickets.length} ticket(s).`);
            }
          }

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
    // Validate ticket count if required tickets are specified
    if (requiredTickets.length > 0 && selectedSeats.length !== requiredTickets.length) {
      setValidationError(`You must select exactly ${requiredTickets.length} seat(s), but you've selected ${selectedSeats.length}.`);
      return;
    }

    if (selectedSeats.length === 0) return;

    // Check if user is authenticated before proceeding to checkout
    fetch('/api/me', { credentials: 'include' })
      .then(res => {
        if (!res.ok) {
          // Not authenticated - redirect to login with booking data
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
          navigate('/login', { state: { redirectTo: 'checkout', booking } });
          return null;
        }
        return res.json();
      })
      .then(user => {
        if (user === null) return; // Already handled redirect above

        // User is authenticated, proceed with checkout
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
        navigate('/checkout', { state: { booking } });
      })
      .catch(err => {
        console.error('Error checking authentication:', err);
        setValidationError('An error occurred. Please try again.');
      });
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
            {requiredTickets.length > 0 && (
              <div className="mb-4 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
                <p className="text-blue-800 font-medium">Ticket Requirements:</p>
                <p className="text-blue-700 text-sm mt-1">
                  You need to select {requiredTickets.length} seat(s) with the following categories:
                </p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {requiredTickets.map((cat, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-white border border-blue-300 rounded text-sm font-medium capitalize"
                    >
                      {cat} (${TICKET_PRICES[cat]})
                    </span>
                  ))}
                </div>
              </div>
            )}
            {requiredTickets.length === 0 && (
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
            )}
            {requiredTickets.length === 0 && (
              <p className="text-sm text-gray-500 mt-2">
                Select a ticket type, then click seats to assign it.
              </p>
            )}
            {requiredTickets.length > 0 && (
              <p className="text-sm text-gray-600 mt-2">
                Seats will be automatically assigned to match your ticket requirements.
              </p>
            )}
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
            {validationError && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {validationError}
              </div>
            )}
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-gray-600 mb-1">
                  Selected Seats: {selectedSeats.length}
                  {requiredTickets.length > 0 && ` / ${requiredTickets.length}`}
                </div>
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
              disabled={selectedSeats.length === 0 || (requiredTickets.length > 0 && selectedSeats.length !== requiredTickets.length)}
              className="w-full py-4 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors text-lg"
            >
              Proceed to Checkout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}