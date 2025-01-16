import { useState, useEffect } from "react";

import { io } from "socket.io-client"


const Test = () => {
    const [socketInstance, setSocketInstance] = useState(null)

    useEffect(() => {
        const socket = io("localhost:5000/");

        setSocketInstance(socket);

        socket.on("connect", (data) => {
            console.log(data);
        });

        socket.on("message", (data) => {
            alert("message: " + data)
        })

        socket.on("disconnect", (data) => {
            console.log(data);
        });

        return () => {
            socket.disconnect();
        };
    }, [])

    const join_room = () => {
        console.log('test')
        socketInstance.emit("join", {
            username: "bob",
            room: 123,
        })
    }
    


    console.log(socketInstance);
    return (
        <>
            <div>hi</div>
            <button onClick={join_room}>join room</button>
        </>
    )
}

export default Test