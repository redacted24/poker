import { Link } from 'react-router-dom'
import './intro.css'

const Intro = () => {
  return (
    <div id="intro-container">
      <h1 id='title'>The Poker Playground</h1>
      <div id='link-buttons'>
        <Link className="react-link-clickable" to='/playground'>
          <button id="campaign" className='link-button'>
            Campaign
          </button>
          <img src="../../src/assets/ui/campaign-castle.svg" alt="doesnt work" id="campaign-image-1"></img>
        </Link>
        <Link className="react-link-clickable" to='/playground'><button id="quickstart" className='link-button'>Quick Start</button></Link>
        <Link className="react-link-clickable" to='/host'><button id="create-table" className='link-button'>Create a Table</button></Link>
      </div>
    </div>
  )
}

export default Intro
