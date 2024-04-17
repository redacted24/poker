import Card from './Card'
import pokerService from '../../services/poker'
import './player.css'
import { useEffect, useState } from 'react'

const Player = ({ name, player, numPlayers, requiredBet, requiredRaise, setTable }) => {
  const [isBetting, setIsBetting] = useState(false)
  const callAmount = requiredBet - player.current_bet
  const minBetAmount = requiredBet + requiredRaise
  const [betAmount, setBetAmount] = useState(minBetAmount)

  const handleChange = (e) => {
    setBetAmount(e.target.value)
  }

  const toggleIsBetting = () => {
    setIsBetting(!isBetting)
  }

  useEffect(() => {
    setBetAmount(minBetAmount)
  }, [minBetAmount])

  const call = async () => {
    const tableData = await pokerService.call({ name })
    setBetAmount(minBetAmount)
    setTable(tableData)
    console.log(tableData)
  }

  const check = async () => {
    const tableData = await pokerService.check({ name })
    setBetAmount(minBetAmount)
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
    setBetAmount(minBetAmount)
    setTable(tableData)
    toggleIsBetting()
    console.log(tableData)
  }

  const positionTag = () => {
    switch (player.position) {
      case 0:
        if (numPlayers == 2) {
          return <img className='position-tag' src='./src/assets/positions/big-blind.png' />
        } else {
          return <img className='position-tag' src='./src/assets/positions/dealer.png' />
        }
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
          <input className='action' type='number' value={betAmount} onChange={handleChange} min={minBetAmount} /> <span id='dollar-sign'>$</span>
          <button className='action' type='button' onClick={toggleIsBetting}>Go back</button>
          <button className='action' type='submit'>Confirm</button>
        </form>
      }
      <p id='balance'>Balance: {player.balance}$</p>
    </div>
  )
}

export default Player