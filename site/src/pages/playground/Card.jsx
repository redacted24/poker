import './card.css'

const Card = ({ card }) => {
  if (card) {
    return <img className='card' src={`./src/assets/cards/${card}.svg`} />
  } else {
    return <img className='card' src='./src/assets/cards/back.png' />
  } 
}

export default Card