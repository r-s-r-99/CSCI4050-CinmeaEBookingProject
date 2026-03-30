import { useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { Film, Eye, EyeOff, CreditCard, Plus, X } from 'lucide-react';

interface PaymentCard {
    id: string;
    cardNumber: string;
    cardName: string;
    expiryDate: string;
    cvv: string;
}

export default function Register() {
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phoneNumber: '',
        address: '',
        zipCode: '',
        houseNumber: '',
        aptNumber: '',
        password: '',
        confirmPassword: '',
        promotions: false,
    });

    const [paymentCards, setPaymentCards] = useState<PaymentCard[]>([]);
    const [showCardForm, setShowCardForm] = useState(false);
    const [newCard, setNewCard] = useState({
        cardNumber: '',
        cardName: '',
        expiryDate: '',
        cvv: '',
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value, type } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
        });
    };

    const handleCardInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        let { name, value } = e.target;

        // Format card number with spaces
        if (name === 'cardNumber') {
            value = value.replace(/\s/g, '').replace(/(\d{4})/g, '$1 ').trim();
            if (value.length > 19) value = value.slice(0, 19);
        }

        // Format expiry date
        if (name === 'expiryDate') {
            value = value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            if (value.length > 5) value = value.slice(0, 5);
        }

        // Limit CVV
        if (name === 'cvv') {
            value = value.replace(/\D/g, '').slice(0, 4);
        }

        setNewCard({
            ...newCard,
            [name]: value,
        });
    };

    const handleAddCard = () => {
        if (newCard.cardNumber && newCard.cardName && newCard.expiryDate && newCard.cvv) {
            setPaymentCards([
                ...paymentCards,
                {
                    id: Date.now().toString(),
                    ...newCard,
                },
            ]);
            setNewCard({
                cardNumber: '',
                cardName: '',
                expiryDate: '',
                cvv: '',
            });
            setShowCardForm(false);
        }
    };

    const handleRemoveCard = (cardId: string) => {
        setPaymentCards(paymentCards.filter(card => card.id !== cardId));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        setSuccess(null);

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match.');
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: formData.email,
                    password: formData.password,
                    firstName: formData.firstName,
                    lastName: formData.lastName,
                    phoneNumber: formData.phoneNumber,
                    promotions: formData.promotions,
                    address: formData.address,
                    zipCode: formData.zipCode,
                    houseNumber: formData.houseNumber,
                    aptNumber: formData.aptNumber,
                    paymentCards: paymentCards,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.error);
                return;
            }

            setSuccess('Registration successful! Please check your email to activate your account.');
            // delay navigation so user can see the success message
            setTimeout(() => navigate('/login'), 3000);

        } catch (err) {
            setError('Something went wrong. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-red-900 to-gray-900 py-8 px-4">
            <div className="max-w-2xl mx-auto">
                {/* Logo */}
                <div className="text-center mb-8">
                    <Link to="/" className="inline-flex items-center gap-2 text-white text-3xl">
                        <Film className="w-10 h-10 text-red-500" />
                        <span>CineBook</span>
                    </Link>
                </div>

                {/* Registration Card */}
                <div className="bg-white rounded-2xl shadow-2xl p-8">
                    <h2 className="text-3xl text-center mb-2">Create Account</h2>
                    <p className="text-gray-600 text-center mb-8">Join CineBook today</p>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Name Fields */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="firstName" className="block text-sm mb-2">
                                    First Name <span className="text-red-500">*</span>
                                </label>
                                <input
                                    type="text"
                                    id="firstName"
                                    name="firstName"
                                    value={formData.firstName}
                                    onChange={handleInputChange}
                                    required
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                    placeholder="John"
                                />
                            </div>
                            <div>
                                <label htmlFor="lastName" className="block text-sm mb-2">
                                    Last Name <span className="text-red-500">*</span>
                                </label>
                                <input
                                    type="text"
                                    id="lastName"
                                    name="lastName"
                                    value={formData.lastName}
                                    onChange={handleInputChange}
                                    required
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                    placeholder="Doe"
                                />
                            </div>
                        </div>

                        {/* Email */}
                        <div>
                            <label htmlFor="email" className="block text-sm mb-2">
                                Email Address <span className="text-red-500">*</span>
                            </label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                required
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                placeholder="your.email@example.com"
                            />
                        </div>

                        {/* Phone Number */}
                        <div>
                            <label htmlFor="phoneNumber" className="block text-sm mb-2">
                                Phone Number <span className="text-gray-400">(Optional)</span>
                            </label>
                            <input
                                type="tel"
                                id="phoneNumber"
                                name="phoneNumber"
                                value={formData.phoneNumber}
                                onChange={handleInputChange}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                placeholder="+1 (555) 123-4567"
                            />
                        </div>

                        {/* Address */}
                        <div>
                            <label className="block text-sm mb-2">Street Address</label>
                            <input
                                type="text"
                                name="address"
                                value={formData.address}
                                onChange={handleInputChange}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                            />
                        </div>

                        <div>
                            <label className="block text-sm mb-2">Zip Code</label>
                            <input
                                type="text"
                                name="zipCode"
                                value={formData.zipCode}
                                onChange={handleInputChange}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm mb-2">House Number</label>
                                <input
                                    type="text"
                                    name="houseNumber"
                                    value={formData.houseNumber}
                                    onChange={handleInputChange}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                                />
                            </div>
                            <div>
                                <label className="block text-sm mb-2">Apartment Number</label>
                                <input
                                    type="text"
                                    name="aptNumber"
                                    value={formData.aptNumber}
                                    onChange={handleInputChange}
                                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                                />
                            </div>
                        </div>

                        {/* Password Fields */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="password" className="block text-sm mb-2">
                                    Password <span className="text-red-500">*</span>
                                </label>
                                <div className="relative">
                                    <input
                                        type={showPassword ? 'text' : 'password'}
                                        id="password"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleInputChange}
                                        required
                                        className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                        placeholder="••••••••"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                                    >
                                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                    </button>
                                </div>
                            </div>
                            <div>
                                <label htmlFor="confirmPassword" className="block text-sm mb-2">
                                    Confirm Password <span className="text-red-500">*</span>
                                </label>
                                <div className="relative">
                                    <input
                                        type={showConfirmPassword ? 'text' : 'password'}
                                        id="confirmPassword"
                                        name="confirmPassword"
                                        value={formData.confirmPassword}
                                        onChange={handleInputChange}
                                        required
                                        className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                                        placeholder="••••••••"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                                    >
                                        {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* Payment Cards Section */}
                        <div>
                            <label className="block text-sm mb-3">Payment Cards (Optional)</label>

                            {/* Existing Cards */}
                            {paymentCards.length > 0 && (
                                <div className="space-y-3 mb-3">
                                    {paymentCards.map(card => (
                                        <div
                                            key={card.id}
                                            className="flex items-center justify-between p-4 border border-gray-300 rounded-lg bg-gradient-to-r from-gray-700 to-gray-900 text-white"
                                        >
                                            <div className="flex items-center gap-3">
                                                <CreditCard className="w-6 h-6" />
                                                <div>
                                                    <div className="font-mono">{card.cardNumber}</div>
                                                    <div className="text-sm text-gray-300">{card.cardName}</div>
                                                </div>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => handleRemoveCard(card.id)}
                                                className="p-1 hover:bg-white/10 rounded transition-colors"
                                            >
                                                <X className="w-5 h-5" />
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}

                            {/* Add Card Form */}
                            {showCardForm ? (
                                <div className="border border-gray-300 rounded-lg p-4 space-y-3">
                                    <div>
                                        <input
                                            type="text"
                                            name="cardNumber"
                                            value={newCard.cardNumber}
                                            onChange={handleCardInputChange}
                                            placeholder="Card Number"
                                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="text"
                                            name="cardName"
                                            value={newCard.cardName}
                                            onChange={handleCardInputChange}
                                            placeholder="Cardholder Name"
                                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
                                        />
                                    </div>
                                    <div className="grid grid-cols-2 gap-3">
                                        <input
                                            type="text"
                                            name="expiryDate"
                                            value={newCard.expiryDate}
                                            onChange={handleCardInputChange}
                                            placeholder="MM/YY"
                                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
                                        />
                                        <input
                                            type="text"
                                            name="cvv"
                                            value={newCard.cvv}
                                            onChange={handleCardInputChange}
                                            placeholder="CVV"
                                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-red-500"
                                        />
                                    </div>
                                    <div className="flex gap-2">
                                        <button
                                            type="button"
                                            onClick={handleAddCard}
                                            className="flex-1 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                                        >
                                            Add Card
                                        </button>
                                        <button
                                            type="button"
                                            onClick={() => setShowCardForm(false)}
                                            className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 transition-colors"
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            ) : (
                                <button
                                    type="button"
                                    onClick={() => setShowCardForm(true)}
                                    className="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-red-500 hover:bg-red-50 transition-colors flex items-center justify-center gap-2 text-gray-600 hover:text-red-600"
                                >
                                    <Plus className="w-5 h-5" />
                                    <span>Add Payment Card</span>
                                </button>
                            )}
                        </div>

                        {/* Promotions Checkbox */}
                        <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-lg">
                            <input
                                type="checkbox"
                                id="promotions"
                                name="promotions"
                                checked={formData.promotions}
                                onChange={handleInputChange}
                                className="w-5 h-5 text-red-600 rounded focus:ring-red-500 mt-0.5"
                            />
                            <label htmlFor="promotions" className="text-sm text-gray-700 cursor-pointer">
                                I want to receive promotional emails about upcoming movies, special offers,
                                and exclusive cinema events. You can unsubscribe at any time.
                            </label>
                        </div>

                        {/* Error message */}
                        {error && (
                            <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                                {error}
                            </div>
                        )}

                        {/* Success message */}
                        {success && (
                            <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm">
                                {success}
                            </div>
                        )}

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-lg disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isLoading ? 'Creating Account...' : 'Create Account'}
                        </button>
                    </form>

                    {/* Sign In Link */}
                    <p className="text-center mt-6 text-sm text-gray-600">
                        Already have an account?{' '}
                        <Link to="/login" className="text-red-600 hover:text-red-700">
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
