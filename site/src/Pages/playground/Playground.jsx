import { useEffect } from 'react'
import Card from './Card'
import './playground.css'
import { useState } from 'react'
import pokerService from '../../services/poker'


const Playground = () => {
  const [hand, setHand] = useState([])
  const [river, setRiver] = useState([])

  useEffect(() => {
    setHand([{
      rank: 5,
      suit: 'd',
      faceup: true
    }, {
      rank: 9,
      suit: 'h',
      faceup: true
    }])


    setRiver([{
      rank: 2,
      suit: 's',
      faceup: true
    }, {
      rank: 5,
      suit: 'h',
      faceup: true
    }, {
      rank: 13,
      suit: 's',
      faceup: true
    }, {
      rank: 8,
      suit: 's',
      faceup: true
    }, {
      rank: 4,
      suit: 'c',
      faceup: true
    }])
  }, [])

  const test = async () => {
    const response = await pokerService.test()
    console.log(response)
  }

  return (
    <>
      <div id='room'>
        <div id='table'>
          <div id='river'>
            {river.map(card => <Card key={`${card.rank}${card.suit}`} {...card} />)}
          </div>
        </div>
        <div id='hand'>
          {hand.map(card => <Card key={`${card.rank}${card.suit}`} {...card} />)}
        </div>
        <div id='buttons'>
          <button className='action' onClick={test}>Call</button>
          <button className='action'>Check</button>
          <button className='action'>Fold</button>
          <button className='action'>Bet</button>
        </div>
      </div>
    </>
  )
}

export default Playground