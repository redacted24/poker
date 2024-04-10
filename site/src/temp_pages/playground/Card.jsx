import './card.css'

const Card = ({ name, facedown }) => {
  if (facedown) {
    return <img className='card' src='./src/assets/cards/back.png' />
  } else {
    return <img className='card' src={`./src/assets/cards/${name}.svg`} />
  } 
}

export default Card