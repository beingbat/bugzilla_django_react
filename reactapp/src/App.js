import React from 'react'
import {BrowserRouter, Route, Routes} from 'react-router-dom';
import Collection from './components/collections'
import './App.css'

const App = () => {
  return (
    <BrowserRouter>
      <div className="appDiv">
        <Routes>
          <Route path="react/:id" element={<Collection/>}>
          </Route>
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App;
