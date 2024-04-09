import {
  BrowserRouter as Router,
  Routes, Route
} from 'react-router-dom'

import Intro from './pages/intro/Intro'
import Playground from './pages/playground/Playground'

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/playground" element={<Playground />} />
        <Route path="/" element={<Intro />} />
      </Routes>
    </Router>
  )
}

export default App