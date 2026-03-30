import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const MockEmailConfirm = () => {
    const navigate = useNavigate();
    const [status, setStatus] = useState('Verifying...');

    useEffect(() => {
        const user = JSON.parse(sessionStorage.getItem('user') || '{}');
        const email = user.email || "test@example.com"; 

        // Tell backend to activate this email
        fetch('/api/confirm', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        })
        .then(res => res.json())
        .then(data => setStatus(data.message));
    }, []);

    return (
        <div className="min-h-screen flex items-center justify-center flex-col gap-4">
            <div className="p-10 border-2 border-green-500 rounded-xl text-center">
                <h1 className="text-3xl font-bold mb-4">Email Confirmation</h1>
                <p className="text-xl italic">{status}</p>
                <button 
                    onClick={() => navigate('/login')}
                    className="mt-6 px-6 py-2 bg-blue-500 text-white rounded-lg"
                >
                    Back to Login
                </button>
            </div>
        </div>
    );
};

export default MockEmailConfirm;