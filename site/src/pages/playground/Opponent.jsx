import Card from './Card'
import './opponent.css'

const Opponent = ({ player }) => {
  const positionTag = () => {
    switch (player.position) {
      case 0:
        return <img className='position-tag' src='./src/assets/positions/dealer.png' />
      case 1:
        return <img className='position-tag' src='./src/assets/positions/small-blind.png' />
      case 2:
        return <img className='position-tag' src='./src/assets/positions/big-blind.png' />
      default:
        return null
    }
  }



  return (
    <div className={`opponent`}>
      <div className='top-elements'>
        <div className='opponent-hand'>
          {player.hand.map(card => <Card key={`${card}`} card={card} />)}
        </div>
        {positionTag()}
      </div>
      <p className={`opponent-worth ${self.active}`}>Balance: {player.balance}$</p>
    </div>
  )
}

export default Opponent