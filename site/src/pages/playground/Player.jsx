import Card from './Card'
import pokerService from '../../services/poker'
import './player.css'

const Player = ({ name, table, player, setTable }) => {
  const call = async () => {
    const tableData = await pokerService.call({ name })
    setTable(tableData)
  }

  const check = async () => {
    const tableData = await pokerService.check({ name })
    setTable(tableData)
  }

  const bet = async () => {
    const amount = parseInt(prompt('Enter your bet: '), 10)
    const tableData = await pokerService.bet({ name, amount })
    setTable(tableData)
  }

  return (
    <div id='player'>
      <div id='hand'>
        {player.hand.map(card => <Card key={`${card}`} card={card} />)}
      </div>
      <div id='buttons'>
        {!!table.requiredBet && <button className='action' onClick={call}>Call ({table.requiredBet}$)</button>}
        {!table.requiredBet && <button className='action' onClick={check}>Check</button>}
        <button className='action' onClick={() => {console.log(table.requiredBet)}}>Fold</button>
        <button className='action' onClick={bet}>Bet</button>
      </div>
      <p id='balance'>Balance: {player.balance}$</p>
    </div>
  )
}

export default Player