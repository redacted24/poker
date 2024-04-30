import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'

const Lobby = () => {
    console.log('lobby')
    const [name, setName] = useState()
    const [table, setTable] = useState()
    const tableId = useParams().id
    let intervalId

    const navigate = useNavigate()

    useEffect(() => {
        const username = prompt('Please enter your username.', 'Bob')
        setName(username)

        const removeTableId = async () => {
            const tableId = window.localStorage.getItem('tableId')
            if (tableId) {
              window.localStorage.clear()
            }
        }
        window.addEventListener('beforeunload', removeTableId)

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


    useEffect(() => {
        const join = async () => {
          const tableData = await pokerService.join({ name, id: tableId })
          setTable(tableData)
          window.localStorage.setItem('tableId', tableData.id)
          toggleFetching(true)
        }
        
        if (name) {
            join()
        }
      }, [name])

    const getTableId = () => {
        return window.localStorage.getItem('tableId')
    }

    const copyLink = () => {
        const gameUrl = `${window.location.host}/lobby/${getTableId()}`
        navigator.clipboard.writeText(gameUrl)
    }

    return (
        <>
            <h2 id='status'>Lobby...</h2>
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
                </div>
            </div>
        </>
    )
}

export default Lobby