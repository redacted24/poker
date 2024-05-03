import Card from './Card'
import './opponent.css'

const Opponent = ({ player, isCurrentPlayer, isNextPlayer, userAtStart }) => {
  const positionTag = () => {
    switch (player.position) {
      case 0:
        return <img className='position-tag' src='../../src/assets/positions/dealer.png' />
      case 1:
        return <img className='position-tag' src='../../src/assets/positions/small-blind.png' />
      case 2:
        return <img className='position-tag' src='../../src/assets/positions/big-blind.png' />
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

  const buttons = document.getElementById('buttons')
  let userHasMoved = false
  if (buttons) {
    userHasMoved = buttons.style.display == 'none'    // To check if the the user has completed their turn
  }

  console.log(player.name, userAtStart, userHasMoved, isNextPlayer)

  if (isCurrentPlayer || userAtStart && userHasMoved && isNextPlayer) {
    status =  'currently-playing'
    setTimeout(2000)
  } else if (!player.active) {
    status = 'not-playing'
  } else if (player.is_all_in) {
    status = 'all-in'
  } else {
    status = 'waiting'
  }

  const generateKey = () => {
    return Math.floor(Math.random() * 1000000)
  }

  return (
    <div className={`opponent ${status}`}>
      <div className='left-elements'>
        <div className='opponent-hand'>
          {player.hand.map(card => <Card key={generateKey()} card={card} />)}
        </div>
        <p className={`opponent-worth`}>Balance: {player.balance}$</p>
      </div>
      <div className='right-elements'>
        <p>{player.name}</p>
        {previousStep()}
        {positionTag()}
      </div>
    </div>
  )
}

export default Opponent