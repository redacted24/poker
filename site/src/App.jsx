import {
  Routes, Route,
  useNavigate
} from 'react-router-dom'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import ls from 'localstorage-slim'
import { useEffect, useState } from 'react'

import Intro from './pages/intro/Intro'
import StartPage from './pages/startpage/StartPage'
import QuickStart from './pages/quickstart/QuickStart'
import Host from './pages/lobby/Host'
import Lobby from './pages/lobby/Lobby'
import Game from './pages/game/Game'
import './app.css'

import { io } from 'socket.io-client'

const App = () => {
    const [socketInstance, setSocketInstance] = useState(null)

    const navigate = useNavigate()

    useEffect(() => {
        `Getting a username from the user, then setting a time to live of 1h`
        const socket = io("localhost:5000/");
        setSocketInstance(socket);

        if (!ls.get('username')) {
            navigate('/start')
        }

        return () => {
            socket.disconnect();
        };
    }, [])

    const notify = (message, type) => {
        toast[type](message, {
        position: "top-right",
        autoClose: 4000,
        pauseOnHover: false,
        toastId: message,
        })
    }

    return (
        <>
        <Routes>
            <Route path="/quick-start" element={<QuickStart />} />
            <Route path="/lobby/:id" element={<Lobby socket={socketInstance} notify={notify} />} />
            <Route path="/game/:id" element={<Game socket={socketInstance} notify={notify} />} />
            <Route path="/host" element={<Host socket={socketInstance} notify={notify} />} />
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
