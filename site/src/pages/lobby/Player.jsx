import ls from 'localstorage-slim'

import pokerServices from '../../services/poker'
import './player.css'

const Player = ({ player, kickable }) => {

    const getTableId = () => {
        return ls.get('tableId')
    }

    const removePlayer = () => {
        pokerServices.leave({ name: player.name, id: getTableId() })
        alert(`${player.name} has been removed`)
    }

    return (
        <div className='list-player'>
            <span className='player-name'>{player.name} </span>
            {kickable && <img className='kick-img' onClick={removePlayer} src='../../src/assets/misc/close-button.svg'/>}
        </div>
    )
}

export default Player