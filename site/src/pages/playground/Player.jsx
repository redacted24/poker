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

  return (
    <div id='player'>
      <div id='hand'>
        {player.hand.map(card => <Card key={`${card}`} card={card} />)}
      </div>
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