import './player.css'

const Player = ({ player }) => {
    return (
        <div className='list-player'>{player.name}</div>
    )
}

export default Player