import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    //User Types
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [loginError, setLoginError] = useState('');

    const handleLogin = async (e: React.MouseEvent) => {
        //Do not refresh the page upon login failure.
        e.preventDefault();

        //Clear login error status if any
        setLoginError('');

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email.trim(), password: password.trim()}),
            }); //response

            const data = await response.json();

            if (response.ok) {
                //Save the user session, establishing login
                sessionStorage.setItem('user', JSON.stringify(data.user));

                //If admin, redirect to admin homepage upon successful login
                if (data.user.role === 'admin') {
                    navigate('/admin-home');
                //Redirect to normal homepage otherwise
                } else {
                    navigate('/');
                } //else

            //Print message to login section, prompting user to try again
            } else {
                setLoginError(data.message || "Invalid email/password. Please try again.");
            } //if/else
        } catch (error) {
            console.error(error);
            setLoginError("Server connection failed.");
        } //try/catch
    }; //handleLogin

    return (
        <div className="min-h-screen flex items-center justify-center flex-col"> {/*The master div*/}
            <h1 className="text-3xl font-bold text-center mb-3">Welcome! Login or Sign Up</h1>

            {/*The container*/}
            <div className="w-[90%] max-w-md border-2 border-gray-200 p-8 rounded-xl flex flex-col gap-6">
                {/*The email div*/}
                <div className="flex flex-col gap-2">
                    <h1 className="text-2xl font-semibold">Email:</h1>
                    <input
                        type="email"
                        className="border-2 border-gray-200 bg-transparent p-2 rounded-lg"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                {/*The password div*/}
                <div className="flex flex-col gap-2">
                    <h1 className="text-2xl font-semibold">Password:</h1>
                    <input 
                        type="password"
                        className="border-2 border-gray-200 bg-transparent p-2 rounded-lg"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button className="italic text-blue-600 hover:text-blue-800 hover:underline">Forgot Password?</button>
                </div>

                {/*Display error message upon unsuccessful login*/}
                {loginError && (<p className="text-red-600 text-center">{loginError}</p>)}

                {/*login/register buttons div*/}
                <div className="flex flex-col gap-3">
                    <button 
                        onClick={handleLogin}
                        className="py-3 rounded-lg font-bold bg-red-500 hover:bg-red-600 text-white">
                            Login
                    </button>
                    {/*Redirect to the Register page*/}
                    <button 
                        onClick={() => navigate('/register')}
                        className="py-3 rounded-lg font-bold bg-gray-500 hover:bg-gray-600 text-white">
                            Register
                    </button>
                </div>
            </div>

            

            
        </div>
    ); //return
}; //const Login



export default Login;