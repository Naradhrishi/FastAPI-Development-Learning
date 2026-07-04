// import { useState, useEffect } from 'react'

// function App() {
//   const [message, setMessage] = useState("Loading message...")
//   const [calculation, setCalculation] = useState(null)

//   useEffect(() => {
//     // Fetch from Endpoint 1
//     fetch('http://localhost:8000/api/message')
//       .then(res => res.json())
//       .then(data => setMessage(data.text))

//     // Fetch from Endpoint 2
//     fetch('http://localhost:8000/api/calculate?number=5')
//       .then(res => res.json())
//       .then(data => setCalculation(data.result))
//   }, [])

//   return (
//     <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
//       <h1>Simplest Full-Stack App</h1>

//       <h3>Backend Message:</h3>
//       <p style={{ color: 'blue' }}>{message}</p>

//       <h3>Backend Calculation (10 x 2):</h3>
//       <p style={{ color: 'green' }}>{calculation !== null ? calculation : "Loading calculation..."}</p>
//     </div>
//   )
// }

// export default App
