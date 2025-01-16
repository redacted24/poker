import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import ls from 'localstorage-slim'
import _, { random } from 'lodash'

import Card from './Card'
import Player from './Player'
import Opponents from './Opponents'

import './game.css'


const Game = ({ socket, notify }) => {
    const [table, setTable] = useState()
    const [inGame, setInGame] = useState(false)
    const [displayBoard, setDisplayBoard] = useState(false)
    const params = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        if (!socket) return undefined

        socket.on("message", (table) => {
            setTable(table)
            ls.set("table_id", table.id, { ttl: 60 * 5 })
        })

        socket.on("start_round", () => {
            ;
        })

    }, [socket])

    const getName = () => {
        return ls.get('username')
    }

    const getTableId = () => {
        return ls.get('tableId')
    }

    const start = () => {
        setDisplayBoard(true)
        setInGame(true)
        socket.emit("start", { name: getName(), table_id: table.id })
    }

//   useEffect(() => {
//     const checkWinner = async () => {
//       if (table && table.winning_player && inGame) {
//         setTimeout(async () => {
//           if (table.winning_player.name == getName()) {
//             notify(`You have won ${table.pot}!`, 'success')
//           } else{
//             notify(`${table.winning_player.name} has won ${table.pot}!`, 'info')
//           }
//           const tableData = await pokerService.next({ name: getName(), id: getTableId() })
//           updateTable(tableData)
//           setDisplayBoard(false)
//         }, 1600)
//       }
//     }
//     checkWinner()
//   }, [table])
  
//   const updateTable = (newTableData) => {
//     if (newTableData.players.length == 1) {
//       notify('All players have left the game. You won!', 'success')
//       pokerService.clear({ id: getTableId() })
//       navigate('/')
//     } else if (newTableData.players.some(p => p.name == getName())) {
//       if (newTableData.player_queue.length !== 0) {
//         setDisplayBoard(true)
//       }
//       setTable(newTableData)
//       console.log(newTableData)
//     } else {
//       notify("You lost all your money and you've been kicked out of the table! Better luck next time :(", 'error')
//       navigate('/')
//     }
//   }

//   const updateTableQueue = () => {
//     const newPlayerQueue = table.player_queue.slice(1)
//     setTable({ ...table, player_queue: newPlayerQueue })
//   }

  if (!table) {
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
                    displayBoard ?
                        (table.board.length === 0) ?
                            <div className='vertical-align'><h1 id='loading'>Cleaning up the table...</h1></div>
                        :
                            <div id='board'>{table.board.map((card, i) => <Card key={i || random(1000, false)} card={card} />)}</div>
                    :
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
                />
            })}

            <Opponents 
                opponents={(
                    table.players
                    .slice(table.players.findIndex(player => player.name === getName()) + 1)
                    .concat(table.players.slice(0, table.players.findIndex(player => player.name === getName())))
                )} 
                playerQueue={table.player_queue} 
            />

      </div>
    </>
  )
}

export default Game
