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

  const previousStep = () => {
    if (player.previous_step) {
      if (player.previous_step.length == 2) {
        return <p>{player.previous_step.join(' ') + ' $'}</p>
      } else {
        return <p>{player.previous_step[0]}</p>
      }
    } else {
      return
    }
  }
  

  return (
    <div className={`opponent`}>
      <div className='top-elements'>
        <div className='opponent-hand'>
          {player.hand.map(card => <Card key={`${card}`} card={card} />)}
        </div>
        {positionTag()}
        {previousStep()}
      </div>
      {!player.active && <em><p className={`opponent-worth`}>Balance: {player.balance}$</p></em>}
      {player.active && <p className={`opponent-worth`}>Balance: {player.balance}$</p>}
    </div>
  )
}

export default Opponent