import { useParams, useNavigate } from 'react-router';
import { Clock, Star, Calendar, MapPin } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Movie, Showtime } from '../types';

export default function MovieDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [showtimes, setShowtimes] = useState<Showtime[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/movies/${id}`)
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
      .catch(err => console.error('Error fetching movie:', err));

    fetch(`/api/showtimes/${id}`)
      .then(res => res.json())
      .then(data => {
        const mapped = data.showtimes.map((s: any) => ({
          id: s.showtime_id,
          movieId: s.movie_id,
          date: s.show_date,
          time: s.show_time,
          theater: 'Main Theater', // your DB doesn't have a theater column yet
        }));
        setShowtimes(mapped);
      })
      .catch(err => console.error('Error fetching showtimes:', err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Loading...</div>;
  }

  if (!movie) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl mb-4">Movie not found</h2>
          <button onClick={() => navigate('/')} className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  // Group showtimes by date
  const groupedShowtimes = showtimes.reduce((acc, showtime) => {
    if (!acc[showtime.date]) acc[showtime.date] = [];
    acc[showtime.date].push(showtime);
    return acc;
  }, {} as Record<string, Showtime[]>);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Movie Header */}
      <div className="relative bg-gray-900 text-white">
        <div
          className="absolute inset-0 opacity-20 bg-cover bg-center"
          style={{ backgroundImage: `url(${movie.poster_url})` }}
        />
        <div className="relative container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-[300px,1fr] gap-8">
            <div className="rounded-lg overflow-hidden shadow-xl">
              <img src={movie.poster_url} alt={movie.title} className="w-full h-auto" />
            </div>
            <div className="flex flex-col justify-center">
              <h1 className="text-4xl mb-4">{movie.title}</h1>
              <div className="flex items-center gap-6 mb-4 text-lg">
                <span className="flex items-center gap-2">
                  <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  {movie.rating}
                </span>
                <span className="px-3 py-1 bg-red-600 rounded-full">{movie.genre}</span>
              </div>
              <p className="text-gray-300 text-lg leading-relaxed">{movie.description}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Showtimes */}
      <div className="container mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-3xl mb-6">Select Showtime</h2>

          {Object.entries(groupedShowtimes).map(([date, times]) => (
            <div key={date} className="mb-8 last:mb-0">
              <div className="flex items-center gap-2 mb-4">
                <Calendar className="w-5 h-5 text-red-600" />
                <h3 className="text-xl">{date}</h3>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {times.map(showtime => (
                  <button
                    key={showtime.id}
                    onClick={() => navigate(`/booking/${showtime.id}`)}
                    className="p-4 border-2 border-gray-200 rounded-lg hover:border-red-600 hover:bg-red-50 transition-colors text-center"
                  >
                    <div className="text-lg mb-1">{showtime.time}</div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}