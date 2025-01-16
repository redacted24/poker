import { useEffect } from 'react'
import useState from 'react-usestateref'
import Player from './Player'
import './host.css'

import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

const Host = ({ socket, notify }) => {    
    const increments = {
        startingBalance: 200,
        smallBlindAmount: 5,
        blindInterval: 5,
    }
    
    const [options, setOptions] = useState({
        startingBalance: 1000,
        smallBlindAmount: 5,
        blindInterval: 0,
        autoRebuy: false,
        gameStats: false,
        dynamicTable: true,
        showAllBotCards: false,
        showAllCards: false
    })

    const [playerList, setPlayerList] = useState([])
    const [table, setTable] = useState()
    const navigate = useNavigate()

    const getName = () => {
        return ls.get('username')
    }

    useEffect(() => {
        if (!socket) return undefined

        socket.emit("host", {
            name: getName()
        })

        socket.on("message", (table) => {
            setTable(table)
            setPlayerList(table.players)
            ls.set("table_id", table.id, { ttl: 60 * 5 })
        })

        socket.on("player_joined", (playerName) => {
            notify(`${playerName} has joined the lobby!`, "success")
        })

        socket.on("player_left", (playerName) => {
            notify(`${playerName} has left the lobby`, "error")
        })

        socket.on("start_game", () => {
            notify("game has started!", "success")
            navigate(`/game/${table.id}`)
        })
    }, [socket])


    const copyLink = () => {
        const gameUrl = `http://${window.location.host}/lobby/${table.id}`
        navigator.clipboard.writeText(gameUrl)

        const link_button = document.getElementById('link-button')
        link_button.textContent = 'Link Copied!'
        setTimeout(() => {
            link_button.textContent = 'Copy Link'
        }, 2000)
    }


    const startGame = () => {
        if (table.players.length >= 2) {
            socket.emit("set_settings", {
                table_id: table.id, ...options
            })
            navigate(`../game/${table.id}`, { replace: true })
        } else {
            notify('You cannot start a game with less than 2 players!', 'error')
        }
    }


    const addBot =  (e) => {
        const bot_type = e.target.id
        socket.emit("add_bot", { bot_type, table_id: table.id })
    }

    const removePlayer = (name) => {
        socket.emit("remove_player", { name, table_id: table.id })
    }


    const handleChange = (e) => {
        const newOptions = { ...options }

        if (e.target.id == 'bigBlindAmount') {
            newOptions['smallBlindAmount'] = e.target.value * increments['smallBlindAmount']
        } else {
            newOptions[e.target.id] = e.target.value * increments[e.target.id]
        }

        setOptions({ ...newOptions })
    }


    const handleCheckChange = (e) => {
        const newOptions = { ...options }
        newOptions[e.target.id] = !options[e.target.id]

        if (e.target.id == 'showAllCards') {
            newOptions['showAllBotCards'] = !options[e.target.id]
        }

        setOptions({ ...newOptions })
    }



    return (
        <>
            <h2 id='status'>Waiting...</h2>
            <div id='lobby'>
                <div id='player-list'>
                    <h3 className='subheader'>Player list</h3>
                    <div id='players'>
                        {playerList.map(p => <Player player_name={p.name} key={p.name} kickable={p.name != getName()} removePlayer={removePlayer}/>)}
                    </div>
                    <div id='link-section'>
                        <button id='link-button' onClick={copyLink}>Copy table link</button>
                    </div>
                </div>
                <div id='settings'>
                    <h3 className='subheader'>Settings</h3>
                    <div id='options'>
                        <div className='section'>
                            <h4 className='first subtitle'>Table Options</h4>
                            <div className='option'>
                                <label className='option-label' htmlFor='startingBalance'>Staring balance: {options.startingBalance}$</label>
                                <input type="range" min="1" max="25" value={options.startingBalance / 200} onChange={handleChange} className="option-slider" id='startingBalance' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='smallBlindAmount'>Small blind amount: {options.smallBlindAmount}$</label>
                                <input type="range" min="0" max="20" value={options.smallBlindAmount / 5} onChange={handleChange} className="option-slider" id='smallBlindAmount' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='bigBlindAmount'>Big blind amount: {options.smallBlindAmount * 2}$</label>
                                <input type="range" min="0" max="20" value={options.smallBlindAmount / 5} onChange={handleChange} className="option-slider" id='bigBlindAmount' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='blindInterval'>Blind interval: +{options.blindInterval}$ per round</label>
                                <input type="range" min="0" max="5" value={options.blindInterval / 5} onChange={handleChange} className="option-slider" id='blindInterval' />
                            </div>
                        </div>

                        
                        <div className='section'>
                            <h4 className='subtitle'>Game Features</h4>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='autoRebuy'>Auto Rebuy</label>
                                <input type='checkbox' checked={options.autoRebuy} onChange={handleCheckChange} className="option-checkbox" id='autoRebuy' />
                            </div>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='gameStats'>Display Game Stats</label>
                                <input type='checkbox' checked={options.gameStats} onChange={handleCheckChange} className="option-checkbox" id='gameStats' />
                            </div>
                        </div>
                        
                        <div className='section'>
                            <h4 className='first subtitle'>Cheats</h4>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='showAllBotCards'>Show cards for bots</label>
                                <input type='checkbox' checked={options.showAllBotCards} onChange={handleCheckChange} className="option-checkbox" id='showAllBotCards' />
                            </div>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='showAllCards'>Show cards for everyone</label>
                                <input type='checkbox' checked={options.showAllCards} onChange={handleCheckChange} className="option-checkbox" id='showAllCards' />
                            </div>
                            <p id='warning'>Warning: every player in the game will receive these cheats!</p>
                        </div>

                        <div className='section'>
                            <h4 className='subtitle'>Add Bots</h4>
                            <div id='bot-buttons'>
                                <div className='bot-button' onClick={addBot} id='better'>Better</div>
                                <div className='bot-button' onClick={addBot} id='scary_cat'>Scary Cat</div>
                                <div className='bot-button' onClick={addBot} id='caller'>Caller</div>
                                <div className='bot-button' onClick={addBot} id='copy_cat'>Copy Cat</div>
                                <div className='bot-button' onClick={addBot} id='tight_bot'>Tight bot</div>
                                <div className='bot-button' onClick={addBot} id='moderate_bot'>Moderate bot</div>
                                <div className='bot-button' onClick={addBot} id='loose_bot'>Loose bot</div>
                                <div className='bot-button' onClick={addBot} id='random'>Random</div>
                            </div>
                        </div>
                        <button id='host-start' onClick={startGame}>Start</button>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Host
