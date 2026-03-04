import { useEffect, useState } from 'react'
import { UseEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import BookingPage from './pages/BookingPage';

function App() {
  const [count, setCount] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  //The state "isBookingOpen" is false by default, which means we need to book a movie in order to trigger this.
  const [isBookingOpen, setIsBookingOpen] = useState(false);

  useEffect(() => { 
    fetch('/api/time')
      .then((response) => response.json())
      .then((data) => setCurrentTime(data.time))
      .catch((error) => console.error('Error fetching time:', error))
  }, [])

  return (
    <>
      {isBookingOpen ? (
        //Go back to the home screen when the back-button is clicked
        <BookingPage onBack={() => setIsBookingOpen(false)} />
        
      ) : (
        /* If false: Show the regular Vite home page */
        <>
          <div>
            <img src={viteLogo} className="logo" alt="Vite logo" />
            <img src={reactLogo} className="logo react" alt="React logo" />
          </div>
          <h1>Vite + React</h1>
          <div className="card">
            <button onClick={() => setCount((count) => count + 1)}>
              count is {count}
            </button>
            <p>The current time is {new Date(currentTime * 1000).toLocaleString()}.</p>
          </div>
          
          {/*Filler button to link to the checkout page*/}
          <button 
            className="book-button" 
            onClick={() => setIsBookingOpen(true)}
          >
            Book Tickets
          </button>
        </>
      )}
    </>
  )
}

export default App
