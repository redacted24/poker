import { Link } from 'react-router-dom'
import { useEffect } from 'react'
import './intro.css'

const Intro = () => {
  // useEffect(() => {
  //   // Used to disable animation load on page load
  //   const DisableLoadAnimation = () => {
  //     let campaign = document.getElementById('campaign')
  //     let quickstart = document.getElementById('quickstart')
  //     let multiplayer = document.getElementById('multiplayer')
      
  //     const addAnimCampaign = () => {
  //       console.log('campaign mouse over')
  //       document.getElementById('campaign-image-1').classList.add('back-animation')
  //       document.getElementById('campaign-image-2').classList.add('back-animation')
  //       campaign.removeEventListener('mouseover', addAnimCampaign)
  //     }
  //     campaign.addEventListener('mouseover', addAnimCampaign)
  //   }
  //   // DisableLoadAnimation()
  // })

  return (
    <div id="intro-container">
      <h1 id='title'>The Poker Playground</h1>
      <div id='link-buttons'>
        <Link className="react-link-clickable" to='/playground'>
          <button id="campaign" className='link-button'>
            Campaign
          </button>
          <img src="../../src/assets/ui/campaign-castle.svg" alt="doesnt work" id="campaign-image-1"></img>
          <img src="../../src/assets/ui/tree1.svg" alt="doesnt work" id="campaign-image-2"></img>
        </Link>
        <Link className="react-link-clickable" to='/playground'>
          <button id="quickstart" className='link-button'>
            Quick Start
          </button></Link>
          <img src="" alt="placeholder" id="quickstart-image-1"></img>
        <Link className="react-link-clickable" to='/host'>
          <button id="multiplayer" className='link-button'>
            Create a Table
          </button>
          <img src="" alt="wtf" id="multiplayer-image-1"></img>
        </Link>
      </div>
    </div>
  )
}

export default Intro
