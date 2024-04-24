import Card from './Card'
import './opponent.css'

const Opponent = ({ player, isCurrentPlayer }) => {
  const positionTag = () => {
    switch (player.position) {
      case 0:
        return <img className='position-tag' src='./src/assets/positions/dealer.png' />
      case 1:
        return <img className='position-tag' src='./src/assets/positions/small-blind.png' />
      case 2:
        return <img className='position-tag' src='./src/assets/positions/big-blind.png' />
      default:
        return <div className='position-tag'></div>
    }
  }

  const previousStep = () => {
    if (player.previous_step) {
      if (player.previous_step.length == 2) {
        return <p className='previous-step'>{player.previous_step.join(' ') + ' $'}</p>
      } else {
        return <p className='previous-step'>{player.previous_step[0]}</p>
      }
    } else {
      return <p className='previous-step'></p>
    }
  }
  
  let status

  if (isCurrentPlayer) {
    status =  'currently-playing'
  } else if (!player.active) {
    status = 'not-playing'
  } else {
    status = 'waiting'
  }

  return (
    <div className={`opponent ${status}`}>
      <div className='left-elements'>
        <div className='opponent-hand'>
          {player.hand.map(card => <Card key={`${card}`} card={card} />)}
        </div>
        <p className={`opponent-worth`}>Balance: {player.balance}$</p>
      </div>
      <div className='right-elements'>
        {previousStep()}
        {positionTag()}
      </div>
    </div>
  )
}

export default Opponent