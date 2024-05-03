import Opponent from './Opponent'
import './opponents.css'

const Opponents = ({ opponents, playerQueue }) => {
  return (
    <div id='opponents'>
        {opponents.map(player => {
            return <Opponent key={player.name} player={player} isCurrentPlayer={playerQueue[0] && playerQueue[0].name == player.name} />
        })}
    </div>
  )
}

export default Opponents