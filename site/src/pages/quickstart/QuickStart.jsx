import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ls from 'localstorage-slim'

import pokerService from '../../services/poker'
import './quickStart.css'


const QuickStart = () => {
  const navigate = useNavigate()

  useEffect(() => {
    const init = async () => {
      const tableData = await pokerService.init({ name: getName() })
      const tableId = tableData.id
      ls.set('tableId', tableId)
      await pokerService.addBot({ id: tableId, bot_type: 'tight_bot' })
      await pokerService.addBot({ id: tableId, bot_type: 'moderate_bot' })
      await pokerService.addBot({ id: tableId, bot_type: 'loose_bot' })
      navigate(`../game/${tableId}`, { replace: true })
    }
    init()
  }, [])

  const getName = () => {
    return ls.get('username')
  }
  
  return (
    <>
      <div id='room'>
        <div id='table'>
          <div className='vertical-align'>
            <h1 id='loading'>Loading...</h1>
          </div>
        </div>
      </div>
    </>
  )
}

export default QuickStart
