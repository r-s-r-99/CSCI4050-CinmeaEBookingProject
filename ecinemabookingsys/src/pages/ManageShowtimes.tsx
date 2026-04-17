import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Calendar, Clock, Film, MapPin, AlertCircle, CheckCircle, ArrowLeft } from 'lucide-react';

interface Movie {
  id: number;
  title: string;
  genre: string;
}

interface Showroom {
  room_id: number;
  room_number: number;
  number_of_seats: number;
}

interface Showtime {
  showtime_id: number;
  movie_title: string;
  show_date: string;
  show_time: string;
  room_number: number;
}

export default function ManageShowtimes() {
  const navigate = useNavigate();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [showrooms, setShowrooms] = useState<Showroom[]>([]);
  const [showtimes, setShowtimes] = useState<Showtime[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [formData, setFormData] = useState({
    movie_id: '',
    show_date: '',
    show_time: '',
    room_id: '',
  });

  const [conflictWarning, setConflictWarning] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [moviesRes, showroomsRes, showtimesRes] = await Promise.all([
          fetch('/api/movies-for-showtimes'),
          fetch('/api/showrooms'),
          fetch('/api/showtimes'),
        ]);

        if (!moviesRes.ok || !showroomsRes.ok || !showtimesRes.ok) {
          throw new Error('Failed to fetch data');
        }

        const moviesData = await moviesRes.json();
        const showroomsData = await showroomsRes.json();
        const showtimesData = await showtimesRes.json();

        setMovies(moviesData.movies || []);
        setShowrooms(showroomsData.showrooms || []);
        setShowtimes(showtimesData.showtimes || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setConflictWarning('');
  };

  const checkForConflicts = async () => {
    if (!formData.room_id || !formData.show_date || !formData.show_time) {
      return;
    }

    try {
      const res = await fetch('/api/showtimes/check-conflict', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          room_id: parseInt(formData.room_id),
          show_date: formData.show_date,
          show_time: formData.show_time,
        }),
      });

      const data = await res.json();
      if (data.has_conflict) {
        setConflictWarning(
          `⚠️ Conflict: ${data.conflicting_showtimes.length} showtime(s) already scheduled at this time in this room.`
        );
      } else {
        setConflictWarning('');
      }
    } catch (err) {
      console.error('Error checking conflict:', err);
    }
  };

  useEffect(() => {
    checkForConflicts();
  }, [formData.room_id, formData.show_date, formData.show_time]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.movie_id || !formData.show_date || !formData.show_time || !formData.room_id) {
      setError('All fields are required');
      return;
    }

    setSubmitting(true);

    try {
      const res = await fetch('/api/showtimes', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          movie_id: parseInt(formData.movie_id),
          show_date: formData.show_date,
          show_time: formData.show_time,
          room_id: parseInt(formData.room_id),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Failed to create showtime');
      }

      setSuccess('Showtime created successfully!');
      setFormData({
        movie_id: '',
        show_date: '',
        show_time: '',
        room_id: '',
      });

      // Refresh showtimes list
      const showtimesRes = await fetch('/api/showtimes');
      const showtimesData = await showtimesRes.json();
      setShowtimes(showtimesData.showtimes || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  const selectedMovie = movies.find(m => m.id === parseInt(formData.movie_id));
  const selectedShowroom = showrooms.find(sr => sr.room_id === parseInt(formData.room_id));

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Back Button */}
        <button
          onClick={() => navigate('/admin')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Admin
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form Section */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-bold mb-6">Add Showtime</h2>

              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <p className="text-red-600 text-sm">{error}</p>
                </div>
              )}

              {success && (
                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-start gap-2">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <p className="text-green-600 text-sm">{success}</p>
                </div>
              )}

              {conflictWarning && (
                <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg flex items-start gap-2">
                  <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                  <p className="text-yellow-700 text-sm">{conflictWarning}</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Movie */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                    <Film className="w-4 h-4" /> Movie *
                  </label>
                  <select
                    name="movie_id"
                    value={formData.movie_id}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-red-600"
                  >
                    <option value="">Select a movie</option>
                    {movies.map(m => (
                      <option key={m.id} value={m.id}>{m.title}</option>
                    ))}
                  </select>
                </div>

                {/* Date */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                    <Calendar className="w-4 h-4" /> Date *
                  </label>
                  <input
                    type="date"
                    name="show_date"
                    value={formData.show_date}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-red-600"
                  />
                </div>

                {/* Time */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                    <Clock className="w-4 h-4" /> Time *
                  </label>
                  <input
                    type="time"
                    name="show_time"
                    value={formData.show_time}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-red-600"
                  />
                </div>

                {/* Showroom */}
                <div>
                  <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                    <MapPin className="w-4 h-4" /> Showroom *
                  </label>
                  <select
                    name="room_id"
                    value={formData.room_id}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 outline-none focus:ring-2 focus:ring-red-600"
                  >
                    <option value="">Select a showroom</option>
                    {showrooms.map(sr => (
                      <option key={sr.room_id} value={sr.room_id}>
                        Room {sr.room_number} ({sr.number_of_seats} seats)
                      </option>
                    ))}
                  </select>
                </div>

                {/* Preview */}
                {selectedMovie && selectedShowroom && formData.show_date && formData.show_time && (
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-sm text-blue-900">
                      <strong>{selectedMovie.title}</strong><br />
                      {new Date(formData.show_date + 'T00:00:00').toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })} at {formData.show_time}<br />
                      Room {selectedShowroom.room_number}
                    </p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={submitting}
                  className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg disabled:bg-gray-400 transition-colors mt-6"
                >
                  {submitting ? 'Creating...' : 'Create Showtime'}
                </button>
              </form>
            </div>
          </div>

          {/* Showtimes List Section */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-bold mb-6">Scheduled Showtimes</h2>

              {showtimes.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <p>No showtimes scheduled yet</p>
                </div>
              ) : (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {showtimes.map(st => (
                    <div key={st.showtime_id} className="p-4 border border-gray-200 rounded-lg hover:border-red-300 transition-colors">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{st.movie_title}</h3>
                          <div className="grid grid-cols-3 gap-4 mt-2 text-sm text-gray-600">
                            <div className="flex items-center gap-1">
                              <Calendar className="w-4 h-4" />
                              {new Date(st.show_date + 'T00:00:00').toLocaleDateString()}
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              {st.show_time}
                            </div>
                            <div className="flex items-center gap-1">
                              <MapPin className="w-4 h-4" />
                              Room {st.room_number}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
