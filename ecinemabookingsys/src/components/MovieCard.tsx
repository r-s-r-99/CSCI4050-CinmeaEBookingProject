import { useEffect, useState } from 'react';
import { Star, Heart, Edit3 } from 'lucide-react';
import { useNavigate, Link } from 'react-router';
import { Movie } from '../types';

interface MovieCardProps {
  movie: Movie & { isEditable?: boolean; editUrl?: string; actions?: string[] };
  isFavorited?: boolean;
  isAdmin?: Boolean;
}

export function MovieCard({ movie, isFavorited: initialFavorited = false, isAdmin = false }: MovieCardProps) {
  const [isFavorited, setIsFavorited] = useState(initialFavorited);
  const navigate = useNavigate();

  const handleFavorite = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const newState = !isFavorited;

    try {
      const res = await fetch('/api/favorites', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          movieId: movie.id,
        }),
      });

      if (!res.ok) {
        throw new Error('Failed to update favorite');
      }

      setIsFavorited(newState);
    } catch (err) {
      console.error(err);
    }
  };

  const handleClick = (e: React.MouseEvent) => {
    // If clicking edit button, don't follow the card link
    if ((e.target as HTMLElement).closest('button')) {
      return;
    }
    navigate(`/movie/${movie.id}`);
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (movie.editUrl) {
      navigate(movie.editUrl);
    }
  };

  return (
    //Route to the admin's movie management page if user is an admin. Route to normal user movie page otherwise.
    <Link 
      to={isAdmin ? 
        `/admin/manage-movies/admin-movie/${movie.id}`
        :
        `/movie/${movie.id}`
      }
    >
      <div className="bg-white rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300">
        <div className="relative aspect-[2/3] overflow-hidden">
          <img
            src={movie.poster_url}
            alt={movie.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          {movie.status === 'Currently Running' && (
            <div className="absolute top-2 right-2 bg-red-600 text-white px-3 py-1 rounded-full text-sm">
              Now Showing
            </div>
          )}
          {movie.status === 'Coming Soon' && (
            <div className="absolute top-2 right-2 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">
              Coming Soon
            </div>
          )}
          {movie.isEditable && (
            <button
              onClick={handleEdit}
              className="absolute top-2 left-2 bg-purple-600 hover:bg-purple-700 text-white p-2 rounded-full transition-colors"
              title="Edit movie"
            >
              <Edit3 className="w-4 h-4" />
            </button>
          )}
        </div>
        <div className="p-4">
          <h3 className="text-lg mb-2 line-clamp-1">{movie.title}</h3>
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span className="flex items-center gap-1">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              {movie.rating}
            </span>
            <button
              onClick={handleFavorite}
              className="transition-colors"
            >
              <Heart
                className={`w-5 h-5 transition-colors ${isFavorited
                  ? 'fill-red-500 text-red-500'
                  : 'text-gray-400 hover:text-red-400'
                  }`}
              />
            </button>
          </div>
          <div className="inline-block px-2 py-1 bg-gray-100 rounded text-sm text-gray-700">
            {movie.genre}
          </div>
        </div>
    </div>
    </Link>
  );
}
