import { Link } from 'react-router-dom'

const Intro = () => {
  return (
    <>
      <h2>The Poker Playground</h2>
      <Link to='/playground'><button>start</button></Link>
    </>
  )
}

export default Intro