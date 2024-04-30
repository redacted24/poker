import { useState, useEffect } from 'react'
import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'

const Host = ({
    name
}) => {
    console.log(name)
    const [table, setTable] = useState()
    let intervalId

    useEffect(() => {
        const removeTableId = async () => {
            const tableId = window.localStorage.getItem('tableId')
            if (tableId) {
              console.log('clearing')
              await pokerService.clear({ tableId })
              window.localStorage.clear()
            }
        }

        window.addEventListener('beforeunload', removeTableId)

        const init = async () => {
            console.log(name)
            const tableData = await pokerService.init({ name })
            console.log(tableData)
            setTable(tableData)
            window.localStorage.setItem('tableId', tableData.id)
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
        if (newTableData.players.some(p => p.name == name)) {
          setTable(newTableData)
        } else {
          navigate('/')
          toggleFetching(false)
        }
    }

    const toggleFetching = (fetching) => {
        if (fetching) {
          const fetchData = async () => {
            console.log('fetching')
            const tableData = await pokerService.getTable({ name, id: getTableId(), })
            updateTable(tableData)
            console.log(tableData)
          }
          const tempIntervalId = setInterval(fetchData, 2500)
          intervalId = tempIntervalId
        } else {
          clearInterval(intervalId)
          intervalId = null
        }
      }

    const getTableId = () => {
        return window.localStorage.getItem('tableId')
    }

    const copyLink = () => {
        const gameUrl = `${window.location.host}/lobby/${getTableId()}`
        navigator.clipboard.writeText(gameUrl)
    }

    const startGame = () => {
        toggleFetching(false)
        
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