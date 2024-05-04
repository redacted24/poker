import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import useState from 'react-usestateref'
import ls from 'localstorage-slim'

import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'

const Lobby = ({ notify, clearIntervals }) => {
    const [table, setTable] = useState()
    const [playerList, setPlayerList, playerListRef] = useState([])
    const params = useParams()
    let intervalId

    const navigate = useNavigate()

    useEffect(() => {
        const join = async () => {
            const tableData = await pokerService.getTable({ name: null, id: params.id })
            const originalUsername = getName()
            let username = getName()

            const tempPlayerList = tableData.players.map(p => p.name)

            if (tempPlayerList.includes(originalUsername)) {
                let i = 1
                while (tempPlayerList.includes(username)) {
                    username = `${originalUsername} (${i})`
                    i += 1
                }
            }

            console.log(username)

            const newTableData = await pokerService.join({ name: username, id: params.id })
            setTable(newTableData)

            ls.set('tableId', newTableData.id)
            toggleFetching(true)
        }
        join()

        const removeTableId = () => {
            pokerService.leave({ name: getName(), id: getTableId() })
            ls.set('tableId', undefined)
        }

        window.addEventListener('beforeunload', removeTableId)

        return () => {
            window.removeEventListener('beforeunload', removeTableId)
            clearIntervals()
        }
    }, [])

    const updateTable = (newTableData) => {
        if (newTableData.player_queue.length !== 0) {
            toggleFetching(false)
            navigate(`../../game/${getTableId()}`)
        } else if (newTableData.players.some(p => p.name == getName())) {
            newTableData.players.forEach(p => {
                if (!playerListRef.current.includes(p.name)) {
                    notify(`${p.name} has joined the lobby!`, 'success')
                }
            })
            playerListRef.current.forEach(p => {
                console.log(p)
                if (!newTableData.players.map(p => p.name).includes(p)) {
                    notify(`${p} has left the lobby!`, 'error')
                }
            })
            setTable(newTableData)
            setPlayerList(newTableData.players.map(p => p.name))
        } else {
            notify('You have been kicked from the lobby!', 'error')
            navigate('../../')
        }
    }

    const toggleFetching = (fetching) => {
        if (fetching) {
          const fetchData = async () => {
            console.log('fetching')
            try {
                const tableData = await pokerService.getTable({ name: getName(), id: getTableId(), })
                updateTable(tableData)
                console.log(tableData)
            } catch {
                alert('The host has closed the lobby.')
                navigate('../../')
            }

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
        if (!ls.get('username')) {
            const username = prompt('Please enter your username.', 'Bob')
            ls.set('username', username, { ttl: 60 * 60 })
        }
        return ls.get('username')
    }

    const getTableId = () => {
        return ls.get('tableId')
    }


    const unsecureCopy = (text) => {
        `Workaround for copying due to browser preventing copying from non secure wesbites`

        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
        } catch (err) {
            alert('Unable to copy to clipboard', err);
        }
        document.body.removeChild(textArea);
    }


    const copyLink = () => {
        const gameUrl = `${window.location.host}/lobby/${getTableId()}`
        try {
            navigator.clipboard.writeText(gameUrl)
        } catch {
            unsecureCopy(gameUrl)
        }
        const link_button = document.getElementById('link-button')
        link_button.textContent = 'Link Copied!'
        setTimeout(() => {
            link_button.textContent = 'Copy Text'
        }, 2000)
    }

    return (
        <>
            <h2 id='status'>Lobby...</h2>
            <div id='lobby'>
                <div id='player-list'>
                    <p className='subheader'>Player list</p>
                    <div id='players'>
                        {table && playerList.map(p => <Player player_name={p} key={p}/>)}
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