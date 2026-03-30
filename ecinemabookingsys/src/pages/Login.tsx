import React from 'react';

const Login = () => {
    return (
        <div className="min-h-screen flex items-center justify-center flex-col"> {/*The master div*/}
            <h1 className="text-3xl font-bold text-center mb-3">Welcome! Login or Sign Up</h1>

            {/*The container*/}
            <div className="w-[90%] max-w-md border-2 border-gray-200 p-8 rounded-xl flex flex-col gap-6">
                {/*The email div*/}
                <div className="flex flex-col gap-2">
                    <h1 className="text-2xl font-semibold">Email:</h1>
                    <input type="email" className="border-2 border-gray-200 bg-transparent p-2 rounded-lg"/>
                </div>

                {/*The password div*/}
                <div className="flex flex-col gap-2">
                    <h1 className="text-2xl font-semibold">Password:</h1>
                    <input type="password" className="border-2 border-gray-200 bg-transparent p-2 rounded-lg"/>
                    <button className="italic text-blue-600 hover:text-blue-800 hover:underline">Forgot Password?</button>
                </div>

                {/*login/register buttons div*/}
                <div className="flex flex-col gap-3">
                    <button className="py-3 rounded-lg font-bold bg-red-500 hover:bg-red-600 text-white">Login</button>
                    <button className="py-3 rounded-lg font-bold bg-gray-500 hover:bg-gray-600 text-white">Register</button>
                </div>
            </div>

            

            
        </div>
    ); //return
}; //const Login

export default Login;