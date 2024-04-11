import Card from './Card'
import './opponent.css'

const Opponent = ({ player }) => {
  return (
    <div className='opponent'>
      <div className='opponent-hand'>
        {player.hand.map(card => <Card key={`${card}`} card={card} />)}
      </div>
      <p className='opponent-worth'>Balance: {player.balance}$</p>
    </div>
  )
}

export default Opponent