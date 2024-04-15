import { useEffect } from 'react'
import Card from './Card'
import Player from './Player'
import Opponent from './Opponent'
import './playground.css'
import { useState } from 'react'
import pokerService from '../../services/poker'


const Playground = () => {
  const [name, setName] = useState('Bob')
  const [inGame, setInGame] = useState(false)
  const [table, setTable] = useState()
  const [displayBoard, setDisplayBoard] = useState(false)

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
      const tableData = await pokerService.init({ name })
      setTable(tableData)
    }
    init()
  }, [name])

  const start = async () => {
    const tableData = await pokerService.start()
    setInGame(true)
    setTable(tableData)
    setDisplayBoard(true)
    console.log(tableData)
  }

  useEffect(() => {
    const checkWinner = async () => {
      if (table && table.winning_player) {
        alert(`${table.winning_player.name} has won ${table.pot}!`)
        const tableData = await pokerService.next()
        setTable(tableData)
        setDisplayBoard(false)
      }
    }
    checkWinner()
  }, [table])

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

  return (
    <>
      <div id='room'>
        <div id='table'>
          <p id='pot'>Pot: {table.pot}$</p>
          {
            displayBoard && 
            <div id='board'>
              {table.board.map((card, i) => <Card key={i} card={card} />)}
            </div>
          }
          {
            !displayBoard &&
            <button id='start-button' onClick={start}>Start</button>
          }
        </div>
        {table.players.map(player => {
          if (player.name == name) {
            return <Player key={name} name={name} player={player} requiredBet={table.required_bet} setTable={setTable} />
          } else {
            return <Opponent key={player.name} player={player} />
          }
        })}

      </div>
    </>
  )
}

export default Playground