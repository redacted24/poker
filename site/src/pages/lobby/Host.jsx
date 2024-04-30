import { useState, useEffect } from 'react'
import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'
import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

const Host = () => {
    const [table, setTable] = useState()
    const navigate = useNavigate()
    let intervalId

    useEffect(() => {
        const removeTableId = async () => {
            const tableId = ls.get('tableId')
            if (tableId) {
              console.log('clearing')
              await pokerService.clear({ tableId })
              ls.set('tableId', undefined)
            }
        }

        window.addEventListener('beforeunload', removeTableId)

        const init = async () => {
            const tableData = await pokerService.init({ name: getName() })
            console.log(tableData)
            ls.set('tableId', tableData.id)
            toggleFetching(true)
          }
        init()

        return () => {
            window.removeEventListener('beforeunload', removeTableId)
            clearInterval(intervalId)
            intervalId = null
        }
    }, [])

    const updateTable = (newTableData) => {
        setTable(newTableData)
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

    const getName = () => {
        return ls.get('username')
    }

    const getTableId = () => {
        return ls.get('tableId')
    }

    const copyLink = () => {
        const gameUrl = `${window.location.host}/lobby/${getTableId()}`
        navigator.clipboard.writeText(gameUrl)
        console.log(gameUrl)
    }

    const startGame = () => {
        toggleFetching(false)
        navigate(`../game/${getTableId()}`)
    }

    return (
        <>
            <h2 id='status'>Waiting...</h2>
            <div id='lobby'>
                <div id='player-list'>
                    <p className='subheader'>Player list</p>
                    <div id='players'>
                        {table && table.players.map(p => <Player player={p} key={p.name}/>)}
                    </div>
                    <div id='link-section'>
                        <p className='share-link'>Share this link to invite others!</p>
                        <button id='link-button' onClick={copyLink}>Copy link</button>
                    </div>
                </div>
                <div id='settings'>
                    <p className='subheader'>Settings</p>
                    <button id='start-button' onClick={startGame}>Start</button>
                </div>
            </div>
        </>
    )
}

export default Host