import { useNavigate, useLocation } from 'react-router';
import { ArrowLeft, AlertCircle, CheckCircle2 } from 'lucide-react';
import { useState, useEffect } from 'react';

const TICKET_PRICES: Record<string, number> = {
  adult: 12,
  senior: 8,
  child: 6,
};

interface SavedCard {
  cardId: number;
  cardName: string;
  cardNumber: string;
  expirationDate: string;
  cvv: string;
}

export default function Payment() {
  const navigate = useNavigate();
  const location = useLocation();

  const token = location.state?.temp_booking_token;
  const booking = location.state?.booking;

  const [cardNumber, setCardNumber] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvc, setCvc] = useState('');
  const [nameOnCard, setNameOnCard] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Saved cards
  const [usePaymentMode, setUsePaymentMode] = useState<'new' | 'saved'>('new');
  const [savedCards, setSavedCards] = useState<SavedCard[]>([]);
  const [selectedCardId, setSelectedCardId] = useState<number | null>(null);
  const [loadingCards, setLoadingCards] = useState(true);

  // Load saved payment cards on mount
  useEffect(() => {
    const loadSavedCards = async () => {
      try {
        const response = await fetch('/api/retrieve-payment-cards', {
          credentials: 'include',
        });
        if (response.ok) {
          const cards = await response.json();
          setSavedCards(cards);
          if (cards.length > 0) {
            setSelectedCardId(cards[0].cardId);
          }
        }
      } catch (err) {
        console.error('Failed to load saved cards:', err);
      } finally {
        setLoadingCards(false);
      }
    };

    loadSavedCards();
  }, []);

  const formatCardNumber = (value: string) => {
    const digits = value.replace(/\D/g, '').slice(0, 16);
    return digits.replace(/(\d{4})/g, '$1 ').trim();
  };

  const formatExpiry = (value: string) => {
    const digits = value.replace(/\D/g, '').slice(0, 4);
    if (digits.length >= 2) {
      return `${digits.slice(0, 2)}/${digits.slice(2)}`;
    }
    return digits;
  };

  const validateForm = () => {
    if (usePaymentMode === 'saved') {
      if (!selectedCardId) {
        setError('Please select a saved card');
        return false;
      }
      return true;
    }

    // New card validation
    const cardDigits = cardNumber.replace(/\s/g, '');
    if (cardDigits.length !== 16) {
      setError('Card number must be 16 digits');
      return false;
    }
    if (!/^\d{2}\/\d{2}$/.test(expiry)) {
      setError('Expiry must be MM/YY format');
      return false;
    }
    if (cvc.length < 3 || cvc.length > 4) {
      setError('CVC must be 3-4 digits');
      return false;
    }
    if (!nameOnCard.trim()) {
      setError('Name on card is required');
      return false;
    }
    return true;
  };

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setError('');

    try {
      let paymentBody: any = {
        temp_booking_token: token,
      };

      if (usePaymentMode === 'saved') {
        // Use saved card
        paymentBody.card_id = selectedCardId;
      } else {
        // Use new card
        paymentBody.card_data = {
          cardNumber: cardNumber.replace(/\s/g, ''),
          expiry,
          cvc,
          nameOnCard,
        };
      }

      const response = await fetch('/api/bookings/process-payment', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paymentBody),
      });

      if (!response.ok) {
        const error_data = await response.json();
        throw new Error(error_data.error || 'Payment failed');
      }

      setSuccess(true);
      setTimeout(() => {
        navigate('/payment-confirmation', { state: { booking } });
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'An error occurred during payment');
      setLoading(false);
    }
  };

  if (!booking) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No booking data found</p>
          <button onClick={() => navigate('/')} className="px-4 py-2 bg-red-600 text-white rounded">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div  className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-3xl">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Order Summary */}
          <div className="md:col-span-2 bg-white rounded-lg shadow-lg p-8">
            <h1 className="text-3xl font-bold mb-8">Complete Payment</h1>

            {success ? (
              <div className="text-center py-12">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                  <CheckCircle2 className="w-10 h-10 text-green-600" />
                </div>
                <h2 className="text-2xl font-bold mb-2">Payment Successful!</h2>
                <p className="text-gray-600">Check your email to confirm your booking.</p>
                <p className="text-sm text-gray-500 mt-4">Redirecting...</p>
              </div>
            ) : (
              <form onSubmit={handlePayment}>
                {error && (
                  <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 flex items-start gap-2">
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                    <p>{error}</p>
                  </div>
                )}

                {/* Tabs for new/saved card */}
                <div className="mb-6 flex gap-4 border-b">
                  <button
                    type="button"
                    onClick={() => setUsePaymentMode('new')}
                    className={`pb-3 px-2 font-semibold transition-colors ${
                      usePaymentMode === 'new'
                        ? 'text-red-600 border-b-2 border-red-600'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    New Card
                  </button>
                  <button
                    type="button"
                    onClick={() => setUsePaymentMode('saved')}
                    disabled={loadingCards || savedCards.length === 0}
                    className={`pb-3 px-2 font-semibold transition-colors ${
                      usePaymentMode === 'saved'
                        ? 'text-red-600 border-b-2 border-red-600'
                        : 'text-gray-600 hover:text-gray-900 disabled:text-gray-300 disabled:cursor-not-allowed'
                    }`}
                  >
                    Saved Cards ({savedCards.length})
                  </button>
                </div>

                {usePaymentMode === 'saved' ? (
                  <>
                    {/* Saved Cards Selection */}
                    {loadingCards ? (
                      <div className="text-center py-6 text-gray-500">Loading saved cards...</div>
                    ) : savedCards.length === 0 ? (
                      <div className="text-center py-6 text-gray-500">No saved cards available</div>
                    ) : (
                      <div className="mb-8">
                        <label className="block text-sm font-semibold mb-3">Select a Card</label>
                        <select
                          value={selectedCardId || ''}
                          onChange={(e) => setSelectedCardId(Number(e.target.value))}
                          className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-600 focus:outline-none"
                        >
                          {savedCards.map((card) => (
                            <option key={card.cardId} value={card.cardId}>
                              {card.cardName} - {card.cardNumber.slice(-4).padStart(16, '*')}
                            </option>
                          ))}
                        </select>
                      </div>
                    )}
                  </>
                ) : (
                  <>
                    {/* New Card Form */}
                    {/* Card Number */}
                    <div className="mb-6">
                      <label className="block text-sm font-semibold mb-2">Card Number</label>
                      <input
                        type="text"
                        placeholder="1234 5678 9012 3456"
                        maxLength="19"
                        value={cardNumber}
                        onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-600 focus:outline-none"
                      />
                      <p className="text-xs text-gray-500 mt-2">Use any 16-digit number for this demo</p>
                    </div>

                    {/* Expiry & CVC */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div>
                        <label className="block text-sm font-semibold mb-2">Expiry Date</label>
                        <input
                          type="text"
                          placeholder="MM/YY"
                          maxLength="5"
                          value={expiry}
                          onChange={(e) => setExpiry(formatExpiry(e.target.value))}
                          className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-600 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold mb-2">CVC</label>
                        <input
                          type="text"
                          placeholder="123"
                          maxLength="4"
                          value={cvc}
                          onChange={(e) => setCvc(e.target.value.replace(/\D/g, ''))}
                          className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-600 focus:outline-none"
                        />
                      </div>
                    </div>

                    {/* Name on Card */}
                    <div className="mb-8">
                      <label className="block text-sm font-semibold mb-2">Name on Card</label>
                      <input
                        type="text"
                        placeholder="John Doe"
                        value={nameOnCard}
                        onChange={(e) => setNameOnCard(e.target.value)}
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-red-600 focus:outline-none"
                      />
                    </div>
                  </>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Processing...' : `Complete Payment - $${booking.totalPrice.toFixed(2)}`}
                </button>
              </form>
            )}
          </div>

          {/* Order Summary Sidebar */}
          <div className="bg-white rounded-lg shadow-lg p-8 h-fit">
            <h3 className="font-bold text-lg mb-4">Order Summary</h3>
            <div className="space-y-3 pb-4 border-b">
              <p className="text-sm"><span className="font-semibold">Movie:</span> {booking.movie.title}</p>
              <p className="text-sm"><span className="font-semibold">Date:</span> {booking.showtime.date}</p>
              <p className="text-sm"><span className="font-semibold">Time:</span> {booking.showtime.time}</p>
              <p className="text-sm"><span className="font-semibold">Seats:</span> {booking.seats.length}</p>
            </div>
            <div className="mt-4 space-y-2">
              {(() => {
                const counts: Record<string, number> = {};
                booking.seats.forEach((s: any) => {
                  counts[s.category] = (counts[s.category] || 0) + 1;
                });
                return Object.entries(counts).map(([cat, count]) => (
                  <div key={cat} className="flex justify-between text-sm capitalize">
                    <span>{count}x {cat}</span>
                    <span>${(count * TICKET_PRICES[cat]).toFixed(2)}</span>
                  </div>
                ));
              })()}
            </div>
            <div className="mt-4 pt-4 border-t flex justify-between font-bold">
              <span>Total:</span>
              <span className="text-red-600">${booking.totalPrice.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
