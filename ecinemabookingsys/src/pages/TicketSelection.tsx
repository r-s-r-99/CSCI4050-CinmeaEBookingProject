import { useParams, useNavigate } from 'react-router';
import { ArrowLeft } from 'lucide-react';
import { useState } from 'react';

type TicketCategory = 'adult' | 'senior' | 'child';

const TICKET_PRICES: Record<TicketCategory, number> = {
  adult: 12,
  senior: 8,
  child: 6,
};

interface TicketSelectionData {
  count: number;
  categories: TicketCategory[];
}

export default function TicketSelection() {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const [ticketCount, setTicketCount] = useState<number>(1);
  const [categories, setCategories] = useState<TicketCategory[]>(['adult']);
  const [error, setError] = useState<string>('');

  // Handle ticket count change
  const handleTicketCountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value) || 0;
    if (value < 0 || value > 20) {
      setError('Ticket count must be between 1 and 20');
      return;
    }
    if (value === 0) {
      setError('You must select at least 1 ticket');
      return;
    }
    setError('');
    setTicketCount(value);
    // Update categories array to match new count
    const newCategories = Array(value).fill('adult') as TicketCategory[];
    newCategories.forEach((_, i) => {
      newCategories[i] = categories[i] || 'adult';
    });
    setCategories(newCategories);
  };

  // Handle individual category change
  const handleCategoryChange = (index: number, category: TicketCategory) => {
    const newCategories = [...categories];
    newCategories[index] = category;
    setCategories(newCategories);
  };

  // Handle continue button
  const handleContinue = () => {
    if (ticketCount <= 0) {
      setError('You must select at least 1 ticket');
      return;
    }
    if (categories.length !== ticketCount) {
      setError('Ticket count mismatch');
      return;
    }

    // Calculate total estimated price
    const estimatedTotal = categories.reduce((sum, cat) => sum + TICKET_PRICES[cat], 0);

    const ticketData: TicketSelectionData = {
      count: ticketCount,
      categories,
    };

    navigate(`/booking/${showtimeId}`, {
      state: {
        ticketSelection: ticketData,
        estimatedTotal,
      },
    });
  };

  // Calculate total estimated price
  const estimatedTotal = categories.reduce((sum, cat) => sum + TICKET_PRICES[cat], 0);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        {/* Back Button */}
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        {/* Card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold mb-2">Select Your Tickets</h1>
          <p className="text-gray-600 mb-8">Choose how many tickets you need and the age category for each.</p>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}

          {/* Ticket Count Input */}
          <div className="mb-8">
            <label htmlFor="ticketCount" className="block text-lg font-semibold mb-3">
              Number of Tickets
            </label>
            <div className="flex items-center gap-4">
              <input
                id="ticketCount"
                type="number"
                min="1"
                max="20"
                value={ticketCount}
                onChange={handleTicketCountChange}
                className="w-24 px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-600 focus:outline-none text-center text-xl"
              />
              <span className="text-gray-600">Up to 20 tickets</span>
            </div>
          </div>

          {/* Category Selection for Each Ticket */}
          <div className="mb-8">
            <h2 className="text-lg font-semibold mb-4">Select Age Category for Each Ticket</h2>
            <div className="space-y-4">
              {categories.map((category, index) => (
                <div key={index} className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                  <span className="font-medium text-gray-700 min-w-12">Ticket {index + 1}:</span>
                  <div className="flex gap-3 flex-wrap">
                    {(Object.entries(TICKET_PRICES) as [TicketCategory, number][]).map(([cat, price]) => (
                      <button
                        key={cat}
                        onClick={() => handleCategoryChange(index, cat)}
                        className={`px-4 py-2 rounded-lg border-2 transition-colors capitalize font-medium ${
                          category === cat
                            ? 'border-red-600 bg-red-50 text-red-600'
                            : 'border-gray-200 hover:border-gray-300 text-gray-700'
                        }`}
                      >
                        {cat} (${price})
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Price Summary */}
          <div className="mb-8 p-4 bg-blue-50 border-2 border-blue-200 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="text-lg font-semibold text-gray-700">Estimated Total:</span>
              <span className="text-2xl font-bold text-red-600">${estimatedTotal.toFixed(2)}</span>
            </div>
            <p className="text-sm text-gray-600 mt-2">Final price determined after seat selection</p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={() => navigate(-1)}
              className="flex-1 px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Back
            </button>
            <button
              onClick={handleContinue}
              className="flex-1 px-6 py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors"
            >
              Continue to Seats
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
