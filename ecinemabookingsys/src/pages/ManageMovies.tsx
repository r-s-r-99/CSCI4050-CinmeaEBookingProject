import { useState, useEffect } from 'react';
import { MovieCard } from '../components/MovieCard';
<<<<<<< HEAD
import { Search, TicketX, Pencil, TicketPlus, CalendarClock, } from 'lucide-react';
=======
import { Search, TicketX, Pencil, TicketPlus, } from 'lucide-react';
>>>>>>> e0ec647a77dc228ef691316dbe0b3406a065c948
import { Movie } from '../types';
import { useNavigate } from 'react-router';

type StatusFilter = 'Now Showing' | 'Coming Soon';

export default function ManageMovies() {
    const navigate = useNavigate();
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
<<<<<<< HEAD
                    id: m.movie_id,
=======
                    id: m.id,
>>>>>>> e0ec647a77dc228ef691316dbe0b3406a065c948
                    title: m.title,
                    genre: m.genre,
                    rating: m.rating,
                    description: m.description,
                    poster_url: m.poster_url,
                    trailer_url: m.trailer_url,
                    status: m.status,
<<<<<<< HEAD
=======
                    isEditable: m.isEditable,
                    editUrl: m.editUrl,
                    actions: m.actions,
>>>>>>> e0ec647a77dc228ef691316dbe0b3406a065c948
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
<<<<<<< HEAD
                        </select>    
                    </div>
                </div>
                
=======
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
>>>>>>> e0ec647a77dc228ef691316dbe0b3406a065c948
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
<<<<<<< HEAD
                                /*Instead of routing to '/movie' (For normal users), clicking on a movie will now
                                * route to /admin/manage-movies/admin-movie, where the admin can add/manage showtimes directly.
                                */
                                <div key={movie.id}>
                                    <MovieCard movie={movie} isAdmin={true} />
                                </div>
                                
=======
                                <MovieCard key={movie.id} movie={movie} />
>>>>>>> e0ec647a77dc228ef691316dbe0b3406a065c948
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-12 text-gray-500">
                            No movies found.
                        </div>
                    )}
                </div>

                <div>
<<<<<<< HEAD
                    {/*Menu Option Grid*/}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-20 mb-15">
                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <button onClick={() => navigate('/admin/manage-movies/add-movies')}>
                                <h3 className="text-xl font-bold text-gray-900 mb-2"><TicketPlus />Add Movies</h3>
                                <p className="text-gray-500 text-sm">Add a movie to the database</p>
                            </button>
                        </div>

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><Pencil />Edit Movies</h3>
                            <p className="text-gray-500 text-sm">Edit movie data</p>
                        </div>

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><TicketX />Delete Movies</h3>
                            <p className="text-gray-500 text-sm">Delete currently offered movies</p>
                        </div>

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <button onClick={() => navigate('/admin/manage-movies/manage-showtimes')}>
                                <h3 className="text-xl font-bold text-gray-900 mb-2"><CalendarClock />Manage Showtimes</h3>
                                <p className="text-gray-500 text-sm">Manage current showtimes of movies</p>
                            </button>
                            
                        </div>

                    </div>
=======
>>>>>>> e0ec647a77dc228ef691316dbe0b3406a065c948
                </div>
            </div>
        </div>
    );
}