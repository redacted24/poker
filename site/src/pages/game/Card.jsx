import "./card.css";
import Draggable from "react-draggable";

const Card = ({ card }) => {
    const handleStart = (e, ui) => {
        ui.node.style.transition = "none";
        ui.node.style.animation = "none";
    };

    const handleStop = (e, ui) => {
        ui.node.style.transition =
            "transform cubic-bezier(.2,.75,.25,.96) 0.55s";
        ui.node.style.animation = "";
        setTimeout(() => {
            ui.node.style.transition = "all 0.4s";
        }, 550);
    };

    if (card) {
        return (
            <Draggable
                onStart={handleStart}
                onStop={handleStop}
                position={{ x: 0, y: 0 }}
            >
                <img
                    className="card noSelect"
                    id={card}
                    src={`/cards/${card}.svg`}
                />
            </Draggable>
        );
    } else {
        return (
            <Draggable
                onStart={handleStart}
                onStop={handleStop}
                position={{ x: 0, y: 0 }}
            >
                <img className="card noSelect" src="/cards/back.png" />
            </Draggable>
        );
    }
};

export default Card;
