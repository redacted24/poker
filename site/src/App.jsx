import {
  BrowserRouter as Router,
  Routes, Route
} from 'react-router-dom'

import Intro from './pages/intro/Intro'
import Playground from './pages/playground/Playground'
import Lobby from './pages/lobby/Lobby'
import './app.css'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/playground" element={<Playground />} />
        <Route path="/lobby" element={<Lobby />} />
        <Route path="/" element={<Intro />} />
      </Routes>
    </Router>
  )
}

export default App