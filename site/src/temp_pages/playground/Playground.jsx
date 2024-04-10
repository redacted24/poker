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

  useEffect(() => {
    const init = async () => {
      await pokerService.clear()

      setName(prompt('Please enter your username.', 'Bob'))
      const data = await pokerService.init({ name })

      setBalance(data.balance)
    }
    init()
  }, [])

  const start = async () => {
    const data = await pokerService.start()

    setInGame(true)

    setHand(data.hand.map(card => { 
      return { name: card, facedown: false }
    }))
    
    setBoard([{ facedown: true }, { facedown: true }, { facedown: true }])
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
    setBoard(data.board.map(card => {
      return { name: card, facedown: false }
    }))
  }

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
          <button className='action' onClick={call}>Call</button>
          <button className='action' onClick={() => {}}>Fold</button>
          <button className='action' onClick={() => {}}>Bet</button>
        </div>
        <p id='balance'>Balance: {balance}$</p>
      </div>
    </>
  )
}

export default Playground