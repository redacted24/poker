import {
  BrowserRouter as Router,
  Routes, Route
} from 'react-router-dom'
import { useEffect, useState } from 'react'

import Intro from './pages/intro/Intro'
import Playground from './pages/playground/Playground'
import Host from './pages/lobby/Host'
import Lobby from './pages/lobby/Lobby'
import Game from './pages/game/Game'
import './app.css'

const App = () => {
  const [name, setName] = useState()

  useEffect(() => {
    const username = prompt('Please enter your username.', 'Bob')
    setName(username)
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="/playground" element={<Playground name={name} />} />
        <Route path="/lobby/:id" element={<Lobby name={name} />} />
        <Route path="/game/:id" element={<Game name={name} />}
        <Route path="/host" element={<Host name={name} />} />
        <Route path="/" element={<Intro />} />
      </Routes>
    </Router>
  )
}

export default App