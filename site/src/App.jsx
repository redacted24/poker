import {
  BrowserRouter as Router,
  Routes, Route
} from 'react-router-dom'
import { useEffect, useState } from 'react'
import ls from 'localstorage-slim'

import Intro from './pages/intro/Intro'
import Playground from './pages/playground/Playground'
import Host from './pages/lobby/Host'
import Lobby from './pages/lobby/Lobby'
import Game from './pages/game/Game'
import './app.css'

const App = () => {

  useEffect(() => {
    `Getting a username from the user, then setting a time to live of 1h`
    if (!ls.get('username')) {
      const username = prompt('Please enter your username.', 'Bob')
      ls.set('username', username, { ttl: 60 * 60 })
    }
  }, [])

  const clearIntervals = () => {
    let currentId = window.setInterval(function() {}, 0);
    while (currentId--) {
      window.clearInterval(currentId)
    }
  }

  return (
    <Router>
      <Routes>
        <Route path="/playground" element={<Playground clearIntervals={clearIntervals}/>} />
        <Route path="/lobby/:id" element={<Lobby clearIntervals={clearIntervals}/>} />
        <Route path="/game/:id" element={<Game clearIntervals={clearIntervals}/>} />
        <Route path="/host" element={<Host clearIntervals={clearIntervals}/>} />
        <Route path="/" element={<Intro />} />
      </Routes>
    </Router>
  )
}

export default App