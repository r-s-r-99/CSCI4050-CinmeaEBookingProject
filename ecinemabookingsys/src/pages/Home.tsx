import { useState, useEffect } from 'react';
import { MovieCard } from '../components/MovieCard';
import { Search } from 'lucide-react';
import { Movie } from '../types';

export default function Home() {
    const [movies, setMovies] = useState<Movie[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedGenre, setSelectedGenre] = useState('All');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('/api/movies/now-showing')
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
        const matchesGenre = selectedGenre === 'All' || movie.genre === selectedGenre;
        return matchesSearch && matchesGenre;
    });

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Hero Section */}
            <div
                className="relative bg-cover bg-center h-96"
                style={{
                    backgroundImage: 'url(https://images.unsplash.com/photo-1640127249308-098702574176?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjaW5lbWElMjB0aGVhdGVyJTIwc2NyZWVufGVufDF8fHx8MTc3MTYwODc1NHww&ixlib=rb-4.1.0&q=80&w=1080)'
                }}
            >
                <div className="absolute inset-0 bg-black bg-opacity-60"></div>
                <div className="relative container mx-auto px-4 h-full flex flex-col justify-center items-center text-white text-center">
                    <h1 className="text-5xl mb-4">Book Your Movie Experience</h1>
                    <p className="text-xl mb-8">Choose from the latest blockbusters and timeless classics</p>

                    <div className="w-full max-w-2xl relative">
                        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Search movies..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-12 pr-4 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-red-500"
                        />
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-4 py-8">
                {/* Genre Filter */}
                <div className="mb-8">
                    <div className="flex gap-2 flex-wrap">
                        {genres.map(genre => (
                            <button
                                key={genre}
                                onClick={() => setSelectedGenre(genre)}
                                className={`px-4 py-2 rounded-full transition-colors ${selectedGenre === genre
                                        ? 'bg-red-600 text-white'
                                        : 'bg-white text-gray-700 hover:bg-gray-100'
                                    }`}
                            >
                                {genre}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Movies Grid */}
                <div>
                    <h2 className="text-3xl mb-6">Now Showing</h2>
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
                            No movies found matching your criteria.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}