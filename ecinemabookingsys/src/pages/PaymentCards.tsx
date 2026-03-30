import { useState } from 'react';
import { CreditCard, Plus, Trash2 } from 'lucide-react';

interface PaymentCardForm {
  id: number;
  cardNumber: string;
  nameOnCard: string;
  expiryDate: string;
  cvv: string;
}

const emptyCard = (id: number): PaymentCardForm => ({
  id,
  cardNumber: '',
  nameOnCard: '',
  expiryDate: '',
  cvv: '',
});

export default function PaymentCards() {
  const [cards, setCards] = useState<PaymentCardForm[]>([]);

  const handleAddCard = () => {
    if (cards.length < 3) {
      setCards([...cards, emptyCard(Date.now())]);
    }
  };

  const handleRemoveCard = (id: number) => {
    setCards(cards.filter((card) => card.id !== id));
  };

  const handleCardChange = (id: number, field: keyof PaymentCardForm, value: string) => {
    setCards(cards.map((card) =>
      card.id === id ? { ...card, [field]: value } : card
    ));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Saving cards:', cards);
    // make API call here
  };

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
              <div>
                <label className="block text-sm text-gray-600 mb-1">CVV / CVC</label>
                <input
                  type="password"
                  value={card.cvv}
                  onChange={(e) => handleCardChange(card.id, 'cvv', e.target.value)}
                  placeholder="•••"
                  maxLength={4}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
                />
              </div>
            </div>
          </div>
        ))}

        {/* Save button */}
        <div className="flex justify-end pt-4">
          <button
            type="submit"
            className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
          >
            Save Cards
          </button>
        </div>
      </form>
    </div>
  );
}