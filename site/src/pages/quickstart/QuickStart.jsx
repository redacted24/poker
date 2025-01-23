import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ls from "localstorage-slim";

import "./quickStart.css";

const QuickStart = ({ socket, notify }) => {
    const navigate = useNavigate();

	useEffect(() => {
		if (!socket) return undefined;

		socket.emit("host", {
			name: getName(),
		});

		socket.on("message", (table) => {
			ls.set("table_id", table.id, { ttl: 60 * 5 });
			console.log(table)

			if (table.players.length !== 1) return undefined;

			setTimeout(() => {
				socket.emit("add_bot", { bot_type: "loose_bot", table_id: table.id });
				socket.emit("add_bot", { bot_type: "moderate_bot", table_id: table.id });
				socket.emit("add_bot", { bot_type: "tight_bot", table_id: table.id });
				notify("game has started!", "success");
				navigate(`../game/${ls.get("table_id")}`, {
					replace: true,
				});
			}, 1000)
		});
		
		return () => {
			socket.off("message");
		}

	}, [socket]);


    const getName = () => {
        return ls.get("username");
    };

    return (
        <>
            <div id="room">
                <div id="table">
                    <div className="vertical-align">
                        <h1 id="loading">Loading...</h1>
                    </div>
                </div>
            </div>
        </>
    );
};

export default QuickStart;
