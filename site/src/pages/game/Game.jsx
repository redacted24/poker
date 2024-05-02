import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import ls from 'localstorage-slim'

import Card from './Card'
import Player from './Player'
import Opponents from './Opponents'

import pokerService from '../../services/poker'
import './game.css'


const Game = ({ clearIntervals }) => {
  const [table, setTable] = useState()
  const [inGame, setInGame] = useState(false)
  const [displayBoard, setDisplayBoard] = useState(false)
  const params = useParams()
  const navigate = useNavigate()
  let intervalId

  useEffect(() => {
    const getTable = async () => {
      const tableData = await pokerService.getTable({ name: getName(), id: params.id })
      setTable(tableData)
      window.localStorage.setItem('tableId', tableData.id)
      toggleFetching(true)
      if (tableData.player_queue.length === 0) {
        start()
      } else {
        setInGame(true)
      }
    }
    getTable()

    const removeTableId = async () => {
      if (getTableId()) {
        console.log('clearing')
        pokerService.leave({ name: getName(), id: getTableId()})
        window.localStorage.clear()
      }
    }
    
    window.addEventListener('beforeunload', removeTableId)

    return () => {
      window.removeEventListener('beforeunload', removeTableId)
      clearIntervals()
      navigate('../../')
    }
  }, [])

  const getName = () => {
    return ls.get('username')
  }

  const getTableId = () => {
    return ls.get('tableId')
  }

  const toggleFetching = (fetching) => {
    if (fetching) {
      const fetchData = async () => {
        console.log('fetching')
        const tableData = await pokerService.getTable({ name: getName(), id: getTableId(), })
        updateTable(tableData)
        console.log(tableData)
      }
      fetchData()
      const tempIntervalId = setInterval(fetchData, 2500)
      intervalId = tempIntervalId
    } else {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  const start = async () => {
    toggleFetching(true)
    const tableData = await pokerService.start({ name: getName(), id: getTableId() })
    toggleFetching(false)
    setInGame(true)
    updateTable(tableData)
    setDisplayBoard(true)
    console.log(tableData)
  }

  useEffect(() => {
    const checkWinner = async () => {
      if (table && table.winning_player && inGame) {
        setTimeout(async () => {
          alert(`${table.winning_player.name} has won ${table.pot}!`)
          const tableData = await pokerService.next({ name: getName(), id: getTableId() })
          updateTable(tableData)
          setDisplayBoard(false)
        }, 800)
      }
    }
    checkWinner()
  }, [table])

  
  const updateTable = (newTableData) => {
    console.log(newTableData.players)
    if (newTableData.players.length == 1) {
      alert('All players have left the game. You won!')
      pokerService.clear({ id: getTableId() })
      navigate('../../')
    } else if (newTableData.players.some(p => p.name == getName())) {
      if (newTableData.player_queue.length !== 0) {
        console.log(inGame)
        setDisplayBoard(true)
      }
      setTable(newTableData)
    } else {
      alert("You lost all your money and you've been kicked out of the table! Better luck next time :(")
      navigate('../../')
    }
  }

  const updateTableQueue = () => {
    const newPlayerQueue = table.player_queue.slice(1)
    updateTable({ player_queue: newPlayerQueue, ...table })
    console.log(table)
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
        {table.players.filter(player => player.name == getName()).map(player => {
            return <Player 
              key={getName()}
              player={player}
              numPlayers={table.players.length}
              playerQueue={table.player_queue}
              requiredBet={table.required_bet}
              requiredRaise={table.required_raise}
              getTableId={getTableId}
              updateTable={updateTable}
              toggleFetching={toggleFetching}
              updateTableQueue={updateTableQueue}
            />
        })}
        <Opponents opponents={table.players.filter(player => player.name !== getName())} playerQueue={table.player_queue} />

      </div>
    </>
  )
}

export default Game