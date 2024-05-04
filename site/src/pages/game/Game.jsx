import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import ls from 'localstorage-slim'
import _ from 'lodash'

import Card from './Card'
import Player from './Player'
import Opponents from './Opponents'

import pokerService from '../../services/poker'
import './game.css'


const Game = ({ notify, clearIntervals }) => {
  const [table, setTable] = useState()
  const [inGame, setInGame] = useState(false)
  const [displayBoard, setDisplayBoard] = useState(false)
  const params = useParams()
  const navigate = useNavigate()

  useEffect(() => {
    const getTable = async () => {
      const tableData = await pokerService.getTable({ name: getName(), id: params.id })
      setTable(tableData)
      window.localStorage.setItem('tableId', tableData.id)
      toggleFetching(true)
      if (tableData.player_queue.length === 0) {
        await start()
      } else {
        setInGame(true)
      }
    }
    getTable()

    const resetUser = async () => {
      console.log('reset')
      const tableId = ls.get('tableId')
      if (tableId) {
        console.log('clearing')
        await pokerService.clear({ id: tableId })
        ls.set('tableId', undefined)
      }
      clearIntervals()
      navigate('/')
    }
    
    window.addEventListener('beforeunload', resetUser)

    return () => {
      resetUser()
      window.removeEventListener('beforeunload', resetUser)
    }
  }, [])

  const getName = () => {
    return ls.get('username')
  }

  const getTableId = () => {
    return ls.get('tableId')
  }

  const startCooldown = (time=500) => {
    toggleFetching(false)
    setTimeout(() => toggleFetching(true), time)
  }

  const toggleFetching = (fetching) => {
    if (fetching) {
      const fetchData = async () => {
        console.log('fetching')
        try {
          const tableData = await pokerService.getTable({ name: getName(), id: getTableId(), })
          updateTable(tableData)
        } catch {
          notify('You have lost connection to the game!', error)
          navigate('/')
        }

      }
      fetchData()
      setInterval(fetchData, 1000)
    } else {
      clearIntervals()
    }
  }

  const start = async () => {
    toggleFetching(true)
    setDisplayBoard(true)
    const tableData = await pokerService.start({ name: getName(), id: getTableId() })
    setInGame(true)
    updateTable(tableData)
    console.log(tableData)
  }

  useEffect(() => {
    const checkWinner = async () => {
      if (table && table.winning_player && inGame) {
        setTimeout(async () => {
          if (table.winning_player.name == getName()) {
            notify(`You have won ${table.pot}!`, 'success')
          } else{
            notify(`${table.winning_player.name} has won ${table.pot}!`, 'info')
          }
          const tableData = await pokerService.next({ name: getName(), id: getTableId() })
          updateTable(tableData)
          setDisplayBoard(false)
        }, 800)
      }
    }
    checkWinner()
  }, [table])
  
  const updateTable = (newTableData) => {
    if (newTableData.players.length == 1) {
      notify('All players have left the game. You won!', 'success')
      pokerService.clear({ id: getTableId() })
      navigate('/')
    } else if (newTableData.players.some(p => p.name == getName())) {
      if (newTableData.player_queue.length !== 0) {
        setDisplayBoard(true)
      }
      setTable(newTableData)
      console.log(newTableData)
    } else {
      notify("You lost all your money and you've been kicked out of the table! Better luck next time :(", 'error')
      navigate('/')
    }
  }

  const updateTableQueue = () => {
    const newPlayerQueue = table.player_queue.slice(1)
    setTable({ ...table, player_queue: newPlayerQueue })
  }

  if (!inGame) {
    return (
      <>
        <div id='room'>
          <div id='table'>
            <div className='vertical-align'>
              <h1 id='loading'>Loading...</h1>
            </div>
          </div>
        </div>
      </>
    )
  }

  const updateTableHeat = () => {
    if (table.dynamic_table) {
      const table_css = document.getElementById('table')
      if (!table || !table_css) return null
      if (table.pot< 200) {
        table_css.style.backgroundColor = "#63ac59fb"
        table_css.style.border = "10px solid #057005"
        if (table_css.firstElementChild) table_css.firstElementChild.style.display = "none"
      } else if (table.pot< 500) {
        table_css.style.backgroundColor = "#77ac59fb"
        table_css.style.border = "10px solid #2c7005"
      } else if (table.pot< 700) {
        table_css.style.backgroundColor = "#9dac59fb"
        table_css.style.border = "10px solid #597005"
      } else if (table.pot< 1300) {
        table_css.style.backgroundColor = "#ac7159fb"
        table_css.style.border = "10px solid #704e05"
      } else {
        table_css.style.backgroundColor = "#ac5959fb"
        table_css.style.border = "10px solid #700505"
        table_css.firstElementChild.style.display = "inline"
      }
    }
  }
  updateTableHeat()
  
  return (
    <>
      <div id='room'>
        <div id='table'>
          <div id = "firegif">
            <img src="/ui/fire.gif" alt="firegif"></img>
            <img src="/ui/fire.gif" alt="firegif"></img>
            <img src="/ui/fire.gif" alt="firegif"></img>
          </div>
          <p id='pot'>Pot: {table.pot}$</p>
          {
            displayBoard && (table.board.length === 0) && <div className='vertical-align'><h1 id='loading'>Cleaning up the table...</h1></div>
          }
          {
            displayBoard && (table.board.length !== 0) && <div id='board'>{table.board.map((card, i) => <Card key={i} card={card} />)}</div>
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
              startCooldown={startCooldown}
            />
        })}
        <Opponents opponents={table.players.filter(player => player.name !== getName())} playerQueue={table.player_queue} />

      </div>
    </>
  )
}

export default Game
