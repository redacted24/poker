import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'

const Lobby = () => {
    const [table, setTable] = useState()
    const params = useParams()
    let intervalId

    const navigate = useNavigate()

    useEffect(() => {
        const join = async () => {
            const tableData = await pokerService.join({ name: getName(), id: params.id })
            setTable(tableData)

            ls.set('tableId', tableData.id)
            toggleFetching(true)
        }
        join()

        const removeTableId = () => ls.set('tableId', undefined)

        window.addEventListener('beforeunload', () => removeTableId)

        return () => {
            window.removeEventListener('beforeunload', removeTableId)
            clearInterval(intervalId)
            intervalId = null
        }
    }, [])

    const updateTable = (newTableData) => {
        if (newTableData.players.some(p => p.name == getName())) {
          setTable(newTableData)
        } else {
          alert("You have been kicked out of the lobby!")
          navigate('../../')
        }
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