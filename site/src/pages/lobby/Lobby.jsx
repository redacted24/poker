import { useState, useEffect } from 'react'
import './lobby.css'

const Lobby = () => {
    const [name, setName] = useState(null)

    useEffect(() => {
        const username = prompt('Please enter your username.', 'Bob')
        setName(username)
    }, [])



    return (
        <>
            <h2 id='status'>Waiting...</h2>
            <div id='lobby'>
                <div id='player-list'>
                    <p className='subheader'>Player list</p>
                    
                </div>
                <div id='settings'>
                    <p className='subheader'>Settings</p>
                </div>
            </div>
        </>
    )
}

export default Lobby