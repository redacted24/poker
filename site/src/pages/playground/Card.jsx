import './card.css'

const Card = ({ rank, suit, facedown }) => {
  if (facedown) {
    return <img className='card' src='./src/assets/cards/back.png' />
  } else {
    return <img className='card' src={`./src/assets/cards/${rank}${suit}.svg`} />
  } 
}

export default Card