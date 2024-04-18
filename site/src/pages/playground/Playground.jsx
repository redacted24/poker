import { useEffect } from 'react'
import Card from './Card'
import Player from './Player'
import Opponents from './Opponents'
import './playground.css'
import { useState } from 'react'
import pokerService from '../../services/poker'


const Playground = () => {
  const [name, setName] = useState('Bob')
  const [inGame, setInGame] = useState(false)
  const [table, setTable] = useState()
  const [displayBoard, setDisplayBoard] = useState(false)
  let intervalId

  useEffect(() => {
    const reset = async () => {
      const username = prompt('Please enter your username.', 'Bob')
      setName(username)
    }
    
    const removeTableId = async () => {
      const tableId = window.localStorage.getItem('tableId')
      if (tableId) {
        console.log('clearing')
        await pokerService.clear({ tableId })
        window.localStorage.clear()
      }
    }
    

    reset()
    window.addEventListener('beforeunload', removeTableId)

    return () => {
      window.removeEventListener('beforeunload', removeTableId)
      clearInterval(intervalId)
      intervalId = null
    }
  }, [])

  useEffect(() => {
    const init = async () => {
      const tableData = await pokerService.init({ name })
      setTable(tableData)
      window.localStorage.setItem('tableId', tableData.id)
    }
    init()
  }, [name])

  const getTableId = () => {
    return window.localStorage.getItem('tableId')
  }

  const toggleFetching = (fetching) => {
    if (fetching) {
      const fetchData = async () => {
        console.log('fetching')
        const tableData = await pokerService.getTable({ id: getTableId() })
        setTable(tableData)
        console.log(tableData)
      }
      const tempIntervalId = setInterval(fetchData, 250)
      intervalId = tempIntervalId
    } else {
      clearInterval(intervalId)
      intervalId = null
    }
  }


  const start = async () => {
    toggleFetching(true)
    const tableData = await pokerService.start({ id: getTableId() })
    toggleFetching(false)
    setInGame(true)
    setTable(tableData)
    setDisplayBoard(true)
    console.log(tableData)
  }

  useEffect(() => {
    const checkWinner = async () => {
      if (table && table.winning_player) {
        alert(`${table.winning_player.name} has won ${table.pot}!`)
        const tableData = await pokerService.next({ id: getTableId() })
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
        {table.players.filter(player => player.name == name).map(player => {
            return <Player 
              key={name}
              name={name}
              player={player}
              numPlayers={table.players.length}
              requiredBet={table.required_bet}
              requiredRaise={table.required_raise}
              getTableId={getTableId}
              setTable={setTable}
              toggleFetching={toggleFetching}
            />
        })}
        <Opponents opponents={table.players.filter(player => player.name !== name)} />

      </div>
    </>
  )
}

export default Playground