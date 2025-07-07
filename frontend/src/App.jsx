import { useState } from 'react'
import { ClerkProviderWithRoutes } from './auth/ClerkProviderWithRoutes.jsx'
import { Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <ClerkProviderWithRoutes>
      <Routes>
       
      </Routes>
    </ClerkProviderWithRoutes>
  )
}

export default App
