import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import ls from "localstorage-slim";

import Player from "./Player";
import "./host.css";

const Lobby = ({ socket, notify }) => {
    const [table, setTable] = useState();
    const [playerList, setPlayerList] = useState([]);
    const params = useParams();

    const navigate = useNavigate();

    useEffect(() => {
        if (!socket) return undefined;

        socket.emit("join", {
            name: getName(),
            table_id: params.id,
        });

        socket.on("message", (table) => {
            setTable(table);
            setPlayerList(table.players);
            ls.set("table_id", table.id, { ttl: 60 * 5 });
        });

        socket.on("change_username", (data) => {
            ls.set("username", data);
        });

        socket.on("player_joined", (playerName) => {
            notify(`${playerName} has joined the lobby!`, "success");
        });

        socket.on("player_left", (playerName) => {
            if (playerName == getName()) {
                notify("You have been kicked out of the lobby!", "error");
                navigate("/");
            } else {
                notify(`${playerName} has left the lobby`, "error");
            }
        });

        socket.on("start_game", () => {
            notify("game has started!", "success");
            navigate(`../game/${ls.get("table_id")}`, { replace: true });
        });
    }, [socket]);

    const getName = () => {
        if (!ls.get("username")) {
            navigate("/start");
            return null;
        }
        return ls.get("username");
    };

    const copyLink = () => {
        const gameUrl = `${window.location.host}/lobby/${table.id}`;
        navigator.clipboard.writeText(gameUrl);

        const link_button = document.getElementById("link-button");
        link_button.textContent = "Link Copied!";
        setTimeout(() => {
            link_button.textContent = "Copy Text";
        }, 2000);
    };

    return (
        <>
            <h2 id="status">Lobby...</h2>
            <div id="lobby">
                <div id="player-list">
                    <p className="subheader">Player list</p>
                    <div id="players">
                        {table &&
                            playerList.map((p) => (
                                <Player player_name={p.name} key={p.name} />
                            ))}
                    </div>
                    <div id="link-section">
                        <button id="link-button" onClick={copyLink}>
                            Copy table link
                        </button>
                    </div>
                </div>
                <div id="settings">
                    <p className="subheader">Settings</p>
                </div>
            </div>
        </>
    );
};

export default Lobby;
