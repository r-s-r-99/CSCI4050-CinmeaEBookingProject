import { useState, useEffect } from 'react';
import { CreditCard, Plus, Trash2, Eye, EyeOff } from 'lucide-react';

interface PaymentCardForm {
  id: number;       // local temp id for new cards; card_id from DB for existing
  cardId?: number;  // DB primary key (undefined for new unsaved cards)
  cardNumber: string;
  nameOnCard: string;
  expiryDate: string;
  cvv: string;
  isNew?: boolean;  // true = not yet in DB
}

const emptyCard = (): PaymentCardForm => ({
  id: Date.now(),
  cardNumber: '',
  nameOnCard: '',
  expiryDate: '',
  cvv: '',
  isNew: true,
});

export default function PaymentCards() {
  const [cards, setCards] = useState<PaymentCardForm[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [showCvv, setShowCvv] = useState<{ [key: number]: boolean }>({});

  const formatExpiry = (dateStr: string): string => {
    // converts "2026-03-01" → "03/26"
    const [year, month] = dateStr.split('-');
    return `${month}/${year.slice(2)}`;
  };

  const formatCardNumber = (value: string): string => {
    return value.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim().slice(0, 19);
  };

  const formatCVV = (value: string): string => {
    return value.replace(/\D/g, '').slice(0, 4).trim();
  };

  useEffect(() => {
    fetch('/api/retrieve-payment-cards', { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error('Failed to load payment cards');
        return res.json();
      })
      .then((data: { cardId: number; cardNumber: string; expirationDate: string, cardName: string; cvv: string }[]) => {
        setCards(data.map(c => ({
          id: c.cardId,
          cardId: c.cardId,
          cardNumber: c.cardNumber ? formatCardNumber(c.cardNumber) : '',
          nameOnCard: c.cardName ?? '',
          expiryDate: c.expirationDate ? formatExpiry(c.expirationDate) : '',
          cvv: c.cvv ? formatCVV(c.cvv) : '',
          isNew: false,
        })));
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleAddCard = () => {
    if (cards.length < 3) {
      setCards([...cards, emptyCard()]);
    }
  };

  const handleRemoveCard = async (id: number) => {
    const card = cards.find(c => c.id === id);

    if (card?.cardId) {
      try {
        await fetch('/api/delete-payment-card', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ cardId: card.cardId }),
        });
      } catch (err) {
        console.error('Failed to delete card:', err);
        return;
      }
    }

    setCards(cards.filter(c => c.id !== id));
  };

  const handleCardChange = (id: number, field: keyof PaymentCardForm, value: string) => {
    if (field === 'cardNumber') {
      value = value.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim();
      if (value.length > 19) value = value.slice(0, 19);
    }

    if (field === 'expiryDate') {
      value = value.replace(/\D/g, '');
      if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
      }
      if (value.length > 5) value = value.slice(0, 5);
    }

    if (field === 'cvv') {
      value = value.replace(/\D/g, '').slice(0, 4);
    }

    setCards(cards.map(card =>
      card.id === id ? { ...card, [field]: value } : card
    ));
  };

  const fetchCards = async (): Promise<PaymentCardForm[]> => {
    const res = await fetch('/api/retrieve-payment-cards', { credentials: 'include' });
    if (!res.ok) throw new Error('Failed to load payment cards');
    const data: { cardId: number; cardNumber: string; expirationDate: string; cardName: string; cvv: string }[] = await res.json();
    const mapped = data.map(c => ({
      id: c.cardId,
      cardId: c.cardId,
      cardNumber: c.cardNumber ? formatCardNumber(c.cardNumber) : '',
      nameOnCard: c.cardName ?? '',
      expiryDate: c.expirationDate ? formatExpiry(c.expirationDate) : '',
      cvv: c.cvv ? formatCVV(c.cvv) : '',
      isNew: false,
    }));
    setCards(mapped);
    return mapped;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSaving) return;
    setIsSaving(true);
    try {
      const currentCards = cards;

      // 2. Save remaining cards (INSERT new, UPDATE existing)
      await Promise.all(
        currentCards.map(card =>
          fetch('/api/update-payment-cards', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              cardId: card.cardId ?? null,
              cardNumber: card.cardNumber.replace(/\s/g, ''),
              expirationDate: card.expiryDate,
              cardName: card.nameOnCard,
              cvv: card.cvv,
            }),
          })
        )
      );

      // 3. Re-fetch to sync real DB state
      await fetchCards();
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error('Failed to save cards:', err);
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center h-full text-gray-500">
      Loading payment cards...
    </div>
  );

  if (error) return (
    <div className="flex items-center justify-center h-full text-red-500">
      {error}
    </div>
  );

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold">Payment Cards</h2>
        {cards.length < 3 && (
          <button
            onClick={handleAddCard}
            className="flex items-center gap-2 px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Add Card
          </button>
        )}
      </div>

      {/* Card count indicator */}
      <p className="text-sm text-gray-500 mb-6">{cards.length} of 3 cards saved</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        {cards.map((card, index) => (
          <div key={card.id} className="border border-gray-200 rounded-xl p-6 bg-gray-50">
            {/* Card header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <CreditCard className="w-5 h-5 text-gray-500" />
                <span className="font-medium text-gray-700">Card {index + 1}</span>
              </div>
              <button
                type="button"
                onClick={() => handleRemoveCard(card.id)}
                className="text-red-500 hover:text-red-700 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>

            {/* Card number */}
            <div className="mb-4">
              <label className="block text-sm text-gray-600 mb-1">Card Number</label>
              <input
                type="text"
                value={card.cardNumber}
                onChange={(e) => handleCardChange(card.id, 'cardNumber', e.target.value)}
                placeholder="1234 5678 9012 3456"
                maxLength={19}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            {/* Name on card */}
            <div className="mb-4">
              <label className="block text-sm text-gray-600 mb-1">Name on Card</label>
              <input
                type="text"
                value={card.nameOnCard}
                onChange={(e) => handleCardChange(card.id, 'nameOnCard', e.target.value)}
                placeholder="John Doe"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            {/* Expiry and CVV side by side */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Expiry Date</label>
                <input
                  type="text"
                  value={card.expiryDate}
                  onChange={(e) => handleCardChange(card.id, 'expiryDate', e.target.value)}
                  placeholder="MM/YY"
                  maxLength={5}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                />
              </div>
              <div className="relative">
                <label className="block text-sm text-gray-600 mb-1">CVV / CVC</label>
                <input
                  type={showCvv[card.id] ? 'text' : 'password'}
                  value={card.cvv}
                  onChange={(e) => handleCardChange(card.id, 'cvv', e.target.value)}
                  placeholder="•••"
                  maxLength={4}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                />
                <button
                  type="button"
                  onClick={() =>
                    setShowCvv((prev) => ({
                      ...prev,
                      [card.id]: !prev[card.id],
                    }))
                  }
                  className="absolute right-3 top-1/2 translate-y-[12%] text-gray-500 hover:text-gray-700"
                >
                  {showCvv[card.id] ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
          </div>
        ))}

        {/* Save button */}
        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={isSaving}
            className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSaving ? 'Saving...' : saved ? 'Saved ✓' : 'Save Cards'}
          </button>
        </div>
      </form>
    </div>
  );
}