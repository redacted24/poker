import {
  Routes, Route,
  useNavigate
} from 'react-router-dom'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import ls from 'localstorage-slim'
import { useEffect } from 'react'

import Intro from './pages/intro/Intro'
import StartPage from './pages/startpage/StartPage'
import QuickStart from './pages/quickstart/QuickStart'
import Host from './pages/lobby/Host'
import Lobby from './pages/lobby/Lobby'
import Game from './pages/game/Game'
import './app.css'

const App = () => {
  const navigate = useNavigate()

  useEffect(() => {
    `Getting a username from the user, then setting a time to live of 1h`
    if (!ls.get('username')) {
      navigate('/start')
    }
  }, [])

  const clearIntervals = () => {
    let currentId = window.setInterval(function() {}, 0);
    while (currentId--) {
      window.clearInterval(currentId)
    }
  }

  const notify = (message, type) => {
    toast[type](message, {
      position: "top-center",
      autoClose: 4000,
      pauseOnHover: false,
      toastId: message,
    })
  }

  return (
    <>
      <Routes>
        <Route path="/quick-start" element={<QuickStart />} />
        <Route path="/lobby/:id" element={<Lobby notify={notify} clearIntervals={clearIntervals}/>} />
        <Route path="/game/:id" element={<Game notify={notify} clearIntervals={clearIntervals}/>} />
        <Route path="/host" element={<Host notify={notify} clearIntervals={clearIntervals}/>} />
        <Route path='/start' element={<StartPage />} />
        <Route path="/" element={<Intro />} />
      </Routes>
      <ToastContainer
        pauseOnFocusLoss={false}
      />
    </>
  )
}

export default App