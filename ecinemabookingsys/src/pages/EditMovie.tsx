import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router';
import { Type, Star, Film, Info, Image, AlertCircle, CheckCircle, ArrowLeft, Trash2 } from 'lucide-react';

export default function EditMovie() {
    const navigate = useNavigate();
    const { id } = useParams();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [deleting, setDeleting] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

    const [movieData, setMovieData] = useState({
        title: '',
        genre: '',
        rating: 'G',
        description: '',
        poster_url: '',
        trailer_url: '',
        status: 'Currently Running',
    });

    useEffect(() => {
        if (!id) return;

        const fetchMovie = async () => {
            try {
                const res = await fetch(`/api/movies/${id}`);
                if (!res.ok) throw new Error('Failed to fetch movie');

                const data = await res.json();
                const m = data.movie;
                setMovieData({
                    title: m.title,
                    genre: m.genre,
                    rating: m.rating,
                    description: m.description,
                    poster_url: m.poster_url,
                    trailer_url: m.trailer_url,
                    status: m.status,
                });
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load movie');
            } finally {
                setLoading(false);
            }
        };

        fetchMovie();
    }, [id]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');

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

        setSaving(true);

        try {
            const res = await fetch(`/api/movies/${id}`, {
                method: 'PUT',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(movieData),
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || 'Failed to update movie');
            }

            setSuccess('Movie updated successfully!');

            setTimeout(() => {
                navigate('/manage-movies');
            }, 2000);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async () => {
        setError('');
        setDeleting(true);

        try {
            const res = await fetch(`/api/movies/${id}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.error || 'Failed to delete movie');
            }

            setShowDeleteConfirm(false);
            navigate('/manage-movies');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to delete movie');
        } finally {
            setDeleting(false);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setMovieData((m) => ({
            ...m,
            [name]: value
        }));
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                <div className="text-center">
                    <p className="text-lg text-gray-600">Loading movie...</p>
                </div>
            </div>
        );
    }

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
                    <h1 className="text-4xl font-bold mb-2">Edit Movie</h1>
                    <p className="text-gray-600 mb-6">Update the movie details below</p>

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
                                <Film className="w-4 h-4" /> Status *
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
                                disabled={saving}
                            >
                                {saving ? 'Saving...' : 'Save Changes'}
                            </button>
                        </div>
                    </form>

                    {/* Delete Section */}
                    <div className="mt-8 pt-8 border-t border-gray-200">
                        <h2 className="text-lg font-semibold text-red-600 mb-4">Danger Zone</h2>
                        <p className="text-gray-600 mb-4">
                            Permanently delete this movie from the database. This action cannot be undone.
                        </p>
                        <button
                            onClick={() => setShowDeleteConfirm(true)}
                            className="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors disabled:bg-gray-400"
                            disabled={deleting}
                        >
                            <Trash2 className="w-5 h-5" />
                            {deleting ? 'Deleting...' : 'Delete Movie'}
                        </button>
                    </div>

                    {/* Delete Confirmation Dialog */}
                    {showDeleteConfirm && (
                        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                            <div className="bg-white rounded-lg shadow-xl p-6 max-w-sm mx-4">
                                <h3 className="text-xl font-bold mb-4">Confirm Delete</h3>
                                <p className="text-gray-600 mb-6">
                                    Are you sure you want to delete <strong>{movieData.title}</strong>? This action cannot be undone.
                                </p>
                                <div className="flex gap-4">
                                    <button
                                        onClick={() => setShowDeleteConfirm(false)}
                                        className="flex-1 border border-gray-300 rounded-lg hover:bg-gray-100 px-4 py-2 font-semibold"
                                        disabled={deleting}
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={handleDelete}
                                        className="flex-1 bg-red-600 hover:bg-red-700 text-white rounded-lg px-4 py-2 font-semibold disabled:bg-gray-400"
                                        disabled={deleting}
                                    >
                                        {deleting ? 'Deleting...' : 'Delete'}
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
