import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ls from "localstorage-slim";

import "./quickStart.css";

const QuickStart = ({ socket }) => {
    const navigate = useNavigate();

    useEffect(() => {
        const init = async () => {
            useEffect(() => {
                if (!socket) return undefined;

                socket.emit("host", {
                    name: getName(),
                });

                socket.on("message", (table) => {
                    setTable(table);
                    setPlayerList(table.players);
                    ls.set("table_id", table.id, { ttl: 60 * 5 });
                });

                socket.emit("set_settings", {
                    table_id: table.id,
                    ...options,
                });

                socket.on("start_game", () => {
                    notify("game has started!", "success");
                    navigate(`../game/${ls.get("table_id")}`, {
                        replace: true,
                    });
                });
            }, [socket]);
        };
        init();
    }, []);

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
