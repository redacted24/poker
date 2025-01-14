import { useEffect } from 'react'
import useState from 'react-usestateref'
import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'
import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

const Host = ({ notify, clearIntervals }) => {
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

    const [playerList, setPlayerList, playerListRef] = useState([])
    const [cooldown, setCooldown] = useState(false)
    const [table, setTable] = useState()
    const navigate = useNavigate()

    let intervalId

    useEffect(() => {
        const removeTableId = async () => {
            const tableId = ls.get('tableId')
            if (tableId) {
              console.log('clearing')
              await pokerService.clear({ id: tableId })
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
            if (window.location.href == window.location.host) removeTableId()
            window.removeEventListener('beforeunload', removeTableId)
            clearIntervals()
        }
    }, [])

    const updateTable = (newTableData) => {
        setTable(newTableData)
        newTableData.players.forEach(p => {
            if (!playerListRef.current.includes(p.name)) {
                notify(`${p.name} has joined the lobby!`, 'success')
            }
        })
        setPlayerList(newTableData.players.map(p => p.name))
    }


    const toggleFetching = (fetching) => {
        if (fetching && !cooldown) {
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
        const gameUrl = `https://${window.location.host}/lobby/${getTableId()}`
        try {
            navigator.clipboard.writeText(gameUrl)
        } catch {
            unsecureCopy(gameUrl)
        }
        const link_button = document.getElementById('link-button')
        link_button.textContent = 'Link Copied!'
        setTimeout(() => {
            link_button.textContent = 'Copy Link'
        }, 2000)
    }

    const startCooldown = (time=1500) => {
        setCooldown(true)
        setTimeout(() => setCooldown(false), time)
    }

    const startGame = () => {
        if (table.players.length >= 2) {
            pokerService.setSettings({ id: getTableId(), ...options })
            toggleFetching(false)
            navigate(`../game/${getTableId()}`, { replace: true })
        } else {
            notify('You cannot start a game with less than 2 players!', 'error')
        }
    }

    const removePlayer = async (player_name_to_remove) => {
        setPlayerList(playerList.filter(p => p !== player_name_to_remove))
        notify(`${player_name_to_remove} has been kicked from the lobby!`, 'error')
        startCooldown()
        await pokerService.leave({ name: player_name_to_remove, id: getTableId() })
    }

    const addBot = async (e) => {
        const bot_type = e.target.id
        if (!playerListRef.current.includes(bot_type)) {
            notify(`${bot_type} has joined the lobby!`, 'success')
        }
        setPlayerList(playerList.concat(bot_type))
        startCooldown()
        const tableData = await pokerService.addBot({ id: getTableId(), bot_type })
        updateTable(tableData)
        console.log(tableData)
    }

    const handleChange = (e) => {
        if (e.target.id == 'bigBlindAmount') {
            const newOptions = { ...options }
            newOptions['smallBlindAmount'] = e.target.value * increments['smallBlindAmount']
            setOptions({ ...newOptions })
        } else {
            const newOptions = { ...options }
            newOptions[e.target.id] = e.target.value * increments[e.target.id]
            setOptions({ ...newOptions })
        }
    }

    const handleCheckChange = (e) => {
        if (e.target.id == 'showAllCards') {
            const newOptions = { ...options }
            newOptions[e.target.id] = !options[e.target.id]
            newOptions['showAllBotCards'] = !options[e.target.id]
            setOptions({ ...newOptions })
        } else {
            const newOptions = { ...options }
            newOptions[e.target.id] = !options[e.target.id]
            setOptions({ ...newOptions })
        }
    }

    return (
        <>
            <h2 id='status'>Waiting...</h2>
            <div id='lobby'>
                <div id='player-list'>
                    <h3 className='subheader'>Player list</h3>
                    <div id='players'>
                        {playerList.map(p => <Player player_name={p} key={p} removePlayer={removePlayer} kickable={p != getName()}/>)}
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
                                <input type="range" min="1" max="25" value={options.startingBalance / 200} onChange={handleChange} class="option-slider" id='startingBalance' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='smallBlindAmount'>Small blind amount: {options.smallBlindAmount}$</label>
                                <input type="range" min="0" max="20" value={options.smallBlindAmount / 5} onChange={handleChange} class="option-slider" id='smallBlindAmount' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='bigBlindAmount'>Big blind amount: {options.smallBlindAmount * 2}$</label>
                                <input type="range" min="0" max="20" value={options.smallBlindAmount / 5} onChange={handleChange} class="option-slider" id='bigBlindAmount' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='blindInterval'>Blind interval: +{options.blindInterval}$ per round</label>
                                <input type="range" min="0" max="5" value={options.blindInterval / 5} onChange={handleChange} class="option-slider" id='blindInterval' />
                            </div>
                        </div>

                        
                        <div className='section'>
                            <h4 className='subtitle'>Game Features</h4>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='autoRebuy'>Auto Rebuy</label>
                                <input type='checkbox' checked={options.autoRebuy} onChange={handleCheckChange} class="option-checkbox" id='autoRebuy' />
                            </div>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='gameStats'>Display Game Stats</label>
                                <input type='checkbox' checked={options.gameStats} onChange={handleCheckChange} class="option-checkbox" id='gameStats' />
                            </div>
                        </div>
                        
                        <div className='section'>
                            <h4 className='first subtitle'>Cheats</h4>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='showAllBotCards'>Show cards for bots</label>
                                <input type='checkbox' checked={options.showAllBotCards} onChange={handleCheckChange} class="option-checkbox" id='showAllBotCards' />
                            </div>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='showAllCards'>Show cards for everyone</label>
                                <input type='checkbox' checked={options.showAllCards} onChange={handleCheckChange} class="option-checkbox" id='showAllCards' />
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
