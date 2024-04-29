import { Link } from 'react-router-dom'
import './intro.css'

const Intro = () => {
  return (
    <>
      <h1 id='title'>The Poker Playground</h1>
      <div id='link-buttons'>
        <Link to='/playground'><button className='link-button'>Campaign</button></Link>
        <Link to='/playground'><button className='link-button'>Quick Start</button></Link>
        <Link to='/lobby'><button className='link-button'>Create a Table</button></Link>
      </div>
    </>
  )
}

export default Intro