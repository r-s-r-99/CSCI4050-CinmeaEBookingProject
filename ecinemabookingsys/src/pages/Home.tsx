import { useState, useEffect } from 'react';
import { MovieCard } from '../components/MovieCard';
import { Search } from 'lucide-react';
import { Movie } from '../types';

type StatusFilter = 'Now Showing' | 'Coming Soon';

export default function Home() {
    const [movies, setMovies] = useState<Movie[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedStatus, setSelectedStatus] = useState<StatusFilter>('Now Showing');
    const [selectedGenre, setSelectedGenre] = useState('All');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/movies')
            .then(res => res.json())
            .then(data => {
                const mapped = data.movies.map((m: any) => ({
                    id: m.movie_id,
                    title: m.title,
                    genre: m.genre,
                    rating: m.rating,
                    description: m.description,
                    poster_url: m.poster_url,
                    trailer_url: m.trailer_url,
                    status: m.status,
                }));
                setMovies(mapped);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching movies:', err);
                setLoading(false);
            });
    }, []);

    const genres = ['All', ...Array.from(new Set(movies.map(m => m.genre)))];

    const filteredMovies = movies.filter(movie => {
        const matchesSearch = movie.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            movie.description.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesStatus = selectedStatus === 'Now Showing'
            ? movie.status === 'Currently Running'
            : movie.status === 'Coming Soon';
        const matchesGenre = selectedGenre === 'All' || movie.genre === selectedGenre;
        return matchesSearch && matchesStatus && matchesGenre;
    });

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
                    <h1 className="text-5xl mb-4">Book Your Movie Experience</h1>
                    <p className="text-xl mb-8">Choose from the latest blockbusters and timeless classics</p>
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

                {/* Movies Grid */}
                <div>
                    <h2 className="text-3xl mb-6">{selectedStatus}</h2>
                    {loading ? (
                        <div className="text-center py-12 text-gray-500">Loading movies...</div>
                    ) : filteredMovies.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                            {filteredMovies.map(movie => (
                                <MovieCard key={movie.id} movie={movie} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 text-gray-500">
                            No movies found.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}