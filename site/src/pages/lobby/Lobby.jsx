import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

import Player from './Player'
import './host.css'

import { io } from 'socket.io-client'

const Lobby = ({ notify }) => {
    const [socketInstance, setSocketInstance] = useState(null)

    const [table, setTable] = useState()
    const [playerList, setPlayerList] = useState([])
    const params = useParams()

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

        socket.on("player_joined", (playerName) => {
            notify(`${playerName} has joined the lobby!`, "success")
        })

        socket.on("player_left", (playerName) => {
            if (playerName == getName()) {
                notify('You have been kicked out of the lobby!', "error")
                navigate('/')
            } else {
                notify(`${playerName} has left the lobby`, "error")
            }
        })

        return () => {
            socket.disconnect();
        }
    }, [])


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