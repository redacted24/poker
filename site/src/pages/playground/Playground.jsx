import { useEffect } from 'react'
import Card from './Card'
import './playground.css'
import { useState } from 'react'
import pokerService from '../../services/poker'


const Playground = () => {
  const [name, setName] = useState('Bob')
  const [inGame, setInGame] = useState(false)
  const [pot, setPot] = useState(0)
  const [balance, setBalance] = useState(0)
  const [hand, setHand] = useState([])
  const [board, setBoard] = useState([])
  const [requiredBet, setRequiredBet] = useState(0)

  useEffect(() => {
    const reset = async () => {
      await pokerService.clear()
      const username = prompt('Please enter your username.', 'Bob')
      setName(username)
    }
    reset()
  }, [])

  useEffect(() => {
    const init = async () => {
      const data = await pokerService.init({ name })
      setBalance(data.balance)
    }
    init()
  }, [name])

  const start = async () => {
    const data = await pokerService.start()

    setInGame(true)

    setHand(data.hand.map(card => { 
      return { name: card, facedown: false }
    }))
    setRequiredBet(data.required_bet)
    setBoard(data.board.map(card => {
      if (card) {
        return { name: card, facedown: false }
      } else {
        return { name: null, facedown: true }
      }
    }))
  }

  if (!inGame) {
    return (
      <>
        <div id='room'>
          <div id='table'>
            <button id='start-button' onClick={start}>Start</button>
          </div>
        </div>
      </>
    )
  }

  const call = async () => {
    const data = await pokerService.call({ name })
    setBalance(data.balance)
    setPot(data.pot)
    setRequiredBet(data.required_bet)
    setHand(data.hand.map(card => { 
      return { name: card, facedown: false }
    }))
    setBoard(data.board.map(card => {
      if (card) {
        return { name: card, facedown: false }
      } else {
        return { name: null, facedown: true }
      }
    }))
  }

  const check = async () => {
    const data = await pokerService.check({ name })
    setBalance(data.balance)
    setPot(data.pot)
    setRequiredBet(data.required_bet)
    setHand(data.hand.map(card => { 
      return { name: card, facedown: false }
    }))
    setBoard(data.board.map(card => {
      if (card) {
        return { name: card, facedown: false }
      } else {
        return { name: null, facedown: true }
      }
    }))
  }

  const bet = async () => {
    const amount = parseInt(prompt('Enter your bet: '), 10)

    const data = await pokerService.bet({ name, amount })
    setBalance(data.balance)
    setPot(data.pot)
    setRequiredBet(data.required_bet)
    setHand(data.hand.map(card => { 
      return { name: card, facedown: false }
    }))
    setBoard(data.board.map(card => {
      return { name: card, facedown: false }
    }))
  }

  console.log(requiredBet)

  return (
    <>
      <div id='room'>
        <div id='table'>
          <p id='pot'>Pot: {pot}$</p>
          <div id='board'>
            {board.map((card, i) => <Card key={i} {...card} />)}
          </div>
        </div>
        <div id='hand'>
          {hand.map(card => <Card key={`${card.name}`} {...card} />)}
        </div>
        <div id='buttons'>
          {!!requiredBet && <button className='action' onClick={call}>Call ({requiredBet}$)</button>}
          {!requiredBet && <button className='action' onClick={check}>Check</button>}
          <button className='action' onClick={() => {console.log(requiredBet)}}>Fold</button>
          <button className='action' onClick={bet}>Bet</button>
        </div>
        <p id='balance'>Balance: {balance}$</p>
      </div>
    </>
  )
}

export default Playground