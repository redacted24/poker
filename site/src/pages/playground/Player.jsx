import Card from './Card'
import pokerService from '../../services/poker'
import './player.css'
import { useState } from 'react'

const Player = ({ name, player, requiredBet, requiredRaise, setTable }) => {
  const [isBetting, setIsBetting] = useState(false)
  const [betAmount, setBetAmount] = useState(0)
  const callAmount = requiredBet - player.current_bet
  const minBetAmount = callAmount + requiredRaise

  const handleChange = (e) => {
    setBetAmount(e.target.value)
  }

  const toggleIsBetting = () => {
    setIsBetting(!isBetting)
  }

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
  
  const bet = async (e) => {
    e.preventDefault()
    const amount = parseInt(betAmount)
    const tableData = await pokerService.bet({ name, amount })
    toggleIsBetting()
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
      {!isBetting &&
        <div id='buttons'>
          {!!callAmount && <button className='action' onClick={call}>Call ({callAmount}$)</button>}
          {!callAmount && <button className='action' onClick={check}>Check</button>}
          <button className='action' onClick={fold}>Fold</button>
          <button className='action' onClick={toggleIsBetting}>Bet</button>
        </div>
      }
      {isBetting && 
        <form onSubmit={bet} id='buttons'>
          <input className='action' type='number' value={betAmount} onChange={handleChange}/>
          <button className='action' type='button' onClick={toggleIsBetting}>Go back</button>
          <button className='action' type='submit'>Confirm</button>
        </form>
      }
      <p id='balance'>Balance: {player.balance}$</p>
    </div>
  )
}

export default Player