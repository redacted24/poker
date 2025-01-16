import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import useState from 'react-usestateref'
import ls from 'localstorage-slim'

import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'
import { io } from 'socket.io-client'

const Lobby = ({ notify }) => {
    const [socketInstance, setSocketInstance] = useState(null)

    const [table, setTable] = useState()
    const [playerList, setPlayerList] = useState([])
    const params = useParams()
    let intervalId

    const navigate = useNavigate()

    useEffect(() => {
        const socket = io("localhost:5000/");
        setSocketInstance(socket);

        socket.emit("join", {
            name: getName(),
            table_id: params.id
        })

        socket.on("message", (data) => {
            setTable(data)
            setPlayerList(data.players)
        })

        socket.on("change_username", (data) => {
            ls.set("username", data)
        })

        return () => {
            socket.disconnect();
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
            navigate('/start')
            return null
        }
        return ls.get('username')
    }

    const getTableId = () => {
        return ls.get('tableId')
    }


    const copyLink = () => {
        const gameUrl = `${window.location.host}/lobby/${getTableId()}`
        navigator.clipboard.writeText(gameUrl)

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
                        {table && playerList.map(p => <Player player_name={p.name} key={p.name}/>)}
                    </div>
                    <div id='link-section'>
                        <button id='link-button' onClick={copyLink}>Copy table link</button>
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