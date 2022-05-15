import React from 'react'
import {BrowserRouter, Route, Routes} from 'react-router-dom';
import Collection from './components/collections'
import Navigation from './components/navbar'
import './App.css'

const App = () => {
  return (
    <BrowserRouter>
      <Navigation/>
      {/* <br/><br/><br/><br/> */}
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
