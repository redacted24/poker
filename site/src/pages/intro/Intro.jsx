import { Link } from 'react-router-dom'
import './intro.css'

const Intro = () => {
  return (
    <div id="intro-container">
      <h1 id='title'>The Poker Playground</h1>
      <div id='link-buttons'>
        <Link className="react-link-clickable" to='/playground'>
          <button id="campaign" className='link-button'>
            <div id="campaign-text">Campaign</div>
          </button>
          <img src="../../src/assets/ui/campaign-castle.svg" alt="doesnt work" id="campaign-image-1"></img>
          <img src="../../src/assets/ui/shield.svg" alt="doesnt work" id="campaign-image-2"></img>
          <img src="../../src/assets/ui/swords.svg" alt="doesnt work" id="campaign-image-3"></img>
          <img src="../../src/assets/ui/heart_filled.svg" alt="doesnt work" id="campaign-image-6"></img>
          <img src="../../src/assets/ui/heart.svg" alt="doesnt work" id="campaign-image-4"></img>
          <img src="../../src/assets/ui/heart.svg" alt="doesnt work" id="campaign-image-5"></img>
          <img src="../../src/assets/ui/sun.svg" alt="doesnt work" id="campaign-image-7"></img>
          <img src="../../src/assets/ui/cloud.svg" alt="doesnt work" id="campaign-image-8"></img>        
          <img src="../../src/assets/ui/cloud.svg" alt="doesnt work" id="campaign-image-9"></img>        
          <img src="../../src/assets/ui/line.svg" alt="doesnt work" id="campaign-image-10"></img>        
          <img src="../../src/assets/ui/bird.svg" alt="doesnt work" id="campaign-image-11"></img>        
        </Link>
        <Link className="react-link-clickable" to='/playground'>
          <button id="quickstart" className='link-button'>
            <div id="quickstart-text">Quick Start</div>
          </button>
          <img src="" alt="placeholder" id="quickstart-image-1"></img>
        </Link>
        <Link className="react-link-clickable" to='/host'>
          <button id="multiplayer" className='link-button'>
            <div id="multiplayer-text">Create a Table</div>
          </button>
          <img src="" alt="wtf" id="multiplayer-image-1"></img>
        </Link>
      </div>
    </div>
  )
}

export default Intro
