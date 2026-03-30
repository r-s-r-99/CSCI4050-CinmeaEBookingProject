import { useState } from 'react';
import { Star, Heart } from 'lucide-react';
import { Link } from 'react-router';
import { Movie } from '../types';

interface MovieCardProps {
  movie: Movie;
}

export function MovieCard({ movie }: MovieCardProps) {
  const [isFavorited, setIsFavorited] = useState(false);

  const handleFavorite = (e: React.MouseEvent) => {
    e.preventDefault(); // prevents the Link from navigating when clicking the heart
    setIsFavorited(!isFavorited);
    // make API call here
  };

  return (
    <Link to={`/movie/${movie.id}`} className="group">
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
                className={`w-5 h-5 transition-colors ${
                  isFavorited
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