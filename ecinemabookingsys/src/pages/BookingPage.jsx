import React, { useState } from 'react';
import { mockMovies } from '../../mockData';
import './BookingPage.css';

/*
TODO: Please help me refine the UI. It's currently really boring because I only programmed this page for functionality.
TODO: Please  perhaps add the ability to select multiple seats based on the number of tickets chosen (already implemented). Currently only one seat can be chosen.
*/


const BookingPage = ({onBack}) => {
    //The current seat is blank; no seat for the user by default
    const [selectedSeat, setSelectedSeat] = useState("");
    //List of available seats to choose from (Will be in a dropdown menu)
    const availableSeats = ["A1", "A2", "B1", "B2", "Z1", "Z2"];
    //Set the initial ticket quantities for the current user
    const [adultQuantity, setAdultQuantity] = useState(0);
    const [childQuantity, setChildQuantity] = useState(0);
    const [seniorQuantity, setSeniorQuantity] = useState(0);
    const [stuQuantity, setStuQuantity] = useState(0);

    return (
        <div className="master-container">
            <nav>
                <div className="menu-options">
                    {/*Links back to the home page.*/}
                    <h1><a href="../App.jsx">CES THEATERS</a></h1>
                    {/*TODO: Implement this to perhaps link to the movies page.*/}
                    <h2 className="movies-tab">MOVIES</h2>
                    {/*TODO: Implement this to perhaps link to the bookings page.*/}
                    <h2 className="bookings-tab">BOOKINGS</h2>
                </div>

                {/*TODO: Implement this. Search does not work yet.*/}
                <input id="search-bar" type="text" placeholder="Search for a movie"/>
            </nav>

            <div className="movie-tix-div">
                <img src={mockMovies[0].poster} alt={mockMovies[0].title} className="movie-poster"/>

                <div className="details">
                    <div className="title-frame">
                        <h1>{mockMovies[0].title}</h1>
                        <div className="movie-specs">
                            <h3>{mockMovies[0].rating}</h3>
                            <p>Today, {mockMovies[0].showtimes[0]} (Auditorium 3)</p>
                        </div>
                    </div>

                    <h3>SELECT TICKETS</h3>
                </div>

                <div className="count-tix">
                    <div className="adult-tix">
                        <p><b>ADULT</b> (${mockMovies[0].prices.adult})</p>
                        {/*Logic to handle increasing and decreasing ticket count using buttons*/}
                        <form>
                            <button type="button" onClick={() => setAdultQuantity(Math.max(0, adultQuantity-1))}>-</button> {/*I got this from https://www.youtube.com/watch?v=o-yskJTNyBo*/}
                            <input id="tix-quantity" type="number" min="0" max="10" value={adultQuantity} onChange={(e) => setAdultQuantity(Number(e.target.value))}/>
                            <button type="button" onClick={() => setAdultQuantity(Math.min(10, adultQuantity+1))}>+</button>
                        </form>
                    </div>

                    <div className="child-tix">
                        <p><b>CHILD</b> (${mockMovies[0].prices.child})</p>
                        <form>
                            <button type="button" onClick={() => setChildQuantity(Math.max(0, childQuantity-1))}>-</button> 
                            <input id="tix-quantity" type="number" min="0" max="10" value={childQuantity} onChange={(e) => setChildQuantity(Number(e.target.value))}/>
                            <button type="button" onClick={() => setChildQuantity(Math.min(10, childQuantity+1))}>+</button>
                        </form>
                    </div>

                    <div className="senior-tix">
                        <p><b>SENIOR</b> (${mockMovies[0].prices.senior})</p>
                        <form>
                            <button type="button" onClick={() => setSeniorQuantity(Math.max(0, seniorQuantity-1))}>-</button> 
                            <input id="tix-quantity" type="number" min="0" max="10" value={seniorQuantity} onChange={(e) => setSeniorQuantity(Number(e.target.value))}/>
                            <button type="button" onClick={() => setSeniorQuantity(Math.min(10, seniorQuantity+1))}>+</button>
                        </form>
                    </div>

                    <div className="student-tix">
                        <p><b>STUDENT</b> (${mockMovies[0].prices.student})</p>
                        <form>
                            <button type="button" onClick={() => setStuQuantity(Math.max(0, stuQuantity-1))}>-</button> 
                            <input id="tix-quantity" type="number" min="0" max="10" value={stuQuantity} onChange={(e) => setStuQuantity(Number(e.target.value))}/>
                            <button type="button" onClick={() => setStuQuantity(Math.min(10, stuQuantity+1))}>+</button>
                        </form>
                    </div>

                </div>
            </div>

            <div className="summary-div">
                <div className="checkoutInfo">
                    {/*This uses the handleSeatSelect function below to change the selectedSeat useState to the chosen seat from the dropdown menu.
                    The Dropdown menu is populated by the seats array on line 9.*/}
                    <div className="select-seat">
                        {/*Logic taken from https://stackoverflow.com/questions/62239420/steps-to-populate-dynamic-dropdown-using-arrays-in-reactjs-using-react-hooks and https://codesandbox.io/s/dropdown-react-p0nj7*/}
                        <label htmlFor="seats">Choose your seat:</label>
                        <select name="seats" onChange={e => handleSeatSelect(e)} value={selectedSeat}> {/*Using the mock seats on line 12*/}
                            <option value="">Select a seat</option>
                            {availableSeats.map((seat, index) => (
                                <option key={index} value={seat}>{seat}</option>
                            ))}
                        </select>
                    </div>

                    <div className="book-sum">
                        <h2>BOOKING SUMMARY</h2>
                        <p>Selected Seat: {selectedSeat}</p>
                        <p><b>TOTAL PRICE: ${subtotal()}.00</b></p>
                    </div>
                </div>

                <button className="pay-button" onClick={() => alert(returnTickets())}>Click on me to Check Out!</button>
            </div>

        </div>
    ); //JSX

    function subtotal() {
        return (14*adultQuantity) + (10*childQuantity) + (11*seniorQuantity) + (12*stuQuantity);
    } //returnSubtotal
    function returnTickets() {
        if (adultQuantity==0 && childQuantity==0 && seniorQuantity==0 && stuQuantity==0) {
            return "You need to choose at least one ticket!";
        } //if
        if (selectedSeat=="") {
            return "You need to select a seat!";
        } //if
        const quantityMsg = `You are checking out ${adultQuantity} adult tickets, ${childQuantity} child tickets, ${seniorQuantity} senior tickets, and ${stuQuantity} student tickets.`;
        return `${quantityMsg}\n\nYour seat is ${selectedSeat}.\n\nThe subtotal is $${subtotal()}.00.`;
    } //returnTickets

    //handles the selection of seats in the select-seat div
    function handleSeatSelect(e) {
        const chosenSeat = e.target.value;
        //set seat use state to the chosen seat
        setSelectedSeat(chosenSeat);
    } //handleSeatSelect

}; //BookingPage

export default BookingPage;