import "./player.css";

const Player = ({ player_name, kickable, removePlayer }) => {
    return (
        <div className="list-player">
            <span className="player-name">{player_name} </span>
            {kickable && (
                <img
                    className="kick-img"
                    onClick={() => removePlayer(player_name)}
                    src="/misc/close-button.svg"
                />
            )}
        </div>
    );
};

export default Player;
