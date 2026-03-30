import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Register = () => {
    const navigate = useNavigate();
    //Take the info input by the user
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: '',
        phone: '',
    }); //useState
    
    //Mock email link
    const [successLink, setSuccessLink] = useState('');

    //Handle submission of user info
    const handleRegistration = async (e: React.FormEvent) => {
        //Prevent the page from refreshing
        e.preventDefault();

        //Confirm passwords match
        if (formData.password !== formData.confirmPassword) {
            alert("Passwords do not match! Please try again.");
            return;
        } //if

        //Call the backend
        const response = await fetch('/api/register', {
            method: 'POST',
            //label for flask
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        }); //response

        const data = await response.json();

        if (response.ok) {
            //Display link on screen
            setSuccessLink(data.confirmation_url);
            alert("Registration successful! Check the link on screen.");
            navigate(`/MockEmailConfirm?email=${formData.email}`);
        } else {
            alert(data.message);
        } //else
  
    }; //handleRegistration

    return (
        <div className="min-h-screen flex items-center justify-center flex-col gap-4">
            <h1 className="text-3xl font-bold">Register</h1>

            <div className="w-[90%] max-w-md border-2 border-gray-200 p-8 rounded-xl flex flex-col gap-4">
                
                {/*Username and Email*/}
                <div className="flex flex-col gap-1">
                    <label className="font-semibold">Username:</label>
                    <input type="text" className="border-2 border-gray-200 p-2 rounded-lg" 
                        onChange={(e) => setFormData({...formData, username: e.target.value})} />
                </div>

                <div className="flex flex-col gap-1">
                    <label className="font-semibold">Email:</label>
                    <input type="email" className="border-2 border-gray-200 p-2 rounded-lg" 
                        onChange={(e) => setFormData({...formData, email: e.target.value})} />
                </div>

                {/* Names Section */}
                <div className="flex gap-2">
                    <div className="flex flex-col gap-1 w-1/2">
                        <label className="font-semibold">First Name:</label>
                        <input type="text" className="border-2 border-gray-200 p-2 rounded-lg" 
                            onChange={(e) => setFormData({...formData, firstName: e.target.value})} />
                    </div>
                    <div className="flex flex-col gap-1 w-1/2">
                        <label className="font-semibold">Last Name:</label>
                        <input type="text" className="border-2 border-gray-200 p-2 rounded-lg" 
                            onChange={(e) => setFormData({...formData, lastName: e.target.value})} />
                    </div>
                </div>

                {/* Phone */}
                <div className="flex flex-col gap-1">
                    <label className="font-semibold">Phone Number:</label>
                    <input type="text" className="border-2 border-gray-200 p-2 rounded-lg" 
                        onChange={(e) => setFormData({...formData, phone: e.target.value})} />
                </div>

                {/* Passwords */}
                <div className="flex flex-col gap-1">
                    <label className="font-semibold">Password:</label>
                    <input type="password" title="password" className="border-2 border-gray-200 p-2 rounded-lg" 
                        onChange={(e) => setFormData({...formData, password: e.target.value})} />
                </div>

                <div className="flex flex-col gap-1">
                    <label className="font-semibold">Confirm Password:</label>
                    <input type="password" title="confirm password" className="border-2 border-gray-200 p-2 rounded-lg" 
                        onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})} />
                </div>

                <button 
                    onClick={handleRegistration} 
                    className="mt-4 py-3 rounded-lg font-bold bg-red-500 hover:bg-red-600 text-white"
                >
                    Register
                </button>

                {/* Success Link */}
                {successLink && (
                    <div className="mt-4 p-3 bg-gray-100 border border-gray-300 rounded text-center">
                        <p className="text-sm mb-1">Confirmation Link:</p>
                        <a href={successLink} className="text-blue-600 underline font-bold italic">
                            Click here to confirm
                        </a>
                    </div>
                )}
            </div>
        </div>
    ); //return
}; //const Register

export default Register;