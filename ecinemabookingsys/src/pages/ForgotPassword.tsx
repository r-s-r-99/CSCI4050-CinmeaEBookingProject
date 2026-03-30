import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ForgotPassword = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [step, setStep] = useState(1); // 1 = Request, 2 = Reset
    const [message, setMessage] = useState('');

    // STEP 1: Just verify the email exists
    const handleSendRequest = async () => {
        const response = await fetch('/api/forgot-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        
        if (response.ok) {
            setStep(2); // Switch to the password inputs "right here"
            setMessage("Email found! Please enter your new password below.");
        } else {
            const data = await response.json();
            alert(data.message || "Email not found.");
        }
    };

    // STEP 2: Update the password in the DB
    const handleUpdatePassword = async () => {
        const response = await fetch('/api/reset-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, newPassword })
        });

        if (response.ok) {
            alert("Password updated! Try logging in now.");
            navigate('/login');
        } else {
            alert("Error updating password.");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center flex-col gap-4 bg-gray-50">
            <h1 className="text-3xl font-bold">Account Recovery</h1>
            
            <div className="w-[90%] max-w-md border-2 border-gray-200 p-8 rounded-xl bg-white shadow-sm flex flex-col gap-4">
                
                {/* STEP 1 UI */}
                {step === 1 && (
                    <>
                        <p className="text-gray-600">Enter your email to reset your password.</p>
                        <input 
                            type="email" 
                            className="border-2 border-gray-200 p-2 rounded-lg"
                            placeholder="Email Address"
                            onChange={(e) => setEmail(e.target.value)} 
                        />
                        <button 
                            onClick={handleSendRequest}
                            className="py-3 rounded-lg font-bold bg-red-500 text-white hover:bg-red-600"
                        >
                            Find Account
                        </button>
                    </>
                )}

                {/* STEP 2 UI (Appears "Right There") */}
                {step === 2 && (
                    <>
                        <p className="text-blue-600 font-semibold">{message}</p>
                        <div className="flex flex-col gap-1">
                            <label className="text-sm font-bold">New Password:</label>
                            <input 
                                type="password" 
                                className="border-2 border-gray-200 p-2 rounded-lg"
                                onChange={(e) => setNewPassword(e.target.value)} 
                            />
                        </div>
                        <button 
                            onClick={handleUpdatePassword}
                            className="py-3 rounded-lg font-bold bg-green-600 text-white hover:bg-green-700"
                        >
                            Update Password
                        </button>
                    </>
                )}

                <button onClick={() => navigate('/login')} className="text-sm underline text-gray-400">
                    Cancel
                </button>
            </div>
        </div>
    );
};

export default ForgotPassword;