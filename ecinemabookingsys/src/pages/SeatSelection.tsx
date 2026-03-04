import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { getShowtimeById, getMovieById } from '../data/movie';
import { Seat } from '../types';
import { ArrowLeft, Monitor } from 'lucide-react';

export default function SeatSelection() {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const showtime = getShowtimeById(showtimeId!);
  const movie = showtime ? getMovieById(showtime.movieId) : null;
  
  const [seats, setSeats] = useState<Seat[]>([]);

  useEffect(() => {
    // Generate seats
    const rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const seatsPerRow = 12;
    const newSeats: Seat[] = [];

    rows.forEach((row, rowIndex) => {
      for (let i = 1; i <= seatsPerRow; i++) {
        // Randomly book some seats for demo
        const isBooked = Math.random() < 0.3;
        // VIP seats in rows F, G, H
        const isVip = rowIndex >= 5;
        
        newSeats.push({
          id: `${row}${i}`,
          row,
          number: i,
          status: isBooked ? 'booked' : 'available',
          type: isVip ? 'vip' : 'regular',
        });
      }
    });

    setSeats(newSeats);
  }, []);

  const toggleSeat = (seatId: string) => {
    setSeats(prev => prev.map(seat => {
      if (seat.id === seatId && seat.status !== 'booked') {
        return {
          ...seat,
          status: seat.status === 'selected' ? 'available' : 'selected',
        };
      }
      return seat;
    }));
  };

  const selectedSeats = seats.filter(s => s.status === 'selected');
  const totalPrice = selectedSeats.reduce((sum, seat) => {
    const basePrice = showtime?.price || 0;
    return sum + (seat.type === 'vip' ? basePrice + 5 : basePrice);
  }, 0);

  const handleConfirmBooking = () => {
    if (selectedSeats.length === 0) return;
    
    const booking = {
      showtime: showtime!,
      movie: movie!,
      seats: selectedSeats,
      totalPrice,
    };
    
    // Store in localStorage
    const existingBookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    existingBookings.push({
      ...booking,
      id: Date.now().toString(),
      bookingDate: new Date().toISOString(),
    });
    localStorage.setItem('bookings', JSON.stringify(existingBookings));
    
    navigate('/confirmation', { state: booking });
  };

  if (!showtime || !movie) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl mb-4">Showtime not found</h2>
          <button
            onClick={() => navigate('/')}
            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
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
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-8">
            <h1 className="text-3xl mb-2">{movie.title}</h1>
            <p className="text-gray-600">
              {showtime.theater} • {showtime.time} • {showtime.date}
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
                      const isVip = seat.type === 'vip';
                      const isAisle = index === 5;
                      
                      return (
                        <div key={seat.id} className="flex gap-2">
                          {isAisle && <div className="w-4" />}
                          <button
                            onClick={() => toggleSeat(seat.id)}
                            disabled={seat.status === 'booked'}
                            className={`w-8 h-8 rounded-t-lg transition-colors ${
                              seat.status === 'booked'
                                ? 'bg-gray-300 cursor-not-allowed'
                                : seat.status === 'selected'
                                ? 'bg-green-500 hover:bg-green-600'
                                : isVip
                                ? 'bg-yellow-200 hover:bg-yellow-300 border-2 border-yellow-400'
                                : 'bg-blue-200 hover:bg-blue-300'
                            }`}
                            title={`${seat.id} - ${isVip ? 'VIP' : 'Regular'}`}
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
              <div className="w-6 h-6 bg-blue-200 rounded-t-lg"></div>
              <span>Available</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-yellow-200 rounded-t-lg border-2 border-yellow-400"></div>
              <span>VIP (+$5)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-green-500 rounded-t-lg"></div>
              <span>Selected</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-gray-300 rounded-t-lg"></div>
              <span>Booked</span>
            </div>
          </div>

          {/* Booking Summary */}
          <div className="border-t pt-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-gray-600">Selected Seats:</div>
                <div className="text-xl">
                  {selectedSeats.length > 0
                    ? selectedSeats.map(s => s.id).join(', ')
                    : 'None'}
                </div>
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