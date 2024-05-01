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
  const [intervalIds, setIntervalIds] = useState([])

  useEffect(() => {
    `Getting a username from the user, then setting a time to live of 1h`
    if (!ls.get('username')) {
      const username = prompt('Please enter your username.', 'Bob')
      ls.set('username', username, { ttl: 60 * 60 })
    }
  }, [])

  const addIntervalId = (newIntervalId) => {
    setIntervalIds(intervalIds.concat(newIntervalId))
  }

  return (
    <Router>
      <Routes>
        <Route path="/playground" element={<Playground addIntervalId={addIntervalId}/>} />
        <Route path="/lobby/:id" element={<Lobby addIntervalId={addIntervalId}/>} />
        <Route path="/game/:id" element={<Game addIntervalId={addIntervalId}/>} />
        <Route path="/host" element={<Host addIntervalId={addIntervalId}/>} />
        <Route path="/" element={<Intro />} />
      </Routes>
    </Router>
  )
}

export default App