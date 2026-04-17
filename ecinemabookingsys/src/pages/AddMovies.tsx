import { useState } from 'react';
import { useNavigate } from 'react-router';
import { TicketPlus, Type, Star, Film, Info, Image, AlertCircle, CheckCircle, ArrowLeft } from 'lucide-react';

export default function AddMovies() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const [movieData, setMovieData] = useState({
        title: '',
        genre: '',
        rating: 'G',
        description: '',
        poster_url: '',
        trailer_url: '',
        status: 'Currently Running',
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        // Validation
        if (!movieData.title.trim()) {
            setError('Title is required');
            return;
        }
        if (!movieData.genre.trim()) {
            setError('Genre is required');
            return;
        }
        if (!movieData.description.trim()) {
            setError('Description is required');
            return;
        }
        if (!movieData.poster_url.trim()) {
            setError('Poster URL is required');
            return;
        }

        setLoading(true);

        try {
            const res = await fetch('/api/movies', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(movieData),
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || 'Failed to add movie');
            }

            setSuccess('Movie added successfully!');

            // Reset form
            setMovieData({
                title: '',
                genre: '',
                rating: 'G',
                description: '',
                poster_url: '',
                trailer_url: '',
                status: 'Currently Running',
            });

            // Redirect after 2 seconds
            setTimeout(() => {
                navigate('/manage-movies');
            }, 2000);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setMovieData((m) => ({
            ...m,
            [name]: value
        }));
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="container mx-auto px-4 max-w-2xl">
                {/* Back Button */}
                <button
                    onClick={() => navigate('/manage-movies')}
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
                >
                    <ArrowLeft className="w-5 h-5" />
                    Back to Manage Movies
                </button>

                <div className="bg-white rounded-xl shadow-md p-8">
                    <h1 className="text-4xl font-bold mb-2">Add New Movie</h1>
                    <p className="text-gray-600 mb-6">Fill in all the movie details below</p>

                    {/* Error Message */}
                    {error && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                            <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                            <p className="text-red-600">{error}</p>
                        </div>
                    )}

                    {/* Success Message */}
                    {success && (
                        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
                            <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                            <p className="text-green-600">{success}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Title */}
                        <div>
                            <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                <Type className="w-4 h-4" /> Movie Title *
                            </label>
                            <input
                                className="w-full border border-gray-300 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-red-600"
                                onChange={handleChange}
                                required
                                name="title"
                                type="text"
                                value={movieData.title}
                                placeholder="Enter movie title"
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            {/* Genre */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                    <Film className="w-4 h-4" /> Genre *
                                </label>
                                <input
                                    className="w-full border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-red-600 px-4 py-2"
                                    onChange={handleChange}
                                    required
                                    name="genre"
                                    type="text"
                                    value={movieData.genre}
                                    placeholder="e.g., Action, Drama"
                                />
                            </div>

                            {/* Rating */}
                            <div>
                                <label className="flex items-center gap-2 font-semibold text-sm mb-2">
                                    <Star className="w-4 h-4" /> Rating
                                </label>
                                <select
                                    className="w-full border border-gray-300 rounded-lg outline-none px-4 py-2 bg-white focus:ring-2 focus:ring-red-600"
                                    onChange={handleChange}
                                    name="rating"
                                    value={movieData.rating}
                                >
                                    <option value="G">G</option>
                                    <option value="PG">PG</option>
                                    <option value="PG-13">PG-13</option>
                                    <option value="R">R</option>
                                    <option value="NC-17">NC-17</option>
                                    <option value="NR">NR</option>
                                </select>
                            </div>
                        </div>

                        {/* Status */}
                        <div>
                            <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                <TicketPlus className="w-4 h-4" /> Status *
                            </label>
                            <select
                                className="w-full border border-gray-300 rounded-lg outline-none px-4 py-2 bg-white focus:ring-2 focus:ring-red-600"
                                onChange={handleChange}
                                name="status"
                                value={movieData.status}
                            >
                                <option value="Currently Running">Currently Running</option>
                                <option value="Coming Soon">Coming Soon</option>
                            </select>
                        </div>

                        {/* Poster URL */}
                        <div>
                            <label className="flex items-center text-sm font-semibold mb-2 gap-2">
                                <Image className="w-4 h-4" /> Poster Image URL *
                            </label>
                            <input
                                className="w-full border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-red-600 px-4 py-2"
                                onChange={handleChange}
                                required
                                name="poster_url"
                                type="url"
                                value={movieData.poster_url}
                                placeholder="https://example.com/poster.jpg"
                            />
                        </div>

                        {/* Trailer URL */}
                        <div>
                            <label className="flex items-center text-sm font-semibold mb-2 gap-2">
                                <Film className="w-4 h-4" /> Trailer URL
                            </label>
                            <input
                                className="w-full border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-red-600 px-4 py-2"
                                onChange={handleChange}
                                name="trailer_url"
                                type="url"
                                value={movieData.trailer_url}
                                placeholder="https://youtube.com/embed/..."
                            />
                        </div>

                        {/* Description */}
                        <div>
                            <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                <Info className="w-4 h-4" /> Description *
                            </label>
                            <textarea
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-red-600"
                                onChange={handleChange}
                                required
                                name="description"
                                rows={4}
                                value={movieData.description}
                                placeholder="Enter movie description"
                            />
                        </div>

                        <div className="flex gap-4 pt-6">
                            <button
                                className="flex-1 border border-gray-300 rounded-lg hover:bg-gray-100 px-6 py-3 font-semibold"
                                type="button"
                                onClick={() => navigate('/manage-movies')}
                            >
                                Cancel
                            </button>
                            <button
                                className="flex-1 bg-red-600 text-white rounded-lg font-bold hover:bg-red-700 px-6 py-3 disabled:bg-gray-400"
                                type="submit"
                                disabled={loading}
                            >
                                {loading ? 'Adding Movie...' : 'Add Movie'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}