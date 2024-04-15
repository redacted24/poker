import Opponent from './Opponent'
import './opponents.css'

const Opponents = ({ opponents }) => {
  return (
    <div id='opponents'>
        {opponents.map(player => {
            return <Opponent key={player.name} player={player} />
        })}
    </div>
  )
}

export default Opponents