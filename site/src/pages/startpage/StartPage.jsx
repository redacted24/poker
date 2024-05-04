import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

import '../intro/intro.css'
import './startPage.css'

const StartPage = () => {
  const [username, setUsername] = useState('')
  const navigate = useNavigate()

  const buttonStyle = () => {
    if (username) {
      return { visibility: 'visible', opacity: 1, scale: 1 }
    } else {
      return { visibility: 'hidden', opacity: 0 }
    }
  }

  const setName = () => {
    ls.set('username', username, { ttl: 60 * 60 })
    navigate(-1)
  }

  return (
    <div id="intro-container">
      <h1 id='title'>The Poker Playground</h1>
      <div id='prompt'>
        <label htmlFor='prompt-input' id='prompt-question'>Please enter your username: </label>
        <input id='prompt-input' type='text' value={username} onChange={(e) => setUsername(e.target.value)}></input>
        <button id='prompt-confirm' style={buttonStyle()} onClick={setName}>Confirm</button>
      </div>
    </div>
  )
}

export default StartPage