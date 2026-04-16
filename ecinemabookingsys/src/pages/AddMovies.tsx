import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TicketX, Pencil, TicketPlus, Type, Star, Film, Info, Image, } from 'lucide-react';


export default function AddMovies() {
    const navigate = useNavigate();
/*
    //This makes sure that only the admin can access this page.
    useEffect(() => {
        fetch('/api/me', { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                if (!data.role || data.role !== 'admin') {
                    alert('Access Denied. You are attempting to access an admin page!');
                    navigate('/');
                }
            })
            .catch(() => {
                navigate('/');
            });
    }, []);
    */

    const [movieData, setMovieData] = useState({
        title: '',
        genre: '',
        rating: 'G',
        description: '',
        poster_url: '',
        trailer_url: '',
        status: '',
    });

    const handleSubmit = async (e: React.FormEvent) => {
        //Prevents page reloading when submitting
        e.preventDefault();

        const res = await fetch('/api/movies', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(movieData),
        });

        if (res.ok) {
            alert("Movie saved successfully.");
        } else {
            alert("Failed to add movie.");
        } //if/else
    }; //handleSubmit

    const handleChange = (e: React.ChangeEvent<any>) => {
        const { name, value } = e.target;
        setMovieData((m) => ({
            ...m,
            [name]: value
        }));
    }; //handleChange

    return (
        <div className="grid h-screen bg-gray-50 py-12 place-items-center">
            <div className="container mx-auto px-4 max-w-2xl">
                <div className="bg-white rounded-xl shadow-md pt-10 pb-10 pl-6 pr-6 ">
                    <h1 className="text-4xl font-bold mb-8">Add New Movie</h1>
                    
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Title */}
                        <div>
                            <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                <Type className="w-4 h-4" /> Movie Title
                            </label>
                            <input
                                className="w-full border rounded-lg px-4 py-2 outline-none focus:border-gray-400"
                                onChange={handleChange}
                                required
                                name="title"
                                type="text"
                                value={movieData.title}
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            {/* Genre */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                    <Film className="w-4 h-4" /> Genre
                                </label>
                                <input
                                    className="w-full border rounded-lg outline-none focus:border-gray-400 px-4 py-2"
                                    onChange={handleChange}
                                    required
                                    name="genre"
                                    type="text"
                                    value={movieData.genre}
                                />
                            </div>

                            {/* Rating */}
                            <div>
                                <label className="flex items-center gap-2 font-semibold text-sm mb-2">
                                    <Star className="w-4 h-4" /> Rating
                                </label>
                                <select 
                                    className="w-full border rounded-lg outline-none px-4 py-2 bg-white"
                                    onChange={handleChange}
                                    name="rating"
                                    value={movieData.rating}
                                >
                                    <option value="G">G</option>
                                    <option value="PG">PG</option>
                                    <option value="PG-13">PG-13</option>
                                    <option value="NC-17">NC-17</option>
                                    <option value="R">R</option>
                                </select>
                            </div>
                        </div>

                        {/* Poster URL */}
                        <div>
                            <label className="flex items-center text-sm font-semibold mb-2 gap-2">
                                <Image className="w-4 h-4" /> Poster Image URL
                            </label>
                            <input
                                className="w-full border rounded-lg outline-none focus:border-gray-400 px-4 py-2"
                                onChange={handleChange}
                                required
                                name="poster_url"
                                type="url"
                                value={movieData.poster_url}

                            />
                        </div>

                        {/* Description */}
                        <div>
                            <label className="flex items-center gap-2 text-sm font-semibold mb-2">
                                <Info className="w-4 h-4" /> Description
                            </label>
                            <textarea
                                className="w-full px-4 py-2 border rounded-lg outline-none focus:border-gray-400"
                                onChange={handleChange}
                                required
                                name="description"
                                rows={3}
                                value={movieData.description}
                            />
                        </div>

                        <div className="flex gap-4">
                            <button
                                className="flex-1 border rounded-lg hover:bg-gray-100 px-6 py-3"
                                type="button"
                                onClick={() => navigate('/admin/manage-movies')}
                            >
                                Cancel
                            </button>
                            <button
                                className="flex-1 bg-red-600 text-white rounded-lg font-bold hover:bg-red-700 px-6 py-3"
                                type="submit"
                            >
                                Add Movie
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    ); //return
}; //AddMovies
