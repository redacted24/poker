import Card from './Card'
import pokerService from '../../services/poker'
import './player.css'
import { useEffect, useState } from 'react'

const Player = ({ 
    player,
    numPlayers,
    playerQueue,
    requiredBet,
    requiredRaise,
    getTableId,
    setTable,
    toggleFetching,
    updateTableQueue
  }) => {

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

  const sendRequest = async (request, content) => {
    updateTableQueue()
    toggleFetching(true)
    const tableData = await request(content)
    toggleFetching(false)
    setBetAmount(minBetAmount)
    setTable(tableData)
    console.log(tableData)
  }

  const call = () => {
    sendRequest(pokerService.call, { name: player.name, id: getTableId() })
  }

  const check = () => {
    sendRequest(pokerService.check, { name: player.name, id: getTableId() })
  }

  const fold = () => {
    sendRequest(pokerService.fold, { name: player.name, id: getTableId() })
  }
  
  const bet = async (e) => {
    e.preventDefault()
    const amount = parseInt(betAmount)
    sendRequest(pokerService.bet, { name: player.name, amount, id: getTableId() })
    toggleIsBetting()
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

  const buttons = () => {
    if (playerQueue[0] && playerQueue[0].name == player.name) {
      if (!isBetting) {
        return (
          <div id='buttons'>
            {!!callAmount && <button className='action' onClick={call}>Call ({callAmount}$)</button>}
            {!callAmount && <button className='action' onClick={check}>Check</button>}
            <button className='action' onClick={fold}>Fold</button>
            <button className='action' onClick={toggleIsBetting}>Bet</button>
          </div>
        )
      } else {
        return (
          <form onSubmit={bet} id='buttons'>
            <input className='action' type='number' value={betAmount} onChange={handleChange} min={minBetAmount} /> <span id='dollar-sign'>$</span>
            <button className='action' type='button' onClick={toggleIsBetting}>Go back</button>
            <button className='action' type='submit'>Confirm</button>
          </form>
        )
      }
    } else {
      return null
    }
  }

  return (
    <div id='player'>
      <div id='hand'>
        {player.hand.map(card => <Card key={`${card}`} card={card} />)}
      </div>
      {positionTag()}
      {buttons()}
      <p id='balance'>Balance: {player.balance}$</p>
    </div>
  )
}

export default Player