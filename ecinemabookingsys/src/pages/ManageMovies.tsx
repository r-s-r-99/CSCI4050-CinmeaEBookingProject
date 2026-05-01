import { useState, useEffect } from 'react';
import { MovieCard } from '../components/MovieCard';
import { Search, TicketPlus } from 'lucide-react';
import { Movie } from '../types';
import { useNavigate } from 'react-router';

type StatusFilter = 'Now Showing' | 'Coming Soon';

export default function ManageMovies() {
    const navigate = useNavigate();
    const [movies, setMovies] = useState<Movie[]>([]);
    const [showtimeFilteredMovies, setShowtimeFilteredMovies] = useState<Movie[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedStatus, setSelectedStatus] = useState<StatusFilter>('Now Showing');
    const [selectedGenre, setSelectedGenre] = useState('All');
    const [selectedDate, setSelectedDate] = useState('');
    const [selectedTime, setSelectedTime] = useState('');
    const [availableDates, setAvailableDates] = useState<string[]>([]);
    const [availableTimes, setAvailableTimes] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [favoritedIds, setFavoritedIds] = useState<Set<number>>(new Set());

    useEffect(() => {
        fetch('/api/movies')
            .then(res => res.json())
            .then(data => {
                const mapped = data.movies.map((m: any) => ({
                    id: m.id,
                    title: m.title,
                    genre: m.genre,
                    rating: m.rating,
                    description: m.description,
                    poster_url: m.poster_url,
                    trailer_url: m.trailer_url,
                    status: m.status,
                    isEditable: m.isEditable,
                    editUrl: m.editUrl,
                    actions: m.actions,
                }));
                setMovies(mapped);
                setShowtimeFilteredMovies(mapped);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching movies:', err);
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        fetch('/api/retrieve-favorites', { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                const ids = new Set<number>(data.favorites.map((f: any) => f.movie_id as number));
                setFavoritedIds(ids);
            })
            .catch(err => console.error('Error fetching favorites:', err));
    }, []);

    useEffect(() => {
        fetch('/api/showtimes/available-dates')
            .then(res => res.json())
            .then(data => {
                setAvailableDates(data.dates || []);
            })
            .catch(err => console.error('Error fetching available dates:', err));
    }, []);

    useEffect(() => {
        if (selectedDate) {
            fetch(`/api/showtimes/available-times?date=${selectedDate}`)
                .then(res => res.json())
                .then(data => {
                    setAvailableTimes(data.times || []);
                    setSelectedTime('');
                })
                .catch(err => console.error('Error fetching available times:', err));
        } else {
            setAvailableTimes([]);
            setSelectedTime('');
        }
    }, [selectedDate]);

    useEffect(() => {
        if (selectedDate || selectedTime) {
            const params = new URLSearchParams();
            if (selectedDate) params.append('date', selectedDate);
            if (selectedTime) params.append('time', selectedTime);

            fetch(`/api/movies/by-showtime?${params}`)
                .then(res => {
                    if (!res.ok) throw new Error(`API error: ${res.status}`);
                    return res.json();
                })
                .then(data => {
                    if (!data.movies) {
                        console.error('Invalid response format:', data);
                        setShowtimeFilteredMovies([]);
                        return;
                    }
                    const mapped = data.movies.map((m: any) => ({
                        id: m.id,
                        title: m.title,
                        genre: m.genre,
                        rating: m.rating,
                        description: m.description,
                        poster_url: m.poster_url,
                        trailer_url: m.trailer_url,
                        status: m.status,
                        isEditable: m.isEditable,
                        editUrl: m.editUrl,
                        actions: m.actions,
                    }));
                    setShowtimeFilteredMovies(mapped);
                })
                .catch(err => {
                    console.error('Error fetching movies by showtime:', err);
                    setShowtimeFilteredMovies([]);
                });
        } else {
            setShowtimeFilteredMovies(movies);
        }
    }, [selectedDate, selectedTime, movies]);

    const genres = ['All', ...Array.from(new Set(movies.map(m => m.genre)))];

    const filteredMovies = showtimeFilteredMovies.filter(movie => {
        const matchesSearch = movie.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            movie.description.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesStatus = selectedStatus === 'Now Showing'
            ? movie.status === 'Currently Running'
            : movie.status === 'Coming Soon';
        const matchesGenre = selectedGenre === 'All' || movie.genre === selectedGenre;
        return matchesSearch && matchesStatus && matchesGenre;
    });

    const handleClearFilters = () => {
        setSelectedDate('');
        setSelectedTime('');
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Hero Section */}
            <div
                className="relative bg-cover bg-center h-96"
                style={{
                    backgroundImage: 'url(https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920&q=80)'
                }}
            >

                <div className="relative container mx-auto px-4 h-full flex flex-col justify-center items-center text-white text-center">
                    <h1 className="text-5xl mb-4">Manage Movies Here</h1>
                    <div className="w-full max-w-2xl relative flex gap-2">
                        <div className="relative flex-1">
                            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white w-5 h-5" />
                            <input
                                type="text"
                                placeholder="Search movies..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500"
                            />
                        </div>
                        <select
                            value={selectedGenre}
                            onChange={(e) => setSelectedGenre(e.target.value)}
                            className="px-4 py-3 rounded-lg text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-red-500 cursor-pointer"
                        >
                            {genres.map(genre => (
                                <option key={genre} value={genre}>{genre}</option>
                            ))}
                        </select>
                    </div>
                </div>

            </div>

            {/*Menu Option Grid*/}
            <div className="bg-white border-t border-gray-200 shadow-sm">
                <div className="container mx-auto px-4 py-8 flex justify-center">
                    <div className="bg-gray-50 p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                        <button onClick={() => navigate('/add-movies')} className="w-full text-left">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><TicketPlus />Add Movies</h3>
                            <p className="text-gray-500 text-sm">Add a movie to the database</p>
                        </button>
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-4 py-8">
                {/* Status Filter */}
                <div className="flex gap-2 mb-8 border-b border-gray-200">
                    {(['Now Showing', 'Coming Soon'] as StatusFilter[]).map(status => (
                        <button
                            key={status}
                            onClick={() => setSelectedStatus(status)}
                            className={`px-6 py-3 text-lg font-medium transition-colors border-b-2 -mb-px ${selectedStatus === status
                                ? 'border-red-600 text-red-600'
                                : 'border-transparent text-gray-500 hover:text-gray-700'
                                }`}
                        >
                            {status}
                        </button>
                    ))}
                </div>

                {/* Showtime Filters */}
                <div className="flex gap-4 mb-8 pb-4 border-b border-gray-200">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Date</label>
                        <select
                            value={selectedDate}
                            onChange={(e) => setSelectedDate(e.target.value)}
                            className="px-4 py-2 rounded-lg text-gray-900 bg-white border border-gray-300 focus:outline-none focus:ring-2 focus:ring-red-500 cursor-pointer"
                        >
                            <option value="">All Dates</option>
                            {availableDates.map(date => (
                                <option key={date} value={date}>{date}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Time</label>
                        <select
                            value={selectedTime}
                            onChange={(e) => setSelectedTime(e.target.value)}
                            disabled={!selectedDate}
                            className="px-4 py-2 rounded-lg text-gray-900 bg-white border border-gray-300 focus:outline-none focus:ring-2 focus:ring-red-500 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <option value="">All Times</option>
                            {availableTimes.map(time => (
                                <option key={time} value={time}>{time}</option>
                            ))}
                        </select>
                    </div>

                    {(selectedDate || selectedTime) && (
                        <button
                            onClick={handleClearFilters}
                            className="px-4 py-2 mt-7 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-lg transition-colors"
                        >
                            Clear Filters
                        </button>
                    )}
                </div>

                {/* Movies Grid */}
                <div>
                    <h2 className="text-3xl mb-6">{selectedStatus}</h2>
                    {loading ? (
                        <div className="text-center py-12 text-gray-500">Loading movies...</div>
                    ) : filteredMovies.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            {filteredMovies.map(movie => (
                                <MovieCard key={movie.id} movie={movie} isFavorited={favoritedIds.has(movie.id)} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 text-gray-500">
                            No movies found.
                        </div>
                    )}
                </div>

                <div>
                </div>
            </div>
        </div>
    );
}
