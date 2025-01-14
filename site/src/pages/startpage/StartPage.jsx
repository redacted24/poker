import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

import '../intro/intro.css'
import './startPage.css'

const StartPage = () => {
  const [username, setUsername] = useState('')
  const navigate = useNavigate()


  const setName = (e) => {
    e.preventDefault()
    ls.set('username', username, { ttl: 60 * 60 })
    navigate(-1)
  }

  return (
    <div id="intro-container">
      <h1 id='prompt-title'>The Poker Playground</h1>
      <form id='prompt' onSubmit={setName}>
        <label htmlFor='prompt-input' id='prompt-question'>Please enter your username: </label>
        <input id='prompt-input' type='text' value={username} onChange={(e) => setUsername(e.target.value)}></input>
        {username && <button id='prompt-confirm' type='submit'>Confirm</button>}
      </form>
    </div>
  )
}

export default StartPage