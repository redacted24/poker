import {
  BrowserRouter as Router,
  Routes, Route
} from 'react-router-dom'

import Intro from './pages/intro/Intro'
import Playground from './pages/playground/Playground'
import Host from './pages/lobby/Host'
import Lobby from './pages/lobby/Lobby'
import './app.css'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/playground" element={<Playground />} />
        <Route path="/lobby/:id" element={<Lobby />} />
        <Route path="/host" element={<Host />} />
        <Route path="/" element={<Intro />} />
      </Routes>
    </Router>
  )
}

export default App