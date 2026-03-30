import { Home, Bell, Calendar, TrendingUp, User, Settings as SettingsIcon, ChevronLeft, Pen, Lock, HelpCircle, Palette, Check } from 'lucide-react';
import { Link } from 'react-router';
import { useState, useEffect } from 'react';
import { MovieCard } from '../components/MovieCard';
import { Search } from 'lucide-react';
import { Movie } from '../types';

type StatusFilter = 'Now Showing' | 'Coming Soon';

const settingsMenuItems = [
    { id: 'edit-profile', label: 'Edit profile', icon: Pen },
    { id: 'notification', label: 'Notification', icon: Bell },
    { id: 'security', label: 'Security', icon: Lock },
    { id: 'appearance', label: 'Appearance', icon: Palette },
    { id: 'help', label: 'Help', icon: HelpCircle },
];

export default function Preferences() {
    const [activeSection, setActiveSection] = useState('edit-profile');
    const [formData, setFormData] = useState({
        firstName: 'Allen',
        lastName: 'Chiu',
        email: 'asc73208@uga.edu',
        address: 'testing address',
        contactNumber: '678-862-6972',
        city: 'Athens',
        state: 'Georgia',
        password: 'need to be hidden',
    });
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

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Handle form submission
        alert('Profile updated successfully!');
    };

    const handleCancel = () => {
        // Reset form or navigate away
    };

    return (
        <div className="flex h-screen bg-white">

            {/* Main Content */}
            <div className="flex-1 overflow-auto">
                <div className="max-w-7xl mx-auto p-12 pb-24">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-12">
                        <h1 className="text-4xl">Preferences</h1>
                        <div className="flex items-center gap-4">
                        </div>
                    </div>

                    <div className="container mx-auto px-6 py-8">
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
            </div>
        </div>
    );
}