import { Link } from "react-router-dom";
import "./intro.css";

const Intro = () => {
    return (
        <div id="intro-container">
            <h1 id="title">The Poker Playground</h1>
            <div id="link-buttons">
                <Link className="react-link-clickable" to="/quick-start">
                    <button id="campaign" className="link-button">
                        <div id="campaign-text">Campaign (in development)</div>
                    </button>
                    <img
                        src="/ui/campaign-castle.svg"
                        alt="doesnt work"
                        id="campaign-image-1"
                    ></img>
                    <img
                        src="/ui/shield.svg"
                        alt="doesnt work"
                        id="campaign-image-2"
                    ></img>
                    <img
                        src="/ui/swords.svg"
                        alt="doesnt work"
                        id="campaign-image-3"
                    ></img>
                    <img
                        src="/ui/heart_filled.svg"
                        alt="doesnt work"
                        id="campaign-image-6"
                    ></img>
                    <img
                        src="/ui/heart.svg"
                        alt="doesnt work"
                        id="campaign-image-4"
                    ></img>
                    <img
                        src="/ui/heart.svg"
                        alt="doesnt work"
                        id="campaign-image-5"
                    ></img>
                    <img
                        src="/ui/sun.svg"
                        alt="doesnt work"
                        id="campaign-image-7"
                    ></img>
                    <img
                        src="/ui/cloud.svg"
                        alt="doesnt work"
                        id="campaign-image-8"
                    ></img>
                    <img
                        src="/ui/cloud.svg"
                        alt="doesnt work"
                        id="campaign-image-9"
                    ></img>
                    <img
                        src="/ui/line.svg"
                        alt="doesnt work"
                        id="campaign-image-10"
                    ></img>
                    <img
                        src="/ui/bird.svg"
                        alt="doesnt work"
                        id="campaign-image-11"
                    ></img>
                </Link>

                <Link className="react-link-clickable" to="/quick-start">
                    <button id="quickstart" className="link-button">
                        <div id="quickstart-text">Quick Start</div>
                    </button>
                    <img
                        src="/ui/cards1.svg"
                        alt="cards1"
                        id="quickstart-image-1"
                    ></img>
                    <img
                        src="/ui/cards2_halfhidden.svg"
                        alt="cards2_halfhidden"
                        id="quickstart-image-2"
                    ></img>
                    <img
                        src="/ui/pokerchip.svg"
                        alt="pokerchip"
                        id="quickstart-image-3"
                    ></img>
                    <img
                        src="/ui/pokerchip.svg"
                        alt="pokerchip"
                        id="quickstart-image-4"
                    ></img>
                    <img
                        src="/ui/card_hidden.svg"
                        alt="card_hidden"
                        id="quickstart-image-5"
                    ></img>
                    <img
                        src="/ui/card_hidden.svg"
                        alt="card_hidden"
                        id="quickstart-image-6"
                    ></img>
                    <img
                        src="/ui/card_hidden.svg"
                        alt="card_hidden"
                        id="quickstart-image-7"
                    ></img>
                </Link>

                <Link className="react-link-clickable" to="/host">
                    <button id="multiplayer" className="link-button">
                        <div id="multiplayer-text">Create a Table</div>
                    </button>
                    <img
                        src="/ui/gears.svg"
                        alt="gear"
                        id="multiplayer-image-1"
                    ></img>
                    <img
                        src="/ui/plus.svg"
                        alt="people"
                        id="multiplayer-image-2"
                    ></img>
                    <img
                        src="/ui/peopleicon.svg"
                        alt="people"
                        id="multiplayer-image-3"
                    ></img>
                    <img
                        src="/ui/plus.svg"
                        alt="plussymbol"
                        id="multiplayer-image-4"
                    ></img>
                    <img
                        src="/ui/robot.svg"
                        alt="robot"
                        id="multiplayer-image-5"
                    ></img>
                </Link>
            </div>
        </div>
    );
};

export default Intro;
