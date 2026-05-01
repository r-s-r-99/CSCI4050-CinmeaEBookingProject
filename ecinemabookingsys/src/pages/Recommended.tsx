import React, { useState } from "react";
import { MovieCard } from "../components/MovieCard";
import { Movie } from "../types";

export default function Recommended() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleGetRecommendations = async () => {
    setLoading(true);
    try {
      const response = await fetch("/api/recommendations", {
        credentials: "include",
      });
      const data = await response.json();

      if (data.status === "success") {
        const recommendationTitles = data.data.ai_recommendations
          ?.split("\n")
          .map((title: string) => title.trim())
          .filter((title: string) => title.length > 0) || [];

        const allMovies: Movie[] = data.data.all_movies.map((m: any) => ({
          id: m.id,
          title: m.title,
          genre: m.genre,
          rating: m.rating,
          description: m.description,
          poster_url: m.poster_url,
          trailer_url: m.trailer_url,
          status: m.status,
        }));

        const recommendedMovies = allMovies.filter((movie) =>
          recommendationTitles.some(
            (title: string) =>
              title.toLowerCase().includes(movie.title.toLowerCase()) ||
              movie.title.toLowerCase().includes(title.toLowerCase())
          )
        );

        setMovies(recommendedMovies);
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoading(false);
      setHasSearched(true);
    }
  };

  return (
    <div className="flex-1 overflow-auto">
      <div className="max-w-7xl mx-auto p-12 pb-24">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <h1 className="text-4xl">Recommendations</h1>
        </div>

        <div className="container mx-auto px-6 py-8">
          {/* Get Recommendations Button */}
          <div className="flex justify-center mb-12">
            <button
              className="px-8 py-3 text-lg font-semibold rounded-lg bg-blue-500 text-white cursor-pointer hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              onClick={handleGetRecommendations}
              disabled={loading}
            >
              {loading ? "Loading..." : "Get Recommendations"}
            </button>
          </div>

          {/* Movies Grid */}
          <div>
            {!hasSearched ? (
              <div className="text-center py-12 text-gray-500">
                Click "Get Recommendations" to see personalized movie suggestions
              </div>
            ) : loading ? (
              <div className="text-center py-12 text-gray-500">
                Loading recommendations...
              </div>
            ) : movies.length > 0 ? (
              <>
                <h2 className="text-3xl mb-6">
                  Recommended for You ({movies.length})
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {movies.map((movie) => (
                    <MovieCard key={movie.id} movie={movie} isFavorited={false} />
                  ))}
                </div>
              </>
            ) : (
              <div className="text-center py-12 text-gray-500">
                No recommendations found.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
