import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ReceiptText, UserPen, Clapperboard, CalendarClock, } from 'lucide-react';


const AdminHome = () => {
    const navigate = useNavigate();

    //This makes sure that only the admin can access this page.
    useEffect(() => {
        //Get the current user info from the current session
        const userS = sessionStorage.getItem('user');
        //If found, assign the session's user to the user constant. null if not found (Not logged in)
        const user = userS ? JSON.parse(userS) : null;

        //If there is no user currently logged in or if the logged in user is not an admin, redirect them to the home page and display a warning.
        if (user===null || user.role !== 'admin') {
            alert("Access Denied. you are attempting to access an admin page!");
            navigate('/');
        } //if
    });

    return (
        <div className="min-h-screen bg-gray-100">
            {/*Hero Section*/}
            <div className="bg-gray-800 py-20 border-b border-red-700">
                <div className="relative container mx-auto px-4 flex flex-col justify-center items-center text-white text-center">
                    <h1 className="text-5xl font-bold mb-4">Welcome, Admin</h1>
                    <p className="text-lg">Cinema E-Booking System Management Page</p>
                </div>
            </div>
            
            <div className="container mx-auto px-4 py-12">
                {/*Admin Menu Seciton*/}
                <div className="flec items-center justify-between">
                    <h2 className="text-3xl font-semibold border-b-20 border-transparent">Admin Menu</h2>

                    {/*Menu Option Grid*/}
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><Clapperboard/>Manage Movies</h3>
                            <p className="text-gray-500 text-sm">Access and update movie availability</p>
                        </div>

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><ReceiptText/>Manage Promotions</h3>
                            <p className="text-gray-500 text-sm">Access and update current promotion codes and data </p>
                        </div>

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><UserPen/>Manage Users</h3>
                            <p className="text-gray-500 text-sm">Access and update user list</p>
                        </div>

                        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer">
                            <h3 className="text-xl font-bold text-gray-900 mb-2"><CalendarClock/>Manage Showtimes</h3>
                            <p className="text-gray-500 text-sm">Access and update current movie showtimes and dates</p>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        
        
    ); //return
}; //AdminHome

export default AdminHome;