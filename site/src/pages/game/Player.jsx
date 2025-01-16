import { useEffect, useState } from 'react'
import Card from './Card'

import './player.css'

const Player = ({ 
        socket,
        player,
        numPlayers,
        playerQueue,
        requiredBet,
        requiredRaise,
        tableId,
    }) => {

    const [isBetting, setIsBetting] = useState(false)
    const callAmount = requiredBet - player.current_bet
    const minBetAmount = requiredBet + requiredRaise
    const [betAmount, setBetAmount] = useState(requiredBet + requiredRaise)

    useEffect(() => {
        setBetAmount(requiredBet + requiredRaise)
    }, [requiredBet, requiredRaise])

    const handleChange = (e) => {
        setBetAmount(e.target.value)
    }

    const toggleIsBetting = () => {
        setIsBetting(!isBetting)
    }

    const sendRequest = async (request) => {
        socket.emit(request, { name: player.name, table_id: tableId })
    }

    const bet = async (e) => {
        e.preventDefault()
        const amount = parseInt(betAmount)
        socket.emit("bet", { name: player.name, amount, table_id: tableId })
        toggleIsBetting()
    }

    const positionTag = () => {
        switch (player.position) {
        case 0:
            if (numPlayers == 2) {
            return <img className='position-tag' src='/positions/big-blind.png' />
            } else {
            return <img className='position-tag' src='/positions/dealer.png' />
            }
        case 1:
            return <img className='position-tag' src='/positions/small-blind.png' />
        case 2:
            return <img className='position-tag' src='/positions/big-blind.png' />
        default:
            return null
        }
    }

    const buttons = () => {
        if (playerQueue[0] && playerQueue[0].name == player.name) {
            if (!isBetting) {
                return (
                    <div id='buttons'>
                        {!!callAmount && <button className='action' onClick={() => sendRequest("call")}>Call ({callAmount}$)</button>}
                        {!callAmount && <button className='action' onClick={() => sendRequest("check")}>Check</button>}
                        <button className='action' id="folding-button" onClick={() => sendRequest("fold")}>Fold</button>
                        <button className='action' id="betting-button" onClick={toggleIsBetting}>Bet</button>
                    </div>
                )
            } else {
                return (
                    <form onSubmit={bet} id='buttons'>
                        <button className='action' type='button' onClick={toggleIsBetting}>Go back</button>
                        <button className='action' id="confirm-button" type='submit'>Confirm</button>
                        <input className='input-field' type='number' value={betAmount} onChange={handleChange} min={minBetAmount} /> <span id='dollar-sign'>$</span>
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
