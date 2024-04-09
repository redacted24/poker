import {
  BrowserRouter as Router,
  Routes, Route
} from 'react-router-dom'

import Intro from './Pages/intro/Intro'
import Playground from './Pages/playground/Playground'

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