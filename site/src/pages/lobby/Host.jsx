import { useState, useEffect } from 'react'
import Player from './Player'
import './host.css'

import pokerService from '../../services/poker'
import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

const Host = ({ clearIntervals }) => {
    const increments = {
        startingIncome: 200,
        smallBlindAmount: 5,
        blindInterval: 5,
    }
    
    const [options, setOptions] = useState({
        startingIncome: 1000,
        smallBlindAmount: 5,
        blindInterval: 0,
        autoRebuy: false,
        gameStats: false,
        showAllCardsBots: false,
        showAllCards: false
    })

    const [playerList, setPlayerList] = useState([])
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
            clearIntervals()
        }
    }, [])

    const updateTable = (newTableData) => {
        setTable(newTableData)
        setPlayerList(newTableData.players.map(p => p.name))
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

    const startGame = () => {
        if (table.players.length >= 2) {
            toggleFetching(false)
            navigate(`../game/${getTableId()}`)
        } else {
            alert('You cannot start a game with less than 2 players!')
        }
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
            newOptions['showAllCardsBots'] = !options[e.target.id]
            setOptions({ ...newOptions })
        } else {
            const newOptions = { ...options }
            newOptions[e.target.id] = !options[e.target.id]
            setOptions({ ...newOptions })
        }
    }

    const removePlayer = async (player_name_to_remove) => {
        setPlayerList(playerList.filter(p => p !== player_name_to_remove))
        await pokerService.leave({ name: player_name_to_remove, id: getTableId() })
        alert(`${player_name_to_remove} has been removed`)
    }

    const addBot = async (e) => {
        const bot_type = e.target.id
        setPlayerList(playerList.concat(bot_type))
        const tableData = await pokerService.addBot({ id: getTableId(), bot_type })
        updateTable(tableData)
        console.log(tableData)
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
                        <p className='share-link'>Share this link to invite others!</p>
                        <button id='link-button' onClick={copyLink}>Copy link</button>
                    </div>
                </div>
                <div id='settings'>
                    <h3 className='subheader'>Settings</h3>
                    <div id='options'>
                        <div className='section'>
                            <h4 className='first subtitle'>Table Options</h4>
                            <div className='option'>
                                <label className='option-label' htmlFor='startingIncome'>Staring income: {options.startingIncome}$</label>
                                <input type="range" min="1" max="25" value={options.startingIncome / 200} onChange={handleChange} class="option-slider" id='startingIncome' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='smallBlindAmount'>Small blind amount: {options.smallBlindAmount}$</label>
                                <input type="range" min="1" max="20" value={options.smallBlindAmount / 5} onChange={handleChange} class="option-slider" id='smallBlindAmount' />
                            </div>
                            <div className='option'>
                                <label className='option-label' htmlFor='bigBlindAmount'>Big blind amount: {options.smallBlindAmount * 2}$</label>
                                <input type="range" min="1" max="20" value={options.smallBlindAmount / 5} onChange={handleChange} class="option-slider" id='bigBlindAmount' />
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
                                <label className='option-label inline' htmlFor='gameStats'>Game Stats</label>
                                <input type='checkbox' checked={options.gameStats} onChange={handleCheckChange} class="option-checkbox" id='gameStats' />
                            </div>
                        </div>
                        
                        <div className='section'>
                            <h4 className='first subtitle'>Cheats</h4>
                            <div className='option checkbox'>
                                <label className='option-label inline' htmlFor='showAllCardsBots'>Show cards for bots</label>
                                <input type='checkbox' checked={options.showAllCardsBots} onChange={handleCheckChange} class="option-checkbox" id='showAllCardsBots' />
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