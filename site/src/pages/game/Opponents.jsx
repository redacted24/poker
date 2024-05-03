import Opponent from './Opponent'
import './opponents.css'

const Opponents = ({ opponents, playerQueue, userName }) => {
  return (
    <div id='opponents'>
        {opponents.map(player => {
            return <Opponent
              key={player.name}
              player={player}
              isCurrentPlayer={playerQueue[0] && playerQueue[0].name == player.name}
              isNextPlayer={playerQueue[1] && playerQueue[1].name == player.name}
              userAtStart={playerQueue[0] && playerQueue[0].name == userName}
            />
        })}
    </div>
  )
}

export default Opponents