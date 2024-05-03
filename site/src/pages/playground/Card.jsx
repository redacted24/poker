import './card.css'
import Draggable from 'react-draggable'


const Card = ({ card }) => {
  if (card) {
    return (
      <Draggable>
        <img className='card' src={`./src/assets/cards/${card}.svg`} />
      </Draggable>
  )} else {
    return (
      <Draggable>
        <img className='card' src='./src/assets/cards/back.png'/>
      </Draggable>)
  }
}

export default Card
