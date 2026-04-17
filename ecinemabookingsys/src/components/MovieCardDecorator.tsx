import { useNavigate } from 'react-router';
import { Movie } from '../types';

interface MovieCardDecoratorProps {
  movie: Movie;
  isAdmin?: boolean;
  isFavorited?: boolean;
}

export function MovieCardDecorator({ movie, isAdmin = false, isFavorited = false }: MovieCardDecoratorProps) {
  const navigate = useNavigate();

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    if (isAdmin) {
      navigate(`/edit-movies/${movie.id}`);
    } else {
      navigate(`/movie/${movie.id}`);
    }
  };

  return (
    <div onClick={handleClick} className="group cursor-pointer">
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
          {isAdmin && (
            <div className="absolute top-2 left-2 bg-purple-600 text-white px-3 py-1 rounded-full text-sm">
              Edit
            </div>
          )}
        </div>
        <div className="p-4">
          <h3 className="text-lg mb-2 line-clamp-1">{movie.title}</h3>
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>{movie.rating}</span>
            <span className="text-xs text-gray-500">{isAdmin ? 'Click to edit' : 'View details'}</span>
          </div>
          <div className="inline-block px-2 py-1 bg-gray-100 rounded text-sm text-gray-700">
            {movie.genre}
          </div>
        </div>
      </div>
    </div>
  );
}
