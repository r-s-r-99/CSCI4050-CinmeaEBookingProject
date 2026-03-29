import React, { useState } from 'react';
import { mockMovies } from '../../mockData';
import './BookingPage.css';



const BookingPage = ({onBack}) => {
    //List of available seats to choose from (Will be in a dropdown menu)
    const [availableSeats, setAvailableSeats] = useState(["A1", "A2", "B1", "B2", "Z1", "Z2"]);
    //Set the chosen seats as an array to be displayed when chosen. Initially empty by default.
    const [selectedSeats, setSelectedSeats] = useState([]);
    //Set the initial ticket quantities for the current user
    const [adultQuantity, setAdultQuantity] = useState(0);
    const [childQuantity, setChildQuantity] = useState(0);
    const [seniorQuantity, setSeniorQuantity] = useState(0);
    const [stuQuantity, setStuQuantity] = useState(0);
    //Store the total number of tickets chosen by the user.
    const totalTicketsChosen = adultQuantity + childQuantity + seniorQuantity + stuQuantity;
    

    return (
        <div className="master-container">
            <nav>
                <div className="menu-options">
                    {/*Links back to the home page.*/}
                    <h2><a href="../App.jsx">CES THEATERS</a></h2>
                    {/*TODO: Implement this to perhaps link to the movies page.*/}
                    <h3 className="movies-tab">MOVIES</h3>
                    {/*TODO: Implement this to perhaps link to the bookings page.*/}
                    <h3 className="bookings-tab">BOOKINGS</h3>
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
                        <select name="seats" onChange={(e) => handleSeatSelect(e.target.value)} value=""> {/*Using the mock seats on line 12*/}
                            <option value="">Select a seat</option>
                            {availableSeats.map((seat, index) => (
                                <option key={index} value={seat}>{seat}</option>
                            ))}
                        </select>
                    </div>

                    <div className="book-sum">
                        <h2>BOOKING SUMMARY</h2>
                        <h4>Selected Seats: </h4>
                        {selectedSeats.map((seat, index) => (
                            <button 
                                key={index} 
                                onClick={() => handleSeatRemoval(seat)}>
                                {seat}
                            </button>
                        ))}
                        <p><b>SUBTOTAL: ${subtotal()}.00</b></p>
                    </div>
                </div>

                <button className="pay-button" onClick={() => alert(returnTickets())}>Click on me to Check Out!</button>
            </div>

        </div>
    ); //JSX

    function subtotal() {
        return `${(14*adultQuantity) + (10*childQuantity) + (11*seniorQuantity) + (12*stuQuantity)}`;
    } //subtotal

    function returnTickets() {
        if (adultQuantity==0 && childQuantity==0 && seniorQuantity==0 && stuQuantity==0) {
            return "You need to choose at least one ticket!";
        } //if
        if (selectedSeats.length==0) {
            return "You need to select a seat!";
        } //if

        if (totalTicketsChosen > selectedSeats.length) {
            return `You have chosen ${totalTicketsChosen} tickets. You must pick ${totalTicketsChosen} seats!`;
        } //if
        const quantityMsg = `You are checking out ${adultQuantity} adult tickets, ${childQuantity} child tickets, ${seniorQuantity} senior tickets, and ${stuQuantity} student tickets.`;
        return `${quantityMsg}\n\nYou have chosen seats ${selectedSeats}.\n\nYour subtotal is $${subtotal()}.00.`;
    } //returnTickets

    //handles the selection of seats in the select-seat div
    function handleSeatSelect(seat) {
        //The system will only allow you to choose a number of seats based on the number of tickets selected to prevent seat booking fraud.
        if (selectedSeats.length >= totalTicketsChosen) {
            alert(`You have chosen ${totalTicketsChosen} tickets. You are only allowed to pick ${totalTicketsChosen} seats!`);
            return;
        } //if

        if (availableSeats.length == 0) {
            alert("There are no more seats available!");
            return;
        } //if
        /*When a seat is chosen, remove it from the availableSeat array and add it to the selectedSeat array
          Use the filter array function to create a new array and remove that array from the availableSeats array
        */
        const removeAvailable = availableSeats.filter(ps => ps !== seat);
        setAvailableSeats(removeAvailable);

        //Add those selected seats to the new selectedSeats array
        setSelectedSeats([...selectedSeats, seat]);
    } //handleSeatSelect

    //handles the removal of selected seats
    function handleSeatRemoval(seat) {
        //Remove seats from chosen list
        const removeSelected = selectedSeats.filter(ps => ps !== seat);
        setSelectedSeats(removeSelected);

        //Add that removed array of seats back to the available seats
        setAvailableSeats([...availableSeats, seat]);
    } //handleSeatRemoval



}; //BookingPage

export default BookingPage;