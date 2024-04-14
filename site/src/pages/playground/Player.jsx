import Card from './Card'
import pokerService from '../../services/poker'
import './player.css'

const Player = ({ name, player, requiredBet, setTable }) => {
  const callAmount = requiredBet - player.current_bet

  const call = async () => {
    const tableData = await pokerService.call({ name })
    setTable(tableData)
    console.log(tableData)
  }

  const check = async () => {
    const tableData = await pokerService.check({ name })
    setTable(tableData)
    console.log(tableData)
  }

  const fold = async () => {
    const tableData = await pokerService.fold({ name })
    setTable(tableData)
    console.log(tableData)
  }

  const bet = async () => {
    const amount = parseInt(prompt('Enter your bet: '), 10)
    const tableData = await pokerService.bet({ name, amount })
    setTable(tableData)
    console.log(tableData)
  }

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
    <div id='player'>
      <div id='hand'>
        {player.hand.map(card => <Card key={`${card}`} card={card} />)}
      </div>
      {positionTag()}
      <div id='buttons'>
        {!!callAmount && <button className='action' onClick={call}>Call ({callAmount}$)</button>}
        {!callAmount && <button className='action' onClick={check}>Check</button>}
        <button className='action' onClick={fold}>Fold</button>
        <button className='action' onClick={bet}>Bet</button>
      </div>
      <p id='balance'>Balance: {player.balance}$</p>
    </div>
  )
}

export default Player